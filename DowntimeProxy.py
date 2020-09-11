# -*- coding: utf-8 -*-

import sys, os, datetime
from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol

class QuarryProtocol(ServerProtocol):
    def player_joined(self):
        time = datetime.datetime.now()
        self.logger.info("%s has connected." % (self.display_name))
        self.close(kick_message)

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

    global host, port, motd, max_players, server_icon, kick_message

    host = "0.0.0.0"
    port = 25565
    motd = "A Minecraft server"
    max_players = 20
    server_icon = None
    kick_message = "Disconnect"

    config.read(path, encoding="utf-8")
    if config.has_option("setting", "host"):
        host = config["setting"]["host"]
    if config.has_option("setting", "port") and re.match("[1-65534]", config["setting"]["port"]):
        port = int(config["setting"]["port"])
    if config.has_option("setting", "motd"):
        motd = str(config["setting"]["motd"])
    if config.has_option("setting", "max_players") and re.match("[1-2147483647]", config["setting"]["port"]):
        max_players = int(config["setting"]["max_players"])
    if config.has_option("setting", "server-icon"):
        server_icon = str(config["setting"]["server-icon"])
    if config.has_option("messages", "kick"):
        kick_message = str(config["messages"]["kick"])

    motd = motd.replace("&","§")
    motd = motd.replace(r"\n","\n")
    kick_message = kick_message.replace("&","§")
    kick_message = kick_message.replace(r"\n","\n")

def main():
    config("server.ini")

    factory = QuarryFactory()
    factory.motd = motd
    factory.max_players = max_players
    factory.icon_path = server_icon

    factory.listen(host, port)
    print("DowntimeProxy has started.")
    print("Host:" , host ,"Port:", port)
    print("Ctrl + C to close")
    reactor.run()

if __name__ == "__main__":
    main()
