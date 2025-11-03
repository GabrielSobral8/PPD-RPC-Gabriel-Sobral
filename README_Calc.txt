Guia rápido - Calculadora RPC
Instalação das dependências:
pip install grpcio grpcio-tools

gerar os arquivos gRPC
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpcCalc.proto

rodar o servidor
python grpcCalc_server.py

rodar o cliente 
python grpcCalc_client.py

