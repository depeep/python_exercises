square1 =  [[2, 7, 6], [9, 5, 1], [4, 3, 8]]

square2 =  [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 16, 15]]


for row in square2:
    for columnWidth in range (len(square1)+1):
        element = str(row[columnWidth])
        print (element.ljust(3),end='' )
    print ()
    

# # exercise 5.13

# square =  [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
# # square =  [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 16, 15]]

# # it is handy to use understandable names for the dimensions of the square (we could do with one name, nr_rows == nr_cols)
# # the letters r and c are used for the index of the rows and columns, respectively
# nr_rows = len(square) ????
# nr_cols = len(square) ????

# # a. print as aligned table
# print("square:")
# print()
# for row in square:
#     for col in row:
#         print(str(col).ljust(3), end = '')
#     print()
