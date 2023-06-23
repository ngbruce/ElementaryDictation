import threading
import time


def start_thread_b():
    # print('Thread A running')
    thread_b = threading.Thread(target=thread_b_func)
    thread_b.daemon = True     # 设置为守护线程
    thread_b.start()
    print('Thread B started')

def thread_b_func():
    while True:
        print('Thread B running')
        time.sleep(2)

def thread_a_func():
    print('Thread A started, going to start B')
    start_thread_b()
    print('Thread A will sleep')
    time.sleep(2)
    print('Thread A end')

def start_thread_a():
    thread_a = threading.Thread(target=thread_a_func)
    thread_a.daemon = True  # 设置为守护线程
    thread_a.start()

start_thread_a()


# while True:
#     pass
time.sleep(5)
print('Main end')