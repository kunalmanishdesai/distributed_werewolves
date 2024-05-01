#Author: Kunal Desai
#Distributed Werewolves
#Updated and tested by: Ailun Pei, Aksa Elizabeth Sunny
#Collaborators: Ailun Pei, Akhil Jose, Aksa Elizabeth Sunny

#Copyright (c) 2012 Ailun Pei, Akhil Jose, Aksa Elizabeth Sunny, Kunal Desai 
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

import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.core.protocol import Connection
from datetime import datetime, timedelta
from uuid import uuid4
import threading
import time
import random
from collections import Counter

startTime = datetime.now()

time_for_each_step = 30

class Moderator(rpyc.Service) :

    def __init__(self) -> None:
        super().__init__()
        self.player_count = 0
        self.clients_connected = {}
        self.player_ids = {}
        self.killed = []
    
    def start(self):
        self.votes = {}
        self.didSomeOneDie = False
        self.death_speech_phase = False
        self.werewolves_vote_phase = False
        self.werewolves_disccusion_phase = False
        self.town_people_disccusion_phase = False
        self.town_people_vote_phase = False

        
    def get_next_player_id(self):
        self.player_count += 1
        return f"player_{self.player_count}"

    def on_connect(self,conn: Connection):
        pass

    def on_disconnect(self,conn):
        pass

    def select_werewolves(self):

        num_werewolves = 1

        client_ids = list(self.clients_connected.keys())
        

        werewolf_ids = random.sample(client_ids, num_werewolves)
        self.werewolves = {client_id: self.clients_connected[client_id] for client_id in werewolf_ids}
        self.towns_people = {client_id: self.clients_connected[client_id] for client_id in self.clients_connected if client_id not in self.werewolves}

        self.broadcast("You are a werewolf",self.werewolves)
        self.broadcast_to_towns_people("You are a town person")


    def broadcast_to_werewolves(self,connection_id,s):
        self.broadcast_except_one(connection_id,s,self.werewolves)
    
    def broadcast_to_towns_people(self,s):
        self.broadcast(s,self.towns_people)

    def exposed_connect(self,host_name, port) -> str:

        connection_id = f"{host_name}:{port}"

        if datetime.now() - startTime >= timedelta(seconds=60): 
            return None
        
        elif connection_id in self.clients_connected: 
            return self.clients_connected[connection_id]
        else:

            player_id = self.get_next_player_id()
            token = uuid4()

            self.player_ids[player_id]  = (connection_id,token)
            self.clients_connected[connection_id] = (player_id,token)

            self.broadcast(f"{player_id} has joined")
            return self.clients_connected[connection_id]


    def exposed_command(self, connection_id, token, s):

        if connection_id not in self.clients_connected:
            self.send_single_message(connection_id, "Cannot send msg without authentication")
        
        elif self.clients_connected[connection_id][1] != token :
            self.send_single_message(connection_id, "Wrong token")
        
        elif self.death_speech_phase == True:

            if self.clients_connected[connection_id][0] == self.killed[-1]:
                self.broadcast_except_one(connection_id, s)
            elif self.clients_connected[connection_id][0] in self.killed:
                self.send_single_message(connection_id, "You cannot participate, you are dead")

        elif self.clients_connected[connection_id][0] in self.killed :
            self.send_single_message(connection_id, "You cannot participate, you are dead")
        
        elif self.werewolves_disccusion_phase and connection_id in self.werewolves :
            self.broadcast_to_werewolves(connection_id,s)
        
        elif self.werewolves_vote_phase and connection_id in self.werewolves:
            self.vote(connection_id,s)
        
        elif self.town_people_disccusion_phase:
            self.broadcast_except_one(connection_id,s)

        elif self.town_people_vote_phase:
            self.town_people_vote(connection_id,s)
        else :
            self.send_single_message(connection_id,"You cannot participate now, wait for your turn")


    def vote(self, connection_id, s):

        voter_id = self.clients_connected[connection_id]

        if s not in self.player_ids : 
            self.send_single_message(connection_id,"No such player")
        elif s in self.killed:
            self.send_single_message(connection_id, "Player {s} already killed")
        elif connection_id in self.votes :
            self.send_single_message(connection_id,"You have already voted")
        else:
            self.votes[connection_id] = s
            self.broadcast_to_werewolves(connection_id,f"Wolf {voter_id[0]} voted {s}")

    
    def town_people_vote(self, connection_id, s):

        voter_id = self.clients_connected[connection_id]

        if s not in self.player_ids : 
            self.send_single_message(connection_id,"No such player")
        elif s in self.killed:
            self.send_single_message(connection_id, "Player {s} already killed")
        elif connection_id in self.votes :
            self.send_single_message(connection_id,"You have already voted")
        else:
            self.votes[connection_id] = s
            self.broadcast_except_one(connection_id,f"Town person {voter_id[0]} voted {s}")

    def send_single_message(self,connection_id, msg) :
        client_host_name, client_port = connection_id.split(":")

        conn = rpyc.connect(client_host_name,client_port)
        conn.root.print(msg)



    def broadcast_except_one(self,except_connection_id,s,players= None):

        if players == None :
            players = self.clients_connected

        s = f"{players[except_connection_id][0]}: {s}"

        print(s)
        for connection_id in players:
            if connection_id != except_connection_id :
                self.send_single_message(connection_id,s)


    def start_werewolves_disccusion(self):
        self.werewolves_disccusion_phase = True
        self.broadcast("Time for werevoles to discuss")

    def end_werewolves_disccusion(self):
        self.werewolves_disccusion_phase = False
        self.broadcast("Time for werevoles to discuss ended")

    def start_werewolves_vote_session(self):
        self.werewolves_vote_phase = True
        self.broadcast("Time for werevoles to vote")
    
    def end_werewolves_vote_session(self):
        self.werewolves_vote_phase = False
        self.broadcast("Time for werevoles to vote ended")

        vote_counts = Counter(list(self.votes.values()))
        self.votes = {}

        most_voted_player = vote_counts.most_common()

        if (len(most_voted_player) == 0) or len(most_voted_player) > 1 and most_voted_player[0][1] == most_voted_player[1][1]:
            self.broadcast("Vote was tied\n No one was killed.")
        else:

            self.didSomeOneDie = True
            player_id = most_voted_player[0][0]
            connection_id = self.player_ids[player_id][0]

            self.killed.append(player_id)
            
            if (connection_id in self.werewolves) :
                del self.werewolves[connection_id]
            
            if (connection_id in self.towns_people) :
                del self.towns_people[connection_id]
            
            # self.send_single_message(connection_id, "You were killed")
            self.broadcast(f"{player_id} was killed")
    

    def start_town_people_disccusion(self):
        self.town_people_disccusion_phase = True
        self.broadcast("Time for town people to discuss")

    def end_town_people_disccusion(self):
        self.town_people_disccusion_phase = False
        self.broadcast("Time for werevoles to discuss ended")

    def start_town_people_vote_session(self):
        self.town_people_vote_phase = True
        self.broadcast("Time for town people to vote")
    
    def end_town_people_vote_session(self):
        self.town_people_vote_phase = False
        self.broadcast("Time for town people to vote ended")

        vote_counts = Counter(list(self.votes.values()))
        self.votes = {}

        most_voted_player = vote_counts.most_common()

        if  (len(most_voted_player) == 0) or len(most_voted_player) > 1 and most_voted_player[0][1] == most_voted_player[1][1]:
            self.broadcast("Vote was tied\n No one was killed.")
        else:

            self.didSomeOneDie = True
            player_id = most_voted_player[0][0]
            connection_id = self.player_ids[player_id][0]

            self.killed.append(player_id)

            if (connection_id in self.werewolves) :
                del self.werewolves[connection_id]
                self.broadcast(f"{player_id} was killed.{player_id} was a werewolf")
            
            if (connection_id in self.towns_people):
                del self.towns_people[connection_id]
                self.broadcast(f"{player_id} was killed.{player_id} was a towns person")

            # self.send_single_message(connection_id, "You were killed")
            
    

    def start_death_speech(self):
        self.death_speech_phase = True
        self.broadcast("Time for died player to give speech")


    def end_death_speech(self):
        self.death_speech_phase = False
        self.didSomeOneDie = False

    def broadcast(self,s,players= None):

        s = f"Moderator: {s}"
        print(s)
        
        if (players == None) :
            players = self.clients_connected
        
        for connection_id in players:
            self.send_single_message(connection_id,s)
    
if __name__ == '__main__':
    try:
        hostname = 'localhost'
        port = 18080

        moderator_instance = Moderator()
        ts = ThreadedServer(moderator_instance, hostname=hostname, port=port)
        server_thread = threading.Thread(target = ts.start)
        server_thread.start()

        moderator_instance.broadcast("Waiting for clients to join")

        time.sleep(time_for_each_step)

        # print("Moderator service started on hostname and port ", ts.host, port)

        # moderator_instance.broadcast("Werewolves are decided")
        moderator_instance.select_werewolves()
        

        while(len(moderator_instance.werewolves) != 0 and len(moderator_instance.werewolves) < len(moderator_instance.towns_people)): 

            moderator_instance.start()
            moderator_instance.start_werewolves_disccusion()

            time.sleep(time_for_each_step)

            moderator_instance.end_werewolves_disccusion()

            moderator_instance.start_werewolves_vote_session()

            time.sleep(time_for_each_step)

            moderator_instance.end_werewolves_vote_session()

            if len(moderator_instance.werewolves) == 0 or len(moderator_instance.werewolves) >= len(moderator_instance.towns_people):
                break

            if (moderator_instance.didSomeOneDie) :
                moderator_instance.start_death_speech()
                time.sleep(time_for_each_step)
                moderator_instance.end_death_speech()
            

            moderator_instance.start_town_people_disccusion()

            time.sleep(time_for_each_step)

            moderator_instance.end_town_people_disccusion()

            moderator_instance.start_town_people_vote_session()

            time.sleep(time_for_each_step)

            moderator_instance.end_town_people_vote_session()

            if len(moderator_instance.werewolves) == 0 or len(moderator_instance.werewolves) >= len(moderator_instance.towns_people):
                break

            if (moderator_instance.didSomeOneDie) :
                moderator_instance.start_death_speech()
                time.sleep(15)
                moderator_instance.end_death_speech()
        
        if (len(moderator_instance.werewolves) == 0) :
            moderator_instance.broadcast("Towns people win")
        else:
            moderator_instance.broadcast("Werewolves win")

    except KeyboardInterrupt:
        print("Interrupt received! Closing server...")
        ts.close()  # Properly close the server if supported
        server_thread.join(timeout=1)  # Wait a bit for thread to finish
        print("Server closed.")