from . import bbModule
from ....bbConfig import bbData
from .... import bbUtil

class bbCloakModule(bbModule.bbModule):
    def __init__(self, name, aliases, duration=0, value=0, wiki="", manufacturer="", icon="", emoji=bbUtil.EMPTY_DUMBEMOJI, techLevel=-1, builtIn=False):
        super(bbCloakModule, self).__init__(name, aliases, value=value, wiki=wiki, manufacturer=manufacturer, icon=icon, emoji=emoji, techLevel=techLevel, builtIn=builtIn)
        
        self.duration = duration

    
    def statsStringShort(self):
        return "Duration: " + str(self.duration) + "s" if self.duration != 0 else "No effect"

    
    def getType(self):
        return bbCloakModule

    
    def toDict(self):
        itemDict = super(bbCloakModule, self).toDict()
        if not self.builtIn:
            itemDict["duration"] = self.duration
        return itemDict


def fromDict(moduleDict):
    return bbCloakModule(moduleDict["name"], moduleDict["aliases"] if "aliases" in moduleDict else [], duration=moduleDict["duration"] if "duration" in moduleDict else 0,
                            value=moduleDict["value"] if "value" in moduleDict else 0, wiki=moduleDict["wiki"] if "wiki" in moduleDict else "",
                            manufacturer=moduleDict["manufacturer"] if "manufacturer" in moduleDict else "", icon=moduleDict["icon"] if "icon" in moduleDict else bbData.rocketIcon,
                            emoji=bbUtil.dumbEmojiFromStr(moduleDict["emoji"]) if "emoji" in moduleDict else bbUtil.EMPTY_DUMBEMOJI, techLevel=moduleDict["techLevel"] if "techLevel" in moduleDict else -1, builtIn=moduleDict["builtIn"] if "builtIn" in moduleDict else False)