# Multi-Elevator Simulation System

A concurrent elevator simulation system implemented in Python. This project demonstrates object-oriented design, asynchronous programming (concurrency without blocking), automated unit testing, client-server network architecture, and an intelligent dispatching algorithm.

---

## Features

1. **Basic Simulation (`elevator_basic.py`)**
   * Core implementation of the `Elevator` class with standard attributes and methods.
   * Concurrent and independent movement of multiple elevators using `asyncio`.
   * Real-time floor status tracking without blocking user inputs.
   * Realistic travel speed simulation (1 second per floor).

2. **Advanced Dispatching Server (`elevator_advanced.py`)**
   * Extends the system to support $N$ elevators serving the building simultaneously.
   * Features a smart **Hall Call** dispatching algorithm that automatically selects the optimal car to minimize passenger waiting time based on distance and current direction.
   * Functions as a centralized TCP server to handle multiple remote requests.

3. **Remote Control Client (`client_console.py`)**
   * A terminal-based user interface that connects remotely to the advanced server via TCP Sockets.
   * Real-time monitoring display that refreshes elevator statuses dynamically.

4. **Automated Testing (`test_elevator.py`)**
   * Comprehensive unit tests covering initial states, movement execution, and the decision-making logic of the dispatch algorithm.

---

## File Structure

```text
├── elevator_basic.py     # Independent dual-elevator manual simulator
├── elevator_advanced.py  # Centralized server with smart dispatching (N elevators)
├── client_console.py     # Remote monitoring and control interface
└── test_elevator.py      # Automated unit tests
```

## Getting Started

Prerequisites
•	Python 3.7 or higher (utilizes asyncio)
### 1. Running the Basic Simulator
To demonstrate the core multi-elevator concurrent movement via standard manual inputs, run the basic version directly:
```
python elevator_basic.py
```

**How to interact:**

  * The console will display the current positions of the elevators.
  *	Enter commands in the format: ElevatorID,CurrentFloor,TargetFloor (e.g., 1,1,5 instructs Elevator 1 to pick up a passenger at 1F and deliver them to 5F).
  *	Since the system is non-blocking, you can issue another command to a different elevator while the first one is still in motion.

### 2. Running the Client-Server Architecture with Smart Dispatching
To demonstrate the networked application along with the intelligent routing algorithm, follow these steps using two separate terminal windows:
  * Step 1: Start the Central Server
```
python elevator_advanced.py
```

(The server will initialize ‭$N$‬ elevators and start listening for connections.)
  * Step 2: Start the Remote Client Panel
```
python client_console.py
```

(The client will connect to the server and display a live status monitor.)
How to interact:
•	In the client terminal, simply enter the travel request as FromFloor,ToFloor (e.g., 3,8 means a passenger calls for an elevator at 3F to go to 8F).
•	The central system will automatically calculate the optimal elevator to assign, while the client monitor updates all floor levels dynamically in real-time.
### 3. Running Unit Tests
To execute the automated test suite and verify system logic:
```
python test_elevator.py
```
