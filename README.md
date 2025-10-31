# ⚙️ Distributed Load Balancer Simulation

A Python-based distributed system that simulates how a **central load balancer** distributes workloads to multiple **worker nodes** based on their real-time CPU usage.  
This project demonstrates the fundamentals of distributed computing, socket programming, and resource-aware task allocation.

---

## 🚀 Overview

The system consists of:
- 🧠 **Master Node (Load Balancer):** Accepts connections from workers, receives their CPU load, and assigns tasks to the least-loaded node.
- 💻 **Worker Nodes:** Connect to the master, send their CPU usage (using `psutil`), and execute tasks when assigned.

This simulation provides insight into how real-world load balancers like Nginx or Kubernetes schedulers handle distributed workloads efficiently.

---

## 🧩 Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Python 3** | Core programming language |
| **Sockets** | Network communication between nodes |
| **psutil** | CPU usage and system metrics |
| **Linux** | Environment for running multiple terminals |

---

## 🧠 Key Features

✅ Real-time CPU monitoring using `psutil`  
✅ Dynamic task assignment based on load  
✅ Supports multiple worker connections  
✅ Simple and interactive distributed simulation  
✅ Cross-terminal setup for a realistic multi-node experience  

---

## 📂 Project Structure
