# distributed_werewolves

python3 -m venv venv
source ./venv/bin/activate

pip install -r requirements.txt

start 1 terminal for server
    python moderator.py

for each client start one terminal
    python host port

for 5 clients:

    python client.py localhost 18081
    python client.py localhost 18082
    python client.py localhost 18083
    python client.py localhost 18084
    python client.py localhost 18085