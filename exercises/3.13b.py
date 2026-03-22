username = "Superman".lower()
password = "Kryptonite"

inputUsername = input ("Please type username: ").lower()
inputPassword = input ("Please type password: ")



if inputUsername == username and inputPassword == password:
    print("Access granted.")
else:
    print("Access denied.")
    

# username hoofdlettergevoeligheid verwijderd door .lower() te gebruiken. 
# Had natuurlijk ook .upper() kunnen gebruiken, of de variabelen na het invoeren kunnen aanpassen 
