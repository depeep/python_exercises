# for n in range(-1):
#     print('another line!')

# for n in range(2, 6):
#     print('another line!')

# for n in range(8, 8):
#     print('another line!')

# for n in range(6, 15, 3):
#      print('another line!')

# for n in range(15, 6, -3):
#     print('another line!')

# for n in range(7):
#     print('n:', n)

# for n in range(0):
#     print('n:', n)

# for n in range(-1, 4):
#     print('n:', n)

# for n in range(5, 3):
#     print('n:', n)

# for n in range(0, 11, 2):
#      print('n:', n)

# for n in range(6, 12, -3):
#     print('n:', n)

# nr_lines_printed = 1
# for number1 in range(4):
#     for number2 in range(5):
#         print('this is line', nr_lines_printed)
#         nr_lines_printed += 1

# for number1 in range(7):
#     for number2 in range(3):
#         total = number1 + number2
#         print('total:', total, end = ', ')
#     print()

# for number1 in range(6):
#     print('number1:', number1)
#     print('----------')
#     for number2 in range(number1):
#         print('number2:', number2)
#     print()

for number1 in range(7):
    for number2 in range(7 - number1):
        print(number2, end = '')
    print()