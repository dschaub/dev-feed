import sys

from twisted.python import log
from twisted.internet import reactor

from autobahn.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampClientProtocol

class PubSubClient(WampClientProtocol):
    def onSessionOpen(self):
        self.sendSimpleEvent()

    def sendSimpleEvent(self):
        self.publish('http://example.com/github', "Whatup!")
        reactor.callLater(2, self.sendSimpleEvent)

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'

    factory = WampClientFactory('ws://localhost:9000', debugWamp = debug)
    factory.protocol = PubSubClient

    connectWS(factory)

    reactor.run()
