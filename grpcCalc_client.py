import grpc
import grpcCalc_pb2
import grpcCalc_pb2_grpc

def menu():
    print("=== Calculadora gRPC ===")
    print("1) Soma")
    print("2) Subtração")
    print("3) Multiplicação")
    print("4) Divisão")
    print("0) Sair")

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = grpcCalc_pb2_grpc.CalculatorStub(channel)
    while True:
        menu()
        opt = input("Escolha: ").strip()
        if opt == "0":
            break
        try:
            x = float(input("x: "))
            y = float(input("y: "))
        except:
            print("Entrada inválida")
            continue
        req = grpcCalc_pb2.Operands(x=x, y=y)
        if opt == "1":
            res = stub.Add(req)
        elif opt == "2":
            res = stub.Sub(req)
        elif opt == "3":
            res = stub.Mul(req)
        elif opt == "4":
            res = stub.Div(req)
        else:
            print("Opção inválida")
            continue
        if res.error:
            print("Erro:", res.error)
        else:
            print("Resultado:", res.value)

if __name__ == '__main__':
    run()
