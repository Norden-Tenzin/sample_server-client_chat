from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory, connectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint
import uuid

class Server(Protocol):
    def __init__(self, users):
        self.users = users
        self.name = ""

    def add_user(self, user_name):
        if user_name not in self.users:
            self.users[self] = user_name
            self.name = user_name
        else:
            self.transport.write("Wrong username, try another".encode('utf-8'))
            
    def connectionMade(self):
        print("NEW CONNECTION MADE")
        user_name = uuid.uuid4()
        self.add_user(user_name)
    
    def dataReceived(self, data: bytes):
        data = data.decode('utf-8')
        
        # if not self.name:
        #     self.add_user(data)
        #     return
                
        for protocol in self.users.keys():
            if protocol != self:
                protocol.transport.write(f"{self.name}: {data}".encode('utf-8'))

    def connectionLost(self, reason = connectionDone):
        del self.users[self]

class ServerFactory(ServerFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Server(self.users)

if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 2000)
    endpoint.listen(ServerFactory())
    reactor.run()