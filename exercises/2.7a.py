import statistics
age1 = int(input('please enter the age of the first person: '))
age2 = int(input('please enter the age of the second person: '))
print("the average age of the two people is", statistics.mean([age1, age2]))
