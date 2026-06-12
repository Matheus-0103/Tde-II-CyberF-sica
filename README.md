# TDE - Programação Concorrente

**Integrantes:** Matheus Murbach, Guilherme Mendonça, João Gabriel, Gustavo Arcanjelo

## Como rodar

Precisa de Python 3.10+, sem bibliotecas externas.

```bash
python parte1_filosofos.py
python parte2_contador.py
python parte3_deadlock.py
```

---

## Parte 1 - Jantar dos Filósofos

5 filósofos numa mesa circular, cada um precisa de 2 garfos pra comer (o da esquerda e direita). O problema é que se todos pegarem o garfo esquerdo ao mesmo tempo, ninguém consegue o direito e todo mundo fica esperando pra sempre (deadlock).

**Solução que usamos:** hierarquia de recursos. Cada garfo tem um índice de 0 a 4, e todo filósofo sempre pega o garfo de menor índice primeiro. Isso impede a espera circular (4ª condição de Coffman), então deadlock nunca acontece.

```
primeiro = min(garfo_esq, garfo_dir)
segundo  = max(garfo_esq, garfo_dir)
```

Testamos com 5 filósofos fazendo 5 ciclos cada, todos completaram sem travar.

---

## Parte 2 - Contador compartilhado

10 threads incrementando o mesmo contador 10.000 vezes cada (esperado: 100.000).

Sem sincronização isso dá errado porque o `contador = contador + 1` não é atômico — são 3 operações (leitura, soma, escrita) e as threads se atrapalham.

Comparamos 3 abordagens:
- **Sem sync:** race condition, valor final errado
- **Semaphore(1):** correto, mas mais lento (overhead de acquire/release em tudo)
- **threading.Lock:** correto e um pouco mais rápido que o semáforo

O GIL do Python não resolve isso porque a operação composta não é atômica mesmo com o GIL.

---

## Parte 3 - Deadlock

Cenário clássico: processo A pega lock_A e quer lock_B, processo B pega lock_B e quer lock_A. Os dois ficam esperando um pelo outro.

Implementamos 3 estratégias:

**Ostrich:** ignora o problema, só mostramos que o deadlock acontece de verdade (os dois travam após o timeout).

**Prevenção por hierarquia:** igual à parte 1, os dois processos sempre adquirem lock_A antes de lock_B. Quebra a espera circular então deadlock é impossível. Desvantagem: precisa definir uma ordem global pra todos os locks do sistema.

**Detecção + recuperação:** os processos tentam pegar o segundo lock com timeout. Se expirar, liberam o que já têm e esperam um tempo antes de tentar de novo (backoff exponencial + um pouco de aleatoriedade pra não ficarem em livelock). Funciona bem, os dois conseguem concluir eventualmente.

---

## Referências

- https://en.wikipedia.org/wiki/Dining_philosophers_problem
- Silberschatz - Operating System Concepts cap. 8
- https://www.geeksforgeeks.org/introduction-of-deadlock-in-operating-system/
