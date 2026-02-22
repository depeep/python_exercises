#`voorbeelden van slicing`
# slicing = input("Enter a string: ")
# print("The first character is:", slicing[0])
# print("The last character is:", slicing[-1])
# print("The first three characters are:", slicing[:3])
# print("The last three characters are:", slicing[-3:])


string_a = '3500 ballons where popped in the world-record attempt.'
string_b = 'X-DSPAM-Confidence: 0.8475'
string_c = 'The economy has grown by 3.57% over the past year.'

startpositie_a = string_a.find('3')
startpositie_b = string_b.find('0')
startpositie_c = string_c.find('3')
eindpositie_a = string_a.rfind('0') + 1# rfind() geeft de positie van het laatste voorkomen van het opgegeven teken, en we voegen 1 toe om de eindpositie te krijgen (omdat slicing exclusief is).
eindpositie_b = string_b.rfind('5') + 1
eindpositie_c = string_c.rfind('7') + 1



getallen_a = string_a[startpositie_a:eindpositie_a]
getallen_b = string_b[startpositie_b:eindpositie_b]   
getallen_c = string_c[startpositie_c:eindpositie_c]

print("The numbers in " + string_a + " are:", getallen_a)
print("The numbers in " + string_b + " are:", getallen_b)
print("The numbers in " + string_c + " are:", getallen_c)

# dit kan een stuk charmanter denk ik (bijvoorbeeld met een for loop en misschineen een array met getallen) maar voor nu laat dit slicing zien.