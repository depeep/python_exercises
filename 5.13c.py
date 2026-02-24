square1 =  [[2, 7, 6], [9, 5, 1], [4, 3, 8]]

square2 =  [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 16, 15]]



# Te ingewikkeld gemaakt, de oplossing (zie onder) is beter en simpeler voor het optellen van kolommen


# teogevoegd
nr_rows = len(square) 
nr_cols = len(square)

# c. totals of each column (version 1)
print("totals of square columns:")
print()
for c in range(nr_cols):
    total = 0
    for row in square:
        total += row[c]
    print(c+1, ':', total)

print()  # for readability

# c. totals of each column (version 2)
# print("totals of square columns:")
# print()
# for c in range(nr_cols):
#     total = 0
#     for r in range(nr_rows):
#         total += square[r][c]
#     print(c+1, ':', total)
