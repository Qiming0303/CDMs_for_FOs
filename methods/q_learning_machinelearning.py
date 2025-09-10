import numpy as np
import random

# --- Problem setup ---
BARS = [0.2, 0.3, 0.3, 0.5, 0.7, 0.8]
TARGET = 1.0
NUM_BARS = len(BARS)

# --- Q-Learning parameters ---
ALPHA = 0.5       # learning rate
GAMMA = 0.9       # discount factor
EPSILON = 0.2     # exploration rate
EPISODES = 1000  # number of episodes
PENALTY = 0.1     # penalty for number of bars
MAX_STEPS = NUM_BARS  # max steps = number of bars

# --- Initialize Q-table ---
bins = np.arange(0, TARGET + 0.51, 0.01)
num_states = len(bins)
Q = np.zeros((num_states, NUM_BARS))

def get_state_index(total_length):
    idx = np.searchsorted(bins, total_length)
    return min(idx, num_states - 1)

def reward(total_length, num_selected):
    if total_length < TARGET:
        return -1.0
    waste = total_length - TARGET
    return 1.0 - (waste + PENALTY * num_selected)

# --- Training ---
for ep in range(EPISODES):
    total = 0.0
    selected_indices = []
    for step in range(MAX_STEPS):
        state_idx = get_state_index(total)
        # Define valid actions (bars not yet selected)
        valid_actions = [i for i in range(NUM_BARS) if i not in selected_indices]
        if not valid_actions:
            break
        # Epsilon-greedy action
        if random.random() < EPSILON:
            action = random.choice(valid_actions)
        else:
            # Choose best Q-value among valid actions
            q_vals = [Q[state_idx, i] for i in valid_actions]
            max_q = max(q_vals)
            best_actions = [valid_actions[i] for i, q in enumerate(q_vals) if q == max_q]
            action = random.choice(best_actions)

        # Take action
        selected_indices.append(action)
        total += BARS[action]
        new_state_idx = get_state_index(total)
        r = reward(total, len(selected_indices))
        # Q-Learning update
        Q[state_idx, action] += ALPHA * (r + GAMMA * np.max(Q[new_state_idx]) - Q[state_idx, action])
        if total >= TARGET:
            break

# --- Extract best solution from Q-table ---
best_solution = []
total = 0.0
selected_indices = []
while total < TARGET:
    state_idx = get_state_index(total)
    valid_actions = [i for i in range(NUM_BARS) if i not in selected_indices]
    if not valid_actions:
        break
    q_vals = [Q[state_idx, i] for i in valid_actions]
    max_q = max(q_vals)
    best_actions = [valid_actions[i] for i, q in enumerate(q_vals) if q == max_q]
    action = random.choice(best_actions)
    selected_indices.append(action)
    best_solution.append(BARS[action])
    total += BARS[action]
    if total >= TARGET:
        break

waste = total - TARGET
fitness = waste + PENALTY * len(best_solution)

print("Q-Learning Best Solution (no repeats):")
print("Bars used:", best_solution)
print("Total length:", total)
print("Fitness (waste + penalty*num_bars):", fitness)
