import itertools

# Problem setup
BARS = [0.2, 0.3, 0.3, 0.5, 0.7, 0.8]
TARGET = 1.0
PENALTY = 0.1  # penalty per bar to prefer fewer bars
EPS = 1e-9

# --- Fitness Function ---
def fitness(solution):
    total = sum(solution)
    if total < TARGET - EPS:
        return float("inf")  # infeasible
    waste = total - TARGET
    return waste + PENALTY * len(solution)

# --- Graph Grammar "rules" ---
def rule_extend(solution, remaining_bars):
    """
    Rule: Extend current solution with one more bar if it doesn't exceed target too much.
    """
    extensions = []
    for i, bar in enumerate(remaining_bars):
        new_sol = solution + [bar]
        if sum(new_sol) <= TARGET + 0.5:  # allow some overshoot
            new_remaining = remaining_bars[:i] + remaining_bars[i+1:]
            extensions.append((new_sol, new_remaining))
    return extensions

def rule_stop(solution):
    """
    Rule: Stop if total length >= target.
    """
    return sum(solution) >= TARGET - EPS

# --- Grammar Expansion Search ---
def grammar_search(bars):
    solutions = []

    def expand(solution, remaining):
        # Apply stop rule
        if rule_stop(solution):
            solutions.append(solution)
            return
        # Apply extend rule
        for new_sol, new_rem in rule_extend(solution, remaining):
            expand(new_sol, new_rem)

    # Start with empty solution
    expand([], bars)
    return solutions

if __name__ == "__main__":
    # Generate candidate solutions
    candidates = grammar_search(BARS)

    # Evaluate fitness
    evaluated = [(fitness(sol), sol) for sol in candidates]
    evaluated = [e for e in evaluated if e[0] != float("inf")]  # filter infeasible
    evaluated.sort(key=lambda x: x[0])

    # Print results
    print("All feasible solutions (sorted by fitness):")
    for fit, sol in evaluated:
        print(f"  {sol}, Total = {sum(sol):.2f}, Fitness = {fit:.3f}")

    # Best solution
    best_fit, best_sol = evaluated[0]
    print("\nBest Solution Found:")
    print("  Bars used:", best_sol)
    print("  Total length:", sum(best_sol))
    print("  Fitness (waste + penalty*bars):", best_fit)
