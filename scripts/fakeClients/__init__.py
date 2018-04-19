from ts3plugin import ts3plugin, PluginHost
from random import choice, getrandbits, randint
from bluscream import timestamp, sendCommand, random_string, loadBadges
import ts3defines, ts3lib

class fakeClients(ts3plugin):
    name = "Fake Clients"
    apiVersion = 21
    requestAutoload = False
    version = "1"
    author = "Bluscream"
    description = ""
    offersConfigure = False
    commandKeyword = "fc"
    infoTitle = None
    menuItems = []
    hotkeys = []

    def __init__(self):
        if PluginHost.cfg.getboolean("general", "verbose"): ts3lib.printMessageToCurrentTab("{0}[color=orange]{1}[/color] Plugin for pyTSon by [url=https://github.com/{2}]{2}[/url] loaded.".format(timestamp(), self.name, self.author))

    def processCommand(self, schid, command):
        clients = 1
        try: clients = int(command)
        except: pass
        self.clients = []
        # (err, clid) = ts3lib.getClientID(schid)
        # (err, cid) = ts3lib.getChannelOfClient(schid, clid)
        (err, clids) = ts3lib.getClientList(schid)
        self.clients.extend(clids)
        e, self.sgroup = ts3lib.getServerVariable(schid, ts3defines.VirtualServerPropertiesRare.VIRTUALSERVER_DEFAULT_SERVER_GROUP)
        e, acg = ts3lib.getServerVariable(schid, ts3defines.VirtualServerPropertiesRare.VIRTUALSERVER_DEFAULT_CHANNEL_GROUP)
        e, dcg = ts3lib.getServerVariable(schid, ts3defines.VirtualServerPropertiesRare.VIRTUALSERVER_DEFAULT_CHANNEL_ADMIN_GROUP)
        self.cgroups = [acg, dcg]
        timestamp, ret, badges = loadBadges()
        self.badges = []
        for badge in ret:
            self.badges.append(badge)
        for i in range(clients):
            cmd = "notifycliententerview"
            client = self.fakeClient(schid)
            for k in client:
                if client[k] != "":
                    cmd += " {}={}".format(k, client[k])
                else: cmd += " {}".format(k)
            sendCommand(self.name, cmd, schid, True, "-")
            self.clients.append(client["clid"])
        return True

    def fakeClient(self, schid):
        client = {}
        client["reasonid"] = "0"
        client["cfid"] = "0"
        (err, cids) = ts3lib.getChannelList(schid)
        cid = choice(cids)
        client["ctid"] = cid
        client["client_channel_group_id"] = choice(self.cgroups)
        client["client_servergroups"] = self.sgroup
        client["client_channel_group_inherited_channel_id"] = cid
        client["client_input_muted"] = randint(0,1)
        client["client_output_muted"] = randint(0,1)
        client["client_outputonly_muted"] = randint(0,1)
        client["client_input_hardware"] = randint(0,1)
        client["client_output_hardware"] = randint(0,1)
        client["client_is_recording"] = randint(0,1)
        client["client_talk_request"] = randint(0,1)
        client["client_type"] = 0 # randint(0,1)
        client["client_is_talker"] = randint(0,1)
        client["client_away"] = randint(0,1)
        client["client_is_channel_commander"] = randint(0,1)
        client["client_is_priority_speaker"] = randint(0,1)
        clid = randint(0,65000)
        while clid in self.clients:
            clid = randint(0, 65000)
        client["clid"] = clid
        client["client_database_id"] = randint(0,1000)
        client["client_talk_power"] = randint(0,99999)
        client["client_unread_messages"] = randint(0,10)
        client["client_needed_serverquery_view_power"] = 0 # randint(0,65000)
        client["client_icon_id"] = "0" # = randint(0,65000)
        client["client_unique_identifier"] = "{}=".format(random_string(27))
        client["client_nickname"] = random_string(randint(3,30))
        client["client_meta_data"] = random_string(randint(0,1)) # 30
        client["client_away_message"] = random_string(randint(0,10)) # 80
        client["client_flag_avatar"] = "" # = random_string(1)
        client["client_talk_request_msg"] = random_string(randint(0,50))
        client["client_description"] = random_string(randint(0,50))
        client["client_nickname_phonetic"] = random_string(randint(3,30))
        client["client_country"] = random_string(2).upper() # "DE" #
        client["client_badges"] = "overwolf={}:badges={}".format(randint(0,1), choice(self.badges)) # random_string(randint(0,30))
        return client