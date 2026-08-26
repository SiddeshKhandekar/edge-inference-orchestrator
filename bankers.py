"""
bankers.py

Implements Banker's Algorithm for deadlock avoidance.
Computes the Need matrix and evaluates resource request safety safely determining safe sequences.
"""
import copy

# Fixed state according to PRD constraints (R0: Compute, R1: Network, R2: Storage)
AVAILABLE = [3, 3, 2]
MAX_NEED = {"P0": [7, 5, 3], "P1": [3, 2, 2], "P2": [9, 0, 2], "P3": [2, 2, 2]}
ALLOCATION = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 2], "P3": [2, 1, 1]}
PROCESSES = ["P0", "P1", "P2", "P3"]

def compute_need(max_need, alloc):
    """Calculates Need matrix (Need = Max - Allocation)."""
    return {p: [max_need[p][i] - alloc[p][i] for i in range(3)] for p in PROCESSES}

def get_safe_sequence(avail, alloc, need):
    """Evaluates if the state is mathematically safe. Returns (is_safe, sequence_list)."""
    work = list(avail)
    finish = {p: False for p in PROCESSES}
    safe_seq = []
    
    while len(safe_seq) < len(PROCESSES):
        made_progress = False
        
        for p in PROCESSES:
            # If unfinished and its entire resource Need can be satisfied by current Work (Available)
            if not finish[p] and all(need[p][i] <= work[i] for i in range(3)):
                # Reclaim resources naturally (simulate it finishing)
                work = [work[i] + alloc[p][i] for i in range(3)]
                finish[p] = True
                safe_seq.append(p)
                made_progress = True
                
        # If we loop completely without completing a new process, we are deadlocked
        if not made_progress:
            break
            
    return len(safe_seq) == len(PROCESSES), safe_seq

def evaluate_request(p_id, request, og_avail, og_alloc, og_need):
    """Pre-evaluates a hypothetical request independently against the original platform state."""
    # Step 1. Validation bound check against declared Max Needs
    if not all(request[i] <= og_need[p_id][i] for i in range(3)):
        return False, "Denied: Request exceeds process declared max limits."
        
    # Step 2. Bound check against immediate availability
    if not all(request[i] <= og_avail[i] for i in range(3)):
        return False, "Denied: Required resources not currently available."
        
    # Step 3. Hypothesis testing (Simulate immediately granting request)
    test_avail = [og_avail[i] - request[i] for i in range(3)]
    test_alloc = copy.deepcopy(og_alloc)
    test_need = copy.deepcopy(og_need)
    
    for i in range(3):
        test_alloc[p_id][i] += request[i]
        test_need[p_id][i] -= request[i]
        
    # Step 4. Core Safety Check 
    is_safe, seq = get_safe_sequence(test_avail, test_alloc, test_need)
    
    if is_safe:
        return True, f"Granted: Resulting mathematical state is confirmed Safe. Execution Sequence: {' -> '.join(seq)}"
    else:
        return False, "Denied: Approving this exact request would inherently leave the system in an UNSAFE deadlocked state."

if __name__ == "__main__":
    need_matrix = compute_need(MAX_NEED, ALLOCATION)
    
    print("--- Need Matrix Computed ---")
    for p in PROCESSES:
        print(f"{p}: {need_matrix[p]}")
        
    print("\n--- Platform Initial State Evaluation ---")
    is_safe, init_seq = get_safe_sequence(AVAILABLE, ALLOCATION, need_matrix)
    print(f"Is Safe Globally? {'YES' if is_safe else 'NO'}")
    if is_safe:
        print(f"Valid Safe Sequence Found: {' -> '.join(init_seq)}")
        
    print("\n--- Independent Request Action Evaluations ---")
    
    # Requirement Request A: P1 requests [1, 0, 2]
    req_a, p_a = [1, 0, 2], "P1"
    print(f"Evaluating {p_a} Requesting {req_a}...")
    success_a, msg_a = evaluate_request(p_a, req_a, AVAILABLE, ALLOCATION, need_matrix)
    print(f"Result: {msg_a}")
    
    # Requirement Request B: P0 requests [2, 0, 2]
    req_b, p_b = [2, 0, 2], "P0"
    print(f"\nEvaluating {p_b} Requesting {req_b}...")
    success_b, msg_b = evaluate_request(p_b, req_b, AVAILABLE, ALLOCATION, need_matrix)
    print(f"Result: {msg_b}")
    
    print("\n--- Validation Check ---")
    # Acceptance parameters defined strictly in the PRD constraints
    if is_safe and success_a and not success_b:
        print("[SUCCESS] Banker's algorithm accurately governed deadlock-avoidance without false restrictions.")
    else:
        print("[FAILED!] Mathematical check parameters did not conform to safe requirements.")
