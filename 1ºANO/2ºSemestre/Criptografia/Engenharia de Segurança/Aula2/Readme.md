## P1

#### P1.1

Depois de gerar 1024 bytes pseudoaleatórios, seguimos para a realização dos testes de 4 comandos que obtem 1024 bytes pseudoaleatórios do sistema e o apresentam em base64.

Comandos:

- 1 -`head -c 32 /dev/random | openssl enc -base64`
- 2 -`head -c 64 /dev/random | openssl enc -base64`
- 3 -`head -c 1024 /dev/random | openssl enc -base64`
- 4 -`head -c 1024 /dev/urandom | openssl enc -base64`

A primeira diferença que podemos observar á primeira vista é o tamanho da sequencia gerada, pois temos 32,64 e 1024 bytes.
Outra diferença é as duas fontes de aleatoriedade utilizadas, pois temos random e urandom.
/dev/random acaba por exigir a espera do resultado, pois este usa pool de entropia, onde os dados aleatórios podem não estar disponíveis no momento. Enquanto o /dev/urandom devolve quantos bytes forem solicitados pelo usuário, logo é “menos” aleatório do que o anterior.
Alem disto, na execução destes comandos foi então possível observar e afirmar o que foi descrito acima. Os comandos que usam /dev/random demoraram mais tempo comparativamente com o que usa /dev/urandom e conforme a quantidade de bytes for superior, maiores será o tempo da execução. Já o comando 4 foi relativamente mais rápido comparativamente com o comando 3.

#### P1.2

Neste caso, foi possível ver um decréscimo do tempo de execução entre os comandos agora executados e os anteriormente executados. Isto deve-se ao fato de quando usa /dev/random para gerar a sequência pseudo aleatória, esta já não sofre com o tal bloqueio. Devido ao algoritmo haveged.

#### P1.3

Ao analisar o programa(código) de geração de segredo aleatório, é possível observar uma função que gera uma string random com ```SecretLength Characters(ascii_letters and digits)``` .

## P2

#### P2.A

Primeiramente criamos uma chave privada ```openssl genrsa -aes128 -out privatekey.pem 1024```

Onde a password escolhida foi ```12345```

A chave tem o seguinte conteudo:

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,403C1460041AE6D47FDECFB65E6242EB

CfCUXeZymsk9H5CyHgGTMqHVbxrgcoNUaMDuAvB1Cd17nxJcqx0yUvMB/kKZ5iMi
4RGCupIIbCF4RopwVNljXqAmC15ItMiSmUm7Y9P4D7BOOYJA5e32tyn5IOUvm+ic
iubgRVge1Nd7K7FbBy9zRN1th2bxGXeSy/tmfFH5nibaSF2RD+ktHrvOdqJMH0fv
gbEErVrj6C+Ejva2b6DXV99CLjukQ3nnPpSRT9+hbQH7Hz4WhxuflybQCOtpVxwL
tiAHCetyBQnpJVB8042WSjDa1S7Uw4RbdK2Pg4IHbhDSTzPZkGoWqkaGRa0EVuz/
2EFInRjg8pAYOlWrGEmsqvoOwAKJ0MFRJlonIeE2b8VOckYCyRg/Vv80dmfz3qQN
qB4vSzwVF0qsarOJd+tiF6wHXfAguZpxrXJIwwL1M+sntxdRsQw1WqqdzFKY55WV
zH3sFAnTBxpDMC2q9aueYFVTKAujVHjA/4YTp8A4UsuGlJ/1ZhHUu2D8K2BIZdqA
glV46eGWHgTj0NhcipS8qxP4Z0OW75Dlzu7MF6bltm17catZxvMUNzzhhJveQjWX
okM8fFn/765vfeRbMxV8GnI3W2Db9tDzBdbwuR4BoaF115YlIyJUk8Ivkm9FRrUg
iIksZOSFitb70hKzG8tJfImaFpX/JnTH+oGr+cVRwdeNeRZT7HU/mLXVrhpJyh5S
Ar61seT+R3UQ/T8GW9c7J7AiQuYEauSS6I7nDT1Zri6s58asyepzad0TgL1R6z8j
PSI60/dyotpTyciEA/tiU41GrXQHDQrby+sUXEYZj1VjbSdj84ptEG3dGEW054ah
-----END RSA PRIVATE KEY-----
```

Para dividir o segredo em 8 partes com quorom de 5 tivemos que utilizar a seguinte linha:

```
python createSharedSecret-app.py 8 5 grupo13 privatekey.pem
```

que utiliza o ficheiro createSharedSecret-app.py, baseado no modulo eVotUM.Cripto para chegar ao resultado apresentado a seguir:

```bash
$ python createSharedSecret-app.py 8 5 grupo13 privatekey.pem
Private key passphrase: 12345
Secret: Agora temos um segredo extremamente confidencial
Component: 1
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjEtZmVlNjYxMGVkMjUwY2U5MmIzY2E3ZGJlODc0MDNmN2Q4MjJjYTc3ZDJhOWUzYjUzMzYxNjRhNmZkODcyZjVlNTE1ODRlMjMwNjcxY2U1NDZjYzc3NWE3ZjQzNzkwZDI2IiwgImdydXBvMTMiLCA1LCA4LCAiN2U2MzQ2NjA5NmQyYzkxOWRjNjYxYWJhMzFiMWUyNDVhM2VkNDFjYjAxYzkwOWU5M2FkMWY4MTBkMzg0ZGU5MCJdfQ.PwEXWmFtCVEb5x3unvZV6RLmpgZAJL_U6chbMQzbNOFbv3A2Ymsb1W3EsLUIZbPraXsptYbXqhedCiVKE0uJxRpHahQJZcIYLKINLy7FYST_98EW-oyrIo5NQ6RMqeYOR6qcKpirGIteqxGm674ZhUm-IzqDji87X4TsuBUisa4
Component: 2
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjItYzAwZmQ3MzYxMWY4MGQzYTM3OWVjNzEwNTAxNjM5MjZiY2M5ZWIwMjg5MmExYTg0NDdlZDdkMWMwMjg2MjMxNjI0NTY1OTk1ZjYwYmIzNWYyMTg1YjMxN2U5YzQxNTA1IiwgImdydXBvMTMiLCA1LCA4LCAiMTY0OGNhMmY0ZjhmODdhZGQ0MTQ0MzQwYWFkYjQ5YzRkYjQ3NGM2N2M4ZDQ0Mzg1Yjc0ZThiYjBjNzBjMDhjMSJdfQ.NTpL7cl12Z0Z_GdxPHmDQNdUBsreoOW_SPy8KwNShM17x2hMavcO-U7W9eOgpFJ1DVgM1kwSAdN4XikLYBFWn8F9OTLYm8CPjd5lnKoGhi0N5DaYoUMuznB1YH0Djg_3HzwGltzAQ3935twSXLj6kMvAw65-Ant7tfzXXCz0XwI
Component: 3
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjMtNmNlMmExYWY5NzMzNmM1ZjhjMjMwODE1NjkwYWYzMDFlNDY2ODUzMmQ3Zjg2YTNiYzYyZmE5YzRmNmYzYzhmYTcxMjc4YzdhZmIxZWI5OWNmMDIwZmYyZDFjZTVkZmMxIiwgImdydXBvMTMiLCA1LCA4LCAiOTdkZTcwNzgyYjgyZjg0NzM5NjI4YjAwZDM0ZjE3ZjY1MTZkMTE5MzcyMjlhMWY1ODc5YzkyNmExNTc4N2FkNCJdfQ.nqe6qefIT_xwPx21eFi8ylUfZ171hc8DLG1LmXSdsOcAqkj1PeDg0EF3-gIg7-oflg6J3WTSB2TMCNLkGY2Epgamlxtwk8z8JZgv_up7lR93_FMsqKpGxvm9BTIKEGCSY5l7KD73ke0djO_JU71qGoSKzIlPEpBCwdUPuntPK18
Component: 4
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjQtY2Y3MDcwZWJlMzQ3Yjg4NGQyYWJlMjEzNTkzM2Y0MWVjMDU1MTVmMDYzZWMwMjJkYmIxNTcxZjQwMzgxODI0M2NkNDcyNzYwMmNmMjE3MzZlMmZhNjYwYmZjMzEwYmNlIiwgImdydXBvMTMiLCA1LCA4LCAiMzU1OTYzNmFhNmJmZTNhYzg5ZjM3MGUxMzJkNTYxMGRkYTU1YjBmYWU0OTZkZmIyNzMzNThmOGI2ZjU3YWUzMSJdfQ.HIbo9FL1oWfRlrkiha3s2mUHlm4qsJN9QYVQ3HcllFIhfyt4XREdGt22tp2PM2rU3XNjKdjwt6fgN6blLVI0aPGoRUPoZY0CPSnII_wK8r_TQmfFo2p9EX6-19_JHrcI06mnzHkaCQezKgvzTLM7_D1fue5kkx9p4lemN_6kAMY
Component: 5
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjUtOTNkZGQ2MDQ4MWExNGVhYWJhYWJkZTk1OTVhMDY1MGExMDEzOTRjMjZlZTRlNTdmMjJkYTc5NjBiODYxYjA1NDA1MTNjMjFkMGRkYjI5YWNjN2UyYTY1OWZmYWY2ZDhlIiwgImdydXBvMTMiLCA1LCA4LCAiMzNmNTgxM2MyMGRmYjI2NzMyMTFlNmJhNjA3NDRjNzljOGIxZDZiZmE2ZDM4NjM2MWE1ODRkMGY5NzRhMzEwNiJdfQ.WT-D7g55eMtGn2XXKkCGb6oZi942zRxU4l9_qFsIcpHeLJsH49ZWAmIbAmwV3HTPuKtcGlTmCdlJNlLGnMIjFrMXeC9sxzRClKP4zG5CbqSGg8fJcoV_m-JuyYLNWbT4drGQj2RJP1EA5zvj4k4_3VApZ7cy-0jDp0bA5-tcv1A
Component: 6
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjYtNDg2MjQyYmMwN2Q0MWM1MDgxYjM2ZjZkODE1OTBmY2Q4YjRiNTBkNTJmYzA0MmM1ZWJiZDY1ZjBlODMzN2IzY2RmZmJkZmRmZWJlODhjYzc4ZmNhMTYxNGY4MjIxMmVkIiwgImdydXBvMTMiLCA1LCA4LCAiZDQ1NzdhZTc3YzVjYTUxOWM4MDI2NjY5OTJkMTBlZTg0YzEzODViZjJiNmRhNGQxZDczNWEzOGM5YzMwMTA4NSJdfQ.lmILzhH4LdPfx2fihyJH9BuK1EGq0kXb26uwLLeRGaT_4dstrOJMrTaKMnmkPZQltOR5A5YE3zzNU9i0fgfrqdHDD0_MGjDS4AzyApR9pbn7JlK2wtDM_kpuMR3aDGmLQXxDgtVvrjpHQdBThPWwMZ_yin0F9RnHWuQJZOpqwyo
Component: 7
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjctNWQ0ODA5N2UxNTliOWY3M2YzNzBlZWIyNmQ2MDVmZWZlMWQwZjBmOWQyNTg3NDA4ZjVmZmRmYjhhODAyZDFjMDIwN2RlZjJkZTBlMjFhOTk0ZWMwYTI5MzBmMDE0MTkzIiwgImdydXBvMTMiLCA1LCA4LCAiNDAwMDIzMDE1NmY0OTY3MTkyOWQ2MDFlNjVlMGFmMjIzMWUxOGY2NjdjZTQ4OGM3YzhkZjM3Zjg1Y2I3MzZhNiJdfQ.SVH5flJYGVwnxCui7Edg5i19wTJ5Kfh78-EgXtMhjpnZ5j9Qjiiwo6Db588VeeTtzo1jqdB92IVNO-riNb_RMdsnz3C1VHiWh2bdB7ut5gzhsfADCcdnG1N5KKB1EaPG_3MXRqcZ8MfCh514FCwMoeyqfJqBEiROAJycCS2Kp6k
Component: 8
eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjgtMjRlYzVkNWY1NGRhZTY5MTY5YjA5ZWMxOThiMjYyNzRiYmE0NzNhNjc3ODRmZWMwMTNlNjkwZmE0ZjQ4Njk0Zjg0Mjg0OWUyZDI0OGViN2QzYmY1ZDA4MmM2N2M3NWZkIiwgImdydXBvMTMiLCA1LCA4LCAiNjg3YjQ5YTY1MTUxMTVlNGM1ZDhkZGJkMTMxNzIzNGY2Y2EyOWVmMDY5Y2VhNjEzMDkyMTNiYjU4NGY0NTk0OSJdfQ.P3uMy8_-9qBruetwX6o_7QCNj6s9MAYHE_2Oabp1Rw85ZzLQGBOb4V57BY3gbF8SL0-zts-Vpw4Se4MXdPmrMw9TIvzfVRLlCznoIkAzneqWUdQaJjS2JVMeP5PW_IhJiJsA1uKMiyEMVSVoE_A93a3_3JfMoUW8FS4s5qbP9Ho
```

Para de seguida recuperar o segredo, geramos o certificado com o comando ```openssl req -key mykey.pem -new -x509 -days 365 -out ce.cert```

o certificado tem o seguinte conteudo:
```
-----BEGIN CERTIFICATE-----
MIICZjCCAc+gAwIBAgIUC+Jdc+Ee1d+yyQXh80B3w3rnWgowDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yMDAyMjUwMDE2MTlaFw0yMTAy
MjQwMDE2MTlaMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEw
HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwgZ8wDQYJKoZIhvcNAQEB
BQADgY0AMIGJAoGBANwXH1eS2xUCZyaXFPpSyKRUYssdSu6tCAg/JvYY6SULH29Q
iaCv06NXYVtkcB2S05E90WJleXARp72azTQDyYbLId9EMMSY2d5Q3k1Z9d2uHYlF
XaVMCZnsvDJXvaZ+A7eLJWN/ZAxOL0A2j9ngqeLD5tWIJsLwxfrTsqj4nZLHAgMB
AAGjUzBRMB0GA1UdDgQWBBSEPWlanXwsAJiY0o4ludFOc5rn3zAfBgNVHSMEGDAW
gBSEPWlanXwsAJiY0o4ludFOc5rn3zAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3
DQEBCwUAA4GBAB46m6O5J05QE+TdCdrK0VyofrxGq3EzpjzrV5vT5n7F46TryW/P
zWIbZKt135/Er3ZC4k9k9LZqr1bUf9ix8aSRkHNpmGoHqbyHIca7drjd1ADi7lUi
dsXOlK32erY5tL20MvKfgTNXlVAQg7brZEtTTb/Z14BMc9cReYDlLQGl
-----END CERTIFICATE-----
```


#### P2.B

A diferença entre as duas é a seguinte:

 Enquanto que **recoverSecretFromComponents-app.py** pede apenas o minimo de componentes (quorum) para reconstruir o segredo, **recoverSecretFromAllComponents-app.py** pede todos os componentes em qual o segredo foi dividido para poder reconstruir

Eis o resultado:
```bash
$ python recoverSecretFromComponents-app.py 5 grupo13 ce.cert
Component 1: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjEtZmVlNjYxMGVkMjUwY2U5MmIzY2E3ZGJlODc0MDNmN2Q4MjJjYTc3ZDJhOWUzYjUzMzYxNjRhNmZkODcyZjVlNTE1ODRlMjMwNjcxY2U1NDZjYzc3NWE3ZjQzNzkwZDI2IiwgImdydXBvMTMiLCA1LCA4LCAiN2U2MzQ2NjA5NmQyYzkxOWRjNjYxYWJhMzFiMWUyNDVhM2VkNDFjYjAxYzkwOWU5M2FkMWY4MTBkMzg0ZGU5MCJdfQ.PwEXWmFtCVEb5x3unvZV6RLmpgZAJL_U6chbMQzbNOFbv3A2Ymsb1W3EsLUIZbPraXsptYbXqhedCiVKE0uJxRpHahQJZcIYLKINLy7FYST_98EW-oyrIo5NQ6RMqeYOR6qcKpirGIteqxGm674ZhUm-IzqDji87X4TsuBUisa4
Component 2: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjItYzAwZmQ3MzYxMWY4MGQzYTM3OWVjNzEwNTAxNjM5MjZiY2M5ZWIwMjg5MmExYTg0NDdlZDdkMWMwMjg2MjMxNjI0NTY1OTk1ZjYwYmIzNWYyMTg1YjMxN2U5YzQxNTA1IiwgImdydXBvMTMiLCA1LCA4LCAiMTY0OGNhMmY0ZjhmODdhZGQ0MTQ0MzQwYWFkYjQ5YzRkYjQ3NGM2N2M4ZDQ0Mzg1Yjc0ZThiYjBjNzBjMDhjMSJdfQ.NTpL7cl12Z0Z_GdxPHmDQNdUBsreoOW_SPy8KwNShM17x2hMavcO-U7W9eOgpFJ1DVgM1kwSAdN4XikLYBFWn8F9OTLYm8CPjd5lnKoGhi0N5DaYoUMuznB1YH0Djg_3HzwGltzAQ3935twSXLj6kMvAw65-Ant7tfzXXCz0XwI
Component 3: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjMtNmNlMmExYWY5NzMzNmM1ZjhjMjMwODE1NjkwYWYzMDFlNDY2ODUzMmQ3Zjg2YTNiYzYyZmE5YzRmNmYzYzhmYTcxMjc4YzdhZmIxZWI5OWNmMDIwZmYyZDFjZTVkZmMxIiwgImdydXBvMTMiLCA1LCA4LCAiOTdkZTcwNzgyYjgyZjg0NzM5NjI4YjAwZDM0ZjE3ZjY1MTZkMTE5MzcyMjlhMWY1ODc5YzkyNmExNTc4N2FkNCJdfQ.nqe6qefIT_xwPx21eFi8ylUfZ171hc8DLG1LmXSdsOcAqkj1PeDg0EF3-gIg7-oflg6J3WTSB2TMCNLkGY2Epgamlxtwk8z8JZgv_up7lR93_FMsqKpGxvm9BTIKEGCSY5l7KD73ke0djO_JU71qGoSKzIlPEpBCwdUPuntPK18
Component 4: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjQtY2Y3MDcwZWJlMzQ3Yjg4NGQyYWJlMjEzNTkzM2Y0MWVjMDU1MTVmMDYzZWMwMjJkYmIxNTcxZjQwMzgxODI0M2NkNDcyNzYwMmNmMjE3MzZlMmZhNjYwYmZjMzEwYmNlIiwgImdydXBvMTMiLCA1LCA4LCAiMzU1OTYzNmFhNmJmZTNhYzg5ZjM3MGUxMzJkNTYxMGRkYTU1YjBmYWU0OTZkZmIyNzMzNThmOGI2ZjU3YWUzMSJdfQ.HIbo9FL1oWfRlrkiha3s2mUHlm4qsJN9QYVQ3HcllFIhfyt4XREdGt22tp2PM2rU3XNjKdjwt6fgN6blLVI0aPGoRUPoZY0CPSnII_wK8r_TQmfFo2p9EX6-19_JHrcI06mnzHkaCQezKgvzTLM7_D1fue5kkx9p4lemN_6kAMY
Component 5: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjUtOTNkZGQ2MDQ4MWExNGVhYWJhYWJkZTk1OTVhMDY1MGExMDEzOTRjMjZlZTRlNTdmMjJkYTc5NjBiODYxYjA1NDA1MTNjMjFkMGRkYjI5YWNjN2UyYTY1OWZmYWY2ZDhlIiwgImdydXBvMTMiLCA1LCA4LCAiMzNmNTgxM2MyMGRmYjI2NzMyMTFlNmJhNjA3NDRjNzljOGIxZDZiZmE2ZDM4NjM2MWE1ODRkMGY5NzRhMzEwNiJdfQ.WT-D7g55eMtGn2XXKkCGb6oZi942zRxU4l9_qFsIcpHeLJsH49ZWAmIbAmwV3HTPuKtcGlTmCdlJNlLGnMIjFrMXeC9sxzRClKP4zG5CbqSGg8fJcoV_m-JuyYLNWbT4drGQj2RJP1EA5zvj4k4_3VApZ7cy-0jDp0bA5-tcv1A
Recovered secret: Agora temos um segredo extremamente confidencial
```

```bash
$ python recoverSecretFromAllComponents-app.py 8 grupo13 ce.cert
Component 1: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjEtZmVlNjYxMGVkMjUwY2U5MmIzY2E3ZGJlODc0MDNmN2Q4MjJjYTc3ZDJhOWUzYjUzMzYxNjRhNmZkODcyZjVlNTE1ODRlMjMwNjcxY2U1NDZjYzc3NWE3ZjQzNzkwZDI2IiwgImdydXBvMTMiLCA1LCA4LCAiN2U2MzQ2NjA5NmQyYzkxOWRjNjYxYWJhMzFiMWUyNDVhM2VkNDFjYjAxYzkwOWU5M2FkMWY4MTBkMzg0ZGU5MCJdfQ.PwEXWmFtCVEb5x3unvZV6RLmpgZAJL_U6chbMQzbNOFbv3A2Ymsb1W3EsLUIZbPraXsptYbXqhedCiVKE0uJxRpHahQJZcIYLKINLy7FYST_98EW-oyrIo5NQ6RMqeYOR6qcKpirGIteqxGm674ZhUm-IzqDji87X4TsuBUisa4
Component 2: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjItYzAwZmQ3MzYxMWY4MGQzYTM3OWVjNzEwNTAxNjM5MjZiY2M5ZWIwMjg5MmExYTg0NDdlZDdkMWMwMjg2MjMxNjI0NTY1OTk1ZjYwYmIzNWYyMTg1YjMxN2U5YzQxNTA1IiwgImdydXBvMTMiLCA1LCA4LCAiMTY0OGNhMmY0ZjhmODdhZGQ0MTQ0MzQwYWFkYjQ5YzRkYjQ3NGM2N2M4ZDQ0Mzg1Yjc0ZThiYjBjNzBjMDhjMSJdfQ.NTpL7cl12Z0Z_GdxPHmDQNdUBsreoOW_SPy8KwNShM17x2hMavcO-U7W9eOgpFJ1DVgM1kwSAdN4XikLYBFWn8F9OTLYm8CPjd5lnKoGhi0N5DaYoUMuznB1YH0Djg_3HzwGltzAQ3935twSXLj6kMvAw65-Ant7tfzXXCz0XwI
Component 3: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjMtNmNlMmExYWY5NzMzNmM1ZjhjMjMwODE1NjkwYWYzMDFlNDY2ODUzMmQ3Zjg2YTNiYzYyZmE5YzRmNmYzYzhmYTcxMjc4YzdhZmIxZWI5OWNmMDIwZmYyZDFjZTVkZmMxIiwgImdydXBvMTMiLCA1LCA4LCAiOTdkZTcwNzgyYjgyZjg0NzM5NjI4YjAwZDM0ZjE3ZjY1MTZkMTE5MzcyMjlhMWY1ODc5YzkyNmExNTc4N2FkNCJdfQ.nqe6qefIT_xwPx21eFi8ylUfZ171hc8DLG1LmXSdsOcAqkj1PeDg0EF3-gIg7-oflg6J3WTSB2TMCNLkGY2Epgamlxtwk8z8JZgv_up7lR93_FMsqKpGxvm9BTIKEGCSY5l7KD73ke0djO_JU71qGoSKzIlPEpBCwdUPuntPK18
Component 4: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjQtY2Y3MDcwZWJlMzQ3Yjg4NGQyYWJlMjEzNTkzM2Y0MWVjMDU1MTVmMDYzZWMwMjJkYmIxNTcxZjQwMzgxODI0M2NkNDcyNzYwMmNmMjE3MzZlMmZhNjYwYmZjMzEwYmNlIiwgImdydXBvMTMiLCA1LCA4LCAiMzU1OTYzNmFhNmJmZTNhYzg5ZjM3MGUxMzJkNTYxMGRkYTU1YjBmYWU0OTZkZmIyNzMzNThmOGI2ZjU3YWUzMSJdfQ.HIbo9FL1oWfRlrkiha3s2mUHlm4qsJN9QYVQ3HcllFIhfyt4XREdGt22tp2PM2rU3XNjKdjwt6fgN6blLVI0aPGoRUPoZY0CPSnII_wK8r_TQmfFo2p9EX6-19_JHrcI06mnzHkaCQezKgvzTLM7_D1fue5kkx9p4lemN_6kAMY
Component 5: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjUtOTNkZGQ2MDQ4MWExNGVhYWJhYWJkZTk1OTVhMDY1MGExMDEzOTRjMjZlZTRlNTdmMjJkYTc5NjBiODYxYjA1NDA1MTNjMjFkMGRkYjI5YWNjN2UyYTY1OWZmYWY2ZDhlIiwgImdydXBvMTMiLCA1LCA4LCAiMzNmNTgxM2MyMGRmYjI2NzMyMTFlNmJhNjA3NDRjNzljOGIxZDZiZmE2ZDM4NjM2MWE1ODRkMGY5NzRhMzEwNiJdfQ.WT-D7g55eMtGn2XXKkCGb6oZi942zRxU4l9_qFsIcpHeLJsH49ZWAmIbAmwV3HTPuKtcGlTmCdlJNlLGnMIjFrMXeC9sxzRClKP4zG5CbqSGg8fJcoV_m-JuyYLNWbT4drGQj2RJP1EA5zvj4k4_3VApZ7cy-0jDp0bA5-tcv1A
Component 6: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjYtNDg2MjQyYmMwN2Q0MWM1MDgxYjM2ZjZkODE1OTBmY2Q4YjRiNTBkNTJmYzA0MmM1ZWJiZDY1ZjBlODMzN2IzY2RmZmJkZmRmZWJlODhjYzc4ZmNhMTYxNGY4MjIxMmVkIiwgImdydXBvMTMiLCA1LCA4LCAiZDQ1NzdhZTc3YzVjYTUxOWM4MDI2NjY5OTJkMTBlZTg0YzEzODViZjJiNmRhNGQxZDczNWEzOGM5YzMwMTA4NSJdfQ.lmILzhH4LdPfx2fihyJH9BuK1EGq0kXb26uwLLeRGaT_4dstrOJMrTaKMnmkPZQltOR5A5YE3zzNU9i0fgfrqdHDD0_MGjDS4AzyApR9pbn7JlK2wtDM_kpuMR3aDGmLQXxDgtVvrjpHQdBThPWwMZ_yin0F9RnHWuQJZOpqwyo
Component 7: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjctNWQ0ODA5N2UxNTliOWY3M2YzNzBlZWIyNmQ2MDVmZWZlMWQwZjBmOWQyNTg3NDA4ZjVmZmRmYjhhODAyZDFjMDIwN2RlZjJkZTBlMjFhOTk0ZWMwYTI5MzBmMDE0MTkzIiwgImdydXBvMTMiLCA1LCA4LCAiNDAwMDIzMDE1NmY0OTY3MTkyOWQ2MDFlNjVlMGFmMjIzMWUxOGY2NjdjZTQ4OGM3YzhkZjM3Zjg1Y2I3MzZhNiJdfQ.SVH5flJYGVwnxCui7Edg5i19wTJ5Kfh78-EgXtMhjpnZ5j9Qjiiwo6Db588VeeTtzo1jqdB92IVNO-riNb_RMdsnz3C1VHiWh2bdB7ut5gzhsfADCcdnG1N5KKB1EaPG_3MXRqcZ8MfCh514FCwMoeyqfJqBEiROAJycCS2Kp6k
Component 8: eyJhbGciOiAiUlMyNTYifQ.eyJvYmplY3QiOiBbIjgtMjRlYzVkNWY1NGRhZTY5MTY5YjA5ZWMxOThiMjYyNzRiYmE0NzNhNjc3ODRmZWMwMTNlNjkwZmE0ZjQ4Njk0Zjg0Mjg0OWUyZDI0OGViN2QzYmY1ZDA4MmM2N2M3NWZkIiwgImdydXBvMTMiLCA1LCA4LCAiNjg3YjQ5YTY1MTUxMTVlNGM1ZDhkZGJkMTMxNzIzNGY2Y2EyOWVmMDY5Y2VhNjEzMDkyMTNiYjU4NGY0NTk0OSJdfQ.P3uMy8_-9qBruetwX6o_7QCNj6s9MAYHE_2Oabp1Rw85ZzLQGBOb4V57BY3gbF8SL0-zts-Vpw4Se4MXdPmrMw9TIvzfVRLlCznoIkAzneqWUdQaJjS2JVMeP5PW_IhJiJsA1uKMiyEMVSVoE_A93a3_3JfMoUW8FS4s5qbP9Ho
Recovered secret: Agora temos um segredo extremamente confidencial
```

A utilidade dos dois poderá depender do quão "seguro" queremos que o nosso segredo seja.
Sendo que **recoverSecretFromComponents-app.py** apenas necessita do numero minimo de componentes para gerar o segredo, podemos assumir que o caso mais util deste seria no caso de ser necessário recuperar o segredo mesmo que partes dos componentes fossem perdidas, ou caso num grupo de elementos que possuissem um componente, quorum elementos poderiam revelar o segredo.
Por exemplo, um codigo de acesso de uma conta bancária, partilhado por uma familia de 3, onde este segredo é divido em 3 com um quorum de 2, sendo que seria sempre necessário dois elementos para aceder à conta (mãe-pai, pai-filho, mae-filho) e evitar mau uso por parte de um único elemento.


 **recoverSecretFromAllComponents-app.py** pede todos os componentes em qual o segredo foi dividido para poder reconstruir, logo o caso mais util deste seria quando o segredo que este esconde só podesse ser revelado caso todas as partes que possuem cada componente concordassem em revelar o segredo.
 
 Um exemplo (exagerado) de um bom caso de uso poderia ser para esconder os codigos de lançamento de uma bomba nuclear.
 Para poder ter acesso ao codigo, cada pessoa que possuisse um componente teria de concordar em transmitir o seu para que o segredo fosse revelado.
 
 ## P4
 
 #### P4.1
 
 Roménia, para a EC "CERTSIGN S.A. - QCert for Esig

Resposta:
Podemos observar a baixo que é usado o SHA256 com RSA como algoritmo de assinatura. A chave possui um tamanho de 4096 bit. O que segundo as recomendações da Nist se encontra acomodado para ser utilizado durante mais uns anos(2030). Em relação ao tamanho da chave-publica podemos ver que se encontra acima do que é recomendado, logo também é adequado.

```bash
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            10:02:a9:80:fb:5f:45:85:dd:08
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = RO, O = CERTSIGN SA, OU = certSIGN ROOT CA G2
        Validity
            Not Before: Feb  6 10:06:03 2017 GMT
            Not After : Feb  6 10:06:03 2027 GMT
        Subject: C = RO, O = CERTSIGN SA, CN = certSIGN Qualified CA, organizationIdentifier = VATRO-18288250
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
                Modulus:
                    00:9d:f5:b2:5a:1a:a8:77:f8:64:93:f9:bd:e7:79:
                    63:dc:d3:e0:48:3c:85:7f:6d:99:b7:34:1d:20:62:
                    16:9c:66:5c:47:29:38:a2:62:c8:f9:fd:ee:06:c4:
                    f5:2b:6d:89:84:bd:52:a7:7c:fe:65:27:59:29:af:
                    da:cc:b2:49:81:61:a7:6e:ce:8d:1f:73:96:77:bd:
                    64:bc:53:2d:99:4f:81:99:d2:9b:ea:81:a1:cd:33:
                    49:8f:0f:5b:53:d1:7e:b1:0d:2c:b6:08:39:19:d2:
                    36:96:53:5b:3e:71:64:b0:ae:08:76:73:d2:4e:9d:
                    07:a0:9f:88:e0:40:b0:cf:14:69:9d:0e:cf:bb:7d:
                    ec:2c:d8:17:c6:4a:17:2a:c9:12:b7:bb:d8:68:48:
                    00:4b:e3:02:49:59:c9:57:c5:54:47:89:8d:40:cf:
                    48:21:67:52:c0:3e:87:3f:fa:ff:a9:7a:5f:a8:7d:
                    d6:59:3e:26:8c:2e:4d:4d:e7:c0:36:72:2e:86:7a:
                    c5:40:49:13:df:53:10:f0:a1:e3:a4:55:63:19:b7:
                    5a:f6:24:c6:21:d3:a9:d2:cb:fc:30:ff:d9:4c:12:
                    a0:2a:8a:c7:96:d8:12:a8:0d:19:82:63:87:b5:f9:
                    c3:c1:e1:d3:89:e5:41:34:5d:12:4b:13:2e:ed:f7:
                    de:0f:e8:11:eb:3c:8e:2f:8b:d1:e3:7a:bf:7b:d2:
                    90:d9:6f:c3:b0:94:77:d9:2d:2b:bf:b3:94:09:21:
                    3a:c8:8e:c4:48:68:90:73:57:b7:18:80:49:1e:5d:
                    dc:af:dc:fb:35:49:b6:b1:65:6a:6f:cd:18:e6:41:
                    2b:3f:91:d0:7e:93:92:9f:4a:a7:4f:93:07:92:4a:
                    60:d9:3f:8f:58:e4:c6:9b:e2:5f:ca:72:5a:9d:06:
                    74:7d:fb:e2:02:e0:f1:39:07:de:38:75:88:6e:c7:
                    84:3d:89:dd:a1:fb:2f:1c:f6:4f:4a:f4:96:05:15:
                    b3:66:c9:f7:6e:4d:a8:e4:dc:5a:4a:b2:fb:24:9a:
                    f3:88:1b:9e:92:84:22:1f:56:45:13:6a:de:e8:db:
                    99:dd:1c:b1:1d:81:e3:a8:c7:58:14:57:b6:9d:7f:
                    53:6c:54:c8:30:34:dc:5c:bb:62:ed:ce:4b:68:fa:
                    08:db:7b:f4:2d:f0:b1:76:e8:bd:61:91:c0:80:fa:
                    32:23:2f:9d:38:1e:64:68:18:9f:6d:e5:50:b1:ca:
                    fc:92:38:26:f9:3e:a8:db:2e:5f:66:c7:6f:85:00:
                    71:7c:d8:2a:ce:f4:3d:d7:03:69:ad:7f:2a:19:11:
                    67:b5:d9:35:42:7c:c6:c1:89:4e:8a:c8:be:15:2f:
                    89:5f:b5
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            Authority Information Access: 
                OCSP - URI:http://ocsp.certsign.ro
                CA Issuers - URI:http://www.certsign.ro/certcrl/certsign-rootg2.crt

            X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:0
            X509v3 Key Usage: critical
                Certificate Sign, CRL Sign
            X509v3 Authority Key Identifier: 
                keyid:82:21:2D:66:C6:D7:A0:E0:15:EB:CE:4C:09:77:C4:60:9E:54:6E:03

            X509v3 Subject Key Identifier: 
                8F:4D:87:51:5E:11:7F:E1:99:C3:91:F1:68:4C:3F:AC:59:04:B1:8B
            X509v3 Certificate Policies: 
                Policy: X509v3 Any Policy
                  CPS: http://www.certsign.ro/repository

            X509v3 CRL Distribution Points: 

                Full Name:
                  URI:http://crl.certsign.ro/certsign-rootg2.crl

    Signature Algorithm: sha256WithRSAEncryption
         b9:2a:57:bb:25:a9:ac:8c:1d:9f:83:09:47:d5:e9:ba:6b:2e:
         48:95:d2:23:55:b6:c8:a3:95:2b:6d:15:bb:31:1d:58:a5:42:
         f0:99:2d:dd:12:ea:da:0e:9d:09:cc:5b:f8:c7:08:69:5c:c9:
         e5:40:2c:9f:c0:14:f3:52:94:c8:b9:11:d4:ef:50:1e:36:c8:
         a9:d0:6e:b6:92:0f:06:a1:55:d9:39:3f:1f:15:c4:19:9d:f4:
         38:a0:dd:c5:84:cc:60:91:42:a1:6e:42:0b:a8:f2:45:81:c0:
         8d:f8:fd:e6:41:86:67:21:19:38:2d:64:bd:75:e9:ba:17:a0:
         a8:21:d7:13:79:f5:51:98:d3:38:d4:58:d8:72:83:e9:57:bf:
         7d:a0:1c:67:6e:ec:4e:3a:c8:b4:3e:87:05:e2:48:be:da:e0:
         be:c5:40:60:45:fc:ab:54:bf:8e:89:78:af:b2:c0:c0:ee:98:
         55:75:ec:ca:df:de:f0:e0:24:71:48:ce:86:5d:2a:18:2d:af:
         2b:62:e5:c1:4a:45:f8:96:84:b2:f6:62:c3:2e:3f:f9:68:03:
         ba:f2:0b:6e:9c:70:89:c6:7c:67:01:6e:e6:d9:cd:d7:f5:09:
         9f:58:7b:f0:cc:a7:f1:88:bc:31:81:7f:76:93:77:14:9e:89:
         ed:40:0b:e9:8b:9e:5c:ba:6c:4a:a9:5f:c0:3c:ea:f8:e2:1e:
         85:92:9a:21:fa:a4:a4:30:09:93:32:05:14:b8:8c:83:f2:ce:
         4b:af:96:ea:91:02:3c:47:70:ed:44:f9:2e:ed:ad:b1:ac:97:
         2a:1f:a8:b8:1b:2b:d2:f3:2b:e5:8c:83:60:9b:15:31:14:5a:
         6e:d2:cd:fe:55:1e:43:c2:27:4b:4f:bd:61:f9:12:f4:1e:d4:
         14:5e:aa:43:fe:21:d4:fe:d1:22:2b:52:ae:fd:3e:ef:c9:a6:
         d2:90:37:65:8b:7a:b1:02:a0:9b:f2:90:fc:35:fd:2a:67:98:
         b4:dd:23:84:4b:49:a3:21:5f:b2:2d:6b:50:9c:21:df:f1:65:
         17:b2:8a:a6:0a:dc:8b:b8:d8:37:c1:07:c1:d9:08:3a:06:1f:
         14:77:32:4f:14:a4:9d:df:54:7a:7b:a5:c3:7e:be:19:be:b3:
         86:10:87:51:a9:44:c8:a3:94:df:44:49:18:43:cb:d3:a3:45:
         93:5b:6e:8a:ae:df:0f:46:dd:93:e6:11:2e:35:4b:7a:85:c4:
         4e:56:df:5f:29:3b:4e:93:65:19:5b:78:d6:d9:e4:6c:c9:fa:
         48:33:ab:a6:9c:ff:25:ca:ea:23:de:46:74:79:e7:d9:33:93:
         e6:a0:b7:95:4b:c0:d7:e6
```
 
![Print](https://github.com/uminho-miei-engseg-19-20/Grupo13/blob/master/Aula2/iimage.png)

