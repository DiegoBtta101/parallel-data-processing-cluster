# Parallel Data Processing with Docker Swarm and NFS

This project demonstrates a distributed system for parallel processing of a large dataframe using Docker Swarm and a shared NFS volume. It was deployed on a physical cluster built from repurposed computer boards, showcasing real-world infrastructure design, automation, and orchestration.

---

## 🔍 Overview

The objective is to process a large CSV file in parallel by splitting the workload across several worker nodes coordinated by a master node. The communication between nodes and data sharing is managed through Docker Swarm and a shared NFS-mounted volume.

This system reflects a real-world DevOps workflow involving infrastructure setup, container orchestration, network configuration, and distributed computation using Python.

---

## 🧱 Architecture

```
               ┌──────────────────────┐
               │      Master Node     │
               │                      │
               │  split_dataframe.py  │
               │     deploys jobs     │
               └──────────┬───────────┘
                          │
               ┌──────────▼───────────┐
               │  Shared NFS Volume   │
               └──────────┬───────────┘
                          │
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
┌────────────┐     ┌────────────┐     ┌────────────┐
│ Worker #1  │     │ Worker #2  │ ... │ Worker #N  │
│ process.py │     │ process.py │     │ process.py │
└────────────┘     └────────────┘     └────────────┘
```

---

## ⚙️ Tech Stack

- Docker & Docker Swarm  
- Python (Pandas, time)  
- NFS (Network File System)  
- Linux (Ubuntu/Debian)  
- Bash scripting   
- SSH   
- Parallel execution and result aggregation  

---

## 🚀 Project Workflow

1. **Setup NFS:**
   - A master node exports an NFS folder.
   - All nodes mount this shared volume to a known path.

2. **Initialize Docker Swarm:**
   - Master node runs `docker swarm init`.
   - Worker nodes join the cluster using the token.

3. **Deploy Containers:**
   - The master splits the dataframe and writes chunked files to NFS.
   - A service is deployed via `docker stack deploy`, spawning processing containers.
   - Each container processes one chunk and writes the result to NFS.

4. **Collect Results:**
   - After all tasks complete, a final container collects partial results and merges them.

---

## 📂 Repository Structure

```
.
├── docker-compose.yml           # Swarm stack definition
├── docker/                      # Dockerfiles for each processing role
│   ├── Dockerfile.split
│   ├── Dockerfile.processing
│   └── Dockerfile.result
├── scripts/                     # Python scripts executed in containers
│   ├── split_dataframe.py
│   ├── split_processing.py
│   └── collect_results.py
├── infra/                       # Infrastructure setup
│   ├── NFS_setup.md
│   ├── Swarm_setup.md
│   └── commands_cheatsheet.md
└── README.md
```

---

## 📸 Example Output

After completion, the result folder contains processed CSV chunks and a final merged output file.

```
[✓] Split file into 6 chunks  
[✓] Deployed 6 worker containers  
[✓] Each processed 1 chunk  
[✓] Collected 6 result files  
[✓] Final file merged successfully  
```

---

## 🔐 Notes

> This project is intended for educational and demonstrative purposes. It assumes basic knowledge of Docker, Linux networking, and Python scripting. It was developed and tested on a physical multi-node environment, but can be adapted to virtualized or cloud-based infrastructure.

---

## ✍️ Author

**Diego Bautista**  
Electronic Engineer & DevOps Enthusiast  
[Portfolio](https://diegobtta101.github.io) • [GitHub](https://github.com/DiegoBtta101)

---

## 📜 License

MIT License. See `LICENSE` for details.
