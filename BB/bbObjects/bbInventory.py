from . import bbInventoryListing

"""
A database of bbInventoryListings.
Aside from the use of bbInventoryListing for the purpose of item quantities, this class is type unaware.
"""
class bbInventory:
    def __init__(self):
        # The actual item listings
        self.items = {}
        # The item types stored
        self.keys = []
        # The total number of items stored; the sum of all item quantities
        self.totalItems = 0
        # The number of item types stored; the length of self.keys
        self.numKeys = 0

    
    """
    Add one or more of an item to the inventory.
    If at least one of item is already in the inventory, that item's bbInventoryListing count will be incremented.
    Otherwise, a new bbInventoryListing is created for item.

    @param item -- The item to add to the inventory
    @param quantity -- Integer amount of item to add to the inventory. Must be at least 1. Default: 1
    """
    def addItem(self, item, quantity=1):
        if quantity < 0:
            raise ValueError("Quantity must be at least 1")
        
        # increment totalItems tracker
        self.totalItems += quantity
        # increment count for existing bbItemListing
        if item in self.items:
            self.items[item].count += quantity
        # Add a new bbItemListing if one does not exist
        else:
            self.items[item] = bbInventoryListing.bbInventoryListing(item, quantity)
            # Update keys and numKeys trackers
            self.keys.append(item)
            self.numKeys += 1


    """
    Remove one or more of an item from the inventory.
    If the amount of item stored in the inventory is now zero, the bbInventoryListing is removed from the inventory.
    At least quantity of item must already be stored in the inventory. 

    @param item -- The item to remove from the inventory
    @param quantity -- Integer amount of item to remove from the inventory. Must be between 1 and the amount of item currently stored, both inclusive. Default: 1
    """
    def removeItem(self, item, quantity=1):
        # Ensure enough of item is stored to remove quantity of it
        if item in self.items and self.items[item].count >= quantity:
            # Update item's count and inventory's totalItems tracker
            self.items[item].count -= quantity
            self.totalItems -= quantity
            # remove the bbItemListing if it is now empty
            if self.items[item].count == 0:
                # update the keys and numKeys trackers
                for i in range(len(self.keys)):
                    if self.keys[i] is item:
                        self.keys.pop(i)
                        break
                # self.keys.remove(item)
                self.numKeys -= 1
                del self.items[item]
        else:
            raise ValueError("Attempted to remove " + str(quantity) + " " + str(item) + "(s) when " + (str(self.items[item].count) if item in self.items else "0") + " are in inventory")

    
    """
    Get the number of pages of items in the inventory, for a given max number of items per page
    E.g, where 3 keys are in the inventory: numPages(1) gives 3. numPages(2) gives 2.

    @param itemsPerPage -- The maximum number of items per page
    @return -- The number of pages required to list all items in the inventory
    """
    def numPages(self, itemsPerPage):
        return int(self.numKeys/itemsPerPage) + (0 if self.numKeys % itemsPerPage == 0 else 1)

    
    """
    Get a list of the bbItemListings on the requested page.
    pageNum is 1 index-based; the first page is 1.
    pageNum must be between 1 and numPages(itemsPerPage).

    @param pageNum -- The number of the page to fetch
    @param itemsPerPage -- The max number of items that can be contained in a single page
    @return -- A list containing the bbInventoryListings contained in the requested inventory page
    """
    def getPage(self, pageNum, itemsPerPage):
        # Validate the requested pageNum
        if pageNum < 1 or pageNum > self.numPages(itemsPerPage):
            raise IndexError("pageNum out of range. min=1 max=" + str(self.numPages(itemsPerPage)))
        
        page = []
        # Splice self.keys around the first and last indices in the requested page
        for item in self.keys[(pageNum - 1) * itemsPerPage: min(pageNum * itemsPerPage, self.numKeys)]:
            # Add the bbItemListings for each of the page's keys to the results list
            page.append(self.items[item])

        return page


    """
    Decide whether a given item is stored in this inventory.

    @param item -- The item to check for membership
    @return -- True if at least one of item is in this inventory, False otherwise
    """
    def stores(self, item):
        return item in self.keys

    
    """
    Get the amount stored of a given item.

    @param item -- The item to count
    @return -- Integer count of number of items in this inventory. 0 if it is not stored in this inventory.
    """
    def numStored(self, item):
        return self.items[item].count if self.stores(item) else 0


    """
    Decide whether or not this bbInventory currently stores any items.

    @return -- True if no items are stored, False if at least one item is stored currently
    """
    def isEmpty(self):
        return self.totalItems == 0


    """
    Remove all items from the inventory.

    """
    def clear(self):
        self.items = {}
        self.keys = []
        self.totalItems = 0
        self.numKeys = 0


    """
    Override [subscript] operator for reading values.
    Currently returns the bbInventoryListing for the item at position key in self.keys.

    @param key -- The index of the key to dereference
    @return -- The bbInventoryListing for the item at the requested index
    """
    def __getitem__(self, key):
        if bool(self.keys): 
            if key in range(len(self.keys)):
                if self.keys[key] in self.items:
                    return self.items[self.keys[key]]
                raise KeyError("Failed get of key number " + str(key) + " - " + str(self.keys[key]) + ". Key does not exist in inventory.")
            raise IndexError("Key of incorrect type or out of range: "+ str(key) + ". Valid range: 0 - " + str(len(self.keys)-1))
        raise ValueError("Attempted to fetch key " + str(key) + ", but keys list is empty")


    """
    Disallow assignment through the [subscript] operator.

    @param key -- ignored
    @param value -- ignored
    """
    def __setitem__(self, key, value):
        raise NotImplementedError("Cannot use [subscript] assignment for class bbInventory. use addItem/removeItem instead.")
        # self.items[self.keys[key]] = value


    """
    Override the 'in' operator.

    @param item -- The object to test for membership
    """
    def __contains__(self, item):
        return item in self.keys
