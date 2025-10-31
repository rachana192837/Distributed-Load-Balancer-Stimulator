# ⚙️ Distributed Load Balancer Simulation

A Python-based distributed system that simulates how a **central load balancer** distributes workloads to multiple **worker nodes** based on their real-time CPU usage.  
This project demonstrates the fundamentals of distributed computing, socket programming, and resource-aware task allocation.

---

## Overview

The system consists of:
- **Master Node (Load Balancer):** Accepts connections from workers, receives their CPU load, and assigns tasks to the least-loaded node.
- **Worker Nodes:** Connect to the master, send their CPU usage (using `psutil`), and execute tasks when assigned.

This simulation provides insight into how real-world load balancers like Nginx or Kubernetes schedulers handle distributed workloads efficiently.

---

## Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Python 3** | Core programming language |
| **Sockets** | Network communication between nodes |
| **psutil** | CPU usage and system metrics |
| **Linux** | Environment for running multiple terminals |

---

## Key Features

Real-time CPU monitoring using `psutil`  
Dynamic task assignment based on load  
Supports multiple worker connections  
Simple and interactive distributed simulation  
Cross-terminal setup for a realistic multi-node experience  

---

## Project Structure
distributed-load-balancer/ │ 
├── master.py          # Load balancer (server) 
├── worker.py          # Worker node (client) 
├── README.md          # Documentation

---
## How to Run

### 1️⃣ Start the Master Node
Open **Terminal 1** and run:
```bash
python3 master.py
```
### 2️⃣ Start One or More Worker Nodes

In Terminal 2, 3, ..., run:
```bash
python3 worker.py
```
### 3️⃣ Observe the Simulation

Workers send their CPU load to the master node.
The master assigns tasks to the least loaded worker.
Workers display when they receive and complete tasks

---
 ## output 
 Worker.py 
 <img width="700" height="400" alt="Screenshot from 2025-10-31 10-54-17" src="https://github.com/user-attachments/assets/32e7cbcb-9aad-46aa-8f3f-545a40f007a4" />
 Master.py
<img width="700" height="400" alt="Screenshot from 2025-10-31 10-54-17(1)" src="https://github.com/user-attachments/assets/826e8711-e6fe-4ee7-8ce5-3f7f10d5ebb4" />
