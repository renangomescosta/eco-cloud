# Conexão
```
ssh -p 2222 user@localhost
```
# Um arquivo
```
scp -P 2222 arquivo.txt user@localhost:~/
```
# Uma pasta inteira
```
scp -P 2222 -r minha-pasta user@localhost:~/
```