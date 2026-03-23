class Account:
    def __init__(self,id, balance, anualInterestRate): # na self overbodig
        self.__id= int(id)
        self.__balance = float(balance)
        self.__anualInterestRate =float(anualInterestRate)

    def setId(self, id):
        self.__id= id

    def setBalance(self, balance): #overbodig hier
        self.__balance = balance

    def setAnulaInterestRate( self, anualInterestRate):
        self.__anualInterestRate = anualInterestRate

    def getId(self):
        return self.__id

    def getBalance(self):
        return self.__balance 

    def getAnulaInterestRate(self):
        return self.__anualInterestRate
    
    def getAnualInterest(self):
        anualInterest = self.__balance * self.__anualInterestRate /100
        return anualInterest
    
    def deposit(self, depositAmount):
        self.__balance += depositAmount

    def withdraw(self, withdrawalAmount):
        self.__balance -= withdrawalAmount

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
        

    


    



        


    
    