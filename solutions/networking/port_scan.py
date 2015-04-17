import socket
from datetime import datetime
from threading import Thread, Lock, active_count
from queue import Queue


# Get input
hostname = input("Enter a host to scan: ")
ip = socket.gethostbyname(hostname)

print("-" * 60)
print("Starting scan of " + ip)
print ("-" * 60)

socket.setdefaulttimeout(0.05)
starttime = datetime.now()

print_lock = Lock()
queue_lock = Lock()
queue = Queue()
done = False

def scan_port():
    while ((not queue.empty()) or (not done)):
        queue_lock.acquire()
        port = queue.get()
        queue_lock.release()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print_lock.acquire()
            print ("Port %d is open!" % port)
            print_lock.release()
        sock.close()

for i in range(1, 65535):
    queue_lock.acquire()
    queue.put(i)
    queue_lock.release()
    if (i < 100):
        t = t = Thread(target=scan_port)
        t.start()

done = True

while (active_count() > 1):
    pass

totaltime = datetime.now() - starttime
print ("Scan complete in %s seconds" % totaltime)
