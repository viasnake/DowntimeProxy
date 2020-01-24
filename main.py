from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol

class QuarryProtocol(ServerProtocol):
    def player_joined(self):
        ServerProtocol.player_joined(self)
        self.close("Disconnect")

class QuarryFactory(ServerFactory):
    protocol = QuarryProtocol

def main(arg):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--host", default="")
    parser.add_argument("-p", "--port", default=25565, type=int)
    parser.add_argument("-m", "--message", default="A Minecraft server")
    args = parser.parse_args(arg)

    factory = QuarryFactory()
    factory.motd = args.message
    factory.max_players = 1

    factory.listen(args.host, args.port)
    reactor.run()

import sys
main(sys.argv[1:])