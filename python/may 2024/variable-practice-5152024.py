#In this lesson we are messing with lists and dictionaries, and loop structures

#initializes the list
my_list = [1, 2, 3, 4]

#initializes the dictionary
myDict = {"Name": "nov0id", "Age": 25}

#Does some stuff to manipulate the list and dictionary
my_list.append(420)

my_list.insert(5, "I LOVE CHEESE")

myDict["Can backflip?"] = False

myDict["Can backflip?"] = True

#Removes an item based off of an index
del my_list[0]

#Removes an item based on the value
my_list.remove(3)

#Removes my "name" key-value pair
del myDict["Name"]

#Appends '1, 2, 3, 4, 5, 6' to my_list using a for loop
for i in range(1, 7):
    my_list.append(i)

x = 0
while len(myDict) < 15:
    myDict[x] = x
    x += 1

#Appends to the dictionary until the dictionary is to a certain length
#Prints the list
print(my_list)
print(myDict)