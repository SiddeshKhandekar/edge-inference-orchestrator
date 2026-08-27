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

**Boundary Structure: Single Region VPC with Four Isolated Subnets**
The deployment utilizes one primary Virtual Private Cloud (VPC) (10.0.0.0/16) logically segmented into exactly four dedicated subnets constraints natively:
*   **Zone-A Subnet:** `10.0.1.0/24`
*   **Zone-B Subnet:** `10.0.2.0/24`
*   **Zone-C Subnet:** `10.0.3.0/24`
*   **Central Platform Compute Subnet:** `10.0.100.0/24` (Hosts the Part 1 Engine)

**Cross-Zone Enforcement Mechanism:**
To enforce hard-bound protection safely, strict **Network Access Control Lists (NACLs)** and Security Group rules functionally block direct inter-zone lateral routing (`10.0.1.0/24` ↔ `10.0.2.0/24` ↔ `10.0.3.0/24`). Zone controllers communicate purely northbound with `10.0.100.0/24`, effectively guaranteeing compute data never travels peer-to-peer.

---

## 3. Network Security Controls (Task 11)

*   **Protect Sensitive Data:** Employs **AES-256 (GCM mode)** encryption with managed customer keys for persistent storage, natively protecting archived sensor telemetry.
*   **Authentication:** Enforces strict **mTLS (Mutual TLS)** using X.509 device certificates to systematically authenticate IoT zone controllers before they can connect to the MQTT broker.
*   **Authorization:** Applies absolute zero-trust **IAM Roles and Policies** to strictly define which API routes an Edge node can uniquely trigger.
*   **Prevent Cyber Attacks:** Leverages a robust **Cloud WAF with AWS Shield DDoS mitigation** and strict rate-limiting at API gateways preventing overload crashes.
*   **Secure Communication:** Encapsulates all in-flight network packets utilizing **TLS 1.3** to securely transmit the real-time public-safety telemetry without mid-stream exposure.
*   **Ensure Availability:** Implements **Auto-Scaling Groups over Multi-AZ clusters** natively, assuring that if a primary cloud component crashes, a redundant instance immediately assumes the load without dropping critical alerts.

---

## 4. IAM & Data Protection (Task 12)

**IAM Role Table:**

| Role Name | Precision Permission Set |
| :--- | :--- |
| **CityDashboardAdminRole** | Total wildcard access to the overarching Cloud Dashboard metrics, configuring Edge Fleet platform deployment routines automatically. |
| **ZoneOperatorRole** | Scoped write-access inherently localized to publish sensor metrics and remotely execute the internal `schedulers.py` compute engine within strict subnets. |
| **ComplianceAuditorRole** | Strict logical read-only access uniquely targeting archiving buckets (S3) and historical telemetry logs to actively inspect platform regulatory vectors. |

**Data Protection Matrix (Data States):**

*   **At Rest:** Protected via **AWS KMS (AES-256)** encryption keys implicitly guarding the `JOBS` dataset and stationary zone-generated sensor logs sitting archived in the cloud storage buckets.
*   **In Transit:** Protected via **TLS 1.3 (Perfect Forward Secrecy)** rigorously encrypting the live hypothetical Banker's Algorithm resource requests transmitted between the isolated zone gateway and the dashboard backend.
*   **In Use:** Protected via **Confidential Computing Enclaves (AWS Nitro)** that securely execute the rigorous `synchronization.py` race-condition OS mathematical computations inside fundamentally isolated, tamper-proof hardware RAM blocks.

---

## 5. IoT Connectivity & Layers (Task 13)

**Sensor & Connectivity Mapping:**
1.  **Traffic-Camera Triggers:** Utilizes **5G**. High bandwidth and ultra-low latency are strictly required to stream high-throughput visual trigger arrays instantly.
2.  **Environmental Air-Quality Sensors:** Utilizes **LoRaWAN**. These sensors send tiny, infrequent byte-sized logs across a massively wide geographic city range natively on low-power batteries for years.
3.  **Wearable Public-Safety Badges (Police/Medical):** Utilizes **NB-IoT / LTE-M**. It provides resilient urban cellular penetration, mobility handovers, and remarkably low power consumption anywhere identically in the metropolitan grid.

**IoT Architecture Stack Mapping:**
*   **Physical Environment:** The physical city intersections, atmosphere conditions, and emergency scenarios.
*   **Perception/Device Layer:** The physical networking appliances (traffic cameras, air-quality monitors, and Wearable cellular beacons).
*   **Gateway Layer:** Ruggedized intersection switchboxes serving as edge MQTT gateways natively translating Edge signals into structured TCP/IP internet packets.
*   **Network Communication Layer:** Connecting via 5G towers and localized Fiber networks navigating the encrypted unified VPC topology mathematically.
*   **Cloud Platform Layer:** **The Part 1 OS engine (running `schedulers.py`, `bankers.py`, etc.)** acting as the central intelligence allocating core compute resources dynamically.
*   **Application Layer:** The centralized Smart City Operations dashboard presenting real-time UI alerts and visual logic to the administrative human operator.

---

## 6. Threats and Mitigations (Task 14)

**Cyber-Threat Modeling:**
1.  **Rogue Gateway Impersonation (IoT Layer):** Hackers theoretically attempt to flood the gateway with spoofed traffic camera triggers to artificially overload the `JOBS` dataset queue.
    *   *Mitigation:* Hardware Security Modules (HSM) rigidly enforcing X.509 client certificates and mTLS natively; the broker instantly rejects any telemetry missing a cryptographically signed hardware identity token.
2.  **Resource Starvation / DoS Attack (Compute Engine Schedulers):** Attackers explicitly inject malicious burst requests artificially triggering CPU starvation inside the central zone logic arrays.
    *   *Mitigation:* Deployment of strict token-bucket API rate-limiting natively tied directly with the Banker's Algorithm admission control checking explicitly alongside dynamic priority aging logic buffering out excessive overloads sequentially.
3.  **Telemetry Interception & Tampering (Network Layer):** Intercepting the public-safety alerts over public ISP nodes identically using MitM injections to essentially corrupt payload metrics passively.
    *   *Mitigation:* Absolute enforcement of TLS 1.3 tunneling rigorously protecting all egress TCP payload traffic natively verified by fundamental payload packet analysis checking natively on arrival.
