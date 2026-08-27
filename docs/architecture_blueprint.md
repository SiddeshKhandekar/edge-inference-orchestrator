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
