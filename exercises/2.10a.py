firstName1 = input("Enter first name 1: ")
lastName1 = input("Enter last name 1: ")
firstName2 = input("Enter first name 2: ")
lastName2 = input("Enter last name 2: ")    
firstName3 = input("Enter first name 3: ")
lastName3 = input("Enter last name 3: ")

# f string formatting, zie https://www.w3schools.com/python/ref_string_format.asp
print ( f"{'First':<11} {'Last'}" ) # max 11 tekens voor first name, rest gaat naar last name
print ( f"{firstName1:<11} {lastName1}" )
print ( f"{firstName2:<11} {lastName2}" )   
print ( f"{firstName3:<11} {lastName3}" )

# Volgens de reader
print()
print (firstName1.ljust(11), lastName1) 
print (firstName2.ljust(11), lastName2)
print (firstName3.ljust(11), lastName3)
