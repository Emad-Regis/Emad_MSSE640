# Project Deployment Report: Local Kubernetes Microservices

**Student:** Emad Fattah

**Class:** MSSE640

**Instructor:** Randell Grainer

---

**Introduction**


Modern cloud-first applications increasingly rely on microservices architectures to ensure scalability, fault tolerance, and language flexibility. Evaluating, developing, and testing these distributed systems, however, requires robust deployment environments that mimic production infrastructure without incurring high cloud platform costs. This project focuses on the local engineering and deployment of Google Cloud Platform’s (GCP) Online Boutique (formerly microservices-demo)—a web-based e-commerce application designed to showcase enterprise modernization patterns using Kubernetes, gRPC, and multi-language services.


While the original blueprint is optimized for Google Kubernetes Engine (GKE), this initiative adapts the cloud-native application to execute entirely within a local bare-metal environment. The target stack leverages Minikube running via the Docker Desktop virtualization driver, specifically optimized to run on an Apple Silicon (M4) ARM64 macOS architecture.

The primary objectives of this deployment were to:

**Overcome Hardware Constraints:** Dynamically scale and calibrate resource allocations (CPU and RAM) to fit localized system limits without compromising application stability.


**Resolve Architecture Barriers:** Bypass legacy virtualization layers (like VirtualBox) by utilizing native containerization engines compatible with Apple Silicon hardware.


**Orchestrate Multi-Language Microservices:** Successfully deploy and audit all 12 system components—encompassing 11 functional microservices (written in Go, C#, Node.js, Python, and Java) and a Redis cache database.


**Establish Local Ingress Routing:** Bridge isolated cluster networking back to the host machine’s browser layer to ensure fully functional, end-to-end user transactions.


The following sections detail the comprehensive environment preparation, manifest execution metrics, network routing configurations, and resource teardown workflows that validated this successful local deployment.


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

Figure1: All pods verifications  

![pic1](/Assignments/Images/Project4_Minikube/1.Pic1.png)

---

## 4. Networking, Routing & Ingress Handling
Because Minikube operates inside an isolated virtual container loop on macOS, its public load balancers are not inherently reachable by default. 

To map internet traffic routing to the host computer, we established an active TCP network port tunnel bridging local web ports to the application's external entry point:
* **Command Executed:**
  ```bash
  kubectl port-forward service/frontend-external 8080:80
  ```
* **Validation Metric:** The terminal logs successfully printed consecutive `Handling connection for 8080` metrics, verifying functional browsing interactions on **`http://localhost:8080`** with full cross-service communication (Cart, Currency, Payments, Recommendations).

Figure2: Boutique

![Pic2](/Assignments/Images/Project4_Minikube/2.Pic2.png)

---

## 5. Teardown Blueprint (For Future Use)
When you wish to de-allocate resources and cleanly dismantle this deployment, run the following sequence in your terminal workspace:

```bash
# 1. Tear down the microservices and network assets
kubectl delete -f ./release/kubernetes-manifests.yaml

# 2. Power down the Minikube virtual instance to reclaim RAM/CPU
minikube stop
```
---
## 6. Video Clip Boutique

1. Click on the link under

2. Click the View raw to download and watch the video.

["Boutique"](/Assignments/Images/Project4_Minikube/2.Video1_T.mp4)

___

 ## Intro to Selenium and Selenium IDE

 

**Selenium** is an open-source umbrella project providing tools and libraries optimized for web browser automation. Originally created to automate manual quality assurance tasks, it has grown into an industry-standard ecosystem used for both web application testing and large-scale web scraping. 

According to the [Selenium Official Website](https://www.selenium.dev/), the project is not just a single utility, but a suite comprised of three core components designed for different use cases:
* **Selenium WebDriver**: A collection of language-specific bindings (supporting Python, Java, C#, JavaScript, and Ruby) that directly communicate with browsers to execute advanced code-based automation.
* **Selenium IDE**: A beginner-friendly browser add-on used to easily capture UI flows.
* **Selenium Grid**: A tool designed to scale testing by running automation scripts in parallel across distinct operating systems and remote machines.

---

### Detailed Overview of Selenium IDE
As detailed in the [Selenium IDE Documentation](https://www.selenium.dev/documentation/ide/), **Selenium IDE (Integrated Development Environment)** is a turn-key, open-source browser extension available for Google Chrome, Mozilla Firefox, and Microsoft Edge. It serves as a rapid prototyping tool that lets users record their manual interactions with a live website and play them back instantly without writing any code. 

#### Core Strengths & Features:
* **No-Code Record and Playback:** Users click through a site while the extension logs actions like clicks and keystrokes automatically.
* **Resilient Element Locators:** To avoid brittle tests, the IDE simultaneously tracks multiple element identifiers (such as ID, XPath, and CSS selectors) when a user interacts with a web component.
* **Control Flow Automation:** Built-in [Selenium IDE Control Flow Commands](https://www.selenium.dev/selenium-ide/) support basic logical loops and conditional expressions (`if`, `while`, `times`) directly inside the graphical interface.
* **Script Exporting:** Recorded tests are saved in a specific format (`.side`), but can be easily exported into target programming languages like Java or Python to be used inside advanced Selenium WebDriver frameworks.

---

###  Technical Breakdown: Selenium IDE vs. Selenium WebDriver

| Capability | Selenium IDE | Selenium WebDriver |
| :--- | :--- | :--- |
| **Primary Interface** | Browser Extension UI | Code Libraries / APIs |
| **Required Skill** | None (No-Code UI) | Intermediate programming |
| **Scripting Language** | Selenese (Internal syntax) | Choice of Python, Java, C#, etc. |
| **Logic Support** | Basic loops and conditionals | Full execution logic of the chosen language |
| **Best Used For** | Prototyping, small scripts, bug reporting | Enterprise test suites, complex scraping |

The [Selenium Downloads Page](https://www.selenium.dev/downloads/) provides immediate access to the official web store links for all supported desktop browsers.

---
### Using Selenium IDE in testing "Boutique" Website:


The Selenium is added in Fire Fox Web Browser for recording the event in Boutique Website 

Figure3: Recording Selenium 

![Pic3](/Assignments/Images/Project4_Minikube/3.Sel_Test.png)


**Exporting the Recorder Files**
The file is exported to three Coding languages 
1. Data Language JSON
   
   ![_🛠️_](/Code/4.EMAD_Demo_BTQ.side)

2. Java

   
   


