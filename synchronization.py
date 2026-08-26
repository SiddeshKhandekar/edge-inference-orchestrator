"""
synchronization.py

Demonstrates highly-optimized native multithreading race conditions 
and strictly resolves them using Peterson's mutual exclusion algorithm.
"""

import threading
import time

# Shared data context
unsync_counter = 100
peterson_counter = 100

# Peterson's lock management variables
flag = [False, False]
turn = 0

def work_unsync(is_consumer):
    """Execution unit mimicking OS reads without resource locks."""
    global unsync_counter
    local_val = unsync_counter
    time.sleep(0.01) # Force preemption probability
    unsync_counter = local_val - 40 if is_consumer else local_val + 25

def execute_unsync():
    """Triggers overlapping thread execution unconditionally."""
    global unsync_counter
    results = []
    print("\n--- Unsynchronized Runs (Target Value: 85) ---")
    
    for i in range(5):
        unsync_counter = 100
        t0 = threading.Thread(target=work_unsync, args=(True,))
        t1 = threading.Thread(target=work_unsync, args=(False,))
        
        t0.start()
        t1.start()
        
        t0.join()
        t1.join()
        
        flag_status = "[RACE CONDITION: CORRUPTED]" if unsync_counter != 85 else ""
        print(f"Run {i+1}: Output = {unsync_counter} {flag_status}")
        results.append(unsync_counter)
        
    return results

def work_peterson(thread_id, is_consumer):
    """Enforces Peterson's mutual exclusion algorithm across shared states."""
    global peterson_counter, flag, turn
    other = 1 - thread_id
    
    # 1. Entry Section
    flag[thread_id] = True
    turn = other
    while flag[other] and turn == other:
        # Simulating CPU yielding while locked out
        time.sleep(0.0001) 
        
    # 2. Critical Section
    local_val = peterson_counter
    time.sleep(0.01) # Force preemption risk directly inside the protected boundary
    peterson_counter = local_val - 40 if is_consumer else local_val + 25
        
    # 3. Exit Section
    flag[thread_id] = False

def execute_peterson():
    """Ensures deterministic thread execution resolving the race hazard."""
    global peterson_counter, flag, turn
    results = []
    print("\n--- Peterson's Algorithm Protection (Target Value: 85) ---")
    
    for i in range(5):
        peterson_counter = 100
        flag = [False, False] # Strict boundary reset
        turn = 0
        
        t0 = threading.Thread(target=work_peterson, args=(0, True))
        t1 = threading.Thread(target=work_peterson, args=(1, False))
        
        t0.start()
        t1.start()
        
        t0.join()
        t1.join()
        
        flag_status = "[SAFE]" if peterson_counter == 85 else "[FAILED YIELD]"
        print(f"Run {i+1}: Output = {peterson_counter} {flag_status}")
        results.append(peterson_counter)
        
    return results

if __name__ == "__main__":
    runs_us = execute_unsync()
    runs_p = execute_peterson()
    
    print("\n--- Validation Acceptance ---")
    # Verify mathematically that the unsynced failed at least once, and peterson succeeded strictly 
    has_corruption = any(value != 85 for value in runs_us)
    is_hardened = all(value == 85 for value in runs_p)
    
    if has_corruption and is_hardened:
        print("[SUCCESS] Verified OS Race Condition Vulnerability & Patched Successfully via Peterson's Logic.")
    else:
        print("[FAILED!] Mathematical failure outside expected boundaries.")
