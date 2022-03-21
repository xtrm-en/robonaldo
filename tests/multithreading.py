import random
from threading import *
import threading
import time

lock = Condition()


def update_context(context: str):
    global ctx
    lock.acquire()
    ctx = context
    lock.release()


def get_context() -> str:
    global ctx
    lock.acquire()
    c = ctx
    lock.release()
    return c


def updater():
    while True:
        print("> Updating ctx")
        update_context(str(random.randint(1, 1000)))
        print("> Done updating")
        time.sleep(float(random.randint(1, 50) / 100))


def processor():
    while True:
        print("current: " + get_context())
        time.sleep(float(random.randint(1, 50) / 100))


T1 = Thread(target=updater)
T2 = Thread(target=processor)

T1.start()
T2.start()
