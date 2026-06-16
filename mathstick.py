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

  # Τερματισμός (Base Case)
         if idx == len(self.tokens):
            if moves <= self.max_k and self._is_valid(current_state):
                self._add_to_results(current_state, moves, path_history)
            return

        # Αναδρομή: δοκιμή υποψήφιων τιμών για το slot
        for cand in self._get_candidates(self.tokens[idx], idx):
            a, r = self._get_cost(self.tokens[idx], cand)
            
            # Δημιουργία νέου state
            new_state = current_state[:]
            new_state[idx] = cand
            
            # Υπολογισμός κινήσεων και delta για το κλάδεμα
            new_moves = moves + a + r
            new_delta = delta + (a - r)

            move_info = self._format_moves(self.tokens[idx], cand, idx)
            self._search(idx + 1, new_state, new_moves, new_delta, path_history + move_info)

    def _get_cost(self, orig, cand):
        orig_s = LAYOUT.get(orig, set())
        cand_s = LAYOUT.get(cand, set())
        return len(cand_s - orig_s), len(orig_s - cand_s)

    def _format_moves(self, orig, cand, slot_idx):
        slot_name = chr(ord('A') + slot_idx)
        orig_s = LAYOUT.get(orig, set())
        cand_s = LAYOUT.get(cand, set())
        
        removed = orig_s - cand_s
        added = cand_s - orig_s
        
        moves = []
        for r in removed:
            for a in added:
                moves.append(f"Move({slot_name}{r}, {slot_name}{a})")
        return moves

    def _is_valid(self, state):
        try:
            eq = "".join(state)
            left, right = eq.split('=')
            return eval(left) == int(right)
        except: return False

    def _get_candidates(self, current, idx):
        # Αν είναι ψηφίο, δοκιμάζουμε 0-9. Αν είναι τελεστής, '+' ή '-'
        if current in ['+', '-']: return ['+', '-']
        return [str(i) for i in range(10)]

    def _add_to_results(self, state, moves, history):
        picks = [m.split(',')[0].replace("Move(", "") for m in history]
        places = [m.split(',')[1].replace(")", "").strip() for m in history]
