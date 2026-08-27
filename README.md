# Edge Inference Orchestrator

This repository encompasses a deterministic edge compute engine and a comprehensive enterprise Cloud-IoT deployment blueprint. Built as an OS Simulation and Cloud Architecture deployment modeling suite.

Included inherently are:
- `docs/architecture_blueprint.md` (Part 2 Cloud Design Document)
- The Python Compute Engine natively spanning Scheduling, Mutex synchronization, Deadlock modeling, and Memory translation boundaries.

This project was built for the course I pursued from Masai in collaboration of IIT Mandi for the domain **Software Development 2.0** as the **Final Project**

---

## How to Execute the Engine
This OS simulation requires **zero external dependencies** and naturally runs entirely on Python's Standard Library. It is broken structurally into localized independent execution scripts.

To natively execute the computations, open a terminal in the repository root and selectively run the Python files:

1. `python schedulers.py` 
   - *Expectation:* Outputs detailed tracking tables for First-Come First-Serve (FCFS), Shortest Job First (SJF/SRTF), Round Robin overhead switching (Quantums 3 and 6), and Priority Starvation (With and Without Aging). Automatically logs metric benchmarks proving PRD assertion alignments exactly.
2. `python synchronization.py` 
   - *Expectation:* Fires up native multithreaded workers explicitly demonstrating a fundamental OS Race Condition continuously failing to arrive at a target value (85). It is then followed sequentially by a hardened Peterson's Mutual Exclusion lock algorithm explicitly guaranteeing deterministic cross-thread safety.
3. `python bankers.py` 
   - *Expectation:* Statically defines state conditions to natively compute the dynamic Need Matrix and execute the Banker's Algorithm limit constraint. Demonstrates successful traversal generating a Safe Sequence globally, while independently denying unsafe hypothetical resource limit breaches to aggressively avoid deadlocks.
4. `python memory_mgmt.py` 
   - *Expectation:* Conducts Logical-to-Physical translation mechanics explicitly enforcing rigorous Bounds Checking thresholds. You will see raw physical overrides natively intercepted for missing mapping keys triggering `PAGE FAULT` exceptions natively, as well as strict `SEGMENTATION FAULT` triggers when processing vectors exceed base limit thresholds mathematically.

---

## Production Deployment Choice: Strategy Justification (Task 8)

Based exclusively on rigid empirical measurements modeled definitively within `schedulers.py`, the **SJF / SRTF Algorithm Family** is proactively chosen as the absolute optimal scheduling architecture for this explicit array of specific zone-controller jobs. 

**Why SJF/SRTF Wins for the Architecture:** 
In an Edge-IoT framework managing deterministic safety telemetry (e.g., traffic triggers), latency determines viability. Computationally simulating the jobs demonstrated that SRTF explicitly delivered the lowest absolute Average Waiting Time natively allowing high-burst telemetry limits to parse and execute instantly compared to generalized sequence modeling.

**Why the other 3 Families were definitively rejected for this explicit workload:**
1. **FCFS (First-Come, First-Served):** Highly unsuitable due to critical convoy throttling hazards across edge boundaries. Our localized engine definitively measured that FCFS resulted in a severely bloated Average Waiting Time of roughly **11.50 engine ticks** natively—which is mathematically double the drag generated under SRTF logic. Allowing deeply exhaustive jobs to stall processors categorically limits sub-second critical IoT processing limits natively.
 
2. **Round Robin (RR):** Proved drastically inefficient dynamically enforcing artificial bounds specifically for deterministic zone controllers. Our mathematical engine explicitly counted forced context rotational swapping measuring up to **17 strict switches natively** rotating exclusively under Quantum 3 conditions. A localized edge network node inherently processing battery limitations wastes continuous massive OS cyclic energy routinely ripping uncompleted payloads purely rather than letting them naturally resolve limits algorithmically. 

3. **Priority Scheduling:** Actively rejected natively due to massive starvation limitations exclusively on low-tier logging routines (e.g., environmental background tracking routines). Our simulator effectively proved that unequivocally devoid of embedded dynamic priority incrementing (Aging), a solitary low-tier baseline process definitively decayed for **29 strict metric ticks internally**—provoking hazardous software timeout overruns inherently.

---


## Future additions after Masai revaluation:

## AI Context: Edge Inference Workloads
While the core engine demonstrates fundamental OS algorithms, the practical application is orchestrating varying **Edge AI processing jobs**. 

* **Prioritization:** The algorithms dynamically allocate CPU cycles between critical Neural Network tasks (e.g., running real-time Computer Vision inferences like YOLOv8 on traffic-camera feeds to detect accidents) and low-priority tasks (e.g., routine environmental aggregations).
  
* **Data Engineering Pipeline:** The architectural pipeline ensures all localized telemetry and sensor archives are securely piped back to centralized Cloud Data Lakes (AWS S3) synchronously. This establishes a continuous feedback loop, providing massive datasets for training next-generation ML models centrally before deploying them back to the edge.


## Software Engineering & MLOps Strategy
To maintain this orchestration engine across a fleet of global Smart City zones, standard DevOps and MLOps practices are theoretically enforced:

* **CI/CD Pipelines:** Future iterations of this compute engine (or the AI models running on it) would be deployed via continuous integration pipelines (e.g., GitHub Actions), executing automated unit tests against the Banker's Algorithm thresholds prior to pushing Over-The-Air (OTA) updates to remote Edge nodes.

* **Infrastructure as Code (IaC):** The VPC-based isolation boundaries and IAM Zero-Trust roles detailed in Part 2 are designed to be entirely automatable using IaC tools like Terraform or AWS CloudFormation, ensuring strictly reproducible platform deployments.


## Deadlock Avoidance in Deep Learning Contexts
The Banker's Algorithm implemented in [bankers.py](cci:7://file:///e:/College/Projects/edge-inference-orchestrator-main/bankers.py:0:0-0:0) currently models standard OS resources (Compute, Networking, Storage). However, strategically, this mechanism is paramount for avoiding deadlocks when concurrently allocating highly limited **Hardware AI Accelerators (Edge TPUs / GPUs)** across concurrent inference threads. Ensuring a secure validation matrix guarantees our visual inference streams never completely lock up the gateway’s graphical memory constraints.
