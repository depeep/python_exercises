# demo program A

def some_function(var_x, var_y):
    var_x = var_x * var_x
    var_y = var_y * 2
    var_z = var_x + var_y
    return var_z

def main():
    # try some_function with different arguments
    result1 = some_function(2, 3)
    result2 = some_function(-1, -5)
    print("result1 and result 2 are:", result1, result2)

main()

# (http://www.pythontutor.com/visualize.html#mode=edit). stap voor stap runnen

# 1. Why is/was this line of code the next to be executed?
# definitie van functie
# definitie van main()
# main()
# result 1 >> naar functie
# stap voor stap door functie
# result 2 >> naar functie
# stap voor stap door functie

# 2. Why do the variables have the values (shown on the right)?
# door de verschillende bewerkingen

# 3. Why do some variables ‘disappear’ after certain steps?
# uit de functie = uit de scope