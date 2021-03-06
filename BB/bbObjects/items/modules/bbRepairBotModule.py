from . import bbModule
from ....bbConfig import bbData
from .... import bbUtil

class bbRepairBotModule(bbModule.bbModule):
    def __init__(self, name, aliases, HPps=0, value=0, wiki="", manufacturer="", icon="", emoji=bbUtil.EMPTY_DUMBEMOJI, techLevel=-1, builtIn=False):
        super(bbRepairBotModule, self).__init__(name, aliases, value=value, wiki=wiki, manufacturer=manufacturer, icon=icon, emoji=emoji, techLevel=techLevel, builtIn=builtIn)

        self.HPps = HPps

    
    def statsStringShort(self):
        return "*HP/s: " + str(self.HPps) + "*"


    def getType(self):
        return bbRepairBotModule

    
    def toDict(self):
        itemDict = super(bbRepairBotModule, self).toDict()
        if not self.builtIn:
            itemDict["HPps"] = self.HPps
        return itemDict


def fromDict(moduleDict):
    return bbRepairBotModule(moduleDict["name"], moduleDict["aliases"] if "aliases" in moduleDict else [], HPps=moduleDict["HPps"] if "HPps" in moduleDict else 0,
                            value=moduleDict["value"] if "value" in moduleDict else 0, wiki=moduleDict["wiki"] if "wiki" in moduleDict else "",
                            manufacturer=moduleDict["manufacturer"] if "manufacturer" in moduleDict else "", icon=moduleDict["icon"] if "icon" in moduleDict else bbData.rocketIcon,
                            emoji=bbUtil.dumbEmojiFromStr(moduleDict["emoji"]) if "emoji" in moduleDict else bbUtil.EMPTY_DUMBEMOJI, techLevel=moduleDict["techLevel"] if "techLevel" in moduleDict else -1, builtIn=moduleDict["builtIn"] if "builtIn" in moduleDict else False)
