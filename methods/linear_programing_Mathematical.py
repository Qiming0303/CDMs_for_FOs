import pulp

# --- Problem setup ---
BARS = [0.2, 0.3, 0.3, 0.5, 0.7, 0.8]
TARGET = 1.0
PENALTY = 0.1  # weight for number of bars

# --- Define the optimization problem ---
prob = pulp.LpProblem("Steel_Bar_Combination", pulp.LpMinimize)

# Decision variables: x[i] = 1 if bar i is used, 0 otherwise
x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(len(BARS))]

# Objective function: minimize waste + penalty * number of bars
total_length = pulp.lpSum([BARS[i] * x[i] for i in range(len(BARS))])
waste = total_length - TARGET
# We want to minimize waste if >=0, so use a positive-only approach
# Since total_length >= TARGET, waste >= 0
prob += waste + PENALTY * pulp.lpSum(x), "Total_Cost"

# Constraint: total length must be >= TARGET
prob += total_length >= TARGET, "TargetLength"

# Solve the problem
solver = pulp.PULP_CBC_CMD(msg=True)  # default solver
prob.solve(solver)

# --- Extract the solution ---
chosen_bars = [BARS[i] for i in range(len(BARS)) if pulp.value(x[i]) == 1]
total_len = sum(chosen_bars)
fitness = total_len - TARGET + PENALTY * len(chosen_bars)

# --- Print results ---
print("Status:", pulp.LpStatus[prob.status])
print("Chosen bars:", chosen_bars)
print("Total length:", total_len)
print("Fitness (waste + penalty*num_bars):", fitness)
