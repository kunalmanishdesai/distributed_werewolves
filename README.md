# Distributed Werewolves Game

## Contributors
- Kunal Desai
- Akhil Jose
- Ailun Pei
- Aksa Elizabeth Sunny

## Implementation
This project is a distributed implementation of the Werewolves game. We have refactored communications to be based on Remote Procedure Calls (RPC), enhancing the game's network efficiency and responsiveness.

## Prerequisites
- Python 3.x
- pip
- virtualenv

## Setup Instructions

### 1. Environment Setup
Create and activate a virtual environment to manage dependencies locally:

```bash
python3 -m venv venv
source ./venv/bin/activate
```

### 2. Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Moderator (Server)
Start the server by running the moderator script in a terminal:

```bash
python moderator.py
```

### 4. Run the Clients
Open a new terminal for each client. Use the following command to start a client, replacing `host` and `port` with the appropriate values. Example for starting five clients:

```bash
python client.py localhost 18081
python client.py localhost 18082
python client.py localhost 18083
python client.py localhost 18084
python client.py localhost 18085
```

### 5. Play the Game
Follow the in-game prompts on each client terminal to play the game.

## Notes
Ensure all terminals (for both moderator and clients) are running within the environment where the dependencies have been installed. If you encounter any issues, verify that the Python version and dependencies are correctly installed and up-to-date.

