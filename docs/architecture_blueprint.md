# Secure Cloud-IoT Deployment Blueprint

## 1. Distributed Architecture & Communication Plan (Task 9)

**Architecture Choice: Hybrid Architecture**
To securely coordinate the diverse zone controllers (which physically run the **Part 1 job scheduler and Banker's safety engine**) with a centralized Smart City Operations dashboard, a **Hybrid Architecture** is established. 
*   **Scalability:** Zone controllers can infinitely scale out their local sensor footprint without flooding the central cloud bottleneck.
*   **Fault Tolerance:** If the cloud dashboard experiences downtime, the localized OS simulation engine will persistently execute its FCFS/Priority routines internally without stalling.
*   **Single Point of Failure (SPOF):** The separation of data collection (Edge) and analytical visualization (Cloud) completely removes catastrophic SPOF constraints from critical safety workflows.

**Concrete Data Flow Protocols:**
*   **(a) Pushing Real-Time Public-Safety Alerts:** Handled **Asynchronously** utilizing **MQTT**. Safety alerts mandate ultra-low latency; asynchronous publish-subscribe functionality guarantees the zone controller does not stall while waiting for network packet acknowledgment in an emergency.
*   **(b) Uploading Full-Day Sensor Log Archivals:** Handled **Synchronously** utilizing **HTTPS (TCP)**. Log archives demand rigorous delivery verification. A synchronous protocol ensures the controller explicitly receives a robust HTTP 200 OK signal, guaranteeing exact data preservation before purging local drives.

---

## 2. VPC-Based Network Boundary Design (Task 10)

**Boundary Structure: Unified VPC with Tri-Subnet Isolation**
The deployment utilizes one primary Virtual Private Cloud (VPC) rigorously separated into precisely three segregated Private Subnets (Zone-A, Zone-B, and Zone-C). 
*   **Logical Isolation:** Implementing subnets mathematically isolates the broadcast domains. If Zone-C experiences a runaway process fault resulting in memory overflow, the virtual boundary isolates the crash entirely.
*   **Customizability:** A unified VPC allows administrators to attach a single centralized Internet Gateway, while heavily customizing localized Network Access Control Lists (NACLs) to strictly limit how specific zones interface with the web.

**Cross-Zone Enforcement Mechanism:**
To enforce hard-bound protection preventing Zone-A's resources from being reached by Zone-B seamlessly, a strict **Network Access Control List (NACL)** rule is implemented directly upon the subnet boundaries. This is not arbitrary firewall processing—it serves as a persistent, stateless boundary check blocking arbitrary inbound/outbound packets explicitly originating from the opposing Zone's designated IP CIDR blocks *before* traffic reaches the host.

---

## 3. Network Security Controls (Task 11)

*   **Protect Sensitive Data:** Employs **AES-256 encryption** with managed customer keys for persistent storage, natively protecting archived sensor telemetry logs at rest.
*   **Authentication:** Enforces strict **mTLS (Mutual TLS)** using X.509 device certificates to systematically authenticate IoT zone controllers before they can connect to the MQTT broker.
*   **Authorization:** Applies absolute zero-trust **IAM Roles and Policies** to strictly define which API routes an Edge node can uniquely trigger.
*   **Prevent Cyber Attacks:** Leverages a robust **Web Application Firewall (WAF)** at the edge network boundary to automatically filter and block malicious DDoS traffic or SQL injection attempts against the central dashboard.
*   **Secure Communication:** Encapsulates all in-flight network packets utilizing **TLS 1.3** to securely transmit the real-time public-safety telemetry without mid-stream exposure.
*   **Ensure Availability:** Implements **Auto-Scaling Groups over Multi-AZ clusters** natively, assuring that if a primary cloud component crashes, a redundant instance immediately assumes the load without dropping critical alerts.

---

## 4. IAM & Data Protection (Task 12)

**IAM Role Table:**

| Role Name | Precision Permission Set |
| :--- | :--- |
| **Smart City Administrator** | Total wildcard access (`*`) to the overarching Cloud Dashboard APIs and global Edge Fleet deployment configurations. |
| **Edge Zone Operator** | Scoped `WriteOnly` access strictly localized to publish sensor metrics and remotely execute the internal `schedulers.py` compute engine purely within their assigned isolated VPC Subnet limits. |
| **Compliance Auditor** | Strict `ReadOnly` access uniquely targeting archiving buckets (S3) and historical telemetry logs to actively inspect platform regulatory health without code-mutation rights. |

**Data Protection Matrix (Data States):**

*   **At Rest:** Protected via **AWS KMS (AES-256)** encryption keys implicitly guarding the `JOBS` dataset and stationary zone-generated sensor logs sitting archived in the cloud storage buckets.
*   **In Transit:** Protected via **TLS 1.3 (Perfect Forward Secrecy)** rigorously encrypting the live hypothetical Banker's Algorithm resource requests (e.g., `[2, 0, 2]`) transmitted between the isolated zone gateway and the dashboard backend.
*   **In Use:** Protected via **Confidential Computing Enclaves (AWS Nitro)** that securely execute the rigorous `synchronization.py` race-condition OS mathematical computations inside fundamentally isolated, tamper-proof hardware RAM blocks.

---

## 5. IoT Connectivity & Layers (Task 13)

**Sensor & Connectivity Mapping:**
1.  **Traffic-Camera Triggers:** Utilizes **5G**. High bandwidth and ultra-low latency are strictly required to stream high-throughput visual trigger arrays instantly.
2.  **Environmental Air-Quality Sensors:** Utilizes **LoRaWAN**. These sensors send tiny, infrequent byte-sized logs across a massively wide geographic city range while functioning natively on low-power batteries for years without maintenance.
3.  **Wearable Public-Safety Badges (Police/Medical):** Utilizes **Bluetooth (BLE)**. It strictly requires continuous, extremely low-power pairing to a localized vehicle or smartphone hub for localized telemetry tracking.

**IoT Architecture Stack Mapping:**
*   **Physical Environment:** The physical city intersections, atmosphere conditions, and emergency scenarios.
*   **Perception/Device Layer:** The physical networking appliances (traffic cameras, air-quality monitors, and BLE wearable badges).
*   **Gateway Layer:** Ruggedized intersection switchboxes serving as edge MQTT gateways natively translating LoRaWAN/BLE signals into TCP/IP internet packets.
*   **Network Communication Layer:** Connecting via 5G towers and localized Fiber networks navigating the encrypted unified VPC topology.
*   **Cloud Platform Layer:** **The Part 1 OS engine (running `schedulers.py`, `bankers.py`, etc.)** acting as the central intelligence allocating core compute resources.
*   **Application Layer:** The centralized Smart City Operations dashboard presenting real-time UI alerts and visual logic to the administrative human operator.

---

## 6. Threats and Mitigations (Task 14)

**Cyber-Threat Modeling:**
1.  **Data Spoofing / Sybil Attack (IoT Layer):** Hackers theoretically attempt to flood the gateway with spoofed traffic camera triggers to artificially overload the `JOBS` dataset queue.
    *   *Mitigation:* X.509 mTLS certificates definitively enforce mutual authentication natively; the broker instantly rejects any telemetry missing a cryptographically signed hardware certificate.
2.  **Man-in-the-Middle (MitM) Attacks (Network Layer):** Intercepting the public-safety alerts over public ISP nodes to steal or inherently corrupt the JSON payload instructions.
    *   *Mitigation:* Absolute enforcement of TLS 1.3 cipher tunnels on all egress TCP traffic preventing active packet sniffing and payload mutation in real-time.
3.  **Cross-Site Scripting / SQL Injection (Application Layer):** Attackers strictly targeting the Smart City dashboard login portals to execute malicious querying on the archived S3 logs.
    *   *Mitigation:* Deploying an AWS Web Application Firewall (WAF) to deeply pre-filter and rigorously parse malformed regex sequences before backend processing occurs.
