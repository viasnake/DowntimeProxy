# -*- coding: utf-8 -*-

import sys, os, datetime
from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol

HOST = "0.0.0.0"
PORT = 25565
MOTD = "A Minecraft server"
MAX_PLAYERS = 20
SERVER_ICON = None
KICK_MESSAGE = "Disconnect"

class QuarryProtocol(ServerProtocol):
    def player_joined(self):
        time = datetime.datetime.now()
        self.logger.info("%s has connected." % (self.display_name))
        self.close(KICK_MESSAGE)

class QuarryFactory(ServerFactory):
    protocol = QuarryProtocol

def config(path):
    import configparser, re
    config = configparser.ConfigParser()

    if not os.path.exists(path):
        config["setting"] = {}
        config["setting"]["host"] = "0.0.0.0"
        config["setting"]["port"] = "25565"
        config["setting"]["motd"] = r"A Minecraft server\n&bDowntimeProxy"
        config["setting"]["max_players"] = "20"
        config["messages"] = {}
        config["messages"]["kick"] = "Disconnect by DowntimeProxy"
        with open("server.ini", "w") as f:
            config.write(f)

    config.read(path, encoding="utf-8")
    if config.has_option("setting", "host"):
        HOST = config["setting"]["host"]
    if config.has_option("setting", "port") and re.match("[1-65534]", config["setting"]["port"]):
        PORT = int(config["setting"]["port"])
    if config.has_option("setting", "motd"):
        MOTD = str(config["setting"]["motd"])
    if config.has_option("setting", "max_players") and re.match("[1-2147483647]", config["setting"]["port"]):
        MAX_PLAYERS = int(config["setting"]["max_players"])
    if config.has_option("setting", "server-icon"):
        SERVER_ICON = str(config["setting"]["server-icon"])
    if config.has_option("messages", "kick"):
        KICK_MESSAGE = str(config["messages"]["kick"])

    MOTD = MOTD.replace("&","§")
    MOTD = MOTD.replace(r"\n","\n")
    KICK_MESSAGE = KICK_MESSAGE.replace("&","§")
    KICK_MESSAGE = KICK_MESSAGE.replace(r"\n","\n")

def main():
    config("server.ini")

    factory = QuarryFactory()
    factory.motd = MOTD
    factory.max_players = MAX_PLAYERS
    factory.icon_path = SERVER_ICON

    factory.listen(HOST, PORT)
    print("DowntimeProxy has started.")
    print("Host:" , HOST ,"Port:", PORT)
    print("Ctrl + C to close")
    reactor.run()

if __name__ == "__main__":
    main()
