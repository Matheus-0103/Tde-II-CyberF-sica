# Parte 2 - contador compartilhado com threads
# Matheus Murbach, Guilherme Mendonça, João Gabriel, Gustavo Arcanjelo

import threading
import time

NUM_THREADS = 10
INCREMENTOS = 10000
ESPERADO = NUM_THREADS * INCREMENTOS

# --- sem sincronizacao ---

contador1 = 0

def inc_sem_sync():
    global contador1
    for _ in range(INCREMENTOS):
        contador1 = contador1 + 1

print("=== sem sincronizacao ===")
contador1 = 0
threads = [threading.Thread(target=inc_sem_sync) for _ in range(NUM_THREADS)]
t0 = time.time()
for t in threads: t.start()
for t in threads: t.join()
print(f"esperado: {ESPERADO}, obtido: {contador1}, perdidos: {ESPERADO - contador1}")
print(f"tempo: {time.time()-t0:.4f}s\n")

# --- com semaforo ---

contador2 = 0
sem = threading.Semaphore(1)
contagem_thread = {}
lock_ct = threading.Lock()

def inc_com_sem(nome):
    global contador2
    local = 0
    for _ in range(INCREMENTOS):
        sem.acquire()
        contador2 += 1
        local += 1
        sem.release()
    with lock_ct:
        contagem_thread[nome] = local

print("=== com semaforo ===")
contador2 = 0
threads = [threading.Thread(target=inc_com_sem, args=(f"t{i}",)) for i in range(NUM_THREADS)]
t0 = time.time()
for t in threads: t.start()
for t in threads: t.join()
print(f"esperado: {ESPERADO}, obtido: {contador2}, correto: {contador2 == ESPERADO}")
print(f"tempo: {time.time()-t0:.4f}s")
print("contagem por thread:", contagem_thread)
print()

# --- com lock nativo (so pra comparar) ---

contador3 = 0
mutex = threading.Lock()

def inc_com_lock():
    global contador3
    for _ in range(INCREMENTOS):
        with mutex:
            contador3 += 1

print("=== com threading.Lock ===")
contador3 = 0
threads = [threading.Thread(target=inc_com_lock) for _ in range(NUM_THREADS)]
t0 = time.time()
for t in threads: t.start()
for t in threads: t.join()
print(f"esperado: {ESPERADO}, obtido: {contador3}, correto: {contador3 == ESPERADO}")
print(f"tempo: {time.time()-t0:.4f}s")
