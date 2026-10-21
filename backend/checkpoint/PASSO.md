# Migração do container `app` com Podman (checkpoint/restore)

Fluxo para mover o container `app`, **com o estado em memória**, da máquina de origem para a máquina de destino.

| Papel   | Máquina      | Função                                   |
|---------|--------------|------------------------------------------|
| Origem  | `user@user`  | Roda a app, gera a imagem e o checkpoint |
| Destino | `ubuntu-vm`  | Recebe os arquivos e restaura o container |

> Todos os comandos `podman` usam `sudo`: o checkpoint/restore (CRIU) só funciona com containers rodando como **root**.

---

## Visão geral

```
ORIGEM                                   DESTINO
1. Exportar imagem    (só se mudou)  ─┐
2. Exportar contexto  (checkpoint)   ─┼─► 3. Transferir ─► 4. Carregar imagem  (só se mudou)
                                      ┘                    5. Restaurar contexto
```

---

## 1. Origem (`user@user`)

### 1.1 Exportar a imagem
Só é necessário quando a imagem for reconstruída.

```bash
sudo podman save localhost/app:latest | gzip > backup/app-$(date +%Y%m%d-%H%M%S).tar.gz
```

### 1.2 Exportar o contexto (checkpoint)

```bash
sudo podman container checkpoint app --leave-running --export backup/cp-$(date +%Y%m%d-%H%M%S).tar.gz
```

- `--leave-running`: mantém a app rodando na origem. **Remova** essa flag para uma migração definitiva; caso contrário, as duas máquinas ficam rodando a app ao mesmo tempo.
- O arquivo exportado já sai compactado; não é necessário `gzip`.

---

## 2. Transferência

### Opção A: pasta compartilhada
Pasta montada nas duas máquinas: `/mnt/compartilhado`

```bash
sudo rsync -av --progress backup/ /mnt/compartilhado/backup/
```

### Opção B: SSH / SCP (a partir do servidor remetente)

Conectar no destino:
```bash
ssh -p 2222 user@localhost
```

Enviar um arquivo:
```bash
scp -P 2222 arquivo.tar.gz user@localhost:~/backup/
```

Enviar uma pasta inteira:
```bash
scp -P 2222 -r backup user@localhost:~/
```

---

## 3. Destino (`ubuntu-vm`)

### 3.1 Carregar a imagem
Só é necessário quando a imagem mudar.

```bash
sudo podman load -i ~/backup/app-XXXXXXXX-XXXXXX.tar.gz
```

### 3.2 Restaurar o contexto

```bash
sudo podman rm -f app 2>/dev/null
sudo podman run --rm --entrypoint true localhost/app:latest   # carrega o perfil AppArmor
sudo podman container restore --import ~/backup/cp-XXXXXXXX-XXXXXX.tar.gz
```

Verificar:
```bash
curl localhost:3000
```

#### Por que o `podman run` antes do restore?
O processo foi salvo rodando sob o perfil AppArmor `containers-default-0.66.0`. O podman só carrega esse perfil no kernel ao **iniciar** um container, e o restore não o carrega sozinho. O `run` com `--entrypoint true` sobe um container que termina na hora, só para carregar o perfil. Sem ele, o restore falha com `container creation timeout` (no log do CRIU: `can't write lsm profile`).

O perfil some ao reiniciar a máquina, então esse passo deve ser feito **sempre** antes do restore.

---

## Pontos de atenção

- **Mesma imagem:** a imagem no destino tem que ser exatamente a usada pelo container no momento do checkpoint. Reconstruiu na origem? Envie a nova imagem antes do próximo restore.
- **Mesmo ambiente:** as duas máquinas precisam das mesmas versões de `podman`, `crun`, `criu` e kernel. Para conferir:
  ```bash
  podman --version; crun --version | head -1; criu --version; uname -r
  ```
- **Não use `--tcp-established`** entre máquinas diferentes: conexões TCP abertas ficam presas ao IP da origem e quebram o restore.
- **Porta 3000 ocupada no destino:** geralmente é um restore anterior travado. Verifique e limpe:
  ```bash
  sudo ss -ltnp | grep :3000
  sudo podman rm -f app
  ```
- **Diagnóstico de falhas no restore:**
  ```bash
  sudo find /var/lib/containers -name restore.log -mmin -10 -exec tail -40 {} \;
  ```

---

## Utilitários

### Ligar as VMs pelo terminal

```bash
virsh -c qemu:///session start boxes-unknown
virsh -c qemu:///session start boxes-unknown-3
```