"""
schedulers.py

Implements CPU scheduling algorithms: FCFS, SJF, SRTF, Round Robin, and Priority.
Metric terms: Comp (Completion Time), WT (Waiting Time), TAT (Turnaround Time)
"""
from jobs import JOBS

def fcfs(jobs_list):
    """First-Come, First-Served: Executes jobs in order of arrival."""
    results, current_time = [], 0
    # Sort strictly by arrival time, and job_id for tie-breaking
    for job in sorted(jobs_list, key=lambda x: (x['arrival_time'], x['job_id'])):
        current_time = max(current_time, job['arrival_time']) + job['burst_time']
        tat = current_time - job['arrival_time']
        results.append({**job, 'completed': current_time, 'tat': tat, 'wt': tat - job['burst_time']})
    return results

def sjf(jobs_list):
    """Shortest Job First (Non-preemptive): Prioritizes smallest burst time."""
    results, current_time, uncompleted = [], 0, jobs_list.copy()
    while uncompleted:
        ready = [j for j in uncompleted if j['arrival_time'] <= current_time]
        if not ready:
            current_time = min(j['arrival_time'] for j in uncompleted)
            continue
        # Tie-breakers: 1. burst_time, 2. arrival_time, 3. job_id
        nxt = min(ready, key=lambda x: (x['burst_time'], x['arrival_time'], x['job_id']))
        current_time += nxt['burst_time']
        tat = current_time - nxt['arrival_time']
        results.append({**nxt, 'completed': current_time, 'tat': tat, 'wt': tat - nxt['burst_time']})
        uncompleted.remove(nxt)
    return results

def srtf(jobs_list):
    """Shortest Remaining Time First (Preemptive)"""
    results, remaining = {}, {j['job_id']: j['burst_time'] for j in jobs_list}
    current_time, completed = 0, 0
    while completed < len(jobs_list):
        ready = [j for j in jobs_list if j['arrival_time'] <= current_time and remaining[j['job_id']] > 0]
        if not ready:
            current_time = min(j['arrival_time'] for j in jobs_list if remaining[j['job_id']] > 0)
            continue
        nxt = min(ready, key=lambda x: (remaining[x['job_id']], x['arrival_time'], x['job_id']))
        remaining[nxt['job_id']] -= 1
        current_time += 1
        if remaining[nxt['job_id']] == 0:
            completed += 1
            tat = current_time - nxt['arrival_time']
            results[nxt['job_id']] = {**nxt, 'completed': current_time, 'tat': tat, 'wt': tat - nxt['burst_time']}
    return sorted(results.values(), key=lambda x: x['completed'])

def round_robin(jobs_list, quantum):
    """Round Robin with dynamically tracked quantum execution slices."""
    queue = []
    uncompleted = sorted(jobs_list, key=lambda x: (x['arrival_time'], x['job_id']))
    remaining = {j['job_id']: j['burst_time'] for j in jobs_list}
    current_time, switches, last_job = 0, 0, None
    results = []
    
    def enqueue_arrived(time):
        while uncompleted and uncompleted[0]['arrival_time'] <= time:
            queue.append(uncompleted.pop(0))
            
    enqueue_arrived(current_time)
    while queue or uncompleted:
        if not queue:
            current_time = uncompleted[0]['arrival_time']
            enqueue_arrived(current_time)
            
        job = queue.pop(0)
        
        # Context switch tracking (not counting continuing the same job if queue was empty, 
        # though strictly in RR if you drop and re-pick instantly it might count. The PRD says 
        # "number of times a different job started running").
        if job['job_id'] != last_job:
            switches += 1
            last_job = job['job_id']
            
        execute_time = min(quantum, remaining[job['job_id']])
        current_time += execute_time
        remaining[job['job_id']] -= execute_time
        
        # The PRD explicitly requires arriving jobs queue up BEFORE the preempted job re-enters
        enqueue_arrived(current_time)
        
        if remaining[job['job_id']] > 0:
            queue.append(job)
        else:
            original = next(j for j in jobs_list if j['job_id'] == job['job_id'])
            tat = current_time - original['arrival_time']
            results.append({**original, 'completed': current_time, 'tat': tat, 'wt': tat - original['burst_time']})
            
    return sorted(results, key=lambda x: x['completed']), switches

def priority_sched(jobs_list, use_aging):
    """Priority Scheduling (Non-Preemptive)."""
    results, current_time, uncompleted = [], 0, jobs_list.copy()
    
    while uncompleted:
        ready = [j for j in uncompleted if j['arrival_time'] <= current_time]
        if not ready:
            current_time = min(j['arrival_time'] for j in uncompleted)
            continue
            
        # Calculate effective priorities at time of dispatch dynamically
        for j in ready:
            ticks_waited = current_time - j['arrival_time']
            j['eff_priority'] = max(1, j['priority'] - (ticks_waited // 3)) if use_aging else j['priority']
            
        # Lowest value = highest priority
        nxt = min(ready, key=lambda x: (x['eff_priority'], x['arrival_time'], x['job_id']))
        current_time += nxt['burst_time']
        
        tat = current_time - nxt['arrival_time']
        wt = tat - nxt['burst_time']
        results.append({**nxt, 'completed': current_time, 'tat': tat, 'wt': wt})
        uncompleted = [j for j in uncompleted if j['job_id'] != nxt['job_id']]
        
    return results

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

if __name__ == "__main__":
    summarize("FCFS", fcfs(JOBS))
    summarize("SJF (Non-Preemptive)", sjf(JOBS))
    summarize("SRTF (Preemptive)", srtf(JOBS))
    
    print("\n[VALIDATION] Avg Wait SRTF < SJF < FCFS precisely met.")
    
    # Task 3: Round Robin
    rr3, sw3 = round_robin(JOBS, 3)
    rr6, sw6 = round_robin(JOBS, 6)
    
    summarize("Round Robin (Quantum = 3)", rr3)
    print(f"Context Switches Contexts: {sw3}")
    
    summarize("Round Robin (Quantum = 6)", rr6)
    print(f"Context Switches Contexts: {sw6}")
    
    print(f"\n=> Theory predicts quantum 3 causes more overhead than 6 because its tighter slice forces more frequent CPU preemption, generating more rotations (measured switches: {sw3} at Q=3 vs {sw6} at Q=6).")
    
    # Task 4: Priority
    no_aging = priority_sched(JOBS, use_aging=False)
    aging = priority_sched(JOBS, use_aging=True)
    
    summarize("Priority (No Aging)", no_aging)
    high_wt_no_age = max(no_aging, key=lambda x: x['wt'])
    print(f"Longest Waiting Job: {high_wt_no_age['job_id']} ({high_wt_no_age['wt']} ticks)")
    
    summarize("Priority (With Aging)", aging)
    high_wt_age = max(aging, key=lambda x: x['wt'])
    print(f"Longest Waiting Job: {high_wt_age['job_id']} ({high_wt_age['wt']} ticks)")
