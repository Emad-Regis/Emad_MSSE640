# Project 3

## Testing with Apache JMeter

**Student:** Emad Fattah
**Class:** MSSE640
**Instructor:** Randell Grainer

---

## Introduction

**Apache JMeter** is a 100% pure Java open-source application designed to load test functional behavior and measure system performance across a broad range of protocols, including HTTP, HTTPS, REST, SOAP, JDBC, and LDAP. Unlike a standard web browser that renders visual pages, JMeter operates strictly at the protocol level, allowing QA engineers to simulate thousands of concurrent virtual users across various testing methodologies. These methodologies include standard load testing for real-world usage, stress testing to find breaking points, spike testing for sudden traffic surges, functional testing for API validation, and endurance testing to uncover long-term issues like memory leaks and resource degradation. The application structures these simulations using an architectural framework comprised of a master Test Plan, Thread Groups to define user behavior, Samplers to send the actual server requests, Assertions to validate response data, and Listeners to gather the metrics required for performance dashboards and reports.

---

## JMeter Load Performance Testing

Load Performance Testing in JMeter refers to simulating multiple concurrent users (Threads) hitting an application/API/server over a defined time period, in order to measure response time, throughput, error rate, and system stability under expected - or extreme - usage conditions.

In JMeter, this is configured primarily through the **Thread Group** element, where you define:

- **Number of Threads (users)** - simulated concurrent users
- **Ramp-Up Period** - time taken to start all threads
- **Loop Count / Duration** - how long or how many times the test runs
- **Scheduler** - controls start/end time of the test

Below are the common types of Load Performance Tests you can build in JMeter, each with a graph showing **Time (X-axis)** vs **Number of Threads (Y-axis)**.

### 1. Ramp-Up Load Test

**Purpose:** Gradually increase the number of virtual users to observe how the system behaves as load builds up, and to identify the point where performance starts degrading.

**JMeter Setup:** Set a Ramp-Up Period (e.g., 60s) to reach the target thread count (e.g., 100), then hold or stop.

> *The thread count increases linearly during the ramp-up window and then plateaus at the target load.*

### 2. Steady State (Constant) Load Test

**Purpose:** Apply a fixed, constant number of users for a sustained period to validate consistent performance (response time, throughput) under a known, stable load.

**JMeter Setup:** Use a short ramp-up to reach target threads quickly, hold constant using the **Scheduler**'s duration, then ramp down.

> *Threads quickly reach a plateau and remain flat for the duration of the test â€” this is the classic "flat-top" load pattern.*

### 3. Step Load Test

**Purpose:** Incrementally increase load in discrete steps (e.g., 25 â†’ 50 â†’ 75 â†’ 100 users) with pauses at each step, to identify at which concurrency level performance starts to degrade (helps find the breaking point gradually rather than a shock).

**JMeter Setup:** Achieved via **Stepping Thread Group** (a JMeter plugin) or multiple Thread Groups scheduled sequentially.

> *Each "step" holds threads at a fixed level for a set duration before increasing to the next tier â€” useful for pinpointing capacity thresholds.*

### 4. Spike Load Test

**Purpose:** Suddenly and sharply increase the number of users for a short burst (simulating flash sales, viral traffic, etc.) to test how the system handles sudden spikes and whether it recovers gracefully afterward.

**JMeter Setup:** Use the **Ultimate Thread Group** or **Concurrency Thread Group** plugin to define sharp spikes, or nested Thread Groups with near-zero ramp-up for rapid increases.

> *Threads jump abruptly to a high peak, drop back to baseline, and may spike again â€” testing elasticity and recovery.*

### 5. Soak (Endurance) Load Test

**Purpose:** Apply a moderate, sustained load over a long duration (hours) to detect issues that only appear over time - such as memory leaks, connection pool exhaustion, or gradual performance degradation.

**JMeter Setup:** Constant thread count with a long **Scheduler duration** (e.g., 1+ hour), often paired with JMeter's **Duration Assertion** and monitoring plugins.

> *Load remains flat but the test runs for an extended time window compared to a standard steady-state test.*

### Summary Table

| Test Type      | Goal                                          | Thread Pattern             |
|-----------------|-----------------------------------------------|-----------------------------|
| Ramp-Up         | Observe gradual load buildup                  | Linear increase to target  |
| Steady State    | Validate performance under known load         | Flat plateau               |
| Step Load       | Find degradation threshold                    | Incremental staircase      |
| Spike           | Test elasticity/recovery                      | Sharp burst(s)             |
| Soak/Endurance  | Detect long-term issues (leaks, degradation)  | Flat, long duration        |

### Key JMeter Metrics to Monitor During Any Load Test

- Response Time (Average, Median, 90th/95th/99th percentile)
- Throughput (requests/sec)
- Error Rate (%)
- Latency vs Connect Time
- Active Threads over Time (built-in JMeter listener graph)

---

## Endurance (Soak) Performance Testing in JMeter

An **Endurance Test** (also known as a **Soak Test**) is a type of performance testing where a system is subjected to a continuous, sustained workload over an extended period â€” typically ranging from 6 hours to 24 hours or longer.

While standard load testing evaluates how a system behaves under expected peak conditions over short intervals (e.g., 10 to 30 minutes), **Endurance Testing focuses on degradation over time**. It exposes critical defects that only manifest under prolonged operations, such as:

- **Memory Leaks / Out of Memory (OOM) Errors:** Heap space that is allocated but never released by Garbage Collection (GC).
- **Resource Exhaustion:** Database connection pool leaks, open file handle limits, or thread lockups.
- **Disk / Storage Saturation:** Unmanaged log growth, temporary file accumulation, or audit table bloat.
- **Performance Degradation (Sluggishness):** Increasing response times or declining throughput over extended running hours.

### 1. Standard Constant Endurance (Soak) Test

**Description**

In a Standard Endurance Test, virtual users (Threads) are ramped up to an expected baseline or average operational load. Once the target thread count is achieved, the load is held **completely flat for a prolonged duration** (e.g., 12 to 24 hours) before ramping down.

**JMeter Configuration**

- **Thread Group:** Standard Thread Group or Concurrency Thread Group.
- **Ramp-Up Period:** Brief initial ramp-up window (e.g., 10â€“30 minutes) to reach target load smoothly without shocking the application.
- **Duration (Scheduler):** Enable **Specify Thread Lifetime** / **Scheduler** and set Duration (e.g., 86400 seconds for 24 hours).
- **Timers:** Use a Constant Throughput Timer or Precise Throughput Timer to maintain a fixed request rate per minute.

- **X-Axis:** Time (Hours)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Key Focus:** Verify that response times, CPU usage, and memory usage remain flat throughout the 20-hour sustained window.

### 2. Step-Up Endurance Test

**Description**

A Step-Up Endurance Test increases the virtual user load in discrete steps, holding each step for an extended time period (e.g., 3 to 4 hours per step). This allows performance engineers to evaluate long-term stability and resource retention at multiple concurrency tiers.

**JMeter Configuration**

- **Thread Group:** Stepping Thread Group (via JMeter Plugins) or Concurrency Thread Group.
- **Steps Configuration:**
  - Start with 50 threads; hold for 3.5 hours.
  - Add 50 threads over a 30-minute ramp; hold for 3.5 hours.
  - Repeat up to peak capacity (e.g., 200 threads).
- **Purpose:** Identifies if memory or resource leaks compound faster at higher thread counts over time.

- **X-Axis:** Time (Hours)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Key Focus:** Detect whether heap consumption or database connection count recovers or degrades proportionally at each stepped level.

### 3. Cyclic / Diurnal Endurance Test

**Description**

Real-world enterprise applications experience natural daily traffic fluctuations â€” high load during business hours and low load overnight. A Cyclic (Diurnal) Endurance Test simulates these multi-day wave patterns over 48 to 72 hours to evaluate system stability and recovery across continuous operational cycles.

**JMeter Configuration**

- **Thread Group:** Ultimate Thread Group (JMeter Plugin) to define custom wave schedules, or Free-Form Arrival Thread Group.
- **Profile Setup:** Configure multiple thread schedules overlapping in time to model peak daytime hours and off-peak nighttime troughs across consecutive days.
- **Purpose:** Tests whether the application successfully performs garbage collection, clears caches, releases idle connections, and recovers performance during off-peak periods.

- **X-Axis:** Time (Hours)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Key Focus:** Verify that nighttime troughs allow full memory recovery and that Day 2 peak performance equals Day 1 peak performance.

### 4. High-Load / Stress Endurance Test

**Description**

A High-Load Endurance Test subjects the system to maximum expected capacity (or near-breaking threshold) for an extended duration (e.g., 12 hours). This is harsher than a standard soak test and tests system resilience, queue backlogs, and recovery under constant high strain.

**JMeter Configuration**

- **Thread Group:** Concurrency Thread Group or standard Thread Group.
- **Ramp-Up:** Steeper ramp to reach maximum thread capacity (e.g., 300 threads).
- **Scheduler Duration:** Set to run continuously at peak volume for 12+ hours.
- **Pacing / Flow Control:** Set throughput pacing to enforce high continuous request rates.

- **X-Axis:** Time (Hours)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Key Focus:** Identify queue overflow, connection pool starvation, thread contention, and degradation under peak capacity.

### Key Metrics to Monitor During Endurance Tests

| Category         | Metric                                | What to Watch For                                                              |
|-------------------|----------------------------------------|----------------------------------------------------------------------------------|
| JMeter Response  | Response Time (90th/95th Percentile)  | Gradual upward slope indicates memory leak or queue build-up                    |
| Throughput       | Transactions Per Second (TPS)         | Unexplained drop in TPS over time points to thread lock or resource bottleneck  |
| Error Rate       | HTTP 5xx / Connection Timeouts        | Errors increasing over time signal resource depletion (e.g., DB pool limits)    |
| JVM Health       | Heap Memory Usage / GC Pause Times    | "Sawtooth" memory pattern is healthy; continuously rising baseline indicates memory leak |
| System Resources | CPU, OS File Descriptors, Disk I/O    | Log files filling disk space; open handles increasing without release           |

### Summary Matrix

| Endurance Test Pattern | Duration    | Thread Pattern                    | Primary Objective                                             |
|--------------------------|-------------|-------------------------------------|-----------------------------------------------------------------|
| Standard Soak            | 12-24 Hours | Flat, constant thread count        | Detect subtle memory leaks and file descriptor exhaustion       |
| Step-Up Endurance        | 12-18 Hours | Incremental stair-step plateaus    | Measure resource consumption across capacity thresholds         |
| Cyclic / Diurnal         | 48-72 Hours | Multi-day sine wave                | Validate off-peak resource cleanup and auto-recovery            |
| High-Load Stress         | 8-12 Hours  | Sustained peak capacity            | Test queue capacity, connection pool stability, and survival    |

---

## Stress and Spike Performance Testing in Apache JMeter

In performance engineering, **Stress Testing** and **Spike Testing** are two essential non-functional test methodologies used to evaluate an application's stability, resilience, upper capacity limits, and recovery capabilities under extreme conditions.

- **Stress Testing** intentionally pushes a system **beyond its normal operational limits** to find the breaking point, observe how gracefully it degrades, and verify that it does not crash or corrupt data under heavy pressure.
- **Spike Testing** evaluates how a system responds to **sudden, dramatic, and short-lived increases in traffic** (e.g., flash sales, breaking news alerts, ticket drops) and whether it quickly recovers once traffic normalizes.

### Part 1: Stress Performance Testing

#### 1. Progressive Step-Stress Test (Finding the Breaking Point)

**Purpose / Description**

The primary objective of a Progressive Step-Stress Test is to identify the maximum load capacity (throughput/concurrency limit) of the target application. Unlike a standard load test â€” which stays within expected peak traffic limits â€” a stress test continually steps up the thread count well past expected peak capacity until performance severely degrades or errors begin occurring.

**JMeter Setup**

- **Thread Group:** Stepping Thread Group or Concurrency Thread Group (via JMeter Plugins).
- **Configuration:**
  - **Initial Load:** Start with expected operational load (e.g., 50 threads).
  - **Step Increments:** Add 50 threads every 10â€“15 minutes.
  - **Duration:** Run until thread count exceeds expected design limit (e.g., 300 threads).
- **Key Observations:** Pinpoint the exact thread count where response times spike exponentially or where HTTP 5xx errors begin appearing.

- **X-Axis:** Time (Minutes)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Graph Pattern:** Escalating staircase profile crossing baseline, maximum designed capacity, and ultimate breaking point zones.

#### 2. Stress / Recovery Test (Over-Capacity / Self-Healing)

**Purpose / Description**

This variation pushes the application deep into an overloaded state (e.g., 200% of maximum capacity) for a sustained period to trigger queue backlogs, memory pressure, and connection pool saturation. The thread count is then immediately dropped back to a normal baseline level to test whether the system can **self-heal and auto-recover** without manual restart or admin intervention.

**JMeter Setup**

- **Thread Group:** Ultimate Thread Group or Concurrency Thread Group.
- **Configuration:**
  - **Phase 1 (Baseline):** 50 threads for 10 minutes.
  - **Phase 2 (Over-Capacity Stress):** Ramp rapidly to 400 threads (200% of capacity) and maintain for 15â€“20 minutes.
  - **Phase 3 (Recovery Phase):** Ramp down to 50 threads and observe for 20 minutes.
- **Key Observations:** Measure the time required for response times and queue lengths to return to normal baseline metrics after the stress is removed.

- **X-Axis:** Time (Minutes)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Graph Pattern:** Sharp rise into extreme stress zone, followed by a plateau under heavy strain, and a drop back down to monitor recovery.

### Part 2: Spike Performance Testing

#### 1. Single Sudden Spike Test

**Purpose / Description**

A Single Spike Test evaluates the system's immediate response when traffic increases by **5x to 10x within seconds or minutes**. This scenario simulates events like push notification broadcasts, breaking news alerts, or limited-inventory drops. The focus is on testing web server request queues, thread pool expansion, auto-scaling trigger speed, and overall system elasticity.

**JMeter Setup**

- **Thread Group:** Ultimate Thread Group or Concurrency Thread Group.
- **Configuration:**
  - **Baseline:** Maintain a low baseline (e.g., 30 threads) for 20 minutes.
  - **Spike Ramp-Up:** Jump from 30 to 300 threads in 1-5 seconds (near-zero ramp-up).
  - **Spike Hold:** Hold peak load for 5 minutes.
  - **Spike Drop:** Drop back to 30 threads in 1-5 seconds.
- **JMeter Timers:** Combine with a **Synchronizing Timer** (Timer element in JMeter) to force all threads to release requests simultaneously at the exact same instant for maximum impact.

- **X-Axis:** Time (Minutes)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Graph Pattern:** A flat baseline with a sudden vertical tower rising to peak concurrency and immediately dropping back.

#### 2. Multi-Spike / Repeated Burst Test

**Purpose / Description**

Real-world enterprise systems often experience repeated traffic surges - such as cron jobs executing, batch processing jobs, or recurring promotional bursts during a live event. A Multi-Spike Test applies successive high-volume traffic bursts separated by short recovery intervals to test whether memory, connection pools, or cache layers compound debt over repeated shocks.

**JMeter Setup**

- **Thread Group:** Ultimate Thread Group.
- **Configuration:**
  - **Baseline:** Constant background load of 40 threads.
  - **Spike 1:** Burst to 250 threads for 4 minutes â†’ drop back to 40 threads for 15 minutes.
  - **Spike 2:** Burst to 300 threads for 4 minutes â†’ drop back to 40 threads for 15 minutes.
  - **Spike 3:** Burst to 220 threads for 4 minutes â†’ drop back to 40 threads.
- **Key Observations:** Check whether peak latency increases with each subsequent spike, which indicates uncollected garbage, thread exhaustion, or unreleased database handles.

- **X-Axis:** Time (Minutes)
- **Y-Axis:** Number of Threads (Virtual Users)
- **Graph Pattern:** Multiple narrow peaks rising from a continuous low baseline level.

### Comparison Summary Table

| Test Type            | Objective                                               | Load Characteristics                                          | Primary Failure Modes Tested                                                |
|------------------------|-----------------------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Step-Stress           | Find absolute breaking point / maximum capacity limit    | Progressive staircase ramp up beyond limit                     | Memory allocation failures, database connection exhaustion, CPU throttling      |
| Stress / Recovery     | Test self-healing and system elasticity after overload    | Over-capacity plateau followed by step-down to baseline         | Queue lockups, unrecovered thread pools, permanent service degradation          |
| Single Spike          | Test shock resistance to immediate traffic surges          | Near-instantaneous spike (5xâ€“10x) for a short duration           | Connection dropouts, HTTP 502/503/504 gateway timeouts, buffer overflows        |
| Multi-Spike / Burst   | Test resilience against repeated surges                    | Multiple successive traffic spikes separated by idle windows    | Resource leakage compounding over time, cache invalidation storms               |

### How to Configure Stress / Spike Tests in JMeter

**1. Key JMeter Plugins Recommended**

Standard JMeter Thread Groups can be limiting for complex stress profiles. Installing the **Custom Thread Groups** plugin via JMeter Plugins Manager gives access to:

- **jp@gc - Ultimate Thread Group**: Allows precise definition of multi-ramp schedules, hold times, and shutdown times per thread allocation group.
- **jp@gc - Concurrency Thread Group**: Provides dynamic control over target concurrency and step increments.

**2. Simulating Instantaneous Load with Timers**

To ensure virtual users hit the target endpoint in exact synchronization during a spike:

- **Synchronizing Timer (Rendezvous Point):** Place a Synchronizing Timer inside the HTTP Request. Set **"Number of Simulated Users to Group by"** to match the spike size (e.g., 300). JMeter will hold all threads until 300 users are ready and release them simultaneously.

**3. Key Metrics to Track**

When evaluating Stress and Spike test results, monitor the following metrics in JMeter listeners or Grafana dashboards:

$$\text{Error Rate (\%)} = \left( \frac{\text{Failed Requests}}{\text{Total Requests}} \right) \times 100$$

- **95thâ€“99th Percentile Response Time:** Shows how hard tail-end requests are impacted during peaks.
- **Throughput (Transactions Per Second):** Watch for throughput flattening or dropping while thread counts increase (a signal of saturation).
- **HTTP Response Codes:** Track transitions from HTTP 200 OK to 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, or 504 Gateway Timeout.
- **System Recovery Time ($$T_{\text{recovery}}$$):** The time required after a spike or stress event for error rates to drop to 0% and response times to return to baseline.

---

## JMeter Test Plan Architecture

In Apache JMeter, performance tests are built using a hierarchical tree of test plan elements. Four of the most fundamental components that form the backbone of almost any JMeter web or API test script are **Thread Groups**, **HTTP Request Samplers**, **Config Elements**, and **Listeners**.

Below is a detailed breakdown of each component, their configurations, and best practices, followed by a structural view of how they interact within a JMeter execution pipeline.

### 1. Thread Groups

**Overview**

A **Thread Group** is the starting point of any JMeter test plan. It controls the virtual user pool, defining **how many concurrent users** (represented as threads) will execute the test scripts, **how fast** they spin up, and **how long** they run. Everything that represents user actions (samplers, controllers, timers) must sit inside a Thread Group.

**Key Parameters / Configurations**

- **Number of Threads (Users) ($$N$$)**: The total number of virtual users executing concurrently during peak load.
- **Ramp-Up Period ($$T_{\text{ramp}}$$ in seconds)**: The total time JMeter takes to start all threads.
  - *Example*: If Threads = 100 and Ramp-Up = 20 seconds, JMeter starts 5 threads every second ($$\frac{N}{T_{\text{ramp}}} = \frac{100}{20} = 5\text{ threads/sec}$$).
- **Loop Count / Duration**:
  - **Loop Count**: Specifies the exact number of times each thread executes the test plan statements before stopping.
  - **Infinite / Duration (sec)**: Runs the thread continuously for a set time (e.g., 1800 seconds for a 30-minute load test).
- **Action to take after a Sampler Error**: Controls thread behavior when a request fails (Continue, Start Next Loop, Stop Thread, Stop Test, Stop Test Now).

**Types of Thread Groups**

- **Standard Thread Group**: Built-in default for simple linear ramp-up and duration tests.
- **setUp Thread Group**: Executes initialization tasks (e.g., login, populating data, clearing database caches) **before** main test threads begin.
- **tearDown Thread Group**: Executes cleanup tasks (e.g., deleting created resources, logging out) **after** main test threads finish.
- **Concurrency Thread Group / Ultimate Thread Group** *(Plugins)*: Allows defining advanced step-wise, spike, or staircase workload profiles.

### 2. HTTP Request Sampler

**Overview**

**Samplers** tell JMeter to send requests to a target server and wait for a response. The **HTTP Request Sampler** is the most widely used sampler in JMeter, designed specifically to test web applications, REST APIs, microservices, and SOAP services.

**Key Parameters / Configurations**

- **Protocol / Domain**: Sets http vs. https, server hostname or IP address, and port number (e.g., 443 for SSL).
- **HTTP Method**: Choose from GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, etc.
- **Path**: The API endpoint or URI route (e.g., `/api/v1/orders`).
- **Parameters / Request Body**:
  - **Parameters tab**: Key-value query parameters attached to the URL (e.g., `?category=electronics&page=1`).
  - **Body Data tab**: Raw JSON, XML, or plain text payload for POST/PUT requests.
  - **Files Upload tab**: Attachment uploads (file path, parameter name, MIME type).
- **Execution Options**:
  - **Follow Redirects**: Automatically follows HTTP 301/302 redirects and records the final response.
  - **Use KeepAlive**: Reuses HTTP connections to avoid overhead from repeated TCP handshakes.

### 3. Config Elements

**Overview**

**Config Elements** act as pre-processors or configuration blueprints that set up default values, manage state, inject headers, or parameterize request data for samplers in their scope. They do not send requests themselves; instead, they alter or enhance the samplers that execute after them.

**Essential Config Elements**

| Config Element                | Function / Usage                                                                                                                                                                                   |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| HTTP Request Defaults         | Defines baseline settings (Protocol, Host Name, Port Number, Default Headers) in one place. All HTTP Samplers inherit these settings unless overridden locally.                                       |
| HTTP Header Manager           | Adds custom HTTP headers to outgoing requests (e.g., `Content-Type: application/json`, `Authorization: Bearer token`, `User-Agent`).                                                                    |
| HTTP Cookie Manager           | Handles session management automatically. It captures Set-Cookie response headers from the server and attaches appropriate cookies to subsequent requests, mimicking browser session persistence.    |
| HTTP Cache Manager            | Simulates browser caching behavior, ensuring static assets are not re-downloaded repeatedly by the same virtual user.                                                                                  |
| CSV Data Set Config           | Parameterizes tests by reading user data (e.g., usernames, passwords, product IDs) line-by-line from a `.csv` file and mapping columns to JMeter variables (e.g., `${username}`).                     |
| User Defined Variables (UDV)  | Declares static global variables available across the entire test plan (e.g., `${BASE_URL}`).                                                                                                          |

### 4. Listeners

**Overview**

**Listeners** capture, analyze, store, and display result data generated by samplers during test execution. They collect key metrics such as latency, response time, throughput in requests per second (TPS), status codes, and error percentages.

**Key Types / Best Practices**

1. **View Results Tree**:
   - *Purpose*: Shows the full HTTP request (headers, body, URL) and full response (status code, headers, payload) for every individual request.
   - *Usage Note*: Essential during **script creation and debugging**. Must be **disabled during actual load tests** as it consumes excessive system memory.
2. **Summary Report / Aggregate Report**:
   - *Purpose*: Tabular summaries showing key statistics across all samplers:
     - **Samples Count**: Total requests sent.
     - **Average, Min, Max**: Response times in milliseconds.
     - **90% / 95% / 99% Percentiles**: Response time threshold below which 90% of requests completed.
     - **Throughput**: Transactions per second (TPS).
     - **Error %**: Percentage of failed requests.
3. **Active Threads Over Time / Response Times Over Time** *(Plugins)*:
   - *Purpose*: Visual line charts plotting concurrency changes, response time trends, and throughput rates over elapsed time.
4. **Backend Listener**:
   - *Purpose*: Streams live test metrics asynchronously to external monitoring backends (e.g., InfluxDB or Prometheus) for display on Grafana real-time dashboards during high-scale load runs.

### Component Architecture / Execution Flow

The workflow sequence within JMeter operates as follows:

1. **Test Plan** acts as the root node.
2. **Thread Groups** instantiate virtual users according to the ramp-up and duration configuration.
3. **Config Elements** evaluate first within scope to inject variables, authentication tokens, session cookies, and target parameters.
4. **HTTP Request Samplers** construct the network payload using the merged configuration and transmit HTTP/S calls to the target system.
5. **Listeners** record response statistics, latency, and status codes for analysis and dashboard reporting.

### Component Best Practices Summary

- **Scoping Rule**: Config elements and listeners apply to all samplers at their hierarchical level and below. Keep HTTP Request Defaults at the top level, but restrict specific HTTP Header Managers to individual request controllers if needed.
- **CLI Mode Execution**: Always run actual load tests in headless Non-GUI mode (`jmeter -n -t plan.jmx -l results.jtl -e -o ./report`) to maximize engine performance and minimize memory overhead.
- **Parameterization**: Combine CSV Data Set Config with HTTP Request Sampler body templates to ensure realistic multi-user variability rather than repeating duplicate hardcoded requests.

---

## Application Performance Index

An **Application Performance Index (Apdex)** is an open industry standard used to measure user satisfaction with the response time of web applications and APIs.

Instead of analyzing disparate technical metrics (like average latency, 95th percentile response times, and error percentages), Apdex synthesizes these performance indicators into a **single normalized score between 0.0 and 1.0** (or 0% to 100%).

In **Apache JMeter**, the Apdex score is prominently featured at the top of the generated **HTML Dashboard Report** to provide executives and engineering teams with an immediate summary of system health relative to defined Service Level Agreements (SLAs).

### 1. How Apdex Categorizes User Experience

Apdex categorizes every request into one of three distinct user experience zones based on response time thresholds defined in milliseconds:

| Zone       | Condition                                   | Weight |
|------------|----------------------------------------------|--------|
| Satisfied   | Response Time â‰¤ T                           | 1.0    |
| Tolerating  | T < Response Time â‰¤ F (where F = 4T)         | 0.5    |
| Frustrated  | Response Time > F, or Error                  | 0.0    |

1. **Satisfied Zone ($$N_S$$)**:
   - **Condition**: Response time is less than or equal to the target threshold T (e.g., â‰¤ 500 ms) and the HTTP status code is successful (200 OK).
   - **User Impact**: The user experiences smooth, uninterrupted application performance.
   - **Score Weight**: 1.0 (100% satisfied).
2. **Tolerating Zone ($$N_T$$)**:
   - **Condition**: Response time is greater than T, but less than or equal to the tolerated threshold F (where F is conventionally set to 4 Ã— T, e.g., 500 ms < Latency â‰¤ 2000 ms).
   - **User Impact**: The user notices a slight delay but completes the transaction without abandoning the action.
   - **Score Weight**: 0.5 (50% satisfied).
3. **Frustrated Zone ($$N_F$$)**:
   - **Condition**: Response time exceeds F (e.g., > 2000 ms) **OR** the request results in an error (e.g., HTTP 500 Server Error, connection timeout, assertion failure).
   - **User Impact**: The user experiences unacceptable slowness or system failure, leading to task abandonment.
   - **Score Weight**: 0.0 (0% satisfied).

### 2. Mathematical Formula

The Apdex score is calculated using the following formula:

$$\text{Apdex Score} = \frac{N_S + \frac{N_T}{2}}{N_S + N_T + N_F}$$

**Example Calculation**

Suppose JMeter executes 10,000 total HTTP requests with a target threshold T = 500 ms and F = 2000 ms:

- **Satisfied Requests ($$N_S$$)**: 8,500 (responded in â‰¤ 500 ms)
- **Tolerating Requests ($$N_T$$)**: 1,000 (responded between 501 ms and 2000 ms)
- **Frustrated Requests ($$N_F$$)**: 500 (300 took > 2000 ms, 200 returned HTTP 500 errors)

$$\text{Apdex} = \frac{8500 + \frac{1000}{2}}{10000} = \frac{9000}{10000} = 0.90$$

An Apdex score of **0.90** indicates a **"Good"** user performance rating.

### 3. Apdex Score Rating Scale

| Apdex Range   | Quality Rating | Assessment / SLA Status                                       |
|-----------------|------------------|---------------------------------------------------------------------|
| 0.94 â€“ 1.00     | Excellent        | Exceptional responsiveness; fully meets strict SLAs.                |
| 0.85 â€“ 0.93     | Good             | Solid performance; minor optimization opportunities.                |
| 0.70 â€“ 0.84     | Fair             | Acceptable under peak load; approaching capacity boundaries.        |
| 0.50 â€“ 0.69     | Poor             | SLA breach; notable user friction and system slowness.              |
| 0.00 â€“ 0.49     | Unacceptable     | Critical performance failure; high error rates or severe latency.   |

### 4. Configuring Apdex in JMeter

JMeter allows you to define global default thresholds as well as specific thresholds for individual API endpoints in the `bin/user.properties` file:

```properties
# Global default Satisfied Threshold T (in milliseconds)
jmeter.reportgenerator.apdex_satisfied_threshold=500

# Global default Tolerated Threshold F (in milliseconds)
jmeter.reportgenerator.apdex_tolerated_threshold=1500

# Overriding Apdex thresholds for specific Samplers / Transactions
# Syntax: jmeter.reportgenerator.apdex_satisfied_threshold.sample_name=value_in_ms
jmeter.reportgenerator.apdex_satisfied_threshold.Login_HTTP_Request=300
jmeter.reportgenerator.apdex_tolerated_threshold.Login_HTTP_Request=1200
jmeter.reportgenerator.apdex_satisfied_threshold.Generate_PDF_Report=2000
jmeter.reportgenerator.apdex_tolerated_threshold.Generate_PDF_Report=8000
```

**Generating the Apdex Report in JMeter**

When you execute a non-GUI load test and generate the HTML report:

```bash
jmeter -n -t test_plan.jmx -l log_results.jtl -e -o ./html_report_output
```

JMeter automatically calculates the Apdex table in the generated dashboard, providing a clear breakdown per request sampler:

| Sampler / Transaction   | Target T (ms) | Tolerated F (ms) | Apdex Score | Rating    |
|---------------------------|-----------------|--------------------|---------------|-------------|
| GET /api/v1/products     | 500             | 1500               | **0.98**      | Excellent   |
| POST /api/v1/checkout    | 1000            | 3000               | **0.88**      | Good        |
| GET /api/v1/reports      | 2000            | 6000               | **0.62**      | Poor        |

### Why Apdex is Valuable in Performance Testing

1. **Combines Latency and Reliability**: Errors automatically penalize the score as "Frustrated," ensuring a fast API that fails 10% of the time cannot score highly.
2. **Business-Friendly Metric**: Provides executive stakeholders with an easy-to-understand single KPI (e.g., *"Our baseline Apdex is 0.92, but under stress test conditions it degrades to 0.58"*).
3. **Endpoint-Specific Benchmarking**: Enables setting realistic expectations for complex operations (e.g., image rendering) versus lightweight operations (e.g., authentication check).

---

## Conclusion

Apache JMeter proves to be a versatile and powerful open-source tool for comprehensive performance testing across the full spectrum of non-functional testing needs. This project explored the breadth of JMeter's capabilities, beginning with foundational load performance tests - Ramp-Up, Steady State, Step Load, Spike, and Soak - each designed to reveal how a system behaves under different concurrency patterns and reveal degradation thresholds before they impact real users. Building on this, endurance (soak) testing demonstrated how sustained, cyclic, and high-load scenarios over extended durations expose subtle but critical defects such as memory leaks, connection pool exhaustion, and disk saturation that short-duration tests cannot detect.

The exploration of stress and spike testing further highlighted JMeter's ability to simulate extreme conditions, from progressive step-stress tests that identify absolute breaking points to sudden traffic spikes that test a system's elasticity and recovery capabilities. These test types are essential for validating that applications not only perform well under expected load but also degrade gracefully and recover cleanly when pushed beyond normal operating boundaries.

Underpinning all of these test strategies is JMeter's modular architecture - Thread Groups, HTTP Request Samplers, Config Elements, and Listeners - which work together to simulate realistic user behavior, inject dynamic configuration and authentication data, and capture detailed performance metrics. Finally, the Apdex scoring methodology ties these technical measurements back to business value, translating raw latency and error data into a single, stakeholder-friendly satisfaction score that can be benchmarked against SLAs.

Taken together, these tools and techniques illustrate that effective performance testing is not a single test execution but a layered strategy: combining load, endurance, stress, and spike testing with well-architected test plans and meaningful metrics like Apdex allows QA and performance engineering teams to build a complete, evidence-based picture of application reliability, scalability, and readiness for production-scale traffic.
