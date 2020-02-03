import sys, os, datetime
from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol

class QuarryProtocol(ServerProtocol):
    def player_joined(self):
        time = datetime.datetime.now()
        print("[", time.strftime("%H:%M:%S"), "][INFO] ", self.display_name, " has connected. Host=", self.remote_addr.host, sep='')
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

    factory = QuarryFactory()
    factory.motd = args.motd
    factory.max_players = max_players

    factory.listen(args.host, args.port)
    print("DowntimeProxy has started.")
    print("Host:" , args.host ,"Port:", args.port)
    print("Ctrl + C to close")
    reactor.run()

if __name__ == "__main__":
    main(sys.argv[1:])