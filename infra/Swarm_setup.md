# 🐳 Docker Swarm Setup Guide

This guide outlines the steps to initialize and configure a Docker Swarm cluster consisting of one master node (manager) and multiple worker nodes. This cluster enables the deployment of parallel workloads for distributed data processing.

---

## 🧭 Swarm Architecture Overview

```
             ┌──────────────────────┐
             │   Manager Node       │
             │  (docker swarm init) │
             └─────────┬────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    Worker Node 1  Worker Node 2  Worker Node N
 (join via token) (join via token) (join via token)
```

---

## 📦 Prerequisites

- All nodes must have Docker installed and running.
- Static IPs are recommended for all nodes.
- All nodes must be on the same local network and reachable via SSH or direct IP.

---

## 🚀 Swarm Initialization (Master Node)

1. **Initialize the swarm:**

   ```bash
   docker swarm init --advertise-addr <manager_ip>
   ```

   Replace `<manager_ip>` with the IP address of the master node.

2. **Copy the worker join command** provided in the output. It looks like:

   ```bash
   docker swarm join --token SWMTKN-xxxxx <manager_ip>:2377
   ```

3. **(Optional) View the join token again later:**

   ```bash
   docker swarm join-token worker
   ```

---

## 🔗 Join Worker Nodes to the Cluster

On each worker node:

1. Run the join command copied from the master node:

   ```bash
   docker swarm join --token SWMTKN-xxxxx <manager_ip>:2377
   ```

2. To confirm the node has joined, go back to the master and run:

   ```bash
   docker node ls
   ```

---

## 🗂 Deploying a Stack with Docker Compose

You can deploy services across the cluster using a `docker-compose.yml` file.

1. On the master node, ensure the compose file is ready.

2. Deploy the stack:

   ```bash
   docker stack deploy -c docker-compose.yml my_stack
   ```

3. Check service status:

   ```bash
   docker service ls
   ```

4. Check running tasks:

   ```bash
   docker service ps <service_name>
   ```

---

## 🛠 Useful Swarm Commands

| Command | Description |
|--------|-------------|
| `docker node ls` | List all nodes in the swarm |
| `docker info` | View swarm status |
| `docker service ls` | List services deployed |
| `docker stack ps <stack>` | Show tasks of a stack |
| `docker stack rm <stack>` | Remove a deployed stack |
| `docker service logs <service>` | View logs for a service |

---

## 🧩 Notes

- Swarm needs port `2377` (cluster management), `7946` (communication), and `4789` (overlay network) open on all nodes.
- If you restart a worker or it loses connection, it automatically reconnects to the cluster if the token remains valid.
- Volumes (like NFS) must be mounted at identical paths across all nodes.

---

## 📘 Related Docs

- [NFS Setup](./NFS_setup.md)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
