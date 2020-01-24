DowntimeProxy
=============
Minecraft downtime proxy
------------------------
DowntimeProxy is a standalone Minecraft server.

Running the exe will launch a separate Minecraft server. The player cannot connect to the server and receives a kick message. Therefore, it can be used as a lightweight server that only responds to pings in the server list.

### Configuration
The configuration file is server.ini generated in the same root as the exe.
```
[setting]
host = 0.0.0.0
port = 25565
motd = A Minecraft server\n&bDowntimeProxy
max_players = 20

[messages]
kick = Disconnect by DowntimeProxy
```

### Source code
The source code is published on GitHub. The license is Apache License 2.0.

This software includes the Python library [Quarry](https://github.com/barneygale/quarry). 
