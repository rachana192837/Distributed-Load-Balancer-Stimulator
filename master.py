#!/usr/bin/env python3
"""
master.py - Simple load balancer server
Listens for worker connections, receives JSON load reports, and assigns tasks
to the least-loaded worker periodically.
"""

import socket
import threading
import json
import time

HOST = "0.0.0.0"
PORT = 5000
LOCK = threading.Lock()

# map: worker_id -> { "conn": socket, "addr": (ip,port), "last_load": float, "last_seen": ts }
workers = {}

def recv_thread(conn, addr):
    """
    Thread to receive JSON messages from a worker.
    Worker sends messages like: {"type":"load", "load":12.3, "id":"worker-1"}
    """
    worker_id = None
    try:
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                try:
                    msg = json.loads(data.decode())
                except Exception:
                    # ignore malformed
                    continue

                if msg.get("type") == "register":
                    worker_id = msg.get("id") or f"{addr[0]}:{addr[1]}"
                    with LOCK:
                        workers[worker_id] = {"conn": conn, "addr": addr, "last_load": msg.get("load", 0.0), "last_seen": time.time()}
                    print(f"[+] Registered worker {worker_id} from {addr}")
                elif msg.get("type") == "load":
                    worker_id = msg.get("id") or f"{addr[0]}:{addr[1]}"
                    with LOCK:
                        if worker_id not in workers:
                            workers[worker_id] = {"conn": conn, "addr": addr, "last_load": msg.get("load", 0.0), "last_seen": time.time()}
                        else:
                            workers[worker_id]["last_load"] = msg.get("load", 0.0)
                            workers[worker_id]["last_seen"] = time.time()
                    # (optional) print status
                    # print(f"Load update: {worker_id} -> {msg.get('load'):.2f}%")
                elif msg.get("type") == "done":
                    print(f"[=] Worker {msg.get('id')} completed task.")
                else:
                    # unsupported message
                    pass
    except Exception as e:
        print("Recv thread error:", e)
    finally:
        # remove worker on disconnect
        if worker_id:
            with LOCK:
                if worker_id in workers:
                    print(f"[-] Worker {worker_id} disconnected.")
                    try:
                        del workers[worker_id]
                    except KeyError:
                        pass

def assign_tasks_periodically(interval=5):
    """
    Every `interval` seconds, pick the least-loaded worker and send a task.
    Task is a simple JSON: {"type":"task","task_id":n}
    """
    task_counter = 0
    while True:
        time.sleep(interval)
        with LOCK:
            # drop stale workers (not seen in last 15s)
            now = time.time()
            stale = [wid for wid, info in workers.items() if now - info["last_seen"] > 15]
            for s in stale:
                print(f"[!] Removing stale worker {s}")
                del workers[s]

            if not workers:
                print("[!] No workers available to assign task.")
                continue

            # choose worker with min last_load
            chosen = min(workers.items(), key=lambda kv: kv[1]["last_load"])
            worker_id, info = chosen
            try:
                payload = {"type": "task", "task_id": task_counter, "work": "compute_pi", "duration": 3}
                info["conn"].sendall(json.dumps(payload).encode())
                print(f"[>] Assigned task {task_counter} to {worker_id} (load={info['last_load']:.2f}%)")
                task_counter += 1
            except Exception as e:
                print(f"[!] Failed to send task to {worker_id}: {e}")
                # remove worker if send fails
                del workers[worker_id]

def accept_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"[*] Load balancer listening on {HOST}:{PORT}")
    # start assigner thread
    threading.Thread(target=assign_tasks_periodically, args=(5,), daemon=True).start()

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=recv_thread, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    accept_loop()
