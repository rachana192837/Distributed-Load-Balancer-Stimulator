#!/usr/bin/env python3
"""
worker.py - Worker process that registers with master, reports CPU load,
listens for tasks, and executes simulated work.
"""

import socket
import threading
import json
import time
import os

MASTER_HOST = "127.0.0.1"
MASTER_PORT = 5000
WORKER_ID = f"worker-{os.getpid()}"

def read_cpu_times():
    """
    Return total and idle CPU times from /proc/stat (first line).
    """
    with open("/proc/stat", "r") as f:
        first = f.readline()
    parts = first.strip().split()[1:]  # skip 'cpu'
    nums = [int(x) for x in parts]
    total = sum(nums)
    idle = nums[3]  # idle is the 4th field
    return total, idle

def get_cpu_percent(interval=1.0):
    """
    Compute CPU percent over an interval by reading /proc/stat twice.
    Returns float percent (0..100)
    """
    t1, idle1 = read_cpu_times()
    time.sleep(interval)
    t2, idle2 = read_cpu_times()
    total_delta = t2 - t1
    idle_delta = idle2 - idle1
    if total_delta == 0:
        return 0.0
    usage = (1.0 - (idle_delta / total_delta)) * 100.0
    return usage

def send_load_loop(sock):
    """
    Periodically send load to master as JSON {"type":"load","id":WORKER_ID,"load":xx}
    """
    # initial register with a load sample
    try:
        initial_load = get_cpu_percent(0.5)
    except Exception:
        initial_load = 0.0
    reg = {"type": "register", "id": WORKER_ID, "load": initial_load}
    sock.sendall(json.dumps(reg).encode())

    while True:
        try:
            load = get_cpu_percent(1.0)
            msg = {"type": "load", "id": WORKER_ID, "load": load}
            sock.sendall(json.dumps(msg).encode())
            # print status locally
            print(f"[L] Sent load {load:.2f}% to master")
            # sleep a bit (we already waited inside get_cpu_percent)
            time.sleep(1.0)
        except BrokenPipeError:
            print("[!] Connection closed by master.")
            break
        except Exception as e:
            print("send_load_loop error:", e)
            break

def listen_for_master(sock):
    """
    Listen for incoming JSON messages from master (tasks).
    """
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("[!] Master closed connection.")
                break
            try:
                msg = json.loads(data.decode())
            except Exception:
                continue
            if msg.get("type") == "task":
                task_id = msg.get("task_id")
                print(f"[>] Received task {task_id}: executing simulated workload...")
                # simulate CPU-heavy work: compute digits of pi or busy loop for duration seconds
                dur = msg.get("duration", 3)
                end = time.time() + dur
                # busy work to consume CPU
                while time.time() < end:
                    # simple math to keep CPU busy
                    _ = sum(i*i for i in range(2000))
                print(f"[=] Task {task_id} done.")
                # notify master
                done_msg = {"type": "done", "id": WORKER_ID, "task_id": task_id}
                try:
                    sock.sendall(json.dumps(done_msg).encode())
                except Exception:
                    pass
        except Exception as e:
            print("listen_for_master error:", e)
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((MASTER_HOST, MASTER_PORT))
    print(f"[*] Connected to master at {MASTER_HOST}:{MASTER_PORT} as {WORKER_ID}")

    t1 = threading.Thread(target=send_load_loop, args=(sock,), daemon=True)
    t2 = threading.Thread(target=listen_for_master, args=(sock,), daemon=True)
    t1.start()
    t2.start()

    # keep main alive while threads run
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting worker.")

if __name__ == "__main__":
    main()
