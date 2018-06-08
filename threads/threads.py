#Multi threading programming in python

list = []
import threading

def download():
    for i in range(1,5000000):
        print i

def matchclip():
  threading.Timer(5.0, matchclip).start()
  list.append("a")

t1 = threading.Thread(target=matchclip)
t1.start()

download()

print list