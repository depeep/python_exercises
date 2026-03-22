# start = 'the apple doesn't fall'
# end = 'far from the tree'
# result = start + end
# length = len(result)
#  voorspelling: error vanwege de apostrof in apple, en dat klopt, want de string is niet correct afgesloten.


# sentence = 'Python is a great programming language.'
# index = sentence.find('g')
# # voorspelling: 12 (beginnen bij 0, dus de 'g' in 'great' is de 12e letter), en dat klopt.
# print("The index of the first occurrence of 'g' is:", index) # toegevoegd om de voorspelling te controleren.

# sentence = 'Oh wow, I love studying!'
# slice = sentence[6:10]
# # # voorspelling: , I l (de slice begint bij index 6, wat de komma is, en eindigt bij index 10, wat de 'l' in 'love' is, maar omdat slicing exclusief is, wordt de 'l' niet meegenomen), en dat klopt.
# print ("The slice of the sentence from index 6 to 10 is:", slice)

sentence = 'This exercise is a little bit more advanced.'
result = len(sentence) * sentence.find('little')
print("The result of the expression is:", result)
print ("The length of the sentence is:", len(sentence))
print ("The index of the first occurrence of 'little' is:", sentence.find('little'))    
