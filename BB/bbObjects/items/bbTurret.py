from .bbItem import bbItem
from ...bbConfig import bbData
from ... import bbUtil

class bbTurret(bbItem):
    dps = 0.0

    def __init__(self, name, aliases, dps=0.0, value=0, wiki="", manufacturer="", icon="", emoji=bbUtil.EMPTY_DUMBEMOJI, techLevel=-1, builtIn=False):
        super(bbTurret, self).__init__(name, aliases, value=value, wiki=wiki, manufacturer=manufacturer, icon=icon, emoji=emoji, techLevel=techLevel, builtIn=builtIn)

        self.dps = dps

    
    def statsStringShort(self):
        return "*Dps: " + str(self.dps) + "*"


    def getType(self):
        return bbTurret

    def toDict(self):
        itemDict = super(bbTurret, self).toDict()
        if not self.builtIn:
            itemDict["dps"] = self.dps
        return itemDict


def fromDict(turretDict):
    if turretDict["builtIn"]:
        return bbData.builtInTurretObjs[turretDict["name"]]
    else:
        return bbTurret(turretDict["name"], turretDict["aliases"], dps=turretDict["dps"], value=turretDict["value"],
                        wiki=turretDict["wiki"] if "wiki" in turretDict else "", manufacturer=turretDict["manufacturer"] if "manufacturer" in turretDict else "",
                        icon=turretDict["icon"] if "icon" in turretDict else bbData.rocketIcon, emoji=bbUtil.dumbEmojiFromStr(turretDict["emoji"]) if "emoji" in turretDict else bbUtil.EMPTY_DUMBEMOJI,
                        techLevel=turretDict["techLevel"] if "techLevel" in turretDict else -1, builtIn=False)
