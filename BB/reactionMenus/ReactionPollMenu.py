from . import ReactionMenu
from ..bbConfig import bbConfig
from .. import bbGlobals, bbUtil
from discord import Colour, NotFound, HTTPException, Forbidden, Emoji, PartialEmoji
from datetime import datetime
from ..scheduling import TimedTask
from ..logging import bbLogger


async def printAndExpirePollResults(msgID):
    menu = bbGlobals.reactionMenusDB[msgID]
    menuMsg = await menu.msg.channel.fetch_message(menu.msg.id)
    results = {}

    if menu.owningBBUser is not None:
        menu.owningBBUser.pollOwned = False

    maxOptionLen = 0
    
    for option in menu.options.values():
        results[option] = []
        if len(option.name) > maxOptionLen:
            maxOptionLen = len(option.name)

    for reaction in menuMsg.reactions:
        if type(reaction.emoji) in [Emoji, PartialEmoji]:
            currentEmoji = bbUtil.dumbEmoji(id=reaction.emoji.id)
        else:
            currentEmoji = bbUtil.dumbEmoji(unicode=reaction.emoji)

        if currentEmoji is None:
            bbLogger.log("ReactPollMenu", "prtAndExpirePollResults", "Failed to fetch dumbEmoji for reaction: " + str(reaction), category="reactionMenus", eventType="INV_REACT")
            pollEmbed = menuMsg.embeds[0]
            pollEmbed.set_footer(text="This poll has ended.")
            await menu.msg.edit(content="An error occured when calculating the results of this poll. The error has been logged.", embed=pollEmbed)
            return

        menuOption = None
        for currentOption in results:
            if currentOption.emoji == currentEmoji:
                menuOption = currentOption
                break

        if menuOption is None:
            # bbLogger.log("ReactPollMenu", "prtAndExpirePollResults", "Failed to find menuOption for emoji: " + str(currentEmoji), category="reactionMenus", eventType="UNKN_OPTN")
            # pollEmbed = menuMsg.embeds[0]
            # pollEmbed.set_footer(text="This poll has ended.")
            # await menu.msg.edit(content="An error occured when calculating the results of this poll. The error has been logged.", embed=pollEmbed)
            # return
            continue

        async for user in reaction.users():
            if user != bbGlobals.client.user:
                validVote = True
                if not menu.multipleChoice:
                    for currentOption in results:
                        if currentOption.emoji != currentEmoji and user in results[currentOption]:
                            validVote = False
                            break
                if validVote and user not in results[menuOption]:
                    results[menuOption].append(user)
                    # print(str(user),"voted for", menuOption.emoji.sendable)
    
    pollEmbed = menuMsg.embeds[0]
    pollEmbed.set_footer(text="This poll has ended.")

    maxCount = 0
    for currentResult in results.values():
        if len(currentResult) > maxCount:
            maxCount = len(currentResult)
    
    if maxCount > 0:
        resultsStr = "```\n"
        for currentOption in results:
            resultsStr += ("🏆" if len(results[currentOption]) == maxCount else "  ") + currentOption.name + (" " * (maxOptionLen - len(currentOption.name))) + " | " + ("=" * int((len(results[currentOption]) / maxCount) * bbConfig.pollMenuResultsBarLength)) + (" " if len(results[currentOption]) == 0 else "")+ " +" + str(len(results[currentOption])) + " Vote" + ("s" if len(results[currentOption]) != 1 else "") + "\n"
        resultsStr += "```"

        pollEmbed.add_field(name="Results", value=resultsStr, inline=False)
    
    else:
        pollEmbed.add_field(name="Results", value="No votes received!", inline=False)

    await menuMsg.edit(embed=pollEmbed)
    if msgID in bbGlobals.reactionMenusDB:
        del bbGlobals.reactionMenusDB[msgID]

    for reaction in menuMsg.reactions:
        await reaction.remove(menuMsg.guild.me)
    

    
                

class ReactionPollMenu(ReactionMenu.ReactionMenu):
    def __init__(self, msg, pollOptions, timeout, pollStarter=None, multipleChoice=False, titleTxt="", desc="", col=None, footerTxt="", img="", thumb="", icon="", authorName="Poll", targetMember=None, targetRole=None, owningBBUser=None):
        self.multipleChoice = multipleChoice
        self.owningBBUser = owningBBUser

        if pollStarter is not None and desc == "":
            desc = "__" + str(pollStarter) + " started a poll!__"

        super(ReactionPollMenu, self).__init__(msg, options=pollOptions, titleTxt=titleTxt, desc=desc, col=col, footerTxt=footerTxt, img=img, thumb=thumb, icon=icon, authorName=authorName, timeout=timeout, targetMember=targetMember, targetRole=targetRole)
        self.saveable = True


    def getMenuEmbed(self):
        baseEmbed = super(ReactionPollMenu, self).getMenuEmbed()
        if self.multipleChoice:
            baseEmbed.add_field(name="This is a multiple choice poll!", value="Voting for more than one option is allowed.", inline=False)
        else:
            baseEmbed.add_field(name="This is a single choice poll!", value="If you vote for more than one option, only one will be counted.", inline=False)

        return baseEmbed

    
    def toDict(self):
        baseDict = super(ReactionPollMenu, self).toDict()
        baseDict["multipleChoice"] = self.multipleChoice
        baseDict["owningBBUser"] = self.owningBBUser.id
        return baseDict

    
    


async def fromDict(rmDict):
    options = {}
    for emojiName in rmDict["options"]:
        emoji = bbUtil.dumbEmojiFromStr(emojiName)
        options[emoji] = ReactionMenu.DummyReactionMenuOption(rmDict["options"][emojiName], emoji)

    msg = await bbGlobals.client.get_guild(rmDict["guild"]).get_channel(rmDict["channel"]).fetch_message(rmDict["msg"])

    timeoutTT = None
    if "timeout" in rmDict:
        expiryTime = datetime.utcfromtimestamp(rmDict["timeout"])
        bbGlobals.reactionMenusTTDB.scheduleTask(TimedTask.TimedTask(expiryTime=expiryTime, expiryFunction=printAndExpirePollResults, expiryFunctionArgs=msg.id))

    return ReactionPollMenu(msg, options, timeoutTT, multipleChoice=rmDict["multipleChoice"] if "multipleChoice" in rmDict else False,
                                titleTxt=rmDict["titleTxt"] if "titleTxt" in rmDict else "",
                                desc=rmDict["desc"] if "desc" in rmDict else "",
                                col=Colour.from_rgb(rmDict["col"][0], rmDict["col"][1], rmDict["col"][2]) if "col" in rmDict else Colour.default(),
                                footerTxt=rmDict["footerTxt"] if "footerTxt" in rmDict else "",
                                img=rmDict["img"] if "img" in rmDict else "",
                                thumb=rmDict["thumb"] if "thumb" in rmDict else "",
                                icon=rmDict["icon"] if "icon" in rmDict else "",
                                authorName=rmDict["authorName"] if "authorName" in rmDict else "",
                                targetMember=dcGuild.get_member(rmDict["targetMember"]) if "targetMember" in rmDict else None,
                                targetRole=dcGuild.get_role(rmDict["targetRole"]) if "targetRole" in rmDict else None,
                                owningBBUser=bbGlobals.usersDB.getUser(rmDict["owningBBUser"]) if "owningBBUser" in rmDict and bbGlobals.usersDB.userIDExists(rmDict["owningBBUser"]) else None)