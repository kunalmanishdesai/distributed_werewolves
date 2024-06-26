#Author: Akhil Jose
#Distributed Werewolves
#Collaborators: Kunal Desai

#Copyright (c) 2024 Ailun Pei, Akhil Jose, Aksa Elizabeth Sunny, Kunal Desai 
#This file is part of istributed Werewolves Game.

#Distributed Werewolves is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#Distributed Werewolves is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Virtual werewolf.  If not, see <http://www.gnu.org/licenses/>.

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
python3 moderator.py
```

### 4. Run the Clients
Open a new terminal for each client. Use the following command to start a client, replacing `host` and `port` with the appropriate values. Example for starting five clients:

```bash
python3 client.py localhost 18081
python3 client.py localhost 18082
python3 client.py localhost 18083
python3 client.py localhost 18084
python3 client.py localhost 18085
```

### 5. Play the Game
Follow the in-game prompts on each client terminal to play the game.

## Special Instructions for Ubuntu 22.04.4 LTS

### Installing Python and pip
If you are running the game on Ubuntu 22.04.4 LTS, ensure you have Python and pip installed. If pip is not installed, you can install it using the following command:

```bash
sudo apt install python3-pip
```

## Notes
Ensure all terminals (for both moderator and clients) are running within the environment where the dependencies have been installed. If you encounter any issues, verify that the Python version and dependencies are correctly installed and up-to-date.

## Licensing
This project is licensed under the GNU General Public License (GPL), version 3 or later, allowing redistribution and modification under the terms specified by the Free Software Foundation. 

The project is provided "as is," without any warranty, including implied warranties of merchantability or fitness for a particular purpose. For more details, see the full GPL at [GNU's website](http://www.gnu.org/licenses/).

Additionally, the use of this code is permitted for future academic courses, unless otherwise stated here.

Copyright (c) 2012 Ailun Pei, Akhil Jose, Aksa Elizabeth Sunny, and Kunal Desai


