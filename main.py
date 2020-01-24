import sys, os
from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol

class QuarryProtocol(ServerProtocol):
    def player_joined(self):
        self.close(kick_message)

class QuarryFactory(ServerFactory):
    protocol = QuarryProtocol

def config(path):
    import configparser, re
    config = configparser.ConfigParser()

    if not os.path.exists(path) :
        config.add_section("setting")
        config.set("setting", "host", "0.0.0.0")
        config.set("setting", "port", 25565)
        config.set("setting", "motd", "A Minecraft server\n&bDowntimeProxy")
        config.set("setting", "max_players", "20")

        config.add_section("messages")
        config.set("messages", "kick", "Disconnect by DowntimeProxy")
 
        with open("server.ini", "w") as config_file:
            config.write(config_file)
    
    global host, port, motd, max_players, kick_message

    host = "0.0.0.0"
    port = 25565
    motd = "A Minecraft server"
    max_players = 20
    kick_message = "Disconnect"

    config.read(path, encoding="utf-8")
    if config.has_option("setting", "host"):
        host = config["setting"]["host"]
    if config.has_option("setting", "port") and re.match("[1-65534]", config["setting"]["port"]):
        port = int(config["setting"]["port"])
    if config.has_option("setting", "motd"):
        motd = config["setting"]["motd"]
    if config.has_option("setting", "max_players") and re.match("[1-2147483647]", config["setting"]["port"]):
        max_players = int(config["setting"]["max_players"])
    if config.has_option("messages", "kick"):
        kick_message = config["messages"]["kick"]

    motd = motd.replace("&","§")
    motd = motd.replace(r"\n","\n")
    kick_message = kick_message.replace("&","§")
    kick_message = kick_message.replace(r"\n","\n")

def main(arg):
    config("server.ini")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--host", default=host)
    parser.add_argument("-p", "--port", default=port, type=int)
    parser.add_argument("-m", "--motd", default=motd)
    args = parser.parse_args(arg)

    factory = QuarryFactory()
    factory.motd = args.motd
    factory.max_players = max_players

    factory.listen(args.host, args.port)
    print("DowntimeProxy has started.")
    print("Host:" , args.host ,"Port:", args.port)
    print("Ctrl + C to close")
    reactor.run()
    print("Bye :)")

if __name__ == "__main__":
    main(sys.argv[1:])