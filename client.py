#Author: Kunal Desai
#Distributed Werewolves
#Updated by: Aksa Elizabeth Sunny
#Collaborators: Ailun Pei, Akhil Jose, Aksa Elizabeth Sunny

#Copyright (c) 2012 Ailun Pei, Akhil Jose, Aksa Elizabeth Sunny, Kunal Desai 
#This file is part of Distributed Werewolves Game.

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
import threading
import sys


class Client_Receiver(rpyc.Service) :

    def on_connect(self,conn):
        pass

    def on_disconnect(self,conn):
        pass

    def exposed_print(self,s):
        print(s)


class Client_Sender():

    def __init__(self, moderatorHostName, moderatorPort, clientHost, clientPort): 
        self.conn = rpyc.connect(moderatorHostName, moderatorPort)
        self.host = clientHost
        self.port = clientPort

        self.connection_id = f"{clientHost}:{clientPort}"

        self.player_id,self.token = self.conn.root.connect(self.host,self.port)
    

    def getPlayerId(self):
        return self.player_id
    
    def send_command(self, command):
        self.conn.root.command(self.connection_id, self.token,command)


def input_loop(client):
    while True:
        x = input()
        if x == "quit":
            break
        client.send_command(x)
    
if __name__ == "__main__" :
    
    if len(sys.argv) < 4:
        print("Usage: python client.py <client_port> <moderator_IP> <moderator_port>")
        sys.exit(1)

    # Bind to all interfaces
    hostname = '0.0.0.0'
    port = int(sys.argv[1])  # Convert the first argument to integer for the port

    # IP and port of the moderator (server)
    moderatorHostName = sys.argv[2]
    moderatorPort = int(sys.argv[3])

    # Create a threaded server for this client
    ts = ThreadedServer(Client_Receiver, hostname=hostname, port=port)
    server_thread = threading.Thread(target = ts.start)
    server_thread.start()

    # print("Client service started on hostname:", hostname," and port:", port)

    # moderatorHostName = "localhost"
    # moderatorPort = 18080

    # Create a client sender to communicate with the moderator

    client = Client_Sender(moderatorHostName, moderatorPort, hostname, port)


    input_thread = threading.Thread(target=input_loop, args=(client,))
    input_thread.start()

    #send connect to client    

    # while(True):

    #     # x = input(f"{client.getPlayerId()}: ")

    #     x = input()
    #     if x == "quit" : break

    #     client.send_command(x)
