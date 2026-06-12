# Parte 3 - deteccao e recuperacao de deadlock
# Matheus Murbach, Guilherme Mendonça, João Gabriel, Gustavo Arcanjelo
#
# cenario: processo A pega lock_a e espera lock_b
#          processo B pega lock_b e espera lock_a
#          => deadlock classico

import threading
import time
import random

TIMEOUT = 2.0

# ---- estrategia 1: ostrich (so pra mostrar o problema) ----

def demo_deadlock():
    print("--- ostrich: mostrando o deadlock ---")
    la = threading.Lock()
    lb = threading.Lock()
    detectado = threading.Event()

    def proc_A():
        la.acquire()
        print("A: pegou lock_a")
        time.sleep(0.05)
        print("A: tentando lock_b...")
        ok = lb.acquire(timeout=3.0)
        if ok:
            lb.release()
        else:
            print("A: nao conseguiu lock_b - deadlock!")
            detectado.set()
        la.release()

    def proc_B():
        lb.acquire()
        print("B: pegou lock_b")
        time.sleep(0.05)
        print("B: tentando lock_a...")
        ok = la.acquire(timeout=3.0)
        if ok:
            la.release()
        else:
            print("B: nao conseguiu lock_a - deadlock!")
            detectado.set()
        lb.release()

    ta = threading.Thread(target=proc_A, name="A")
    tb = threading.Thread(target=proc_B, name="B")
    ta.start(); tb.start()
    ta.join(5); tb.join(5)

    if detectado.is_set():
        print("resultado: deadlock confirmado (ostrich nao faz nada)\n")
    else:
        print("resultado: nao travou dessa vez (sorte no escalonamento)\n")


# ---- estrategia 2: prevencao por hierarquia ----

def demo_prevencao():
    print("--- prevencao: hierarquia de locks (A sempre antes de B) ---")
    la = threading.Lock()
    lb = threading.Lock()
    ordem = []
    lock_ord = threading.Lock()

    def proc(nome):
        # ambos adquirem na mesma ordem: lock_a -> lock_b
        la.acquire()
        print(f"{nome}: pegou lock_a")
        lb.acquire()
        print(f"{nome}: pegou lock_b, executando...")
        time.sleep(random.uniform(0.05, 0.15))
        lb.release()
        la.release()
        print(f"{nome}: liberou tudo")
        with lock_ord:
            ordem.append(nome)

    ta = threading.Thread(target=proc, args=("A",))
    tb = threading.Thread(target=proc, args=("B",))
    ta.start(); tb.start()
    ta.join(); tb.join()
    print(f"resultado: sem deadlock, ordem de conclusao: {ordem}\n")


# ---- estrategia 3: deteccao com timeout + backoff ----

tent_A = [0]
tent_B = [0]

def demo_deteccao():
    print("--- deteccao + recuperacao: timeout e backoff exponencial ---")
    la = threading.Lock()
    lb = threading.Lock()
    concluidos = []
    lk = threading.Lock()

    def proc_A():
        while True:
            tent_A[0] += 1
            la.acquire()
            print(f"A: pegou lock_a (tentativa {tent_A[0]})")
            time.sleep(0.05)
            ok = lb.acquire(timeout=TIMEOUT)
            if ok:
                print("A: pegou lock_b, executando secao critica")
                time.sleep(0.1)
                lb.release()
                la.release()
                print("A: concluido!")
                with lk: concluidos.append("A")
                break
            else:
                la.release()
                espera = 0.1 * (2 ** tent_A[0])
                print(f"A: deadlock detectado, recuando {espera:.2f}s")
                time.sleep(espera)

    def proc_B():
        while True:
            tent_B[0] += 1
            lb.acquire()
            print(f"B: pegou lock_b (tentativa {tent_B[0]})")
            time.sleep(0.05)
            ok = la.acquire(timeout=TIMEOUT)
            if ok:
                print("B: pegou lock_a, executando secao critica")
                time.sleep(0.1)
                la.release()
                lb.release()
                print("B: concluido!")
                with lk: concluidos.append("B")
                break
            else:
                lb.release()
                espera = 0.1 * (2 ** tent_B[0]) + random.uniform(0, 0.1)
                print(f"B: deadlock detectado, recuando {espera:.2f}s")
                time.sleep(espera)

    ta = threading.Thread(target=proc_A, name="A")
    tb = threading.Thread(target=proc_B, name="B")
    ta.start(); tb.start()
    ta.join(30); tb.join(30)
    print(f"resultado: ambos concluiram, ordem: {concluidos}")
    print(f"tentativas: A={tent_A[0]}, B={tent_B[0]}\n")


if __name__ == "__main__":
    print("=== Parte 3: Deadlock - deteccao e recuperacao ===\n")
    demo_deadlock()
    demo_prevencao()
    demo_deteccao()

    print("=== comparativo ===")
    print("ostrich    -> mais simples, mas trava pra sempre")
    print("prevencao  -> garante que nao trava, mas precisa ordenar tudo")
    print("deteccao   -> mais flexivel, se recupera, mas tem overhead")
