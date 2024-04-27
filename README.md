# Distributed Werewolves
Contributors: Kunal Desai, Akhil Jose, Ailun Pei, Aksa Elizabeth Sunny

## Implementation
We have refactored communcations to be based on RPC for the distributed werewolved implementation.

## Steps to run
1. Run the following commands on each terminal you use (Moderator and Clients)
```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

2. Run moderator (server) on one terminal.
```
python moderator.py
```

3. For each client start a new terminal.
Client command syntax:
```
python client.py host port
```
Eg: For 5 clients:

```
python client.py localhost 18081
python client.py localhost 18082
python client.py localhost 18083
python client.py localhost 18084
```

4. Play the game.
    python client.py localhost 18085
