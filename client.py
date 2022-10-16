from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

class Client(Protocol):
    def __init__(self): 
        reactor.callInThread(self.send_data)

    def connectionMade(self):
        print("Whats your name?")
        # name = input()

    def dataReceived(self, data: bytes):
        print(data.decode('utf-8'))

    def send_data(self):
        while True:
            data = input(":")
            self.transport.write(data.encode('utf-8'))

class ClientFactory(ReconnectingClientFactory):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print("IN FAILED")
        print(reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print("IN LOST")
        print(reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 2000)
    endpoint.connect(ClientFactory())
    reactor.run()