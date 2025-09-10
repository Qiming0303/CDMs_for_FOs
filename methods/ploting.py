import csv

# Table data
columns = ["Method", "Selection Logic", "Evaluation", "Update/Iteration", "Strength", "Weakness"]
# Replace "≤" with "<=" and "×" with "x" in the text
data = [
    ["Best Fit Heuristic",
     "Pick bar that minimizes remaining gap toward target",
     "Evaluate total length after each step",
     "Greedy, stop when target reached",
     "Very fast, simple",
     "May overlook better solutions"],
    
    ["Linear Programming",
     "Consider all bars simultaneously",
     "Objective = minimize waste + penalty x bars",
     "Solver returns global optimum",
     "Guarantees global optimum",
     "Requires precise mathematical formulation"],
    
    ["Metaheuristic (GA)",
     "Randomly generate population of solutions",
     "Fitness = waste + bar count",
     "Crossover/mutation -> new population, elites retained",
     "Can handle complex/large problems",
     "No guarantee of global optimum, stochastic"],
    
    ["Graph Grammar",
     "Apply rewriting rules for bar combinations",
     "Check if sum <= 1",
     "Generate new sequences recursively",
     "Systematic exploration of combinations",
     "Rule design required, may miss solutions if rules incomplete"],
    
    ["Physics-based (Dynamic Relaxation)",
     "Random sequences connected as hinges",
     "Energy = deviation from target + penalty",
     "System relaxes under physics until stable",
     "Intuitive, visualizes structural behavior",
     "Stochastic, not ideal for discrete problems"],
    
    ["Q-Learning",
     "Sequentially select bars according to learned policy (one-time use)",
     "Reward = 1 - (waste + penalty x bars)",
     "Q-table updated over episodes",
     "Learns optimal policy, scalable",
     "Needs training, sensitive to parameters"]
]


with open("bar_methods_ascii.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(data)

print("CSV saved with UTF-8 BOM for Excel compatibility.")
