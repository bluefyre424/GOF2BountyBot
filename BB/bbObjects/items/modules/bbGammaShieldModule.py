from . import bbModule
from ....bbConfig import bbData
from .... import bbUtil

class bbGammaShieldModule(bbModule.bbModule):
    def __init__(self, name, aliases, effect=0, value=0, wiki="", manufacturer="", icon="", emoji=bbUtil.EMPTY_DUMBEMOJI, techLevel=-1, builtIn=False):
        super(bbGammaShieldModule, self).__init__(name, aliases, value=value, wiki=wiki, manufacturer=manufacturer, icon=icon, emoji=emoji, techLevel=techLevel, builtIn=builtIn)

        self.effect = effect

    
    def statsStringShort(self):
        return "*Gamma Shielding: " + ("+" if self.effect >= 1 else "-") + str(round(((self.effect - 1) * 100) if self.effect > 1 else (self.effect * 100))) + "%*"


    def getType(self):
        return bbGammaShieldModule

    
    def toDict(self):
        itemDict = super(bbGammaShieldModule, self).toDict()
        if not self.builtIn:
            itemDict["effect"] = self.effect
        return itemDict


def fromDict(moduleDict):
    return bbGammaShieldModule(moduleDict["name"], moduleDict["aliases"] if "aliases" in moduleDict else [], effect=moduleDict["effect"] if "effect" in moduleDict else 1,
                            value=moduleDict["value"] if "value" in moduleDict else 0, wiki=moduleDict["wiki"] if "wiki" in moduleDict else "",
                            manufacturer=moduleDict["manufacturer"] if "manufacturer" in moduleDict else "", icon=moduleDict["icon"] if "icon" in moduleDict else bbData.rocketIcon,
                            emoji=bbUtil.dumbEmojiFromStr(moduleDict["emoji"]) if "emoji" in moduleDict else bbUtil.EMPTY_DUMBEMOJI, techLevel=moduleDict["techLevel"] if "techLevel" in moduleDict else -1, builtIn=moduleDict["builtIn"] if "builtIn" in moduleDict else False)
