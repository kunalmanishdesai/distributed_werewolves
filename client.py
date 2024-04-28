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
    
    hostname = sys.argv[1]
    port = int(sys.argv[2])  # Ensure the port is an integer
    moderatorHostName = sys.argv[3]
    moderatorPort = int(sys.argv[4])  # Ensure the port is an integer

    # Create a threaded server for this client
    ts = ThreadedServer(Client_Receiver, hostname=hostname, port=port)
    server_thread = threading.Thread(target = ts.start)
    server_thread.start()

    # print("Client service started on hostname:", hostname," and port:", port)

    # moderatorHostName = "localhost"
    # moderatorPort = 18080

    # Create a client sender to communicate with the moderator

    client = Client_Sender(moderatorHostname, moderatorPort, hostname, port)


    input_thread = threading.Thread(target=input_loop, args=(client,))
    input_thread.start()

    #send connect to client    

    # while(True):

    #     # x = input(f"{client.getPlayerId()}: ")

    #     x = input()
    #     if x == "quit" : break

    #     client.send_command(x)
