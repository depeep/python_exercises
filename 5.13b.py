square1 =  [[2, 7, 6], [9, 5, 1], [4, 3, 8]]

square2 =  [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 16, 15]]


for column in square2:
    total = 0
    for row in range (len(square2)):
        element = str(column[row])
        print (element.ljust(3), end='' )
        total = total + column[row]
    print (total)

 
    

# # b. totals of each row (version 1)
# print("totals of square rows:")
# print()
# for n, row in enumerate(square, 1):
#     print(n, ':', sum(row))

# # b. totals of each row (version 2)
# # print("totals of square rows:")
# # print()
# # for r in range(nr_rows):
# #     print(r+1, ':', sum(square[n]))

# print()  # for readability
