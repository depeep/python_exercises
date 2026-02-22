#`voorbeelden van slicing`
# slicing = input("Enter a string: ")
# print("The first character is:", slicing[0])
# print("The last character is:", slicing[-1])
# print("The first three characters are:", slicing[:3])
# print("The last three characters are:", slicing[-3:])


string_a = '3500 ballons where popped in the world-record attempt.'
string_b = 'X-DSPAM-Confidence: 0.8475'
string_c = 'The economy has grown by 3.57% over the past year.'


getallen_a = string_a[:4]
getallen_b = string_b[-6:]   
getallen_c = string_c[25:29]

print("The numbers in " + string_a + " are:", getallen_a)
print("The numbers in " + string_b + " are:", getallen_b)
print("The numbers in " + string_c + " are:", getallen_c)
