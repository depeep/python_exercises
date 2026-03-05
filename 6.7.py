def safeSelect(lst, item):
    if item in list:
        print (item, 'is correct. You may pass! Good luck trying to find the Holy Grail')
    else:
        print (item, ' is not in the list')


    # return item


list = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
print ("There are those who call me ..... Tim!")
name = input ('What is your name? ')
quest = input ("What is your quest? ")
item = input("What is your favourite colour?)")
safeSelect (list, item)