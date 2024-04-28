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
