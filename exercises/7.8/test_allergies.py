from allergies import Allergy

def test():
    myAllergy = Allergy("leerstofallergie",["boeken", "schriften"])
    print()
    print (myAllergy.getName())
    print (myAllergy.getFoods())
    myAllergy.addFood("penneworst")
    print (myAllergy.getFoods())
    myAllergy.removeFood("boeken")
    print (myAllergy.getFoods())

test()
