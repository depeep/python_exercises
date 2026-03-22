class Account:
    def __init__(self,id, balance, anualInterestRate):
        self.id = int(id)
        self.balance = float(balance)
        self.anualInterestRate =float(anualInterestRate)

    def setId(self, id):
        self.id = id

    def setBalance(self, balance):
        self.balance = balance

    def setAnulaInterestRate( self, anualInterestRate):
        self.anualInterestRate = anualInterestRate

    def getId(self):
        return self.id

    def getBalance(self):
        return self.balance 

    def getAnulaInterestRate(self):
        return self.anualInterestRate
    
    def getAnualInterest(self):
        anualInterest = self.balance * self.anualInterestRate /100
        return anualInterest
    
    def deposit(self, depositAmount):
        self.balance += depositAmount

    def withdraw(self, withdrawalAmount):
        self.balance -= withdrawalAmount

myAccount = Account(1122, 20000, 4.5)

print ('My account has:')
print ('ID: ', myAccount.getId())
print ('Balance: ', myAccount.getBalance())
print ( 'After withdrawing 2500, balance is: ', end ='')
myAccount.withdraw(2500)
print (myAccount.getBalance())
print ( 'After depositing  3000, balance is: ', end ='')
myAccount.deposit(3000)
print (myAccount.getBalance())
print ('anual interest: ', myAccount.getAnualInterest())
        

    


    



        


    
    