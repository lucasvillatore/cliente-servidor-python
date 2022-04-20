# Relatorio Trabalho Cache em Tabela Hash
Aluno: Leonardo Bueno Nogueira Kruger GRR: 20180130

Aluno: Lucas Block Villatore GRR: 20171677

## Descrição do trabalho

1. Você tem 3 servidores de temperatura em lugares extremos do mundo: ou normalmente muito frios ou normalmente muito quentes. Cada um destes servidores recebem uma resposta e simplemente mandam uma resposta com um número inteiro que mais se aproxima da temperatura medida.
2. Um cliente não acessa os servidores individualmente, e sim uma cache que mantém os últimos valores recebidos dos 3 servidores. Assim evitamos que o cliente tenha que fazer 3 acessos muito distantes, para fazer 1 acesso mais próximo.
3. A cache mantém uma tabela cache com os dados, com um prazo de validade para cada entrada de 30 segundos. Implemente o cliente. Implemente também a tabela cache da maneira eficiente que foi apresentada em sala de aula. Quando chega uma requisição e algum valor expirou, deve ser feita nova consulta ao servidor original.
4. Para os 3 servidores, a dupla pode tanto implementá-los como servidores do trabalho, utilizando número aleatórios dentro de uma faixa razoável para os valores de temperatura ou, alternativamente, obter as informações adequadamente na Web.
5. Devem ser apresentados logs para múltiplas execuções. Mostre com clareza situações em que uma requisição de usuário encontra/não encontra a cache com informações válidas.

## Informações
Linguagem de programação: Python
## Implementação
### Servidores:
Conforme a descrição do trabalho, existem três servidores que:
1. Ao receber uma requisição 
2. Mandam uma resposta com um número representando sua temperatura, para melhorar a dinamica do projeto cada servidor possui um *range* de temperatura para retornar.
```python
def get_temperature(): # Função que retorna temperatura do servidor
    print("Checking temperature on server 1")
    time.sleep(randrange(5))
    return randrange(30) - 6

if __name__ == "__main__":
    connection, address = create_connection(HOST, PORT)

    print("Connected by {}".format(address))
    while True:
        data = connection.recv(MESSAGE_SIZE_IN_BYTES) # 1. Recebe requisição/conexão
        temperature = get_temperature()
        print("Temperature on server 3 is {}".format(temperature))
        connection.sendall(str(temperature).encode("utf-8")) # 2. Envia a resposta 
```
### Cache:
Na cache é mantido a tabela dos dados de temperatura dos servidores e o prazo de validade para cada entrada e em caso de requisição retorna os valores guardados se estiverem validos ou faz uma nova consulta caso contrario.
1. É estabelicida conexão com cada servidor, e salvo na estrutura servers[]
2. Em seguida é inicializada a tabela cache com uma linha para cada servidor ( ainda sem valores dos servidores ).
3. Cria conexão da Cache, escutando no HOST e PORT especificados.
4. Ao receber uma nova conexão;
5. Para cada linha na tabela;
6. Realiza a checagem de validez dos dados;
7. Se invalido faz uma requisição para atualizar pegar os valores.
8. Se valido pega os valores da tabela cache
9. Envia a resposta da requisição.
```python
if __name__ == "__main__":
    # 1. Cria conexão com servidores
    servers = []
    print("Establishing connection with server 1")
    servers.append(make_connection_to_server(HOST_1, PORT_1))
    print("Establishing connection with server 2")
    servers.append(make_connection_to_server(HOST_2, PORT_2))
    print("Establishing connection with server 3")
    servers.append(make_connection_to_server(HOST_3, PORT_3))
    # 2. Inicializa tabela cache
    CACHE_TABLE = init_cache_table(servers)
    # 3. Inicializa conexão cache (cache listen on cache host, port)
    connection, address = create_connection(CACHE_HOST, CACHE_PORT)

    print("Connected by {}".format(address))
    while(True):
        # 4. Recebe nova conexão
        data = connection.recv(MESSAGE_SIZE_IN_BYTES)
        temperature_from_servers = []
        # 5. Para cada linha na tabela cache
        for cache_row in CACHE_TABLE:
            is_from_cache = True
            # 6. Checagem se o valor é valido
            if already_expired_cache_server_row(cache_row):
                is_from_cache = False
                print("Cache from {} is expired, requesting a new temperature".format(cache_row.get("server_name")))
                # 7. Se invalido faz uma requisição para atualizar pegar os valores
                cache_row = request_temperature_from_server(cache_row)
                print("Updating row {} from cache table".format(cache_row.get("server_name")))
                update_cache_table(cache_row)
            else:
                # 8. Se valido pega os valores da tabela cache
                print("Cache from {} stil valid, getting temperature from cache".format(cache_row.get("server_name")))
            print()

            temperature_from_servers.append({
                "temperature": cache_row.get("temperature"),
                "is_from_cache": is_from_cache,
                "server_name": cache_row.get("server_name")
            })
        # 9. Retorna os valores
        connection.sendall(str(json.dumps(temperature_from_servers)).encode("utf-8"))

        time.sleep(5)
```
### Cliente
No cliente é executado a requisição das temperaturas dos servidores para a cache.
1. É estabelecida conexão com a cache.
2. Envia a requisição;
3. Recebe a resposta;
4. Print dos resultados
```python

def make_connection_to_server(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    time.sleep(1)
    return client

def print_result(temperature_informations):
    is_from_cache = "WAS" if temperature_informations.get("is_from_cache") else "WAS NOT"
    temperature = temperature_informations.get("temperature")
    server = temperature_informations.get("server_name")

    print("Temperature on {} is {} and {} received from cache".format(server, temperature, is_from_cache))

if __name__ == '__main__':
    pass
    # 1. Cria conexão com cache
    client = make_connection_to_server(CACHE_HOST, CACHE_PORT)
    
    while True:
        # 2. Envia requisição para cache
        client.sendall(b"Get temperature")

        # 3. Recebe resposta
        temperatures = client.recv(MESSAGE_SIZE_IN_BYTES)
        temperatures = json.loads(temperatures.decode("utf-8"))

        # 4. Print resposta
        for temperature in temperatures:
            print_result(temperature)
        print()
```

### Como executar

Digite os seguintes comandos no terminal

Cada comando deve ser executado em um próprio terminal
```bash
$ python3 servidor1.py
```
```bash
$ python3 servidor2.py
```
```bash
$ python3 servidor3.py
```
```bash
$ python3 cache.py
```
```bash
$ python3 cliente.py
```