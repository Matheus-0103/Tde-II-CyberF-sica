# Parte 1 - Jantar dos filosofos
# Matheus Murbach, Guilherme Mendonça, João Gabriel, Gustavo Arcanjelo

import threading
import time
import random

N = 5
CICLOS = 5

# um semaforo pra cada garfo
garfos = [threading.Semaphore(1) for _ in range(N)]
refeicoes = [0] * N

def filosofo(p):
    left = p
    right = (p + 1) % N

    # pega sempre o menor indice primeiro pra nao ter deadlock
    # isso quebra a espera circular (condicao 4 de coffman)
    if left < right:
        primeiro, segundo = left, right
    else:
        primeiro, segundo = right, left

    for i in range(CICLOS):
        t = random.uniform(0.5, 1.5)
        print(f"filosofo {p} pensando ({t:.1f}s)")
        time.sleep(t)

        garfos[primeiro].acquire()
        garfos[segundo].acquire()

        print(f"filosofo {p} comendo - ciclo {i+1}/{CICLOS}")
        time.sleep(random.uniform(0.3, 0.8))

        garfos[segundo].release()
        garfos[primeiro].release()

        refeicoes[p] += 1

    print(f"filosofo {p} terminou ({refeicoes[p]} refeicoes)")


if __name__ == "__main__":
    threads = []
    for i in range(N):
        t = threading.Thread(target=filosofo, args=(i,))
        threads.append(t)

    inicio = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\ntempo: {time.time()-inicio:.2f}s")
    print(f"refeicoes por filosofo: {refeicoes}")
    print(f"total: {sum(refeicoes)}")
