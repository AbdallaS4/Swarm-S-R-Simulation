import numpy as np
 
 
class SharedMemory:
    
 
    def __init__(self, w, h, grid=20):
        self.grid = grid
        self.w    = w // grid
        self.h    = h // grid
        self.visited = np.zeros((self.w, self.h), dtype=np.float32)
        self.found   = set()
 
    def mark(self, x, y):
        """Record a robot visit at world position (x, y)."""
        gx = int(x) // self.grid
        gy = int(y) // self.grid
        if 0 <= gx < self.w and 0 <= gy < self.h:
            self.visited[gx][gy] += 1
 
    def add_found(self, x, y):
        """Mark a resource as found."""
        self.found.add((int(x) // self.grid, int(y) // self.grid))
 
    def get_frontiers(self):
        """
        Return world-coord centres of unvisited cells that border
        at least one visited cell (Yamauchi 1998 frontier detection).
        """
        v = self.visited
        frontiers = []
        for gx in range(1, self.w - 1):
            for gy in range(1, self.h - 1):
                if v[gx][gy] == 0:
                    if (v[gx+1][gy] > 0 or v[gx-1][gy] > 0 or
                            v[gx][gy+1] > 0 or v[gx][gy-1] > 0):
                        frontiers.append((gx * self.grid, gy * self.grid))
        return frontiers
 
    def coverage(self):
        """Fraction [0,1] of grid cells visited at least once."""
        total = self.w * self.h
        if total == 0:
            return 0.0
        return float(np.count_nonzero(self.visited)) / total