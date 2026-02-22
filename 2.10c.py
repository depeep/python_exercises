rhymeWord1 = input("Enter rhyme word 1: ")
rhymeWord2 = input("Enter rhyme word 2: ")
rhymeWord3 = input("Enter rhyme word 3: ")
rhymeWord4 = input("Enter rhyme word 4: ")

length1 = len(rhymeWord1)
length2 = len(rhymeWord2)
length3 = len(rhymeWord3)
length4 = len(rhymeWord4)

maxLength = max(length1, length2, length3, length4)

print ("Rhyme words:")
print ( f"{rhymeWord1:>{maxLength}}")
print ( f"{rhymeWord2:>{maxLength}}")
print ( f"{rhymeWord3:>{maxLength}}")    
print ( f"{rhymeWord4:>{maxLength}}")


# f string formatting, zie https://www.w3schools.com/python/ref_string_format.asp

