## Questão 1

#### 1.1

Para utilizar a data de hoje e para a data incluida ser "Bloco inicial da koreCoin" , mudamos:


```javascript
createGenesisBlock(){
        return new Block(0, "02/01/2018", "Genesis Block", "0");
    }
```

para:

```javascript
 createGenesisBlock(){
        return new Block(0, Date(), "Bloco inicial da koreCoin", "0");
    }
```

Sendo que ```Date()``` dá-nos o dia atual, e a hora.

O output será algo assim:

```bash
"chain": [
        {
            "index": 0,
            "timestamp": "Fri Mar 20 2020 21:31:19 GMT+0000 (GMT)",
            "data": "Bloco inicial da koreCoin",
            "previousHash": "0",
            "hash": "5373580d3e1a5ccd906bd11afb9b7a60f7937657023d1d929ec483c86969b1f3"
        },
```

#### 1.2

Para adicionar novos blocos apenas temos de invocar a função addBlock(), e introduzir os dados necessários, neste caso, o index, o timestamp e a os dados associados

```javascript
koreCoin.addBlock(new Block (1, "01/01/2018", {amount: 20}));
koreCoin.addBlock(new Block (2, "02/01/2018", {amount: 40}));
koreCoin.addBlock(new Block (3, "02/01/2018", {amount: 40}));
//novos blocos
koreCoin.addBlock(new Block (4, Date(), {amount: 100}));
koreCoin.addBlock(new Block (5, Date(), {amount: 200}));
koreCoin.addBlock(new Block (5, Date(), {amount: 200}));
``` 

O output:

```bash
{
    "chain": [
        {
            "index": 0,
            "timestamp": "Fri Mar 20 2020 21:46:22 GMT+0000 (GMT)",
            "data": "Bloco inicial da koreCoin",
            "previousHash": "0",
            "hash": "9b484af541bea8fd64a71748e5f4c5c948c8c30271fb8b4a3d87e697fb9ac4db"
        },
        {
            "index": 1,
            "timestamp": "01/01/2018",
            "data": {
                "amount": 20
            },
            "previousHash": "9b484af541bea8fd64a71748e5f4c5c948c8c30271fb8b4a3d87e697fb9ac4db",
            "hash": "3628885b4d3b93082db9c7c9dd1d0370f9fd481e5a04bf36be4fdc84982db99e"
        },
        {
            "index": 2,
            "timestamp": "02/01/2018",
            "data": {
                "amount": 40
            },
            "previousHash": "3628885b4d3b93082db9c7c9dd1d0370f9fd481e5a04bf36be4fdc84982db99e",
            "hash": "6598fa0e526f13f6b6903e87ac00df117bffc422f4c90ebcf9b0774ed697a227"
        },
        {
            "index": 3,
            "timestamp": "02/01/2018",
            "data": {
                "amount": 40
            },
            "previousHash": "6598fa0e526f13f6b6903e87ac00df117bffc422f4c90ebcf9b0774ed697a227",
            "hash": "93091a951bd37c1fb323215ced0ae9d1515917c335ac76d0df90939157342fa5"
        },
        {
            "index": 4,
            "timestamp": "Fri Mar 20 2020 21:46:22 GMT+0000 (GMT)",
            "data": {
                "amount": 100
            },
            "previousHash": "93091a951bd37c1fb323215ced0ae9d1515917c335ac76d0df90939157342fa5",
            "hash": "fa170eda0075f42607900ad4e3d13b1baa66e139c7e278cc1a8bfcc146223f31"
        },
        {
            "index": 5,
            "timestamp": "Fri Mar 20 2020 21:46:22 GMT+0000 (GMT)",
            "data": {
                "amount": 200
            },
            "previousHash": "fa170eda0075f42607900ad4e3d13b1baa66e139c7e278cc1a8bfcc146223f31",
            "hash": "85a9a22b1c14c680a7d9bf1fe5a6478edbd243a02fa56a276f3b8946db417ad0"
        },
        {
            "index": 5,
            "timestamp": "Fri Mar 20 2020 21:46:22 GMT+0000 (GMT)",
            "data": {
                "amount": 200
            },
            "previousHash": "85a9a22b1c14c680a7d9bf1fe5a6478edbd243a02fa56a276f3b8946db417ad0",
            "hash": "efb3d7e4ef417d8b43ca8d1a3195dfc77bcaf7de59d71a165694bf6dadd37067"
        }
    ]
}
```

## Questão 2

#### 2.1

Primeiramente, para simplificar a mudança de dificuldade, recebemos o valor como argumento da linha de comandos.
Para isso mudamos no construtor da ```class Blockchain()``` para o seguinte:

```javascript
class Blockchain{
    constructor(){
        this.chain = [this.createGenesisBlock()];
        this.difficulty = parseInt(process.argv[2]);
    }
```
O output:

```bash
user@user:~/Documentos/Grupo13/Aula5$ time node p2.js 2
difficulty 2
Mining block 1...
Block mined: 007abd29e589b6a35f6107095cbc8a3628b7a8ff9ac5f7a203f79b262fff077e
Mining block 2...
Block mined: 009d3e5e004957e04604a4032cc58a97f33adb6711f93bc7514de8fe4a531a37
Mining block 3...
Block mined: 004bb82a658a99fd8c9f0d40ec9e69d3a441dacb6383242659b1ff8f7b42195b

real    0m0,091s
user    0m0,091s
sys     0m0,013s

user@user:~/Documentos/Grupo13/Aula5$ time node p2.js 3
difficulty 3
Mining block 1...
Block mined: 0007c25169f5256ebb80fcbb423b582a8e699a759e41abb28906295973f9de4c
Mining block 2...
Block mined: 0004af57b70136e9f4b5309f92d518b3f297168d4cf47d4f9354808daadce457
Mining block 3...
Block mined: 00075796ab77bb5289bb9a952b91047482b3348d54d915ff5e5bce28256d01fe

real    0m0,341s
user    0m0,364s
sys     0m0,034s

user@user:~/Documentos/Grupo13/Aula5$ time node p2.js 4
difficulty 4
Mining block 1...
Block mined: 0000023168f87d968813b22c4dc92f60c127ff5084af8487d913d497ea7a7900
Mining block 2...
Block mined: 00008e0c291aaf728e015855328b14e651231cce209e6413503fd299e0df6c5e
Mining block 3...
Block mined: 0000fb4a126ef4c1c3c93bf2ed25e8db4c7da2ec89a46aad4f7bf092afd8b6b4

real    0m1,555s
user    0m1,595s
sys     0m0,057s

user@user:~/Documentos/Grupo13/Aula5$ time node p2.js 5
difficulty 5
Mining block 1...
Block mined: 0000023168f87d968813b22c4dc92f60c127ff5084af8487d913d497ea7a7900
Mining block 2...
Block mined: 000000b950a180294edddf4340a2d5834119a41bf89e4b2027f341f0fc02365e
Mining block 3...
Block mined: 0000088dc9c3115ee6ab7e95d2e8836f932d75d303ab451a825241acde589a58

real    0m20,328s
user    0m20,489s
sys     0m0,283s
```

Podemos verificar que à medida que a dificuldade aumenta, o tempo de processamento aumenta também.
Isto deve-se ao facto de que à medida que a dificuldade aumenta (neste caso a dificuldade traduz-se no numero de zeros por qual a hash começa, então 001 é mais dificil que 01) o número de soluções disponiveis diminui,e como não conseguimos influenciar o valor de uma hash, o sistema necessita de encontrar um valor de hash que comece com x número de zeros, o que requer mais poder de processamento, e como tal demorará mais tempo.


#### 2.2

O código do proof of work é o seguinte:

```python
def proof_of_work(last_proof):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = last_proof + 1
  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain
  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor
```

Isto traduzido corresponde ao seguinte:
 
Quando o valor atual(incrementor) seja divisivel por 9 e divisivel pelo valor do Proof of Work anterior, o valor atual é devolvido como Proof of Work.
O algoritmo implementado consiste no mínimo múltiplo comum de 9 e do valor do Proof of Work anteiror.

O algoritmo implementado não serviria para minerar devido ao facto de:

- Não requer elevado poder computacional
- Ser de fácil resolução
- A complexidade é linear em relação à ultima solução
- As Proof of Work dependem da anterior, permitindo calcular as seguintes




