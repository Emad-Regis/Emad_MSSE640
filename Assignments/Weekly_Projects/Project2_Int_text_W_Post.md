# Project 2: Integration Testing with Postman

**Student:** EMAD FATTAH

**Class:** MSSE640

**Instructor:** Randall Granier

---

## Project Introduction

In contemporary software engineering, web applications are designed around decoupled, service-oriented architectures that rely heavily on robust communication protocol standards and Application Programming Interfaces (APIs). Understanding the fundamental mechanics of the Hypertext Transfer Protocol (HTTP), state management strategies, security frameworks, and cross-origin controls is essential for building scalable, secure, and resilient software systems.

This report bridges foundational theoretical network concepts with hands-on software verification and integration testing methodologies. The document is structured into two core sections:

- **Part 1: Theoretical Foundations** — Provides an in-depth analysis of HTTP architecture (client-server model, anatomical structure of messages, request verbs, and status codes), state management (statelessness vs. state persistence via Cookies and JWTs), modern API design paradigms (decoupling, microservices, and Open Banking case studies), Cross-Origin Resource Sharing (CORS), and modern API security mechanisms (HTTPS, OAuth 2.0, and Rate Limiting).

- **Part 2: API Implementation & Integration Testing with Postman** — Demonstrates the practical application of these principles through the execution and validation of the Triangle Classifier API. This includes establishing Postman test collections, configuring dynamic environment variables (`{{url}}`), executing 8 distinct integration test requests (covering GET/POST routes, success scenarios, and edge-case error handling), and analyzing stateless server dynamics versus client-side state persistence.

---

## PART 1: Foundations of HTTP, API Architectures, and Modern Web Integration

### 1. Executive Summary

This report provides a comprehensive overview of the Hypertext Transfer Protocol (HTTP), modern Application Programming Interface (API) design, security frameworks, and cross-origin communication policies. Understanding these foundational internet mechanics is critical for engineering scalable, secure, and interoperable modern web applications.

---

### 2. HTTP Architecture & Core Functionality

#### 2.1 The Client-Server Model

The World Wide Web operates fundamentally on a distributed, collaborative client-server architecture using HTTP. Communication is directional and structured:

- **Clients:** End-user applications—primarily web browsers or mobile clients—that initiate communication by generating upstream requests.
- **Servers:** Computational nodes that listen for incoming requests, process business logic, and transmit downstream responses containing the requested resources.

#### 2.2 Anatomical Structure of HTTP Messages

Both HTTP requests and responses adhere to a strict structural delineation divided into two primary segments:

```
+-------------------------------------------------------+
|  Start Line (HTTP Method/Status + Target/Protocol)   |
+-------------------------------------------------------+
|  Headers (Metadata: Content-Type, Auth, Caching)     |
+-------------------------------------------------------+
|                                                       |
|  Message Body (Payload: JSON, HTML, Binary Data)     |
|                                                       |
+-------------------------------------------------------+
```

- **Headers:** Key-value pairs containing vital metadata. They instruct the recipient on how to handle the connection, identify the data format (`Content-Type`), pass authorization tokens, or define caching parameters.
- **Body:** The core data payload. In requests, this typically contains form data or JSON configurations to be saved. In responses, it carries the requested asset, such as an HTML file, an image binary, or raw data string text.

---

### 3. Communication Protocols: Methods and Status Codes

#### 3.1 HTTP Verbs (Methods)

HTTP verbs define the semantic intent of an operation being executed against a specific Uniform Resource Identifier (URI). Modern architectures map these directly to Create, Read, Update, and Delete (CRUD) database transactions.

| HTTP Verb | Operation Target | Idempotent | Description |
|-----------|-----------------|------------|-------------|
| GET       | Read            | Yes        | Retrieves data from the server without altering its persistent state. |
| POST      | Create          | No         | Submits data payloads to create a new resource entity on the server. |
| PUT       | Update          | Yes        | Replaces an entire target resource with an updated payload. |
| DELETE    | Delete          | Yes        | Destroys the specified resource on the target server. |

#### 3.2 Categorization of HTTP Status Codes

Servers reply with standardized three-digit integers to definitively convey the success or failure status of an inbound request.

- **1 Informational:** Handshake or protocol status updates (e.g., `101 Switching Protocols`).
- **2 Success:** The action was successfully received, understood, and accepted (e.g., `200 OK`, `201 Created`).
- **3 Redirection:** The client must take additional action to resolve the requested resource location (e.g., `301 Moved Permanently`).
- **4 Client Error:** Indicates an issue originating from the client, such as invalid syntax or missing permissions (e.g., `401 Unauthorized`, `404 Not Found`).
- **5 Server Error:** Indicates the client issued a structurally valid request, but the server encountered an internal failure (e.g., `500 Internal Server Error`, `503 Service Unavailable`).

---

### 4. State Management and Protocol Characteristics

#### 4.1 The Stateless Nature of HTTP

By design, HTTP is a stateless protocol. The server treats each received request completely independently and retains zero contextual memory or transactional data regarding previous requests from that specific client.

#### 4.2 State Persistence Mechanisms

Because complex workflows (such as e-commerce shopping carts or secure user sessions) require continuity, developers bypass stateless design limitations using external management state layers embedded within the HTTP headers:

- **Cookies:** Small data packages generated by the server, saved locally by the browser, and sent back automatically with every subsequent request.
- **Session Storage:** Server-side files mapped to a unique temporary ID sent to the client.
- **JSON Web Tokens (JWT):** Cryptographically signed, self-contained strings passed inside the HTTP `Authorization` header to verify client identity on every request.

---

### 5. APIs in Modern System Architectures

#### 5.1 System Decoupling and the Role of APIs

Application Programming Interfaces (APIs) serve as the structural abstraction layers that allow disparate software programs to communicate. Modern software design leverages APIs to isolate frontend consumer interfaces from backend data-layer operations. This enables microservice architectures, where autonomous services can scale, fail, and update independently without breaking monolithic dependencies.

#### 5.2 Open APIs and Ecosystem Growth

An Open API (publicly exposed API) features published endpoints accessible to external developers. They drive digital transformation by eliminating redundant code creation and allowing companies to monetize core functionalities as third-party services.

#### 5.3 Modern Application Case Study: Open Banking

Open APIs have fundamentally restructured international financial ecosystems through frameworks like Open Banking.

- **Application Implementation:** Digital budgeting applications securely consolidate client asset metrics directly from independent financial providers without handling sensitive master credentials.
- **Functional Integration:** When a user authorizes access, the aggregator app makes an authenticated REST call to the financial institution's Open API architecture.
- **Security Outcome:** The bank validates the token and outputs transactional metadata over a secure channel. The client's banking passwords remain fully ring-fenced within the home bank's native environment.

---

### 6. Cross-Origin Resource Sharing (CORS)

#### 6.1 The Same-Origin Policy (SOP) Constraint

To protect users from malicious script operations, modern web browsers enforce the Same-Origin Policy. This baseline defense restricts scripts running in a browser tab from fetching resources or posting payloads to an entirely different domain, port, or protocol.

#### 6.2 The CORS Resolution Framework

Cross-Origin Resource Sharing (CORS) is a system configuration that allows servers to selectively bypass SOP restrictions.

```
[ Client Browser ] --- 1. Preflight OPTIONS ---> [ External Server ]
[                ] <-- 2. Allow-Origin Header -- [                 ]
[                ]
[ Client Browser ] --- 3. Actual HTTP Request --> [ External Server ]
```

When a cross-origin script attempts an insecure method (like a POST or PUT request), the browser intercepts the transaction and sends a pre-flight `OPTIONS` request to the target host. The target server must return explicit `Access-Control-Allow-Origin` headers declaring that the requesting domain has permission to interact with its endpoints. If these headers are missing, the browser blocks the execution.

---

### 7. API Security Mechanisms and Access Protocols

To maintain confidentiality, integrity, and availability, production-grade APIs utilize multi-layered defense frameworks:

- **Transport Layer Security (HTTPS):** Encrypts the entire HTTP data stream in transit, protecting headers, methods, and payloads from man-in-the-middle interception.
- **API Keys:** Unique identification strings passed in the URI or headers to track usage and authenticate the requesting system.
- **OAuth 2.0 Framework:** An authorization framework that issues short-lived, permission-scoped tokens. This permits third-party applications to interact with resources without exposing core user authentication profiles.
- **Rate Limiting (Throttling):** Defends backend database clusters against denial-of-service (DoS) vectors by dropping traffic that exceeds structural volume thresholds (e.g., maximum 100 requests per minute per IP address).
- **Access Requirements:** To integrate with a secure API, a developer must enroll in the provider's management console, generate an encrypted client identity, and programmatically attach that asset to the outbound HTTP request header payload (typically structured as `Authorization: Bearer <token>`).

---

### 8. Public Data Repositories

The following public Open APIs provide structured, live data configurations for integration testing and product development:

| API | Description |
|-----|-------------|
| **OpenWeatherMap API** | Supplies global, real-time meteorological metrics, localized temperatures, and historical climate analytics. |
| **NASA Open APIs** | Offers programmatic access to celestial data pipelines, satellite imaging telemetry, and planetary exploration datasets. |
| **GitHub REST API** | Exposes version-control infrastructure data, public repository states, and code contribution metrics. |
| **REST Countries API** | Delivers comprehensive structural information regarding global geopolitical territories, currencies, and languages. |
| **JSONPlaceholder API** | Serves as a zero-auth, simulated database endpoint delivering mock JSON structures for prototyping client interfaces. |

---

### 9. References

- Open API Financial Architecture Frameworks. FPT AI Factory Systems. Available at: (https://fpt.ai)
- Modern Rest API Registries and Public Infrastructure. CodeFile Developers Portal. Available at: coderfile.io
- Open-Source API Ecosystems. ApiScout Architecture Guides. Available at: apiscout.dev

---

## PART 2: Triangle Classifier API

**Base URL:** `/api`

---

[Click To Open Triangle Classifier API](https://triangle-classifier.replit.app)

---

### Endpoints

#### `POST /api/triangle/classify`

Submit three side lengths, get back validity and type.

**Request body:**

```json
{ "a": 3, "b": 4, "c": 5 }
```

**Success response (200):**

```json
{ "valid": true, "type": "scalene", "sides": { "a": 3, "b": 4, "c": 5 } }
```

**Error response (400):**

```json
{ "valid": false, "error": "INVALID_SIDE", "message": "Side a must be greater than zero (got 0)." }
```

| Error Code       | Meaning                                  |
|------------------|------------------------------------------|
| `INVALID_SIDE`   | A side is zero or negative               |
| `INVALID_TRIANGLE` | Sides fail the triangle inequality     |
| `INVALID_INPUT`  | Missing side or non-numeric value        |

---

#### `GET /api/triangle/types`

Returns the three triangle type definitions with examples.

**Response (200):**

```json
{
  "types": [
    { "type": "equilateral", "description": "All three sides are equal.", "example": { "a": 5, "b": 5, "c": 5 } },
    { "type": "isosceles",   "description": "Exactly two sides are equal.", "example": { "a": 5, "b": 5, "c": 8 } },
    { "type": "scalene",     "description": "All three sides are different.", "example": { "a": 3, "b": 4, "c": 5 } }
  ]
}
```

---

### Test it with curl

```bash
# Classify a triangle
curl -X POST /api/triangle/classify \
  -H "Content-Type: application/json" \
  -d '{"a": 3, "b": 4, "c": 5}'

# List triangle types
curl /api/triangle/types
```

---

### Postman Implementation

The implementation is covered across two video clips:

**Video 1:**
1. Create a collection
2. Create a test GET request to perform a listing of the items in a database
3. Create an Environment for your Collection
4. Refactor the request to include environment variables for the base URL (`{{url}}`)

To download the video clip 

[Open This Link](https://github.com/Emad-Regis/Emad_MSSE640/blob/Emad-Regis-patch-1/Assignments/Images/Project_2_Postman/M1_P2.mp4)

Click Raw (or Download)


![Make_collection](/Assignments/Images/Project_2_Postman/Create_Collections.png)


Fig1: Create Collection 

![Make_Env](/Assignments/Images/Project_2_Postman/Create_Env.png)

Fig2: Create Environment

**Video 2:**
1. Create 7 additional requests including GET requests and at least one POST request

To download the video clip

[Open This Link](https://github.com/Emad-Regis/Emad_MSSE640/blob/Emad-Regis-patch-1/Assignments/Images/Project_2_Postman/M2_P2.mp4)

Click Raw (or Download)

![Clarify](/Assignments/Images/Project_2_Postman/Clarify.png)

Fig3: Triangle Clarify 

---

### Explanation

#### 1. No Data Persisted in This API

**The API is stateless.**

The `POST /api/triangle/classify` endpoint does one thing: it receives three side lengths, runs the classification logic, and returns a result. There is no database, no file storage, and no in-memory store anywhere in the server code. Once the response is sent, nothing is saved.

**There are no Update or Delete operations.**

The API only exposes two triangle-related endpoints:

| Method | Path                      | Operation                         |
|--------|---------------------------|-----------------------------------|
| POST   | `/api/triangle/classify`  | Classify (compute and return)     |
| GET    | `/api/triangle/types`     | Read static definitions           |

There are no PUT, PATCH, or DELETE routes — so Update and Delete don't exist at all. The `GET /types` endpoint returns hardcoded data baked directly into the route handler, not data fetched from storage.

**What actually happens on each POST:**

```
Request arrives → validate sides → classify → return JSON → done
```

Every request is independent. The server holds no memory of previous requests. If you classify `3, 4, 5` a hundred times, the API processes each one fresh with no record of any prior call.

**Where history does live:**

The last-5 classifications shown in the web UI are stored in React component state (`useState`) in the browser — client-side only. They disappear on page refresh and are never sent back to the server.

**Summary:**

| CRUD Operation          | Supported? | Persisted?                         |
|-------------------------|------------|------------------------------------|
| Create (POST classify)  | ✅         | ❌ No — result returned, nothing saved |
| Retrieve (GET types)    | ✅         | N/A — static, hardcoded            |
| Update                  | ❌ No endpoint | ❌                             |
| Delete                  | ❌ No endpoint | ❌                             |

---

#### 2. Data Returned for the Requests

**✅ Success — Equilateral**

```
POST /api/triangle/classify
Body: { "a": 5, "b": 5, "c": 5 }
```

```json
{
  "valid": true,
  "type": "equilateral",
  "sides": { "a": 5, "b": 5, "c": 5 }
}
```

---

**✅ Success — Isosceles**

```
POST /api/triangle/classify
Body: { "a": 5, "b": 5, "c": 8 }
```

```json
{
  "valid": true,
  "type": "isosceles",
  "sides": { "a": 5, "b": 5, "c": 8 }
}
```

---

**✅ Success — Scalene**

```
POST /api/triangle/classify
Body: { "a": 3, "b": 4, "c": 5 }
```

```json
{
  "valid": true,
  "type": "scalene",
  "sides": { "a": 3, "b": 4, "c": 5 }
}
```

---

**❌ Error — Zero side (`INVALID_SIDE`)**

```
POST /api/triangle/classify
Body: { "a": 0, "b": 4, "c": 5 }
```

```json
{
  "valid": false,
  "error": "INVALID_SIDE",
  "message": "Side a must be greater than zero (got 0)."
}
```

---

**❌ Error — Triangle inequality violated (`INVALID_TRIANGLE`)**

```
POST /api/triangle/classify
Body: { "a": 1, "b": 2, "c": 10 }
```

```json
{
  "valid": false,
  "error": "INVALID_TRIANGLE",
  "message": "Sides 1, 2, 10 do not satisfy the triangle inequality (the sum of any two sides must exceed the third)."
}
```

---

**❌ Error — Missing field (`INVALID_INPUT`)**

```
POST /api/triangle/classify
Body: { "a": 3, "b": 4 }
```

```json
{
  "valid": false,
  "error": "INVALID_INPUT",
  "message": "Request body must include sides a, b, and c."
}
```

---

**📖 Reference — `GET /api/triangle/types`**

```json
{
  "types": [
    { "type": "equilateral", "description": "All three sides are equal.",      "example": { "a": 5, "b": 5, "c": 5 } },
    { "type": "isosceles",   "description": "Exactly two sides are equal.",    "example": { "a": 5, "b": 5, "c": 8 } },
    { "type": "scalene",     "description": "All three sides are different.",  "example": { "a": 3, "b": 4, "c": 5 } }
  ]
}
```

---

**💓 Health — `GET /api/healthz`**

```json
{ "status": "ok" }
```

---

All eight responses above were captured live from the running server. Every success response includes `valid: true`, the triangle type, and the original sides echoed back. Every error response includes `valid: false`, a machine-readable error code, and a human-readable message.

---

## Project Conclusion

This project successfully demonstrated how core network protocol principles directly govern modern API design, software integration, and quality assurance workflows. By pairing theoretical analysis with practical hands-on testing in Postman, the report established a complete end-to-end framework for evaluating web service behavior.

Key takeaways and engineering insights from this project include:

- **Protocol & Architecture Mastery:** HTTP serves as the foundational protocol for distributed modern systems. Its inherently stateless architecture provides high scalability, while localized state mechanisms (such as JWTs and cookies) allow applications to maintain session context securely without compromising backend design.

- **Robust Security & Interoperability:** Adopting multi-layered security frameworks—including HTTPS encryption, OAuth 2.0 token authorization, rate limiting, and CORS headers—is critical for shielding microservices against unauthorized access and cross-origin exploit vectors while facilitating seamless ecosystem integration.

- **Practical Integration Testing & Verification:** Through the hands-on testing of the Triangle Classifier API using Postman, the importance of deterministic, stateless request processing was validated. Leveraging Postman collections and dynamic environment variables (`{{url}}`) enabled automated, repeatable test workflows across multiple functional endpoints.

- **Defensive Error Handling & API Contracts:** Verifying explicit HTTP response statuses (`200 OK` for successful equilateral, isosceles, and scalene classifications; `400 Bad Request` for invalid side lengths, triangle inequality violations, or missing parameters) highlighted the importance of standardizing error payloads. Clear machine-readable error codes and human-readable messages foster seamless integration between frontend consumer applications and backend microservices.

In conclusion, synthesizing theoretical web architecture principles with rigorous, automated integration testing ensures the delivery of high-quality, resilient, and secure software applications capable of operating effectively in enterprise microservice environments.
