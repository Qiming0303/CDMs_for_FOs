import pybullet as p
import pybullet_data
import time
import random

# Problem setup
BARS = [0.2, 0.3, 0.3, 0.5, 0.7, 0.8]
TARGET = 1.0
NUM_SOLUTIONS = 10   # number of random candidate solutions
SIM_STEPS = 240      # simulation steps for relaxation
TIME_STEP = 1.0 / 240.0

def evaluate_energy(solution):
    """Energy = squared error + penalty for number of bars"""
    total = sum(solution)
    if total < TARGET:
        return float("inf")  # infeasible
    waste = abs(total - TARGET)
    return waste**2 + 0.1 * len(solution)

def simulate_solution(solution, title="Solution"):
    """Simulate one solution with dynamic relaxation (gravity + hinges)."""
    cid = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, -9.8, 0)

    # Ground as supports
    plane = p.loadURDF("plane.urdf")

    # Create bars
    bar_ids = []
    x_pos = 0
    for length in solution:
        half_extents = [length / 2.0, 0.05, 0.05]
        col_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)
        vis_id = p.createVisualShape(p.GEOM_BOX, halfExtents=half_extents,
                                     rgbaColor=[0, 1, 0, 1])
        bar_id = p.createMultiBody(baseMass=1,
                                   baseCollisionShapeIndex=col_id,
                                   baseVisualShapeIndex=vis_id,
                                   basePosition=[x_pos + half_extents[0], 0.05, 0])
        bar_ids.append(bar_id)
        x_pos += length

    # Fix first and last bars
    p.createConstraint(bar_ids[0], -1, -1, -1, p.JOINT_FIXED, [0, 0, 0],
                       [-(solution[0] / 2), 0, 0], [0, 0, 0])
    p.createConstraint(bar_ids[-1], -1, -1, -1, p.JOINT_FIXED, [0, 0, 0],
                       [solution[-1] / 2, 0, 0], [TARGET, 0, 0])

    # Connect hinges
    for i in range(len(bar_ids) - 1):
        p.createConstraint(bar_ids[i], -1, bar_ids[i + 1], -1,
                           p.JOINT_POINT2POINT, [0, 0, 0],
                           [solution[i] / 2, 0, 0],
                           [-solution[i + 1] / 2, 0, 0])

    # Add overlay text
    p.addUserDebugText(title, [0.3, 0.5, 0.3], [1, 0, 0], textSize=2)

    # Run simulation steps
    for _ in range(SIM_STEPS):
        p.stepSimulation()
        time.sleep(TIME_STEP)

    input("Press Enter to close this simulation...")
    p.disconnect()

def run_random_solutions(n=NUM_SOLUTIONS):
    results = []
    for i in range(n):
        num_bars = random.randint(2, len(BARS))  # at least 2 bars
        solution = random.sample(BARS, num_bars)
        e = evaluate_energy(solution)
        results.append((solution, e))

    # Sort results by energy
    results.sort(key=lambda x: x[1])
    best_solution, best_energy = results[0]
    worst_solution, worst_energy = results[-1]

    # Print all results
    print("\n=== Candidate Solutions ===")
    for i, (sol, e) in enumerate(results):
        print(f"Solution {i+1}: {sol}, Energy = {e:.4f}")

    print("\n=== Best Solution ===")
    print(f"Chosen bars: {best_solution}, Energy = {best_energy:.4f}")
    print("\n=== Worst Solution ===")
    print(f"Chosen bars: {worst_solution}, Energy = {worst_energy:.4f}")

    # Show best in GUI
    simulate_solution(best_solution, title=f"Best Solution {best_solution}, E={best_energy:.3f}")

    # Show worst in GUI
    simulate_solution(worst_solution, title=f"Worst Solution {worst_solution}, E={worst_energy:.3f}")

if __name__ == "__main__":
    run_random_solutions()
