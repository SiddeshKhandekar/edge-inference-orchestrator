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

1. **`python main.py`** 
   - *Expectation:* Acts as the global execution orchestrator. It sequentially unspools and logs deeply formatted terminal tables for all algorithms (FCFS, SJF, SRTF, Round Robin, Priority), fires up multithreaded Peterson Mutex tests, executes the Banker's deadlock safety matrices, and mathematically throws the MMU Address Translation boundaries automatically.
2. **`python -m unittest discover tests`** 
   - *Expectation:* Spins up the automated QA Testing Engine. It executes 7 strict unit tests rigorously validating the exact algorithmic outputs against the PRD requirements (e.g., verifying Round Robin strictly outputs 16 context switches at Q=3). Everything will mathematically output a successful `OK` natively.
3. **`python schedulers.py`** 
   - *Expectation:* Independently evaluates all CPU scheduling metrics. Outputs formatted tables for First-Come First-Serve (FCFS), Shortest Job First (SJF/SRTF), Round Robin context overhead tracking, and Priority CPU mapping.
4. **`python synchronization.py`** 
   - *Expectation:* Independently executes the OS concurrency demonstration. Validates Thread-0 / Thread-1 collision metrics and naturally restores synchronization safely using Peterson's strict boolean flags.
5. **`python bankers.py`** 
   - *Expectation:* Independently processes the static Edge Resource constraints. Models the Banker's safety loop to ensure deadlock-free evaluation paths for granting or natively denying hypothetical resource workloads.
6. **`python memory_mgmt.py`** 
   - *Expectation:* Independently computes Paging and Segmentation boundary limits natively, raising mathematically correct physical address resolutions alongside precise `PAGE FAULT` anomalies.

---

## Production Deployment Choice: Strategy Justification (Task 8)

Based exclusively on rigid empirical measurements modeled definitively within `schedulers.py`, the **SJF / SRTF Algorithm Family** is proactively chosen as the absolute optimal scheduling architecture for this explicit array of specific zone-controller jobs. 

**Why SJF/SRTF Wins for the Architecture:** 
In an Edge-IoT framework managing deterministic safety telemetry (e.g., traffic triggers), latency determines viability. Computationally simulating the jobs demonstrated that SRTF explicitly delivered the lowest absolute Average Waiting Time natively allowing high-burst telemetry limits to parse and execute instantly compared to generalized sequence modeling.

**Why the other 3 Families were definitively rejected for this explicit workload:**
1. **FCFS (First-Come, First-Served):** Highly unsuitable due to critical convoy throttling hazards across edge boundaries. Our terminal engine definitively measured that FCFS resulted in a severely bloated Average Waiting Time natively reaching up to **17.12 engine ticks**—which is mathematically destructive to efficiency parameters generated under SRTF logic. Allowing deeply exhaustive jobs to stall processors completely limits sub-second critical IoT processing limits natively.
 
2. **Round Robin (RR):** Proved drastically inefficient dynamically enforcing artificial bounds specifically for deterministic zone controllers. Our mathematical engine explicitly counted forced context rotational swapping measuring exactly **16 strict switches natively** rotating exclusively under Quantum 3 conditions. A localized edge network node inherently processing battery limitations wastes continuous massive OS cyclic energy routinely ripping uncompleted payloads rather than letting them naturally resolve limits algorithmically. 

3. **Priority Scheduling:** Actively rejected natively due to massive starvation limitations exclusively on low-tier logging routines (e.g., environmental background tracking routines). Our simulator effectively proved that unequivocally devoid of embedded dynamic priority incrementing (Aging), a solitary low-tier baseline process definitively decayed for **33 strict metric ticks internally**—provoking hazardous software timeout overruns inherently.

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
