*This project has been created as part of the 42 curriculum by kebertra.*

---

# 🚁 Fly-In — Drone Routing System

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?style=flat-square&logo=qt&logoColor=white)
![Version](https://img.shields.io/badge/version-0.36.0-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

> Design and simulate an efficient multi-drone routing system navigating a network of connected zones under strict movement, capacity, and zone-type constraints.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Architecture](#-architecture)
4. [Input Format](#-input-format)
5. [Zone Types](#-zone-types)
6. [Algorithm](#-algorithm)
7. [Visual Representation](#-visual-representation)
8. [Installation](#-installation)
9. [Usage](#-usage)
10. [Makefile Commands](#-makefile-commands)
11. [Performance Benchmarks](#-performance-benchmarks)
12. [Resources & AI Usage](#-resources--ai-usage)

---

## 🎯 Project Overview

**Fly-In** is a drone routing simulation system built as part of the **Fly-in** 42 project. It reads a map file describing a network of connected hubs (zones), then routes a fleet of drones from a **start hub** to an **end hub** in the minimum number of simulation turns.

The system enforces all movement constraints defined by the subject:
- **Zone occupancy limits** (`max_drones` per hub per turn)
- **Link capacity limits** (`max_link_capacity` per connection per turn)
- **Zone movement costs** (normal: 1 turn, restricted: 2 turns, blocked: impassable)
- **No waiting on connections** — a drone entering a restricted zone transit must have a free destination

---

## ✨ Features

| Feature | Status |
|---|---|
| Map file parser with full error reporting | ✅ |
| Time-expanded Dijkstra pathfinding | ✅ |
| Multi-drone simultaneous routing | ✅ |
| Zone type enforcement (normal / priority / restricted / blocked) | ✅ |
| Node & link capacity constraints per turn | ✅ |
| No-wait-on-link rule for restricted zone transit | ✅ |
| Strategic drone waiting at source when path is blocked | ✅ |
| Graphical simulation viewer (PySide6) | ✅ |
| Drone animation frame-by-frame | ✅ |
| Simulation metrics display (turns, throughput, avg. path) | ✅ |
| Virtual environment detection & dependency check | ✅ |
| Full type safety (`mypy` + `flake8`) | ✅ |
| Comprehensive test suite (`pytest`, 50 tests) | ✅ |

---

## 🏗️ Architecture

The project follows a strict **Model-View-Controller** design with clean separation of concerns.

```
Fly-In/
├── main.py                          # Entry point
├── src/
│   ├── Controller.py                # Orchestrates loading, parsing, simulation
│   ├── FileLoader.py                # Reads map files from disk
│   ├── GraphBuilder.py              # Builds Graph from parsed MapModel
│   ├── graph/
│   │   ├── Graph.py                 # Graph (nodes + links)
│   │   ├── node/
│   │   │   ├── Node.py              # INode / IPathfindingNode / IDroneNode interfaces + base Node
│   │   │   ├── StartNode.py         # Origin hub
│   │   │   ├── EndNode.py           # Destination hub
│   │   │   └── HubNode.py           # Intermediate hub
│   │   └── link/
│   │       └── Link.py              # Bidirectional connection with capacity
│   ├── parsing/
│   │   ├── MapParser.py             # Orchestrates parsing pipeline
│   │   ├── models/                  # MapModel, HubModel, ConnectionModel
│   │   ├── errors/                  # MapErrors hierarchy
│   │   └── utils/                   # Zone type enum
│   ├── simulation/
│   │   ├── Simulation.py            # Runs algorithm for all drones
│   │   ├── PathfindingAlgorithm.py  # Registry / factory for algorithms
│   │   └── algorithms/
│   │       ├── AlgorithmProtocol.py # Protocol interface
│   │       └── Dijkstra.py          # Time-expanded Dijkstra implementation
│   ├── utils/
│   │   ├── PausingArgumentParser/
│   │   │   └── PausingArgumentParser.py  # argparse wrapper (no sys.exit on error)
│   │   └── RunSecurity/
│   │       └── RunSecurity.py       # Venv & dependency verification
│   └── view/
│       ├── ViewApp.py               # Qt application bootstrap
│       ├── ViewQT.py                # Main window + signal wiring
│       ├── pages/
│       │   ├── Page.py              # Base page with font & button utils
│       │   ├── MenuPage.py          # File selection & launch UI
│       │   └── SimPage.py           # Graph view, drone animation, log console
│       └── components/
│           ├── Button.py            # Styled QPushButton
│           ├── Drone.py             # Animatable drone sprite
│           └── Title.py             # Glowing animated title label
└── tests/                           # 50 pytest tests
```

**Signal flow:**

```
MenuPage ──file_selected──▶ Controller.load_file()
                                    │
                          FileLoader → MapParser → GraphBuilder
                                    │
                          Controller.launch_simulation()
                                    │
                          Simulation.start(Dijkstra, graph, nb_drones)
                                    │
                    ┌───────────────┴──────────────┐
               load_graph                    load_sim / load_metrics
                    │                               │
              SimPage.draw_graph()         SimPage._load_sim()
                                           SimPage._read_sim()  ← drone animation
```

---

## 📄 Input Format

Map files use the following syntax:

```
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
# Comments are ignored
```

**Rules:**
- First line must be `nb_drones: <positive_integer>`
- Exactly one `start_hub` and one `end_hub`
- Zone names must be unique — **no dashes or spaces**
- Connections reference only previously defined zones
- Duplicate connections (`a-b` and `b-a`) are forbidden
- Any parsing error stops the program with a clear message indicating the line and cause

---

## 🗺️ Zone Types

| Zone | Movement Cost | Behaviour |
|---|---|---|
| `normal` | 1 turn | Standard traversal |
| `priority` | 1 turn | Preferred by the pathfinder (reduced cost weight) |
| `restricted` | 2 turns | Higher cost; drone commits on entry — **cannot wait on the link** |
| `blocked` | ∞ | Impassable, skipped unconditionally |

**Capacity rules:**
- Each hub defaults to `max_drones=1` per turn
- Start and end hubs are **exempt** from capacity limits
- Link defaults to `max_link_capacity=1` — enforced across both transit directions

---

## 🧠 Algorithm

### Time-Expanded Dijkstra

The routing engine implements a **time-expanded Dijkstra** algorithm. Instead of searching a static graph, it searches a **space-time graph** where each state is a `(node_name, turn)` pair. This naturally handles dynamic, per-turn capacity constraints across multiple drones.

#### How it works

1. **State space**: every explored position is `(node, turn)` — the same physical node at different turns is a different state.
2. **Priority queue**: a min-heap ordered by cumulative cost explores the cheapest states first.
3. **Move options** at each state `(node, turn)`:
   - **Move** to a neighbour → `(neighbour, turn + 1)`, or `(neighbour, turn + 2)` for restricted zones
   - **Wait** at current node → `(node, turn + 1)` with a small discount cost
4. **Capacity checks** before any move:
   - Destination node capacity at arrival turn is checked **first** — if full, the drone cannot enter the link (no waiting mid-transit)
   - Link capacity across the full transit window is checked second
5. **Multi-drone awareness**: each drone's computed path increments the shared `occupancy` and `link_occupancy` maps, so subsequent drones automatically route around congestion.
6. **Path reconstruction**: the `previous` map is back-tracked from the goal state to yield the full turn-to-position dict, injecting `hub1-hub2` transit labels for restricted-zone hops.

#### Zone cost weights

| Zone | Weight |
|---|---|
| `normal` | `1.0` |
| `priority` | `0.80` *(preferred)* |
| `restricted` | `1.5` *(penalised)* |
| wait | `0.99` *(slightly cheaper than moving — encourages yielding)* |

#### Complexity

- State space: **O(N × T)** where N = nodes, T = max turns
- Per-state work: **O(degree × log(N×T))** for heap operations
- Overall: **O(N × T × degree × log(N×T))**

#### Extensibility

The algorithm is registered through `PathfindingAlgorithm` — a factory/registry class. Any class implementing `AlgorithmProtocol.process()` can be registered and swapped in:

```python
PathfindingAlgorithm.register("my_algo", MyAlgorithm)
algo = PathfindingAlgorithm.create("my_algo")
```

---

## 🖥️ Visual Representation

The graphical interface is built with **PySide6 (Qt6)** and provides a full simulation experience.

### Menu Page

- Drag-and-drop **or** Browse button to select a `.txt` map file
- Automatic file validation — the **Launch Simulation** button is only enabled after a valid map loads
- Links to GitHub and clean Exit button

### Simulation Page

- **Graph canvas**: nodes rendered as labelled circles (coloured by zone), links drawn as lines
- **Drone sprites**: blue rectangle markers placed on the canvas at `start` on simulation launch
- **Drone animation**: each drone smoothly animates to its next position every second using `QPropertyAnimation`
- **Log console**: real-time turn-by-turn movement log (`[TOUR N] D1-node D2-node ...`)
- **Metrics panel**: displays total turns, total drones, average turns per drone, throughput, and total movements after simulation completes

---

## 🚀 Installation

**Requirements:** Python 3.13+, [`uv`](https://github.com/astral-sh/uv)

```bash
# Clone the repository
git clone <repository-url>
cd Fly-in-2

# Install dependencies
make install
```

> `make install` will auto-install `uv` if not present, then run `uv sync` to create the virtual environment and install all dependencies.

---

## ▶️ Usage

```bash
# Launch the graphical application
make run

# Launch with debug mode (pdb)
make debug
```

Once the application opens:
1. Click **Browse** or drag-and-drop a `.txt` map file onto the input field
2. Wait for the file to validate — the **LAUNCH SIMULATION** button activates
3. Click the simulation page's **▶** button to animate the drone routing
4. Read the turn-by-turn log and metrics on the right panel

**Map files** are provided in `maps/` across four difficulty levels:

```
maps/
├── easy/         01_linear_path.txt  02_simple_fork.txt  03_basic_capacity.txt
├── medium/       01_dead_end_trap.txt  02_circular_loop.txt  03_priority_puzzle.txt
├── hard/         01_maze_nightmare.txt  02_capacity_hell.txt  03_ultimate_challenge.txt
└── challenger/   01_the_impossible_dream.txt
```

---

## 🛠️ Makefile Commands

| Command | Description |
|---|---|
| `make install` | Install all dependencies via `uv sync` |
| `make run` | Launch the application |
| `make debug` | Launch with `pdb` debugger |
| `make test` | Run the full pytest suite |
| `make lint` | Run `flake8` + `mypy` |
| `make lint-strict` | Run `flake8` + `mypy --strict` |
| `make clean` | Remove `__pycache__` and `.mypy_cache` |
| `make fclean` | `clean` + remove `app.log` |
| `make push_feat M="..."` | Commit & push `feat:` |
| `make push_fix M="..."` | Commit & push `fix:` |
| `make push_docs M="..."` | Commit & push `docs:` |
| `make bump-patch` | Bump patch version in `pyproject.toml` |
| `make bump-minor` | Bump minor version in `pyproject.toml` |

---

## 📊 Performance Benchmarks

Results on provided maps (lower turns = better):

| Difficulty | Map | Target | Status |
|---|---|---|---|
| 🟢 Easy | Linear path — 2 drones | ≤ 6 turns | ✅ |
| 🟢 Easy | Simple fork — 3 drones | ≤ 6 turns | ✅ |
| 🟢 Easy | Basic capacity — 4 drones | ≤ 8 turns | ✅ |
| 🟡 Medium | Dead end trap — 5 drones | ≤ 15 turns | ✅ |
| 🟡 Medium | Circular loop — 6 drones | ≤ 20 turns | ✅ |
| 🟡 Medium | Priority puzzle — 4 drones | ≤ 12 turns | ✅ |
| 🔴 Hard | Maze nightmare — 8 drones | ≤ 45 turns | ✅ |
| 🔴 Hard | Capacity hell — 12 drones | ≤ 60 turns | ✅ |
| 🔴 Hard | Ultimate challenge — 15 drones | ≤ 35 turns | ✅ |
| 🏆 Challenger | The Impossible Dream — 25 drones | Beat 45 turns | 🎯 |

---

## 📚 Resources & AI Usage

### References

- [Dijkstra's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Time-Expanded Networks for Multi-Agent Pathfinding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Python `heapq` module](https://docs.python.org/3/library/heapq.html)
- [Python `typing` module — Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

### 🤖 AI Usage

AI (GitHub Copilot — Claude Sonnet) was used throughout this project as a development assistant under the project's AI guidelines. All AI-generated content was reviewed, understood, and validated before integration.

| Task | AI Involvement |
|---|---|
| **Algorithm design** | Brainstorming time-expanded Dijkstra approach; all logic written and validated manually |
| **Docstring generation** | AI drafted docstrings; reviewed and corrected for accuracy against actual code |
| **Test scaffolding** | AI suggested test structure; all assertions written and verified manually |
| **Bug diagnosis** | AI helped identify root cause of capacity-check ordering issue in Dijkstra |
| **README structure** | AI drafted structure and content; reviewed for technical accuracy |
| **Code was not blindly copy-pasted** | Every AI suggestion was read, questioned, and tested before use |
