import sys

from twisted.python import log
from twisted.internet import reactor

from autobahn.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampClientProtocol

# maybe use RSS? https://github.com/organizations/Betterment/betterdan.private.atom?token=(get a token)
from github import Github

class GithubClient(WampClientProtocol):
    def __init__(self):
        self.ghub = Github('########', '########')
        self.user = self.ghub.get_user()
        self.bment = self.ghub.get_organization('Betterment')

    def onSessionOpen(self):
        self.feed()

    def feed(self):
        for item in self.getNewItems():
            self.publish('http://example.com/github', item)
        reactor.callLater(2, self.feed)

    def getNewItems(self):
        allowed_events = [
            'commit_comment', 'delete', 'member', 'push',
            'pull_request', 'pull_request_review_comment']

        events = self.user.get_organization_events(self.bment)
        if events:
            result = []
            for event in events:
                if event.type in allowed_events:
                    result.append({
                        'user': event.actor.login,
                        'repo': event.repo.name,
                        'payload': event.payload
                    })
            return result

        return []

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'

    factory = WampClientFactory('ws://localhost:9000', debugWamp = debug)
    factory.protocol = GithubClient

    connectWS(factory)

    reactor.run()
