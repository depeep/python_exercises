
def makeCheeseSandwich():
   print("take first slice of bread ...")
   print("put cheese on it")
   print("cover cheese with a slice of bread")

def makeJamSandwich():
    print("take first slice of bread ...")
    print("put jam on it")
    print("cover jam with a slice of bread")

def addFruit():  
    fruits = [apple, banana, coconut] 
    for fruit in (fruits):
        print("add one", fruit)
    
def main():
    print("prepare bag lunch")
    print()
    print("make 3 cheese sandwiches")
    for CheeseSandwich in range (3):
        makeCheeseSandwich()
    print("make 2 jam sandwiches")
    for jamSandwich in range(2):
        makeJamSandwich()
    print("adding fruits")
    addFruit()

if __name__ == "__main()__":
    main()
