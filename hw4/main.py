import os
import threading
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import Process
from threading import Thread
import math

import multiprocessing as mp


def fib(n):
    if n == 1:
        return [0]
    res = [0, 1]
    for _ in range(n - 2):
        res.append(res[-1] + res[-2])

    return res


def integrate(f, a, b, job, n_jobs=1, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    iters_per_job = n_iter // n_jobs
    start = iters_per_job * job
    end = min(n_iter, iters_per_job * (job + 1))
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


if __name__ == "__main__":
    # easy
    N = 100000
    start_time = time.time()
    for _ in range(10):
        fib(N)
    sync_time = time.time() - start_time

    threads = []
    for _ in range(10):
        threads.append(Thread(target=fib, args=(N,)))
    start_time = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    thread_time = time.time() - start_time

    processes = []
    for _ in range(10):
        processes.append(Process(target=fib, args=(N,)))
    start_time = time.time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    process_time = time.time() - start_time

    with open(f'artifacts/easy.txt', 'w') as file:
        file.write(f'Sync: {sync_time} seconds\n')
        file.write(f'Thread: {thread_time} seconds\n')
        file.write(f'Process: {process_time} seconds\n')

    # medium
    cpu_num = mp.cpu_count()
    with open('artifacts/medium_logs.txt', 'w') as logs, open('artifacts/medium_comparison.txt', 'w') as file:
        for n_jobs in range(1, 2 * cpu_num + 1):
            threads = []
            file.write(f'Run {n_jobs} threads:\n')
            start = time.time()
            executor = ThreadPoolExecutor(max_workers=n_jobs)

            for i in range(n_jobs):
                threads.append(executor.submit(integrate, math.cos, 0, math.pi / 2, i, n_jobs))
            res = 0
            for t in as_completed(threads):
                res += t.result()
            end = time.time()
            file.write(f'time: {end - start} seconds, result: {res}\n\n')

            now = datetime.now()
            logs.write(f'{now.strftime("%Y-%m-%d %H:%M:%S")}: Run {threading.get_ident()} thread\n')

            processes = []
            file.write(f'Run {n_jobs} processes:\n')
            start = time.time()
            executor = ProcessPoolExecutor(max_workers=n_jobs)
            for i in range(n_jobs):
                processes.append(executor.submit(integrate, math.cos, 0, math.pi / 2, i, n_jobs))
            res = 0
            for p in as_completed(processes):
                res += p.result()
            end = time.time()
            file.write(f'time: {end - start} seconds, result: {res}\n\n')

            now = datetime.now()
            timestamp = datetime.timestamp(now)
            logs.write(f'{now.strftime("%Y-%m-%d %H:%M:%S")}: Run {os.getpid()} process\n')
