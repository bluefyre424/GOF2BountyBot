from ..bbConfig import bbData, bbConfig
from .items import bbModuleFactory, bbShip, bbWeapon, bbTurret
from . import bbInventory, bbInventoryListing
import random
from ..logging import bbLogger

class bbShop:
    def __init__(self, maxShips=bbConfig.shopDefaultShipsNum, maxModules=bbConfig.shopDefaultModulesNum, maxWeapons=bbConfig.shopDefaultWeaponsNum, maxTurrets=bbConfig.shopDefaultTurretsNum, shipsStock=bbInventory.bbInventory(), weaponsStock=bbInventory.bbInventory(), modulesStock=bbInventory.bbInventory(), turretsStock=bbInventory.bbInventory(), currentTechLevel=bbConfig.minTechLevel):
        self.maxShips = maxShips
        self.maxModules = maxModules
        self.maxWeapons = maxWeapons
        self.maxTurrets = maxTurrets
        self.currentTechLevel = currentTechLevel

        # TODO: Somewhere, stocks are getting passed in and shared amongst all shops. Fix this. Temporary manual deep copy here to make sure each shop gets its own inventory objects.
        # self.shipsStock = shipsStock
        # self.weaponsStock = weaponsStock
        # self.modulesStock = modulesStock
        # self.turretsStock = turretsStock

        self.shipsStock = bbInventory.bbInventory()
        self.weaponsStock = bbInventory.bbInventory()
        self.modulesStock = bbInventory.bbInventory()
        self.turretsStock = bbInventory.bbInventory()

        if shipsStock.isEmpty() and weaponsStock.isEmpty() and modulesStock.isEmpty() and turretsStock.isEmpty():
            self.refreshStock()
        else:
            for itemListing in shipsStock.items.values():
                self.shipsStock.addItem(itemListing.item, itemListing.count)
            for itemListing in weaponsStock.items.values():
                self.weaponsStock.addItem(itemListing.item, itemListing.count)
            for itemListing in modulesStock.items.values():
                self.modulesStock.addItem(itemListing.item, itemListing.count)
            for itemListing in turretsStock.items.values():
                self.turretsStock.addItem(itemListing.item, itemListing.count)


    def refreshStock(self, level=-1):
        self.shipsStock.clear()
        self.weaponsStock.clear()
        self.modulesStock.clear()
        self.turretsStock.clear()
        # self.currentTechLevel = random.randint(bbConfig.minTechLevel, bbConfig.maxTechLevel)
        if level == -1:
            self.currentTechLevel = bbConfig.pickRandomShopTL()
        else:
            if level not in range(bbConfig.minTechLevel, bbConfig.maxTechLevel + 1):
                raise ValueError("Attempted to refresh a shop at tech level " + str(level) + ". must be within the range " + str(bbConfig.minTechLevel) + " to " + str(bbConfig.maxTechLevel))
            self.currentTechLevel = level
            
        for i in range(self.maxShips):
            itemTL = bbConfig.pickRandomItemTL(self.currentTechLevel)
            if len(bbData.shipKeysByTL[itemTL - 1]) != 0:
                self.shipsStock.addItem(bbShip.fromDict(bbData.builtInShipData[random.choice(bbData.shipKeysByTL[itemTL - 1])]))

        for i in range(self.maxModules):
            itemTL = bbConfig.pickRandomItemTL(self.currentTechLevel)
            if len(bbData.moduleObjsByTL[itemTL - 1]) != 0:
                self.modulesStock.addItem(random.choice(bbData.moduleObjsByTL[itemTL - 1]))

        for i in range(self.maxWeapons):
            itemTL = bbConfig.pickRandomItemTL(self.currentTechLevel)
            if len(bbData.weaponObjsByTL[itemTL - 1]) != 0:
                self.weaponsStock.addItem(random.choice(bbData.weaponObjsByTL[itemTL - 1]))

        # if random.randint(1, 100) <= bbConfig.turretSpawnProbability:
        for i in range(self.maxTurrets):
            itemTL = bbConfig.pickRandomItemTL(self.currentTechLevel)
            if len(bbData.turretObjsByTL[itemTL - 1]) != 0:
                self.turretsStock.addItem(random.choice(bbData.turretObjsByTL[itemTL - 1]))


    def getStockByName(self, item):
        if item == "all" or item not in bbConfig.validItemNames:
            raise ValueError("Invalid item type: " + item)
        if item == "ship":
            return self.shipsStock
        if item == "weapon":
            return self.weaponsStock
        if item == "module":
            return self.modulesStock
        if item == "turret":
            return self.turretsStock
        else:
            raise NotImplementedError("Valid, but unrecognised item type: " + item)


    def userCanAffordItemObj(self, user, item):
        return user.credits >= item.getValue()


    # SHIP MANAGEMENT
    def userCanAffordShipIndex(self, user, index):
        return self.userCanAffordItemObj(user, self.shipsStock[index].item)


    def amountCanAffordShipObj(self, amount, ship):
        return amount >= ship.getValue()

    
    def amountCanAffordShipIndex(self, amount, index):
        return self.amountCanAffordShipObj(amount, self.shipsStock[index].item)


    def userBuyShipIndex(self, user, index):
        self.userBuyShipObj(user, self.shipsStock[index].item)
        
        
    def userBuyShipObj(self, user, requestedShip):
        if self.userCanAffordItemObj(user, requestedShip):
            self.shipsStock.removeItem(requestedShip)
            user.credits -= requestedShip.getValue()
            user.inactiveShips.addItem(requestedShip)
        else:
            raise RuntimeError("user " + str(user.id) + " attempted to buy ship " + requestedShip.name + " but can't afford it: " + str(user.credits) + " < " + str(requestedShip.getValue()))


    def userSellShipObj(self, user, ship):
        user.credits += ship.getValue()
        self.shipsStock.addItem(ship)
        user.inactiveShips.removeItem(ship)
    

    def userSellShipIndex(self, user, index):
        self.userSellShipObj(user, user.inactiveShips[index].item)


    
    # WEAPON MANAGEMENT
    def userCanAffordWeaponIndex(self, user, index):
        return self.userCanAffordItemObj(user, self.weaponsStock[index].item)


    def userBuyWeaponIndex(self, user, index):
        self.userBuyWeaponIndex(user, self.weaponsStock[index].item)
        

    def userBuyWeaponObj(self, user, requestedWeapon):
        if self.userCanAffordItemObj(user, requestedWeapon):
            self.weaponsStock.removeItem(requestedWeapon)
            user.credits -= requestedWeapon.getValue()
            user.inactiveShips.addItem(requestedWeapon)
        else:
            raise RuntimeError("user " + str(user.id) + " attempted to buy weapon " + requestedWeapon.name + " but can't afford it: " + str(user.credits) + " < " + str(requestedWeapon.getValue()))


    def userSellWeaponObj(self, user, weapon):
        user.credits += weapon.getValue()
        self.weaponsStock.addItem(weapon)
        user.inactiveWeapons.removeItem(weapon)
    

    def userSellWeaponIndex(self, user, index):
        self.userSellWeaponObj(user, user.inactiveWeapons[index].item)


    
    # MODULE MANAGEMENT
    def userCanAffordModuleIndex(self, user, index):
        return self.userCanAffordItemObj(user, self.modulesStock[index].item)


    def userBuyModuleIndex(self, user, index):
        self.userBuyModuleIndex(user, self.modulesStock[index].item)
        

    def userBuyModuleObj(self, user, requestedModule):
        if self.userCanAffordItemObj(user, requestedModule):
            self.modulesStock.removeItem(requestedModule)
            user.credits -= requestedModule.getValue()
            user.inactiveShips.addItem(requestedModule)
        else:
            raise RuntimeError("user " + str(user.id) + " attempted to buy module " + requestedModule.name + " but can't afford it: " + str(user.credits) + " < " + str(requestedModule.getValue()))


    def userSellModuleObj(self, user, module):
        user.credits += module.getValue()
        self.modulesStock.addItem(module)
        user.inactiveModules.removeItem(module)
    

    def userSellModuleIndex(self, user, index):
        self.userSellModuleObj(user, user.inactiveModules[index].item)



    # TURRET MANAGEMENT
    def userCanAffordTurretIndex(self, user, index):
        return self.userCanAffordItemObj(user, self.turretsStock[index].item)


    def userBuyTurretIndex(self, user, index):
        self.userBuyTurretIndex(user, self.turretsStock[index].item)
        
        
    def userBuyTurretObj(self, user, requestedTurret):
        if self.userCanAffordItemObj(user, requestedTurret):
            self.turretsStock.removeItem(requestedTurret)
            user.credits -= requestedTurret.getValue()
            user.inactiveShips.addItem(requestedTurret)
        else:
            raise RuntimeError("user " + str(user.id) + " attempted to buy turret " + requestedTurret.name + " but can't afford it: " + str(user.credits) + " < " + str(requestedTurret.getValue()))


    def userSellTurretObj(self, user, turret):
        user.credits += turret.getValue()
        self.turretsStock.addItem(turret)
        user.inactiveTurrets.removeItem(turret)
    

    def userSellTurretIndex(self, user, index):
        self.userSellTurretObj(user, user.inactiveTurrets[index].item)



    def toDict(self):
        shipsStockDict = []
        for ship in self.shipsStock.keys:
            if ship in self.shipsStock.items:
                shipsStockDict.append(self.shipsStock.items[ship].toDict())
            else:
                bbLogger.log("bbShp", "toDict", "Failed to save invalid ship key '" + str(ship) + "' - not found in items dict", category="shop", eventType="UNKWN_KEY")

        weaponsStockDict = []
        for weapon in self.weaponsStock.keys:
            if weapon in self.weaponsStock.items:
                weaponsStockDict.append(self.weaponsStock.items[weapon].toDict())
            else:
                bbLogger.log("bbShp", "toDict", "Failed to save invalid weapon key '" + str(weapon) + "' - not found in items dict", category="shop", eventType="UNKWN_KEY")

        modulesStockDict = []
        for module in self.modulesStock.keys:
            if module in self.modulesStock.items:
                modulesStockDict.append(self.modulesStock.items[module].toDict())
            else:
                bbLogger.log("bbShp", "toDict", "Failed to save invalid module key '" + str(module) + "' - not found in items dict", category="shop", eventType="UNKWN_KEY")

        turretsStockDict = []
        for turret in self.turretsStock.keys:
            if turret in self.turretsStock.items:
                turretsStockDict.append(self.turretsStock.items[turret].toDict())
            else:
                bbLogger.log("bbShp", "toDict", "Failed to save invalid turret key '" + str(turret) + "' - not found in items dict", category="shop", eventType="UNKWN_KEY")

        return {"maxShips":self.maxShips, "maxWeapons":self.maxWeapons, "maxModules":self.maxModules, "currentTechLevel":self.currentTechLevel,
                    "shipsStock":shipsStockDict, "weaponsStock":weaponsStockDict, "modulesStock":modulesStockDict, "turretsStock":turretsStockDict}


def fromDict(shopDict):
    shipsStock = bbInventory.bbInventory()
    for shipListingDict in shopDict["shipsStock"]:
        shipsStock.addItem(bbShip.fromDict(shipListingDict["item"]), quantity=shipListingDict["count"])

    weaponsStock = bbInventory.bbInventory()
    for weaponListingDict in shopDict["weaponsStock"]:
        weaponsStock.addItem(bbWeapon.fromDict(weaponListingDict["item"]), quantity=weaponListingDict["count"])

    modulesStock = bbInventory.bbInventory()
    for moduleListingDict in shopDict["modulesStock"]:
        modulesStock.addItem(bbModuleFactory.fromDict(moduleListingDict["item"]), quantity=moduleListingDict["count"])

    turretsStock = bbInventory.bbInventory()
    for turretListingDict in shopDict["turretsStock"]:
        turretsStock.addItem(bbTurret.fromDict(turretListingDict["item"]), quantity=turretListingDict["count"])

    return bbShop(shopDict["maxShips"], shopDict["maxWeapons"], shopDict["maxModules"], currentTechLevel=shopDict["currentTechLevel"] if "currentTechLevel" in shopDict else 1,
                    shipsStock=shipsStock, weaponsStock=weaponsStock, modulesStock=modulesStock, turretsStock=turretsStock)
