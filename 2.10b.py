rhymeWord1 = input("Enter rhyme word 1: ")
rhymeWord2 = input("Enter rhyme word 2: ")
rhymeWord3 = input("Enter rhyme word 3: ")
rhymeWord4 = input("Enter rhyme word 4: ")
print ("Rhyme words:")
print ( f"{rhymeWord1:>20}")
print ( f"{rhymeWord2:>20}")
print ( f"{rhymeWord3:>20}")    
print ( f"{rhymeWord4:>20}")


# f string formatting, zie https://www.w3schools.com/python/ref_string_format.asp

# Volgens de reader 
print()
print (rhymeWord1.rjust(20)) 
print (rhymeWord2.rjust(20)) 
print (rhymeWord3.rjust(20)) 
print (rhymeWord4.rjust(20)) 