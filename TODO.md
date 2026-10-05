# Tarefas

## Tarefa 1: Docker vs VM

#### Verificar se alguém já fez algo parecido
R: Docs

#### Entender a fundo a diferença entre **Docker** e **VM**
R: [Link](https://aws.amazon.com/pt/compare/the-difference-between-docker-vm/)

Obs:. Ir para "Compartilhamento de recursos"

Obs2:. Ir para "Quando usar uma máquina virtual"


### Exportar o Container como Arquivo (Backup Físico)
**Comita o estado**
```Bash
docker commit nome_do_container minha_imagem_backup:v1
```

**Salva o estado para .taz**

Obs:. Aqui entraria a compressão do arquivo
> Problema: Não dá para salvar muita coisa, se não fica caro.

```Bash
docker save minha_imagem_backup:v1 -o meu_backup_completo.tar
```
**Carrega o estado em outra instância com Load**
```Bash
docker load -i meu_backup_completo.tar
```

## Tarefa 2: Otimizar o NEMESIS algorithm

1. Seguir a linha de tentar otimizar o **NEMESIS algorithm**
2. Investigar o cálculo **CPU x Memória**, que parece estranho
3. Reduzir migrações escolhendo melhor as máquinas
4. Fazer 2 sorteios com base na reunião e na série histórica (**dia x noite**)
5. **Esse sorteio**: pode existir 1 PC que o `sorted` não favorece
   - **5.1 Busca exaustiva**: olhar todos e selecionar o mais econômico possível
   - **5.2 Busca ao contrário**: ordenar pela energia verde
   

