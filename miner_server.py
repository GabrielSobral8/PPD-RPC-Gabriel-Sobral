import grpc
from concurrent import futures
import time, random, hashlib, threading
import miner_pb2, miner_pb2_grpc

class MinerServicer(miner_pb2_grpc.MinerServicer):
    def __init__(self):
        self.lock = threading.Lock()
        self.transactions = {}
        self._new_transaction(0)

    def _new_transaction(self, txid=None):
        with self.lock:
            if txid is None:
                txid = max(self.transactions.keys()) + 1 if self.transactions else 0
            challenge = random.randint(1, 4)
            self.transactions[txid] = {'challenge': challenge, 'solution': '', 'winner': -1}
            return txid

    def getTransactionID(self, request, context):
        with self.lock:
            pending = [tid for tid, v in self.transactions.items() if v['winner'] == -1]
            if not pending:
                new = self._new_transaction()
                return miner_pb2.IntMsg(value=new)
            return miner_pb2.IntMsg(value=min(pending))

    def getChallenge(self, request, context):
        tid = request.transaction_id
        with self.lock:
            if tid not in self.transactions:
                return miner_pb2.ChallengeResponse(challenge=-1)
            return miner_pb2.ChallengeResponse(challenge=self.transactions[tid]['challenge'])

    def getTransactionStatus(self, request, context):
        tid = request.transaction_id
        with self.lock:
            if tid not in self.transactions:
                return miner_pb2.StatusResponse(status=-1)
            return miner_pb2.StatusResponse(status=0 if self.transactions[tid]['winner'] != -1 else 1)

    def submitChallenge(self, request, context):
        tid, cid, sol = request.transaction_id, request.client_id, request.solution
        with self.lock:
            if tid not in self.transactions:
                return miner_pb2.SubmitRes(result=-1)
            tx = self.transactions[tid]
            if tx['winner'] != -1:
                return miner_pb2.SubmitRes(result=2)
            h = hashlib.sha1(sol.encode()).hexdigest()
            needed = '0' * tx['challenge']
            if h.startswith(needed):
                tx['solution'], tx['winner'] = sol, cid
                self._new_transaction()
                return miner_pb2.SubmitRes(result=1)
            else:
                return miner_pb2.SubmitRes(result=0)

    def getWinner(self, request, context):
        tid = request.transaction_id
        with self.lock:
            if tid not in self.transactions:
                return miner_pb2.WinnerResponse(winner=-1)
            w = self.transactions[tid]['winner']
            return miner_pb2.WinnerResponse(winner=0 if w == -1 else w)

    def getSolution(self, request, context):
        tid = request.transaction_id
        with self.lock:
            if tid not in self.transactions:
                return miner_pb2.SolutionStruct(status=-1, solution='', challenge=0)
            tx = self.transactions[tid]
            status = 0 if tx['winner'] != -1 else 1
            return miner_pb2.SolutionStruct(status=status, solution=tx['solution'], challenge=tx['challenge'])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    miner_pb2_grpc.add_MinerServicer_to_server(MinerServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print('Servidor minerador gRPC rodando em :50052')
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
