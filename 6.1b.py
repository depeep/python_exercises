# demo program B

def print_reverse_float_range(lower, upper, step):
    # print 1/x for a range of float values between lower and upper
    current = lower
    while current < upper:
        value = 1 / current
        print("value of 1 /", current, ":", value)
        current += step
    return

def main():
    # try print_reverse_float_range with different arguments
    print_reverse_float_range(2.5, 2.8, 0.1)
    print_reverse_float_range(2.0, 4.0, 0.5)

main()

# Answer the following questions after every step (‘Forward’ press):

# Why is/was this line of code the next to be executed?


# Why do the variables have the values (shown on the right)?

# Why do some variables ‘disappear’ after certain steps?