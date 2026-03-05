def getPentagonalNumber(n):
    pentagonalNumber = (3*n**2-n)/2
    return int(pentagonalNumber)

def main():
    for i in range (10):
        penta = getPentagonalNumber(i)
        print ('pentagonal number ', i, '= ', penta)

if __name__=="__main__":
    main()




