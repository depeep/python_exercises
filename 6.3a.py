def multiply(numbers):
    result = 1
    for number in (numbers):
        result= result * number
    return result


def main():
    numbers1 =  [-1, 2, -3, 4, -5]
    numbers2 = [42] 
    numbers3 =  [-10, 15, 0, 347]
    print (multiply(numbers1))
    print (multiply(numbers2))
    print (multiply(numbers3))

if __name__ == "__main__":
    main()



