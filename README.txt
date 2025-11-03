Guia rápido - Minerador RPC
Instale as libs:
pip install grpcio grpcio-tools

Gere os arquivos do gRPC
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. miner.proto

Rode o servidor 
python miner_server.py

Rode o cliente 
python miner_client.py

