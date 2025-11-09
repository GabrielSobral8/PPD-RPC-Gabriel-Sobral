import grpc, hashlib, random, string, threading, time
from concurrent.futures import ThreadPoolExecutor
import miner_pb2, miner_pb2_grpc

def menu():
    print("\n=== Minerador gRPC ===")
    print("1) getTransactionID")
    print("2) getChallenge")
    print("3) getTransactionStatus")
    print("4) getWinner")
    print("5) getSolution")
    print("6) Mine")
    print("0) Sair")

def brute_worker(stop_event, found_event, challenge, result_holder, worker_id):
    chars = string.ascii_letters + string.digits
    while not stop_event.is_set() and not found_event.is_set():
        s = ''.join(random.choice(chars) for _ in range(8))
        h = hashlib.sha1(s.encode()).hexdigest()
        if h.startswith('0' * challenge):
            result_holder['solution'] = s
            found_event.set()
            print(f"[Thread {worker_id}] Solução encontrada: {s}")
            break

def mine(stub, client_id):
    print("\n--- Iniciando mineração ---")
    txid = stub.getTransactionID(miner_pb2.Empty()).value
    print(f"TransactionID atual: {txid}")

    challenge = stub.getChallenge(miner_pb2.ChallengeRequest(transaction_id=txid)).challenge
    if challenge == -1:
        print("Transaction inválida.")
        return
    print(f"Challenge (dificuldade): {challenge}")

    # Cria eventos
    stop_event = threading.Event()
    found_event = threading.Event()
    result_holder = {}

    # Inicia threads
    print("Mineração iniciada (usando 6 threads)...")
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(brute_worker, stop_event, found_event, challenge, result_holder, i) for i in range(6)]
        # Espera até achar a solução
        while not found_event.is_set():
            time.sleep(0.1)

        # Sinaliza para as outras threads pararem
        stop_event.set()

    sol = result_holder.get('solution')
    if not sol:
        print("Nenhuma solução encontrada (algo deu errado).")
        return

    print(f"\nSolução final encontrada: {sol}")
    print("Enviando solução para o servidor...")
    try:
        res = stub.submitChallenge(miner_pb2.SubmitReq(transaction_id=txid, client_id=client_id, solution=sol))
        print("Resposta recebida do servidor!")
        if res.result == 1:
            print("Solução aceita! Você venceu a transação.")
        elif res.result == 0:
            print("Solução inválida (hash não bate).")
        elif res.result == 2:
            print("Desafio já foi solucionado por outro cliente.")
        elif res.result == -1:
            print("Transaction inválida.")
        else:
            print("Resposta desconhecida do servidor:", res.result)
    except Exception as e:
        print("Erro ao enviar solução:", e)

    print("--- Mineração finalizada ---\n")

def run():
    channel = grpc.insecure_channel('localhost:50052')
    stub = miner_pb2_grpc.MinerStub(channel)
    client_id = random.randint(1, 9999)
    print("Seu ClientID:", client_id)

    while True:
        menu()
        op = input("Escolha: ").strip()
        if op == "0":
            break
        elif op == "1":
            print("TransactionID:", stub.getTransactionID(miner_pb2.Empty()).value)
        elif op == "2":
            tid = int(input("transactionID: "))
            print("Challenge:", stub.getChallenge(miner_pb2.ChallengeRequest(transaction_id=tid)).challenge)
        elif op == "3":
            tid = int(input("transactionID: "))
            print("Status:", stub.getTransactionStatus(miner_pb2.ChallengeRequest(transaction_id=tid)).status)
        elif op == "4":
            tid = int(input("transactionID: "))
            print("Winner:", stub.getWinner(miner_pb2.ChallengeRequest(transaction_id=tid)).winner)
        elif op == "5":
            tid = int(input("transactionID: "))
            sol = stub.getSolution(miner_pb2.ChallengeRequest(transaction_id=tid))
            print("Status:", sol.status, "Solution:", sol.solution, "Challenge:", sol.challenge)
        elif op == "6":
            mine(stub, client_id)
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    run()
