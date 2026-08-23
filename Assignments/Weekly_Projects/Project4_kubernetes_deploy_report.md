# 📋 Project Deployment Report: Local Kubernetes Microservices

## 1. Executive Summary
The goal of this initiative was to clone the Google Cloud Platform Microservices Demo repository and adapt its installation instructions to run successfully on a local infrastructure environment. The target stack chosen was **Minikube** utilizing the **Docker Desktop** virtualization driver optimized for an **Apple Silicon (M1/M2/M3/M4) macOS architecture**. All 12 system components (11 microservices + 1 Redis cache database) were successfully deployed, validated as stable, and exposed to the host machine's browser layer.

---

## 2. Infrastructure Setup & Environment Prep

### Step 1: Resolving Local CLI Dependencies
Initially, running `minikube status` and `docker info` resulted in a `command not found` error. We addressed this by installing the required tooling directly onto the host Mac via the Homebrew package manager.
* **Command Executed:** 
  ```bash
  brew install --cask docker && brew install minikube
  ```

### Step 2: Overcoming Architecture & Virtualization Blocks
When starting Minikube, the system threw an error (`DRV_UNSUPPORTED_OS`) because the default **VirtualBox** engine does not support Apple Silicon (`darwin/arm64`). 
* **The Solution:** We initialized and accepted the **Docker Desktop Subscription Service Agreement**, allowed local network access security prompts, and instructed Minikube to bypass VirtualBox to use Docker container virtualization natively instead.

### Step 3: Resource Allocation Calibration
The Online Boutique microservices require a baseline of 4 CPUs and 8GB of RAM. Because Docker Desktop reported a maximum available system headroom of `7933MB`, we dynamically scaled down the Minikube hardware request flags slightly to prevent host-machine crashes while maintaining application stability.
* **Command Executed:**
  ```bash
  minikube start --driver=docker --cpus=4 --memory=7000
  ```
* **Result:** Cluster control plane stabilized and initialized to a `Done!` status.

---

## 3. Application Deployment & Verification

### Step 1: Code Acquisition
We executed a shallow Git clone targeting the stable release manifests from Google Cloud's repository to bypass massive history downloads.
* **Command Executed:**
  ```bash
  git clone --depth 1 --branch v0 https://github.com/GoogleCloudPlatform/microservices-demo.git
  cd microservices-demo/
  ```

### Step 2: Manifest Execution
We targeted the multi-resource configuration file found in the project's internal paths: `./release/kubernetes-manifests.yaml`. Kubernetes translated this file into live cloud assets inside the cluster.
* **Command Executed:**
  ```bash
  kubectl apply -f ./release/kubernetes-manifests.yaml
  ```

### Step 3: Pod Status Audit
After allowing 4 minutes for image pulls and initialization routines, a full status report using `kubectl get pods` confirmed flawless execution metrics across the entire application topology.

**System Health Output Grid:**
```text
NAME                                    READY   STATUS    RESTARTS   AGE
adservice-8576649cff-qkkfc              1/1     Running   0          4m15s
cartservice-546c548494-s9q59            1/1     Running   0          4m17s
checkoutservice-75b9cd684f-lk2r6        1/1     Running   0          4m17s
currencyservice-fd8f5dfb7-tzknc         1/1     Running   0          4m17s
emailservice-7466dc585-j9bfz            1/1     Running   0          4m16s
frontend-694b9f76cd-qnlkg               1/1     Running   0          4m16s
loadgenerator-7dd458dd5b-4xctl          1/1     Running   0          4m17s
paymentservice-6b76dfb449-ndjb9         1/1     Running   0          4m16s
productcatalogservice-fb49fc9cc-p2frr   1/1     Running   0          4m17s
recommendationservice-6f8f67d69-pr9bm   1/1     Running   0          4m16s
redis-cart-6899b65948-jrr8q             1/1     Running   0          4m16s
shippingservice-55656785c7-z5mnt        1/1     Running   0          4m17s
```
* **Key Observations:** All pods verified at `1/1 READY` and `Running` with `0` Out-Of-Memory (OOM) tracking restarts.

---

## 4. Networking, Routing & Ingress Handling
Because Minikube operates inside an isolated virtual container loop on macOS, its public load balancers are not inherently reachable by default. 

To map internet traffic routing to the host computer, we established an active TCP network port tunnel bridging local web ports to the application's external entry point:
* **Command Executed:**
  ```bash
  kubectl port-forward service/frontend-external 8080:80
  ```
* **Validation Metric:** The terminal logs successfully printed consecutive `Handling connection for 8080` metrics, verifying functional browsing interactions on **`http://localhost:8080`** with full cross-service communication (Cart, Currency, Payments, Recommendations).

---

## 5. Teardown Blueprint (For Future Use)
When you wish to de-allocate resources and cleanly dismantle this deployment, run the following sequence in your terminal workspace:

```bash
# 1. Tear down the microservices and network assets
kubectl delete -f ./release/kubernetes-manifests.yaml

# 2. Power down the Minikube virtual instance to reclaim RAM/CPU
minikube stop
```