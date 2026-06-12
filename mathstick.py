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
