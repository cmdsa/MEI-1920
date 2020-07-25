## [Questão 1](Questao1)

[init-app.py](Questao1/init-app.py)

[blindSignature-app.py](Questao1/blindSignature-app.py)

[ofusca-app.py](Questao1/ofusca-app.py)

[desofusca-app.py](Questao1/desofusca-app.py)

[verify-app.py](Questao1/verify-app.py)

## Experiência 2.1

#### Questão

**Vá ao site www.ssllabs.com e efetue o SSL Server test para o site do Governo Português https://www.portugal.gov.pt/. E analise resultado.**

![Image](Imagens/result21.png)

Podemos observar que o SSL report classifica o host (https://www.portugal.gov.pt/) como A+, isto deve-se ao fato de este site trabalhar em browsers com suporte Server Name Indication, o que permite ao servidor hospedar com segurança diversos certificados  TLS/SSL de diversos sites apenas num único ip. Além disso tem implementada HSTS com longa duração, o que lhe permite estar protegido contra ataques de downgrade protocol e também “roubo” de cookies.
No restante relatório podemos ver informações sobre certificado: o tipo de algoritmo usado(SHA256withRSA), o tamanho da chave(2048 bits), a data de validade do certificado, o emissor do certificado entre outros parâmetros referentes ao certificado em questão.
Abaixo temos mais alguns certificados adicionais e os seus respetivos dados, e por fim temos um descrição de quais protocolos são aceites/usados e suas respetivas versões, além das Cipher Suites.

## Questão 2.1

**Escolha dois sites de empresas cotadas no NASDAQ.**
1. Anexe os resultados do SSL Server test à sua resposta.
2. Analise o resultado do SSL Server test relativo ao site escolhido com pior rating. Que comentários pode fazer sobre a sua segurança. Porquê?
3. É natural que tenha reparado na seguinte informação: "OpenSSL Padding Oracle vuln. (CVE-2016-2107)" na secção de detalhe do protocolo. O que significa, para efeitos práticos?

![fortyseveninc](Imagens/fortyseveninc.png)
Imagem – SSL Report do site da empresa fortyseveninc

![karyopharm](Imagens/karyopharm.png)
Imagem – SSL Report do site da empresa karyopharm

![CalavoGrowers](Imagens/Calavo_Growers.png)
Imagem – SSL Report da empresa Calavo Growers

## Questão 2.1.2

Na recolha dos relatórios SSL podemos verificar que grande parte dos sites das empresas cotadas no NASDAQ possuem uma avaliação semelhante, logo escolhemos um relatório que se sobressaiu aos outros, o da empresa Calavo Growers, e é deste relatório que iremos fazer análise.
Este relatório classifica o site da empresa Calavo Growser Inc. com T, ou se ignorarmos os problemas de confiança seria classificada com C. Esta avaliação deve-se principalmente ao fato do certificado deste server não ser confiável. Na analise do certificado é possível observar o porquê, pois o certificado em questão está expirado(fora de validade), como se pode verificar na figura abaixo.

![validoate](Imagens/validoate.png)

Para além do certificado expirado, este server está vulnerável ataques POODLE, sendo possível mitigar desativando SSL 3 . O site também aceita cifras RC4 com protocolos antigos considerados “Fracos” e até mesmo “Inseguros”. O fato deste server não suportar Forward Secrecy nos browser de referencia e de suportar TLS 1.0 e TLS 1.1 torna esta avaliação ainda mais negativa. 

![ssl](Imagens/ssl.png)

Porque ao não usar sigilo direto, o sigilo de encaminhamento acaba por não proteger as sessões anteriores contra futuros comprometimentos da chave privada. Principalmente com a troca de chaves RSA que não fornece sigilo direto. 

![rsakeys](Imagens/rsakeys.png)

## Questão 2.1.3
Inicialmente começamos por analisar o CVE fornecido na NVD(National Vulnerability DataBase), onde verificamos que se trata da implementação da AES-NI numas quantas versões do OpenSSL não considerar a alocação de memória durante uma determinada verificação de preenchimento, o que pode levar aos atacantes obtenher informações sensíveis em texto limpo, isto é não criptografado por meio de um ataque de padding-oracle a uma sessão AES CBC . 
É uma vulnerabilidade classificada com 5.9 pela NVD, o que é considerada com um risco médio.
Segundo um artigo disponibilizado pelo próprio relatório SSL, diz-nos que os conjuntos de cifras CBC no TLS possuem uma falha de design: primeiro calculam o HMAC do texto sem formatação e depois criptografam, isto usando Cipher Block Chaining. 
Porem quem recebe tenha que decifrar a mensagem e comparar o HMAC sem nunca dar a conhecer o tamanho de padding. 
Caso o atacante conheça o tamanho poderá aprender o ultimo byte de cada bloco e iterativamente, a mensagem na sua totalidade. A isto é chamado padding oracle.

![example](Imagens/example.jpg)

Neste mesmo bloco, é referido uma solução que se baseia no seguinte:
“Escrever todo o HMAC e o código de verificação do padding de modo a executar em tempo perfeitamente constante.”

Referência: https://blog.cloudflare.com/yet-another-padding-oracle-in-openssl-cbc-ciphersuites/

Resumidamente, o ponto crucial desta vulnerabilidade é guardar a comparação de cada bit da verificação, isto permite que o atacante apenas saiba se tudo ta certo ou errado.


## Experiencia 3.1

#### Questão 3.0

**Utilize o ssh-audit para efetuar um teste ao servidor algo.paranoidjasmine.com, i.e.**

Ao fazer uso do comando ```python ssh-audit.py algo.paranoidjasmine.com```, é possível efetuar um teste ao servidor algo.paranoidjasmine.com, como mostra a figura abaixo.

![paranoidjasmine](Imagens/paranoidjasmine.png)

Figura - Teste ao servidor algo.paranoidjasmine.com

## Questão 3.1.1 

**Anexe os resultados SSH à tua resposta.**

Após fazer registo no shodan, realizamos diversas pesquisas de algumas empresas cotadas na NASDAQ de modo a nos facilitar a pesquisa por servidores ssh na porta 22.

**Empresa 1:**

```bash
python ssh-audit.py 146.152.205.96
# general
(gen) banner: SSH-2.0-OpenSSH_8.0
(gen) software: OpenSSH 8.0
(gen) compatibility: OpenSSH 7.3+, Dropbear SSH 2016.73+
(gen) compression: enabled (zlib@openssh.com)

# key exchange algorithms
(kex) curve25519-sha256                     -- [warn] unknown algorithm
(kex) curve25519-sha256@libssh.org          -- [info] available since OpenSSH 6.5, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp256                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp384                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp521                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) diffie-hellman-group-exchange-sha256  -- [warn] using custom size modulus (possibly weak)
                                            `- [info] available since OpenSSH 4.4
(kex) diffie-hellman-group16-sha512         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
(kex) diffie-hellman-group18-sha512         -- [info] available since OpenSSH 7.3
(kex) diffie-hellman-group14-sha256         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
(kex) diffie-hellman-group14-sha1           -- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 3.9, Dropbear SSH 0.53

# host-key algorithms
(key) rsa-sha2-512                          -- [info] available since OpenSSH 7.2
(key) rsa-sha2-256                          -- [info] available since OpenSSH 7.2
(key) ssh-rsa                               -- [info] available since OpenSSH 2.5.0, Dropbear SSH 0.28
(key) ecdsa-sha2-nistp521                   -- [fail] using weak elliptic curves
                                            `- [warn] using weak random number generator could reveal the key
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(key) ssh-ed25519                           -- [info] available since OpenSSH 6.5

# encryption algorithms (ciphers)
(enc) chacha20-poly1305@openssh.com         -- [info] available since OpenSSH 6.5
                                            `- [info] default cipher since OpenSSH 6.9.
(enc) aes256-gcm@openssh.com                -- [info] available since OpenSSH 6.2
(enc) aes128-gcm@openssh.com                -- [info] available since OpenSSH 6.2
(enc) aes256-ctr                            -- [info] available since OpenSSH 3.7, Dropbear SSH 0.52
(enc) aes192-ctr                            -- [info] available since OpenSSH 3.7
(enc) aes128-ctr                            -- [info] available since OpenSSH 3.7, Dropbear SSH 0.52

# message authentication code algorithms
(mac) umac-64-etm@openssh.com               -- [warn] using small 64-bit tag size
                                            `- [info] available since OpenSSH 6.2
(mac) umac-128-etm@openssh.com              -- [info] available since OpenSSH 6.2
(mac) hmac-sha2-256-etm@openssh.com         -- [info] available since OpenSSH 6.2
(mac) hmac-sha2-512-etm@openssh.com         -- [info] available since OpenSSH 6.2
(mac) hmac-sha1-etm@openssh.com             -- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 6.2
(mac) umac-64@openssh.com                   -- [warn] using encrypt-and-MAC mode
                                            `- [warn] using small 64-bit tag size
                                            `- [info] available since OpenSSH 4.7
(mac) umac-128@openssh.com                  -- [warn] using encrypt-and-MAC mode
                                            `- [info] available since OpenSSH 6.2
(mac) hmac-sha2-256                         -- [warn] using encrypt-and-MAC mode
                                            `- [info] available since OpenSSH 5.9, Dropbear SSH 2013.56
(mac) hmac-sha2-512                         -- [warn] using encrypt-and-MAC mode
                                            `- [info] available since OpenSSH 5.9, Dropbear SSH 2013.56
(mac) hmac-sha1                             -- [warn] using encrypt-and-MAC mode
                                            `- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 2.1.0, Dropbear SSH 0.28

# algorithm recommendations (for OpenSSH 8.0)
(rec) -ecdh-sha2-nistp521                   -- kex algorithm to remove 
(rec) -ecdh-sha2-nistp384                   -- kex algorithm to remove 
(rec) -diffie-hellman-group14-sha1          -- kex algorithm to remove 
(rec) -ecdh-sha2-nistp256                   -- kex algorithm to remove 
(rec) -diffie-hellman-group-exchange-sha256 -- kex algorithm to remove 
(rec) -ecdsa-sha2-nistp521                  -- key algorithm to remove 
(rec) -hmac-sha2-512                        -- mac algorithm to remove 
(rec) -umac-128@openssh.com                 -- mac algorithm to remove 
(rec) -hmac-sha2-256                        -- mac algorithm to remove 
(rec) -umac-64@openssh.com                  -- mac algorithm to remove 
(rec) -hmac-sha1                            -- mac algorithm to remove 
(rec) -hmac-sha1-etm@openssh.com            -- mac algorithm to remove 
(rec) -umac-64-etm@openssh.com              -- mac algorithm to remove 
```
**Empresa 2:**
```bash
# general
(gen) banner: SSH-2.0-OpenSSH_7.4
(gen) software: OpenSSH 7.4
(gen) compatibility: OpenSSH 7.3+ (some functionality from 6.6), Dropbear SSH 2016.73+ (some functionality from 0.52)
(gen) compression: enabled (zlib@openssh.com)

# key exchange algorithms
(kex) curve25519-sha256                     -- [warn] unknown algorithm
(kex) curve25519-sha256@libssh.org          -- [info] available since OpenSSH 6.5, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp256                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp384                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp521                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) diffie-hellman-group-exchange-sha256  -- [warn] using custom size modulus (possibly weak)
                                            `- [info] available since OpenSSH 4.4
(kex) diffie-hellman-group16-sha512         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
(kex) diffie-hellman-group18-sha512         -- [info] available since OpenSSH 7.3
(kex) diffie-hellman-group-exchange-sha1    -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 2.3.0
(kex) diffie-hellman-group14-sha256         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
(kex) diffie-hellman-group14-sha1           -- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 3.9, Dropbear SSH 0.53
(kex) diffie-hellman-group1-sha1            -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [fail] disabled (in client) since OpenSSH 7.0, logjam attack
                                            `- [warn] using small 1024-bit modulus
                                            `- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 2.3.0, Dropbear SSH 0.28

# host-key algorithms
(key) ssh-rsa                               -- [info] available since OpenSSH 2.5.0, Dropbear SSH 0.28
(key) rsa-sha2-512                          -- [info] available since OpenSSH 7.2
(key) rsa-sha2-256                          -- [info] available since OpenSSH 7.2
(key) ecdsa-sha2-nistp256                   -- [fail] using weak elliptic curves
                                            `- [warn] using weak random number generator could reveal the key
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(key) ssh-ed25519                           -- [info] available since OpenSSH 6.5

# encryption algorithms (ciphers)
(enc) chacha20-poly1305@openssh.com         -- [info] available since OpenSSH 6.5
                                            `- [info] default cipher since OpenSSH 6.9.
(enc) aes128-ctr                            -- [info] available since OpenSSH 3.7, Dropbear SSH 0.52
(enc) aes192-ctr                            -- [info] available since OpenSSH 3.7
(enc) aes256-ctr                            -- [info] available since OpenSSH 3.7, Dropbear SSH 0.52
(enc) aes128-gcm@openssh.com                -- [info] available since OpenSSH 6.2
(enc) aes256-gcm@openssh.com                -- [info] available since OpenSSH 6.2
(enc) aes128-cbc                            -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [warn] using weak cipher mode
                                            `- [info] available since OpenSSH 2.3.0, Dropbear SSH 0.28
(enc) aes192-cbc                            -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [warn] using weak cipher mode
                                            `- [info] available since OpenSSH 2.3.0
(enc) aes256-cbc                            -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [warn] using weak cipher mode
                                            `- [info] available since OpenSSH 2.3.0, Dropbear SSH 0.47
(enc) blowfish-cbc                          -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [fail] disabled since Dropbear SSH 0.53
                                            `- [warn] disabled (in client) since OpenSSH 7.2, legacy algorithm
                                            `- [warn] using weak cipher mode
                                            `- [warn] using small 64-bit block size
                                            `- [info] available since OpenSSH 1.2.2, Dropbear SSH 0.28
(enc) cast128-cbc                           -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [warn] disabled (in client) since OpenSSH 7.2, legacy algorithm
                                            `- [warn] using weak cipher mode
                                            `- [warn] using small 64-bit block size
                                            `- [info] available since OpenSSH 2.1.0
(enc) 3des-cbc                              -- [fail] removed (in server) since OpenSSH 6.7, unsafe algorithm
                                            `- [warn] using weak cipher
                                            `- [warn] using weak cipher mode
                                            `- [warn] using small 64-bit block size
                                            `- [info] available since OpenSSH 1.2.2, Dropbear SSH 0.28

# message authentication code algorithms
(mac) umac-64-etm@openssh.com               -- [warn] using small 64-bit tag size
                                            `- [info] available since OpenSSH 6.2
(mac) umac-128-etm@openssh.com              -- [info] available since OpenSSH 6.2
(mac) hmac-sha2-256-etm@openssh.com         -- [info] available since OpenSSH 6.2
(mac) hmac-sha2-512-etm@openssh.com         -- [info] available since OpenSSH 6.2
(mac) hmac-sha1-etm@openssh.com             -- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 6.2
(mac) umac-64@openssh.com                   -- [warn] using encrypt-and-MAC mode
                                            `- [warn] using small 64-bit tag size
                                            `- [info] available since OpenSSH 4.7
(mac) umac-128@openssh.com                  -- [warn] using encrypt-and-MAC mode
                                            `- [info] available since OpenSSH 6.2
(mac) hmac-sha2-256                         -- [warn] using encrypt-and-MAC mode
                                            `- [info] available since OpenSSH 5.9, Dropbear SSH 2013.56
(mac) hmac-sha2-512                         -- [warn] using encrypt-and-MAC mode
                                            `- [info] available since OpenSSH 5.9, Dropbear SSH 2013.56
(mac) hmac-sha1                             -- [warn] using encrypt-and-MAC mode
                                            `- [warn] using weak hashing algorithm
                                            `- [info] available since OpenSSH 2.1.0, Dropbear SSH 0.28

# algorithm recommendations (for OpenSSH 7.4)
(rec) -diffie-hellman-group14-sha1          -- kex algorithm to remove 
(rec) -ecdh-sha2-nistp256                   -- kex algorithm to remove 
(rec) -diffie-hellman-group-exchange-sha256 -- kex algorithm to remove 
(rec) -diffie-hellman-group1-sha1           -- kex algorithm to remove 
(rec) -diffie-hellman-group-exchange-sha1   -- kex algorithm to remove 
(rec) -ecdh-sha2-nistp521                   -- kex algorithm to remove 
(rec) -ecdh-sha2-nistp384                   -- kex algorithm to remove 
(rec) -ecdsa-sha2-nistp256                  -- key algorithm to remove 
(rec) -blowfish-cbc                         -- enc algorithm to remove 
(rec) -3des-cbc                             -- enc algorithm to remove 
(rec) -aes256-cbc                           -- enc algorithm to remove 
(rec) -cast128-cbc                          -- enc algorithm to remove 
(rec) -aes192-cbc                           -- enc algorithm to remove 
(rec) -aes128-cbc                           -- enc algorithm to remove 
(rec) -hmac-sha2-512                        -- mac algorithm to remove 
(rec) -umac-128@openssh.com                 -- mac algorithm to remove 
(rec) -hmac-sha2-256                        -- mac algorithm to remove 
(rec) -umac-64@openssh.com                  -- mac algorithm to remove 
(rec) -hmac-sha1                            -- mac algorithm to remove 
(rec) -hmac-sha1-etm@openssh.com            -- mac algorithm to remove 
(rec) -umac-64-etm@openssh.com              -- mac algorithm to remove 
```

## Questão 3.1.2

**Indique o software e versão utilizada pelos servidores ssh.**

Como é possível observar nas imagens acima, o software e versão utilizada pelos servidores ssh são:

**Empresa 1:**
- 146.152.205.96 – Intel Corporation
- Software: OpenSSH
- Versão: 8.0

**Empresa 2:**
- 193.164.17.134 – Apple Tecnologies LLC 
- Software: OpenSSH
- Versão: 7.4


## Questão 3.1.3
Através de uma busca por CVE no NVD(National vulnerability DataBase) e recorrendo ao próprio shodan podemos concluir que a versão 7.4 possui já duas vulnerabilidades descobertas e publicadas enquanto que a versão 8.0 ainda não possui quaisquer vulnerabilidades publicadas. Os CVE’s das vulnerabilidades podem ser observadas na imagem abaixo.

![applevul](Imagens/applevul.png)

Figura. - Vulnerabilidades encontradas – Apple Tecnologies LLC 


## Questão 3.1.4

**E qual tem a vulnerabilidade mais grave (de acordo com o CVSS score identificado no CVE details)?**

A vulnerabilidade com o CVE-2018-15919 é considerada mais grave dentro das enumeradas, esta possui um CVSS score na versão 3.x de 5.3(Medium) e na versão 2.0 um apontuaçao semelhante de 5.0(Medium), enquanto que a outra é apenas considerada baixa em termo de gravidade, com uma pontuaçao de 3.0.


## Questão 3.1.5

**Para efeitos práticos, a vulnerabilidade indicada no ponto anterior é grave? Porquê?**

A vulnerabilidade em questão é considerada grave, pois esta pode permitir que um invasor/atacante aproveite a vulnerabilidade de enumeração de usuario, permitindo o recolher contas de usuarios validos, o que pode ajudar no uso de um ataque de força bruta. Mas felizmente esta vulnerabilidade foi corrigida nas versoes superiores a esta. 
