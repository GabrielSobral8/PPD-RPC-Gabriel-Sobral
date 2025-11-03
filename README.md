## PPD-RPC-Gabriel-Sobral
#1. Metodologia de Implementação

Esse trabalho foi dividido em duas partes: a primeira era uma calculadora simples usando RPC, e a segunda era uma simulação de mineração de criptomoedas usando o mesmo tipo de comunicação.

#Atividade 1 – Calculadora RPC

Pra parte da calculadora, eu usei Python com gRPC, porque é mais fácil de configurar e entender o que tá acontecendo do que fazer em C.
A ideia foi criar um servidor que tem as funções básicas (somar, subtrair, multiplicar e dividir) e um cliente que chama essas funções como se fossem locais, mas na verdade elas estão sendo executadas remotamente.

Criei um arquivo .proto pra definir a estrutura da comunicação (as mensagens e os serviços) e depois usei o comando do grpc_tools pra gerar os arquivos automáticos.
Depois disso, foi só implementar o servidor com as funções e o cliente com um menu de texto bem simples, pra digitar os números e escolher a operação.

O foco foi deixar tudo bem direto: o cliente manda os valores, o servidor faz a conta e devolve o resultado. É tipo uma função normal, mas dividida entre dois programas diferentes.

#Atividade 2 – Minerador RPC

Na parte do minerador, a ideia era fazer algo parecido com uma rede de mineração de criptomoedas, só que de um jeito simples, só pra testar o conceito.

O servidor fica com uma tabela de transações, e cada uma tem um desafio (challenge), uma solução e quem foi o vencedor.
Esse desafio é um número que indica a “dificuldade”, e o cliente precisa achar uma string que, quando transformada em hash SHA-1, comece com uma certa quantidade de zeros.
Quando o cliente acha essa string, ele manda pro servidor, que verifica se tá certo e, se estiver, marca aquele cliente como o vencedor.

Implementei o cliente com várias threads, pra tentar várias soluções ao mesmo tempo (como se fossem vários “mineradores”).
Depois que uma thread acha a resposta, ela para as outras e manda pro servidor validar.

#2. Testes
Calculadora

Rodei primeiro o servidor e depois o cliente em terminais separados.
Testei as quatro operações e todas funcionaram tranquilo.
Também testei divisão por zero e o servidor retornou uma mensagem de erro certinha, sem travar.
A resposta foi bem rápida, então deu pra ver que o RPC tava funcionando direitinho.

Minerador

Nessa parte eu deixei o servidor rodando e abri dois clientes diferentes.
Cada cliente mostrava o mesmo desafio e tentava achar a solução.
O primeiro que encontrava mandava pro servidor e virava o “vencedor”.
Depois disso, o servidor automaticamente criava uma nova transação com outro desafio.
Testei várias vezes e todos os métodos (getChallenge, getWinner, etc.) estavam respondendo como esperado.

A mineração funcionou, mas dependendo da dificuldade demorava um pouco (quanto mais zeros exigidos no hash, mais tempo levava pra achar uma solução).

#3. Resultados e Conclusão

No final, deu tudo certo.
Os dois projetos (calculadora e minerador) rodaram sem erro e mostraram bem como funciona o conceito de RPC — o cliente pedindo algo pra outro programa fazer e só recebendo o resultado pronto, como se fosse tudo local.

A calculadora foi o exemplo mais simples, servindo pra entender o básico.
O minerador foi mais interessante, porque deu pra testar threads, múltiplos clientes e o lado “competitivo” da mineração.

O trabalho ajudou a entender melhor como dois programas conseguem conversar entre si pela rede, sem precisar lidar diretamente com sockets ou protocolos complicados.
Acho que a parte do gRPC facilitou muito, porque ele já cuida de toda a parte chata de comunicação e a gente foca só na lógica.
