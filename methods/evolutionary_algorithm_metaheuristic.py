import random

# Problem setup
BARS = [0.2, 0.3, 0.3, 0.5, 0.7, 0.8]
TARGET = 1.0

# --- Fitness Function ---
def fitness(solution):
    """Fitness = waste + 0.1 * number of bars; lower is better."""
    total = sum(BARS[i] for i in solution)
    if total < TARGET:
        return float("inf")  # infeasible
    waste = total - TARGET
    return waste + 0.1 * len(solution)

# --- Generate Random Solution ---
def random_solution():
    """Randomly add bars until total >= TARGET, stop after first excess."""
    solution = []
    available_indices = list(range(len(BARS)))
    total = 0

    while total < TARGET and available_indices:
        i = random.choice(available_indices)
        if total + BARS[i] > TARGET + 0.5:  # optional: limit max overshoot
            available_indices.remove(i)
            continue
        solution.append(i)
        available_indices.remove(i)
        total = sum(BARS[j] for j in solution)

    return solution

# --- Crossover ---
def crossover(parent1, parent2):
    """One-point crossover avoiding duplicates."""
    if not parent1 or not parent2:
        return parent1[:]
    point = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child = parent1[:point] + [i for i in parent2[point:] if i not in parent1[:point]]
    return child

# --- Mutation ---
def mutate(solution, mutation_rate=0.2):
    """Randomly replace or add bars."""
    new_solution = solution[:]
    available_indices = [i for i in range(len(BARS)) if i not in new_solution]
    total = sum(BARS[j] for j in new_solution)

    # Replace bars
    for idx in range(len(new_solution)):
        if random.random() < mutation_rate and available_indices:
            new_index = random.choice(available_indices)
            available_indices.remove(new_index)
            new_solution[idx] = new_index

    # Add bars if total < TARGET
    while total < TARGET and available_indices:
        i = random.choice(available_indices)
        new_solution.append(i)
        available_indices.remove(i)
        total = sum(BARS[j] for j in new_solution)

    return new_solution

# --- Remove duplicate solutions ---
def unique_solutions(solutions):
    """Remove duplicates while preserving order."""
    seen = set()
    unique = []
    for sol in solutions:
        t = tuple(sorted(sol))  # sort so [0.3,0.7] == [0.7,0.3]
        if t not in seen:
            seen.add(t)
            unique.append(sol)
    return unique

# --- Genetic Algorithm ---
def genetic_algorithm(pop_size=12, generations=15, elite_size=3, mutation_rate=0.2):
    # Initialize population
    population = [random_solution() for _ in range(pop_size)]

    for gen in range(generations):
        # Evaluate fitness
        scored = [(fitness(sol), sol) for sol in population]
        scored.sort(key=lambda x: x[0])

        # Select top elites and remove duplicates
        elites = [sol for _, sol in scored[:elite_size]]
        elites = unique_solutions(elites)

        # Generate new population
        new_population = elites[:]
        while len(new_population) < pop_size:
            parent1, parent2 = random.choices(elites, k=2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        # Print generation summary
        print(f"\nGeneration {gen+1}:")
        for fit_val, sol in scored:
            bars_used = [BARS[i] for i in sol]
            print(f"  Solution: {bars_used}, Fitness: {fit_val:.3f}")
        print("  Elites:")
        for i, elite in enumerate(elites):
            print(f"    Elite {i+1}: {[BARS[j] for j in elite]}, Fitness = {fitness(elite):.3f}")

    # Final best solution
    best_fitness, best_solution = min((fitness(sol), sol) for sol in population)
    return best_solution, best_fitness

if __name__ == "__main__":
    best_solution, best_fit = genetic_algorithm()
    print("\nBest Solution Found:")
    print("Bars used:", [BARS[i] for i in best_solution])
    print("Total length:", sum(BARS[i] for i in best_solution))
    print("Fitness (waste + bars*0.1):", best_fit)
