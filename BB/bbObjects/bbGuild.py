from . import bbShop
from .bounties.bountyBoards import BountyBoardChannel
from ..userAlerts import UserAlerts

class bbGuild:
    def __init__(self, id, announceChannel=-1, playChannel=-1, shop=None, bountyBoardChannel=None, alertRoles={}, ownedRoleMenus=0):
        if type(id) == float:
            id = int(id)
        elif type(id) != int:
            raise TypeError("id must be int, given " + str(type(id)))

        if type(announceChannel) == float:
            announceChannel = int(announceChannel)
        elif type(announceChannel) != int:
            raise TypeError("announceChannel must be int, given " + str(type(announceChannel)))

        if type(playChannel) == float:
            playChannel = int(playChannel)
        elif type(playChannel) != int:
            raise TypeError("playChannel must be int, given " + str(type(playChannel)))
        
        if shop is not None and type(shop) != bbShop.bbShop:
            raise TypeError("shop must be bbShop, given " + str(type(shop)))

        self.id = id
        self.announceChannel = announceChannel
        self.playChannel = playChannel

        self.shop = bbShop.bbShop() if shop is None else shop
        
        self.alertRoles = {}
        for alertID in UserAlerts.userAlertsIDsTypes.keys():
            if issubclass(UserAlerts.userAlertsIDsTypes[alertID], UserAlerts.GuildRoleUserAlert):
                self.alertRoles[alertID] = alertRoles[alertID] if alertID in alertRoles else -1
        
        self.bountyBoardChannel = bountyBoardChannel
        self.hasBountyBoardChannel = bountyBoardChannel is not None
        self.ownedRoleMenus = ownedRoleMenus


    def getAnnounceChannelId(self):
        if not self.hasAnnounceChannel():
            raise ValueError("This guild has no announce channel set")
        return self.announceChannel


    def getPlayChannelId(self):
        if not self.hasPlayChannel():
            raise ValueError("This guild has no play channel set")
        return self.playChannel


    def setAnnounceChannelId(self, announceChannelId):
        self.announceChannel = announceChannelId


    def setPlayChannelId(self, playChannelId):
        self.playChannel = playChannelId
    

    def hasAnnounceChannel(self):
        return self.announceChannel != -1


    def hasPlayChannel(self):
        return self.playChannel != -1


    def removePlayChannel(self):
        if not self.hasPlayChannel():
            raise ValueError("Attempted to remove play channel on a bbGuild that has no playChannel")
        self.playChannel = -1

    
    def removeAnnounceChannel(self):
        if not self.hasAnnounceChannel():
            raise ValueError("Attempted to remove announce channel on a bbGuild that has no announceChannel")
        self.announceChannel = -1



    def getUserAlertRoleID(self, alertID):
        return self.alertRoles[alertID]


    def setUserAlertRoleID(self, alertID, roleID):
        self.alertRoles[alertID] = roleID


    def removeUserAlertRoleID(self, alertID):
        self.alertRoles[alertID] = -1

    
    def hasUserAlertRoleID(self, alertID):
        if alertID in self.alertRoles:
            return self.alertRoles[alertID] != -1
        raise KeyError("Unknown GuildRoleUserAlert ID: " + alertID)


    
    async def addBountyBoardChannel(self, channel, client, factions):
        if self.hasBountyBoardChannel:
            raise RuntimeError("Attempted to assign a bountyboard channel for guild " + str(self.id) + " but one is already assigned")
        self.bountyBoardChannel = BountyBoardChannel.BountyBoardChannel(channel.id, {}, -1)
        await self.bountyBoardChannel.init(client, factions)
        self.hasBountyBoardChannel = True

    
    def removeBountyBoardChannel(self):
        if not self.hasBountyBoardChannel:
            raise RuntimeError("Attempted to remove a bountyboard channel for guild " + str(self.id) + " but none is assigned")
        self.bountyBoardChannel = None
        self.hasBountyBoardChannel = False


    def toDictNoId(self):
        return {"announceChannel":self.announceChannel, "playChannel":self.playChannel, 
                "bountyBoardChannel": self.bountyBoardChannel.toDict() if self.hasBountyBoardChannel else None,
                "alertRoles": self.alertRoles,
                "shop": self.shop.toDict(),
                "ownedRoleMenus": self.ownedRoleMenus
                }


def fromDict(id, guildDict):
    # # old format conversion code
    # if "bountyNotifyRoleId" in guildDict:
    #     alertRoles = {"bounties_new": guildDict["bountyNotifyRoleId"]}
    #     if "shopRefreshRoleId" in guildDict:
    #         alertRoles["shop_refresh"] = guildDict["shopRefreshRoleId"]
    #     if "systemUpdatesMajorRoleId" in guildDict:
    #         alertRoles["system_updates_major"] = guildDict["systemUpdatesMajorRoleId"]
    #     if "systemUpdatesMinorRoleId" in guildDict:
    #         alertRoles["system_updates_minor"] = guildDict["systemUpdatesMinorRoleId"]
    #     if "systemMiscRoleId" in guildDict:
    #         alertRoles["system_misc"] = guildDict["systemMiscRoleId"]
    #     return bbGuild(id, announceChannel=guildDict["announceChannel"], playChannel=guildDict["playChannel"], shop=bbShop.fromDict(guildDict["shop"]) if "shop" in guildDict else bbShop.bbShop(), bountyBoardChannel=guildDict["bountyBoardChannel"] if "bountyBoardChannel" in guildDict else -1,
    #                     alertRoles=alertRoles)
    # else:
    # new format code
    return bbGuild(id, announceChannel=guildDict["announceChannel"], playChannel=guildDict["playChannel"],
                    shop=bbShop.fromDict(guildDict["shop"]) if "shop" in guildDict else bbShop.bbShop(),
                    bountyBoardChannel=BountyBoardChannel.fromDict(guildDict["bountyBoardChannel"]) if "bountyBoardChannel" in guildDict and guildDict["bountyBoardChannel"] != -1 else None,
                    alertRoles=guildDict["alertRoles"] if "alertRoles" in guildDict else {}, ownedRoleMenus=guildDict["ownedRoleMenus"] if "ownedRoleMenus" in guildDict else 0)
