import sys
import argparse
import json
import re

# Τα layouts των ψηφίων (0-9) σύμφωνα με την Εικόνα 1
LAYOUT = {
    '0': {1, 2, 3, 4, 5, 6}, '1': {2, 3}, '2': {0, 1, 2, 4, 5},
    '3': {0, 1, 2, 3, 4}, '4': {0, 1, 2, 3, 6}, '5': {0, 1, 3, 4, 6},
    '6': {0, 1, 3, 4, 5, 6}, '7': {1, 2, 3}, '8': {0, 1, 2, 3, 4, 5, 6},
    '9': {0, 1, 2, 3, 4, 6}
}

class MatchstickSolver:
    def __init__(self, problem, max_k):
        self.problem = problem
        self.max_k = max_k
        self.nodes_visited = 0
        self.nodes_pruned = 0
        self.solutions = {str(i): [] for i in range(1, max_k + 1)}
        self.tokens = list(problem.replace(" ", ""))

    def solve(self):
        # Ξεκινάμε την αναζήτηση από το 1ο slot (index 0)
        self._search(0, self.tokens, 0, 0, [])

    def _search(self, idx, current_state, moves, delta, path_history):
        self.nodes_visited += 1

        # Pruning: Αν έχουμε υπερβεί το budget κινήσεων
        if moves > self.max_k:
            self.nodes_pruned += 1
            return
