def count_found(resources):
    return sum(1 for r in resources if r.found)
 
 
def all_found(resources):
    return all(r.found for r in resources)
 
 
class MetricsTracker:
    
 
    def __init__(self, total):
        self.total      = total
        self.frame      = 0
        self.find_times = {}   # resource index -> frame first found
 
    def tick(self, resources, memory):
        self.frame += 1
        for i, r in enumerate(resources):
            if r.found and i not in self.find_times:
                self.find_times[i] = self.frame
 
    def summary(self, memory):
        found = len(self.find_times)
        avg_t = (sum(self.find_times.values()) / found) if found else 0
        return {
            "found":          found,
            "total":          self.total,
            "frames":         self.frame,
            "coverage_%":     round(memory.coverage() * 100, 1),
            "avg_find_frame": round(avg_t, 1),
        }
 