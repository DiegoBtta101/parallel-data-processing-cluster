# 🧾 Commands Cheatsheet

This cheat sheet provides quick access to the most commonly used commands during development, deployment, and monitoring of a Docker Swarm–based distributed data processing environment with NFS.

---

## 🐧 Linux & Networking

### 📡 IP and Host Configuration

```bash
ip addr show                  # Show IP addresses
hostname -I                   # Display current IP address
sudo nano /etc/hostname       # Edit hostname
sudo nano /etc/hosts          # Map hostnames to IPs
```

### 🔄 Mounting NFS

```bash
sudo mount <server_ip>:/nfs/data /nfs/data
df -h                         # Check if mount succeeded
mount -t nfs                  # Show NFS mounts
```

---

## 🐳 Docker

### 🛠️ General Docker Commands

```bash
docker ps -a                  # List all containers
docker images                 # List local images
docker rm <container_id>      # Remove container
docker rmi <image_id>         # Remove image
```

### 🐳 Docker Build & Run

```bash
docker build -t split_image -f Dockerfile.split .
docker run --rm split_image
```

---

## 🐝 Docker Swarm

### 🔧 Swarm Management

```bash
docker swarm init --advertise-addr <manager_ip>
docker swarm join-token worker
docker node ls
docker info                   # View swarm status
```

### 📦 Stack Deployment

```bash
docker stack deploy -c docker-compose.yml my_stack
docker service ls
docker service ps <service_name>
docker service logs <service_name>
docker stack ps my_stack
docker stack rm my_stack
```

---

## 📂 File Operations (Shared NFS Volume)

```bash
ls /nfs/data
cat /nfs/data/filename.csv
rm /nfs/data/*.csv
```

---

## 🐍 Python Scripts (Standalone Execution)

```bash
python3 scripts/split_dataframe.py
python3 scripts/split_processing.py
python3 scripts/collect_results.py
```

---

## 📁 Docker Volumes

```bash
docker volume ls
docker volume inspect <volume_name>
```

---

## 🧪 Testing Mounts and Permissions

```bash
touch /nfs/data/test.txt
echo "hello" > /nfs/data/test.txt
cat /nfs/data/test.txt
```

---

## 🧩 Miscellaneous

### 🧱 File Permissions

```bash
sudo chmod -R 777 /nfs/data
sudo chown nobody:nogroup /nfs/data
```

### 🔥 Clear Everything (Dangerous)

```bash
docker system prune -a
```

---

## 🔗 See Also

- [NFS Setup Guide](./NFS_setup.md)
- [Swarm Setup Guide](./Swarm_setup.md)
