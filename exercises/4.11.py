positives = 0
negatives = 0
total = 0
average = 0
counter = 0
invoer = int(input("Enter a number (0 to stop): "))
if invoer != 0:
    while invoer != 0:
        total += invoer                             
        counter += 1
        if invoer > 0:
            positives += 1
        elif invoer < 0:
            negatives += 1
        average = total / counter
        invoer = int(input("Enter a number (0 to stop): "))

    print("Number of positives:", positives)
    print("Number of negatives:", negatives)    
    print("Total:", total)
    print("Average:", average)
else:
    print("No numbers were entered.")