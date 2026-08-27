"""
main.py
Master Orchestration CLI Runner recursively executing Tasks 2-7 natively for production checks.
"""
from schedulers import fcfs, sjf, srtf, round_robin, priority_sched, summarize
from jobs import JOBS
import synchronization as sync
import bankers
import memory_mgmt as mem

def run_part_1():
    print("============= STARTING OS EDGE INFERENCE ENGINE =============")
    
    print("\n[Executing Core Hardware Provisioning Algorithms]")
    summarize("FCFS", fcfs(JOBS))
    summarize("SJF (Non-Preemptive)", sjf(JOBS))
    summarize("SRTF (Preemptive)", srtf(JOBS))
    
    rr3, sw3 = round_robin(JOBS, 3)
    summarize("Round Robin (Quantum=3)", rr3)
    print(f"-> Verified Context Switches: {sw3}")
    
    rr6, sw6 = round_robin(JOBS, 6)
    summarize("Round Robin (Quantum=6)", rr6)
    print(f"-> Verified Context Switches: {sw6}")
    
    print("\n[Executing Priority & Starvation Matrix]")
    summarize("Priority (No Aging Simulator)", priority_sched(JOBS, False))
    summarize("Priority (Dynamic Aging Execution)", priority_sched(JOBS, True))
    
    print("\n[Executing OS Race-Condition Diagnostics]")
    print(f"Untethered Mutex Collisions: {sync.execute_unsync()}")
    print(f"Peterson Cryptographic Mutex: {sync.execute_peterson()}")
    
    print("\n[Executing Banker's Edge Safety Module]")
    need = bankers.compute_need(bankers.MAX_NEED, bankers.ALLOCATION)
    print("Hypothesis A [1,0,2]:", bankers.evaluate_request("P1", [1,0,2], bankers.AVAILABLE, bankers.ALLOCATION, need)[1])
    print("Hypothesis B [2,0,2]:", bankers.evaluate_request("P0", [2,0,2], bankers.AVAILABLE, bankers.ALLOCATION, need)[1])

    print("\n[Executing Address MMU Translation Engine]")
    print(mem.translate_page(3000))
    print(mem.translate_page(5000))
    print(mem.translate_segment((1, 350)))

if __name__ == "__main__":
    run_part_1()
