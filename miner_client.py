import grpc, hashlib, random, string, threading, time
from concurrent.futures import ThreadPoolExecutor
import miner_pb2, miner_pb2_grpc

def menu():
    print('\n=== Minerador gRPC ===')
    print('1) getTransactionID')
    print('2) getChallenge')
    print('3) getTransactionStatus')
    print('4) getWinner')
    print('5) getSolution')
    print('6) Mine')
    print('0) Sair')

def brute_worker(stop, found, ch, result):
    chars = string.ascii_letters + string.digits
    while not stop.is_set() and not found.is_set():
        s = ''.join(random.choice(chars) for _ in range(8))
        h = hashlib.sha1(s.encode()).hexdigest()
        if h.startswith('0'*ch):
            result['solution'] = s
            found.set()

def mine(stub, cid):
    txid = stub.getTransactionID(miner_pb2.Empty()).value
    print('TransactionID atual:', txid)
    ch = stub.getChallenge(miner_pb2.ChallengeRequest(transaction_id=txid)).challenge
    print('Challenge:', ch)
    stop, found = threading.Event(), threading.Event()
    result = {}
    with ThreadPoolExecutor(max_workers=6) as exe:
        for _ in range(6):
            exe.submit(brute_worker, stop, found, ch, result)
        while not found.is_set():
            time.sleep(0.2)
    sol = result.get('solution', '')
    print('Solução encontrada:', sol)
    res = stub.submitChallenge(miner_pb2.SubmitReq(transaction_id=txid, client_id=cid, solution=sol))
    print('Resultado da submissão:', res.result)

def run():
    channel = grpc.insecure_channel('localhost:50052')
    stub = miner_pb2_grpc.MinerStub(channel)
    cid = random.randint(1, 9999)
    print('Seu ClientID:', cid)
    while True:
        menu()
        op = input('Escolha: ')
        if op == '0': break
        elif op == '1':
            print('TransactionID:', stub.getTransactionID(miner_pb2.Empty()).value)
        elif op == '2':
            tid = int(input('transactionID: '))
            print('Challenge:', stub.getChallenge(miner_pb2.ChallengeRequest(transaction_id=tid)).challenge)
        elif op == '3':
            tid = int(input('transactionID: '))
            print('Status:', stub.getTransactionStatus(miner_pb2.ChallengeRequest(transaction_id=tid)).status)
        elif op == '4':
            tid = int(input('transactionID: '))
            print('Winner:', stub.getWinner(miner_pb2.ChallengeRequest(transaction_id=tid)).winner)
        elif op == '5':
            tid = int(input('transactionID: '))
            sol = stub.getSolution(miner_pb2.ChallengeRequest(transaction_id=tid))
            print('Status:', sol.status, 'Solution:', sol.solution, 'Challenge:', sol.challenge)
        elif op == '6':
            mine(stub, cid)
        else:
            print('Opção inválida.')

if __name__ == '__main__':
    run()
