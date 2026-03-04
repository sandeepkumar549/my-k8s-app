# ☸️ Kubernetes Application Deployment

A complete guide and project for deploying applications on Kubernetes using Minikube on Windows. This repository contains multiple app deployments — Python, HTML, and Ubuntu-based — all running on a local Kubernetes cluster.

![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows_11-0078D6?style=for-the-badge&logo=windows&logoColor=white)

---

## 📁 Project Structure

```
kubernetes-deployment/
│
├── my-app/                        # App 1 — Python Web App
│   ├── app.py                     # Python HTTP server
│   ├── Dockerfile                 # Uses python:3.11-slim
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
│
├── k8s-html-app/                  # App 2 — HTML Store App
│   ├── app/
│   │   ├── index.html             # Beautiful store HTML page
│   │   └── Dockerfile             # Uses nginx:alpine
│   └── k8s/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── deployment.yaml
│       └── service.yaml
│
├── ubuntu-k8s-app/                # App 3 — Ubuntu Based App
│   ├── app/
│   │   ├── app.py                 # Python server with Ubuntu info
│   │   └── Dockerfile             # Uses ubuntu:22.04
│   └── k8s/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── secret.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       └── hpa.yaml
│
└── README.md
```

---

## 🧰 Prerequisites

Make sure these are installed on your Windows PC before starting:

| Tool | Version | Download |
|---|---|---|
| Docker Desktop | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Minikube | v1.38+ | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/) |
| kubectl | Latest | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/) |
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |
| VS Code | Latest | [code.visualstudio.com](https://code.visualstudio.com/) |
| Git | Latest | [git-scm.com](https://git-scm.com/download/win) |

---

## ⚙️ Initial Setup

### 1. Set Docker as Default Minikube Driver
```powershell
minikube config set driver docker
```

### 2. Start Minikube
```powershell
# Make sure Docker Desktop is open first!
minikube start
```

### 3. Verify Everything is Running
```powershell
minikube status
kubectl get nodes
```

Expected output:
```
NAME       STATUS   ROLES           AGE
minikube   Ready    control-plane   1m   ✅
```

---

## 🚀 App 1 — Python Web App (`my-app`)

A simple Python HTTP server deployed with 3 replicas.

### Deploy
```powershell
cd my-app

# Point to Minikube's Docker
minikube docker-env | Invoke-Expression

# Build image
docker build -t hello-app:v1 .

# Deploy to Kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Open in browser
minikube service hello-app-service -n my-app
```

### Check Status
```powershell
kubectl get pods -n my-app
kubectl get all -n my-app
```

---

## 🌐 App 2 — HTML Store App (`k8s-html-app`)

A beautiful KubeStore HTML page served by nginx.

### Deploy
```powershell
cd k8s-html-app/app

# Point to Minikube's Docker
minikube docker-env | Invoke-Expression

# Build image
docker build -t html-app:v1 .

# Deploy to Kubernetes
cd ../k8s
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Open in browser
minikube service html-app-service -n my-html-app
```

### Check Status
```powershell
kubectl get pods -n my-html-app
kubectl get all -n my-html-app
```

---

## 🐧 App 3 — Ubuntu Based App (`ubuntu-k8s-app`)

A Python web server running inside an Ubuntu 22.04 container.

### Deploy
```powershell
cd ubuntu-k8s-app/app

# Point to Minikube's Docker
minikube docker-env | Invoke-Expression

# Build image (takes longer — Ubuntu is bigger!)
docker build -t ubuntu-app:v1 .

# Deploy to Kubernetes
cd ../k8s
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Open in browser
minikube service ubuntu-app-service -n my-ubuntu-app
```

### Check Status
```powershell
kubectl get pods -n my-ubuntu-app
kubectl get all -n my-ubuntu-app
```

---

## 📋 Kubernetes Files Explained

### `namespace.yaml`
Creates an isolated neighborhood for your app inside the cluster.
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
```

### `configmap.yaml`
Stores non-sensitive settings like environment name, app name, version.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-app-config
  namespace: my-app
data:
  APP_ENV: "production"
  APP_NAME: "Hello App"
```

### `secret.yaml`
Stores sensitive data like passwords and API keys in base64 encoding.
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: hello-app-secret
  namespace: my-app
type: Opaque
data:
  DB_PASSWORD: bXlzZWNyZXRwYXNzd29yZA==
```

### `deployment.yaml`
Tells Kubernetes how many replicas to run and which image to use.
```yaml
spec:
  replicas: 3              # Run 3 copies
  strategy:
    type: RollingUpdate    # Zero downtime updates
```

### `service.yaml`
Creates a stable network address to reach your pods.
```yaml
spec:
  type: NodePort           # Accessible from outside
  ports:
    - port: 8080
      nodePort: 30080
```

### `hpa.yaml`
Automatically scales pods up/down based on CPU and memory usage.
```yaml
spec:
  minReplicas: 2           # Always keep at least 2
  maxReplicas: 10          # Never go above 10
  metrics:
    - averageUtilization: 70   # Scale up when CPU > 70%
```

### `ingress.yaml`
Gives your app a real domain name with HTTPS support.
```yaml
rules:
  - host: hello.myapp.com
    http:
      paths:
        - path: /
          backend:
            service:
              name: hello-app-service
```

---

## 🔧 Common Commands

### View Running Resources
```powershell
# All pods
kubectl get pods -n my-app

# All resources
kubectl get all -n my-app

# Watch pods in real time
kubectl get pods -n my-app --watch
```

### Debugging
```powershell
# Check why a pod failed
kubectl describe pod <pod-name> -n my-app

# View pod logs
kubectl logs <pod-name> -n my-app

# Get inside a pod
kubectl exec -it <pod-name> -n my-app -- /bin/sh
```

### Scaling
```powershell
# Scale to 5 replicas
kubectl scale deployment hello-app --replicas=5 -n my-app

# Enable auto-scaling
kubectl apply -f hpa.yaml
minikube addons enable metrics-server
```

### Updating App
```powershell
# Build new version
docker build -t hello-app:v2 .

# Update deployment
kubectl set image deployment/hello-app hello-app=hello-app:v2 -n my-app

# Check rollout status
kubectl rollout status deployment/hello-app -n my-app

# Rollback if something goes wrong
kubectl rollout undo deployment/hello-app -n my-app
```

### Open Kubernetes Dashboard
```powershell
minikube dashboard
```

---

## ⚠️ Important Rules

```
1. Always open Docker Desktop BEFORE running minikube start
2. Always run minikube docker-env | Invoke-Expression before docker build
3. Always apply configmap + secret BEFORE deployment
4. Use PowerShell — NOT Git Bash for minikube commands
5. Use imagePullPolicy: Never for local images
```

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `GUEST_DRIVER_MISMATCH` | Old Hyper-V cluster exists | `minikube delete` then `minikube start` |
| `dockerDesktopLinuxEngine not found` | Docker Desktop not running | Open Docker Desktop first |
| `ImagePullBackOff` | Image not in Minikube Docker | Run `minikube docker-env \| Invoke-Expression` then rebuild |
| `CreateContainerConfigError` | ConfigMap or Secret missing | `kubectl apply -f configmap.yaml` and `secret.yaml` first |
| `Invoke-Expression not found` | Using Git Bash instead of PowerShell | Switch to PowerShell or use `eval $(minikube docker-env)` |

---

## 🔄 Daily Workflow

```powershell
# Morning — Start everything
# 1. Open Docker Desktop (wait for Engine running)
minikube start
minikube docker-env | Invoke-Expression

# Deploy your app
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Open in browser
minikube service <service-name> -n <namespace>

# Evening — Stop everything
minikube stop
```

---

## 🖼️ Docker Images Used

| App | Base Image | Size | Why |
|---|---|---|---|
| Python App | `python:3.11-slim` | ~80MB | Lightweight, fast |
| HTML App | `nginx:alpine` | ~40MB | Best for serving HTML |
| Ubuntu App | `ubuntu:22.04` | ~230MB | Full OS, more control |

---

## 📚 What I Learned

- ✅ How Kubernetes manages containerized applications
- ✅ Difference between Pods, Deployments, Services, Ingress
- ✅ How ConfigMaps and Secrets work
- ✅ Rolling updates with zero downtime
- ✅ Horizontal Pod Autoscaling (HPA)
- ✅ Debugging pods using `kubectl describe` and `kubectl logs`
- ✅ How to use Minikube on Windows with Docker driver

---

## 👨‍💻 Author

**DELL** — Learning Kubernetes on Windows 11 with Minikube

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
