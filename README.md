# Cutting Stock Problem – Method Comparison

This repository demonstrates and compares six different computational methods for solving a simple **cutting stock problem**:

> Given six steel bars of lengths **0.2m, 0.3m, 0.3m, 0.5m, 0.7m, and 0.8m**,  
> the task is to assemble them to achieve a target span of **1.0m** with minimal waste and using the fewest number of bars.

The goal is to showcase how different algorithmic paradigms approach the same problem, their strengths, weaknesses, and typical results.

---

## 📦 Setup

### 1. Clone this repository
```bash
git clone https://github.com/your-username/cutting-stock-methods.git
cd cutting-stock-methods
```
### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```
### 3. Install requirements
```bash
pip install -r requirements.txt
```
### 📚 Methods Included

Each method has its own script under the `methods/` directory.

| Method | Description | Dependencies |
|--------|-------------|--------------|
| Best Fit Heuristic | Iteratively selects the bar that best fills the remaining gap. | None (Python stdlib only) |
| Genetic Algorithm (GA) | Evolves a population of candidate solutions with crossover, mutation, and elitism. | `numpy`, `tqdm` |
| Linear Programming (LP) | Formulates as an optimization model with constraints and solves for global optimum. | `PuLP` |
| Physics-based Simulation | Uses PyBullet to relax bar assemblies dynamically under forces. | `pybullet` |
| Graph Grammar Rule-based | Applies rewriting rules to combine bars into feasible solutions. | None |
| Q-Learning (Reinforcement Learning) | Learns a policy through trial and error over many episodes. | `numpy` |

### ▶️ How to Run
Run any method by calling the corresponding script inside the methods/ directory.
For example:

```bash
python methods/best_fit.py
python methods/genetic_algorithm.py
python methods/linear_programming.py
python methods/physics_simulation.py
python methods/graph_grammar.py
python methods/q_learning.py
```
### 📊 Comparison
The repository also includes a Comparison Summary Table (see comparison/) that evaluates each method in terms of Logic, Strengths, Weaknesses.
This helps readers understand not just the results but also the reasoning behind each approach.

### 🔬 Reproducibility
All methods are implemented in Python 3.10+.

Randomized methods (GA, Q-learning) use fixed seeds for reproducibility.

Code is intentionally kept simple and transparent, making it easy for researchers, educators, and students to explore.

### 📂 Repository Structure
```bash

cutting-stock-methods/
│
├── methods/              # Each method implementation
│   ├── best_fit.py
│   ├── genetic_algorithm.py
│   ├── linear_programming.py
│   ├── physics_simulation.py
│   ├── graph_grammar.py
│   ├── q_learning.py
│
├── requirements.txt      # Dependencies
├── README.md             # Documentation (this file)
└── .gitignore
```
### 🔗 Citation
If you use this repository in your research or teaching, please cite it as:
Qiming Sun, "Comparative Study of Computational Methods for Cutting Stock Problems," GitHub Repository, 2025. 
