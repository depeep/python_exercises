nr_of_students = [
    ['study-year', 2014, 2015, 2016],
    ['Psy. & Tech.', 243, 298, 324],
    ['Informatics', 847, 939, 951],
    ['Mathematics', 148, 160, 194] ]

# a. print the nr of math students in 2014
print (nr_of_students[3][1])
print ()

# b. print a list of all studies in nr_of_students
for i in range (1,4):
    print (nr_of_students[i][0])
print()
# print('b. list of studies:')
# for study in nr_of_students[1:]:
#     print(study[0])


# c. print the student nrs of ‘Informatics’ of all years in nr_of_students
print (nr_of_students[2][1:4])
print()
# print('c. student nrs of Informatics:')
# for year in range(1, 4):
#     print(nr_of_students[0][year], nr_of_students[2][year])


# d. print the nr of students of each study in 2015
for i in nr_of_students:
    print (i[0],i[2])  # i is hier dus nr_of_students[getal] en niet alleen een getal!
print()
# print('d. nr of students in 2015')
# for study in nr_of_students:
#     print(study[0], '\t', study[2])

# e. prints the sum of numbers of students over the studies, for each separate year
for i in range (1,4):
    totaal = nr_of_students[i][1] + nr_of_students[i][2] + nr_of_students[i][3] # i is hier wel een getal!
    print ("total nr of students in", nr_of_students[i][0], totaal)
print()

# print('e. total student nrs over the years')
# for year in range(1, 4):
#     total = 0
#     for study in range(1, 4):
#         total = total + nr_of_students[study][year]
#     print(nr_of_students[0][year], total)