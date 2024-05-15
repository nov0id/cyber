#In this lesson we are messing with lists and dictionaries

#initializes the list
my_list = [1, 2, 3, 4]

#initializes the dictionary
myDict = {"Name": "nov0id", "Age": 24}

#Does some stuff to manipulate the list and dictionary
my_list.append(420)

my_list.insert(5, "I LOVE CHEESE")

myDict["Can backflip?"] = False

#Removes an item based off of an index
del my_list[0]

#Removes an item based on the value
my_list.remove(3)

#Removes my "name" key-value pair
del myDict["Name"]

#Prints the list
print(my_list)
print(myDict)