# Swarm-Based Search and Rescue Simulation

## Overview

This project implements a simulation of swarm robotics for search and rescue (SaR) operations. It investigates how multiple simple autonomous agents can cooperate to efficiently locate targets in a constrained environment without relying on centralised control.

The system is designed as part of a Final Year Project and focuses on comparing different swarm coordination strategies in terms of coverage, efficiency, and behaviour.

---

## Features

* Multi-agent swarm simulation using Python
* Real-time visualisation using Pygame
* Multiple swarm strategies:

  * **Random Walk** (baseline)
  * **Boids (Flocking)** – cohesion, separation, alignment
  * **Hive / Frontier-Based Exploration** – shared memory + intelligent exploration
* Structured environments (rooms, corridors, obstacles)
* Shared memory system using grid-based heatmaps
* Performance metrics:

  * Time to locate targets
  * Number of targets found
  * Comparative behaviour across strategies

---

## Technologies Used

* **Python 3**
* **Pygame** – rendering and simulation loop
* **NumPy** – grid-based memory and efficient computation

---

## Project Structure

```
swarm-search-rescue-simulation/
│
├── main.py          # Main simulation loop and experiment control
├── robot.py         # Agent behaviour, sensing, movement
├── swarm.py         # Swarm coordination strategies
├── environment.py   # Terrain and resource generation
├── memory.py        # Shared grid-based memory system
├── metrics.py       # Performance evaluation functions
└── README.md
```

---

## Installation

### 1. Clone the repository


### 2. Install dependencies

```
pip install pygame numpy
```

---

## How to Run

```
python main.py
```

* The simulation will start directly.
* The swarm strategy is selected within the code (in `main.py`).
* Results are displayed in real-time within the simulation window.

---

## How It Works

### Agents

Each robot is an autonomous agent capable of:

* Local sensing (detecting nearby resources)
* Obstacle avoidance
* Independent movement with stochastic variation
* Contributing to a shared memory system

---

### Shared Memory (Hive Strategy)

* The environment is divided into a grid
* Robots mark visited cells in a heatmap
* Frontier cells (edges of explored space) are detected
* Robots use this information to guide exploration

---

### Swarm Strategies

#### Random Walk

* Pure stochastic exploration
* No coordination
* Serves as a baseline

#### Boids (Flocking)

* Agents exhibit:

  * Cohesion (move toward group)
  * Separation (avoid crowding)
* Produces coordinated movement but may reduce coverage efficiency

#### Hive / Frontier-Based

* Agents share environmental knowledge
* Move toward unexplored frontiers
* Minimises redundant exploration
* Typically achieves the fastest search performance

---

## Evaluation Metrics

The system evaluates swarm performance using:

* **Targets Found** – number of resources located
* **Time Steps** – simulation duration
* **Exploration Efficiency** – inferred from heatmap coverage and resources located
---

## Example Scenario

The simulation represents a disaster environment where:

* Obstacles restrict movement (e.g., collapsed structures)
* Targets represent survivors
* Multiple agents must coordinate without central control

---

## Future Improvements

* Communication range constraints
* Agent failure simulation (robustness testing)
* Role-based agents (scouts vs workers)
* Data export (CSV logging)
* Dynamic environments

---

## Author

**Abdalla Saleh**
BEng (Hons) Software Engineering
University of Greenwich

---


