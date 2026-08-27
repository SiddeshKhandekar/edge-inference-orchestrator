"""
test_engine.py
Automated Testing Suite rigorously verifying PRD invariants across the OS computation engine natively.
"""
import unittest
from jobs import JOBS
import schedulers as sched
import synchronization as sync
import bankers as bank
import memory_mgmt as mem

class TestOSComputeEngine(unittest.TestCase):
    
    def test_job_dataset_immutability(self):
        self.assertEqual(len(JOBS), 8)
        self.assertEqual(JOBS[0]['job_id'], "Z1-J01")
        
    def test_scheduling_averages(self):
        avg_wait = lambda res: sum(r['wt'] for r in res) / len(res)
        avg_wait_fcfs = avg_wait(sched.fcfs(JOBS))
        avg_wait_sjf = avg_wait(sched.sjf(JOBS))
        avg_wait_srtf = avg_wait(sched.srtf(JOBS))
        self.assertTrue(avg_wait_srtf < avg_wait_sjf < avg_wait_fcfs)
        
    def test_round_robin_switches(self):
        _, sw3 = sched.round_robin(JOBS, 3)
        _, sw6 = sched.round_robin(JOBS, 6)
        self.assertEqual(sw3, 16)
        self.assertEqual(sw6, 10)
        
    def test_priority_aging_mitigation(self):
        no_age = sched.priority_sched(JOBS, False)
        age = sched.priority_sched(JOBS, True)
        
        longest_wait_no_aging = max(no_age, key=lambda x: x['wt'])['job_id']
        longest_wait_aging = max(age, key=lambda x: x['wt'])['job_id']
        
        wt_no_aging_z3 = next(j['wt'] for j in no_age if j['job_id'] == "Z3-J02")
        wt_aging_z3 = next(j['wt'] for j in age if j['job_id'] == "Z3-J02")
        
        self.assertEqual(longest_wait_no_aging, "Z3-J02")
        self.assertNotEqual(longest_wait_aging, "Z3-J02")
        self.assertTrue(wt_aging_z3 < wt_no_aging_z3)
        
    def test_peterson_synchronization(self):
        unsynced_runs = sync.execute_unsync()
        peterson_runs = sync.execute_peterson()
        self.assertTrue(any(val != 85 for val in unsynced_runs))
        self.assertTrue(all(val == 85 for val in peterson_runs))
        
    def test_bankers_algorithm(self):
        need = bank.compute_need(bank.MAX_NEED, bank.ALLOCATION)
        initial_safe, _ = bank.get_safe_sequence(bank.AVAILABLE, bank.ALLOCATION, need)
        
        req_p1_granted, _ = bank.evaluate_request("P1", [1,0,2], bank.AVAILABLE, bank.ALLOCATION, need)
        req_p0_granted, _ = bank.evaluate_request("P0", [2,0,2], bank.AVAILABLE, bank.ALLOCATION, need)
        
        self.assertTrue(initial_safe)
        self.assertTrue(req_p1_granted)
        self.assertFalse(req_p0_granted)
        
    def test_memory_translation(self):
        # Paging 
        self.assertTrue("Physical: 5380" in mem.translate_page(260))
        self.assertTrue("Physical: 2524" in mem.translate_page(1500))
        self.assertTrue("Physical: 10168" in mem.translate_page(3000))
        self.assertTrue("PAGE FAULT" in mem.translate_page(5000))
        
        # Segmentation 
        self.assertTrue("Physical: 1150" in mem.translate_segment((0, 150)))
        self.assertTrue("SEGMENTATION FAULT" in mem.translate_segment((1, 350)))
        self.assertTrue("Physical: 600" in mem.translate_segment((2, 100)))

if __name__ == '__main__':
    unittest.main()
