# 📂 NFS Setup Guide

This guide explains how to set up a Network File System (NFS) to share a common volume between nodes in a Docker Swarm cluster for parallel data processing.

The NFS volume allows all containers across the cluster (master and workers) to read and write files to a centralized location, enabling efficient coordination and result aggregation.

---

## 🧭 Architecture Overview

```
          ┌──────────────────────┐
          │   Master Node (NFS)  │
          │                      │
          │   /nfs/data/export   │
          └────────┬─────────────┘
                   │
   ┌───────────────┼────────────────┐
   ▼               ▼                ▼
Worker 1     Worker 2          Worker N
Mounts NFS   Mounts NFS        Mounts NFS
```

---

## 🖥️ Step-by-Step Setup

### 📌 On the Master Node (NFS Server)

1. **Install NFS Server:**

   ```bash
   sudo apt update
   sudo apt install nfs-kernel-server
   ```

2. **Create export directory:**

   ```bash
   sudo mkdir -p /nfs/data
   sudo chown nobody:nogroup /nfs/data
   sudo chmod 777 /nfs/data
   ```

3. **Configure export rules:**

   Edit the `/etc/exports` file:

   ```bash
   sudo nano /etc/exports
   ```

   Add a line like:

   ```
   /nfs/data 192.168.1.0/24(rw,sync,no_subtree_check,no_root_squash)
   ```

   Replace `192.168.1.0/24` with your actual subnet.

4. **Apply export settings:**

   ```bash
   sudo exportfs -ra
   sudo systemctl restart nfs-kernel-server
   ```

5. **Allow NFS through firewall (if enabled):**

   ```bash
   sudo ufw allow from 192.168.1.0/24 to any port nfs
   ```

---

### 📌 On Each Worker Node (NFS Clients)

1. **Install NFS client:**

   ```bash
   sudo apt update
   sudo apt install nfs-common
   ```

2. **Create mount point:**

   ```bash
   sudo mkdir -p /nfs/data
   ```

3. **Mount NFS volume:**

   Replace `<master_ip>` with the actual IP address of your NFS server.

   ```bash
   sudo mount <master_ip>:/nfs/data /nfs/data
   ```

4. **(Optional) Add to `/etc/fstab` for persistence:**

   ```bash
   <master_ip>:/nfs/data  /nfs/data  nfs  defaults  0  0
   ```

---

## ✅ Test the Setup

From the **master node**, create a test file:

```bash
echo "test" | sudo tee /nfs/data/hello.txt
```

On each **worker node**, check if the file exists:

```bash
cat /nfs/data/hello.txt
```

If successful, the shared volume is working properly.

---

## 🧩 Notes

- All nodes must be on the same private network.
- Make sure NFS ports are open in your firewall/router.
- The `/nfs/data` directory must be mounted at the **same path on all nodes** for Docker volume consistency.
- You can use `mount -t nfs` and `df -h` to verify mounts.

---

## 📦 Used In This Project

This NFS setup supports:
- `split_dataframe.py`: writes chunks to `/nfs/data`
- `split_processing.py`: reads/writes partial results from `/nfs/data`
- `collect_results.py`: merges results stored in `/nfs/data`

---

    