import threading
import time
from time import sleep


class myThread(threading.Thread):
    def __init__(self, threadId, name, count):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count

    def run(self):
        print("Starting: " + self.name + "\n")
        threadLock.acquire()
        print_time(self.name, 1, self.count)
        threadLock.release()
        print("Exiting : " + self.name + "\n")


class myThread2(threading.Thread):
    def __init__(self, threadId, name, count):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count

    def run(self):
        print("Starting: " + self.name + "\n")
        threadLock.acquire()
        threadLock.release()
        print_time(self.name, 1, self.count)
        print("Exiting : " + self.name + "\n")


def print_time(name, delay, count):
    while count:
        time.sleep(delay)
        print("%s: %s %s" % (name, time.ctime(time.time()), count) + "\n")
        count -= 1


threadLock = threading.Lock()

thread1 = myThread(1, "Thread1", 5)
thread2 = myThread2(2, "Thread2", 10)
thread3 = myThread2(3, "Loading page", 5)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join
print("Done main thread")
