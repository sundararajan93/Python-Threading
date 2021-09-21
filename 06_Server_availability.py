import subprocess
import time
from subprocess import PIPE
import threading

servers = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5', '192.168.1.6']

def check_availability(server):
    p = subprocess.run(['ping', '-c', '1', server], stdout=PIPE, stderr=PIPE)
    if p.returncode == 0:
        print(f"{server} is Available")
    else:
        print(f"{server} is Unreachable")

def main():
    start = time.perf_counter()
    threads = []
    for server in servers:
        t = threading.Thread(target=check_availability, args=[server])
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    
    finish = time.perf_counter()
    print(f"Executed in {round(finish- start, 2)} second(s)")

if __name__ == '__main__':
    main()