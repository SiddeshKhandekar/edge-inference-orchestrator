"""
schedulers.py

Implements CPU scheduling algorithms: FCFS, SJF (Non-preemptive), and SRTF (Preemptive).
Metric terms:
- Comp (Completion Time)
- WT (Waiting Time)
- TAT (Turnaround Time)
"""
from jobs import JOBS

def fcfs(jobs_list):
    """First-Come, First-Served: Executes jobs in order of arrival."""
    results = []
    current_time = 0
    
    # Sort strictly by arrival time, and job_id for tie-breaking
    for job in sorted(jobs_list, key=lambda x: (x['arrival_time'], x['job_id'])):
        current_time = max(current_time, job['arrival_time']) + job['burst_time']
        tat = current_time - job['arrival_time']
        
        # Merge dictionary data cleanly
        results.append({**job, 'completed': current_time, 'tat': tat, 'wt': tat - job['burst_time']})
        
    return results

def sjf(jobs_list):
    """Shortest Job First (Non-preemptive): Prioritizes smallest burst time."""
    results = []
    current_time = 0
    uncompleted = jobs_list.copy()
    
    while uncompleted:
        # Filter jobs that have arrived
        ready_jobs = [j for j in uncompleted if j['arrival_time'] <= current_time]
        
        if not ready_jobs:
            current_time = min(j['arrival_time'] for j in uncompleted)
            continue
            
        # Tie-breakers: 1. burst_time, 2. arrival_time, 3. job_id
        nxt = min(ready_jobs, key=lambda x: (x['burst_time'], x['arrival_time'], x['job_id']))
        current_time += nxt['burst_time']
        tat = current_time - nxt['arrival_time']
        
        results.append({**nxt, 'completed': current_time, 'tat': tat, 'wt': tat - nxt['burst_time']})
        uncompleted.remove(nxt)
        
    return results

def srtf(jobs_list):
    """Shortest Remaining Time First (Preemptive)"""
    results = {}
    remaining = {j['job_id']: j['burst_time'] for j in jobs_list}
    current_time, completed = 0, 0
    
    while completed < len(jobs_list):
        # Ready jobs with pending execution
        ready = [j for j in jobs_list if j['arrival_time'] <= current_time and remaining[j['job_id']] > 0]
        
        if not ready:
            current_time = min(j['arrival_time'] for j in jobs_list if remaining[j['job_id']] > 0)
            continue
            
        # Tie-breakers: 1. remaining time, 2. arrival_time, 3. job_id
        nxt = min(ready, key=lambda x: (remaining[x['job_id']], x['arrival_time'], x['job_id']))
        remaining[nxt['job_id']] -= 1
        current_time += 1
        
        if remaining[nxt['job_id']] == 0:
            completed += 1
            tat = current_time - nxt['arrival_time']
            results[nxt['job_id']] = {**nxt, 'completed': current_time, 'tat': tat, 'wt': tat - nxt['burst_time']}
            
    # Sort output chronologically by completion time
    return sorted(results.values(), key=lambda x: x['completed'])

def summarize(name, res):
    """Helper to display terminal table and compute averages cleanly."""
    print(f"\n--- {name} ---")
    print("ID       | Arrival | Burst | Comp | WT | TAT")
    print("-" * 45)
    for r in res:
        print(f"{r['job_id']} | {r['arrival_time']:<7} | {r['burst_time']:<5} | {r['completed']:<4} | {r['wt']:<2} | {r['tat']}")
        
    avg_wt = sum(r['wt'] for r in res) / len(res)
    avg_tat = sum(r['tat'] for r in res) / len(res)
    print("-" * 45)
    print(f"Avg Wait: {avg_wt:.2f} | Avg Turnaround: {avg_tat:.2f}")
    return avg_wt

if __name__ == "__main__":
    w_fcfs = summarize("FCFS", fcfs(JOBS))
    w_sjf = summarize("SJF (Non-Preemptive)", sjf(JOBS))
    w_srtf = summarize("SRTF (Preemptive)", srtf(JOBS))
    
    print("\n--- Acceptance Check ---")
    # Acceptance criteria specific validation
    if w_srtf < w_sjf < w_fcfs:
        print("[SUCCESS] Avg Wait SRTF < SJF < FCFS precisely met.")
    else:
        print("[FAILED!] Did not meet criteria.")
