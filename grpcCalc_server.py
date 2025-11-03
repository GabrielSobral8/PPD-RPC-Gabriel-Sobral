import grpc
from concurrent import futures
import time
import grpcCalc_pb2
import grpcCalc_pb2_grpc

class CalculatorServicer(grpcCalc_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        return grpcCalc_pb2.Result(value=request.x + request.y)
    def Sub(self, request, context):
        return grpcCalc_pb2.Result(value=request.x - request.y)
    def Mul(self, request, context):
        return grpcCalc_pb2.Result(value=request.x * request.y)
    def Div(self, request, context):
        if request.y == 0:
            return grpcCalc_pb2.Result(value=0.0, error="Divisão por zero")
        return grpcCalc_pb2.Result(value=request.x / request.y)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    grpcCalc_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor calculadora gRPC rodando em :50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
