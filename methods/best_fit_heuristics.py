# Heuristic Best Fit Method for Cutting Stock Problem (with floating-point fix)

def best_fit(bars, target, eps=1e-9):
    """
    Selects bars step by step to minimize the remaining unfilled target length.
    """
    solution = []
    remaining = target
    available = bars.copy()

    while remaining > eps and available:
        # Pick the bar that leaves the least remaining length (but does not exceed target)
        best_bar = None
        best_gap = float("inf")

        for bar in available:
            if bar <= remaining + eps and (remaining - bar) < best_gap:
                best_bar = bar
                best_gap = remaining - bar

        if best_bar is None:
            # No bar fits the remaining space, stop
            break

        # Add chosen bar to solution and update
        solution.append(best_bar)
        available.remove(best_bar)
        remaining -= best_bar

    # Compute waste (allowing for tolerance)
    total_length = sum(solution)
    waste = max(0, target - total_length)

    return solution, waste


if __name__ == "__main__":
    # Problem setup
    bars = [0.2, 0.3, 0.3, 0.5, 0.7, 0.8]
    target = 1.0

    solution, waste = best_fit(bars, target)

    print("Target length:", target)
    print("Available bars:", bars)
    print("Chosen bars:", solution)
    print("Total length used:", sum(solution))
    print("Waste:", waste)
