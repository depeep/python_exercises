filename = input ("Enter the filename: ")

invalidCharacters = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
for character in invalidCharacters:
    if character in filename:
        print ("The filename is invalid.")
        break   
else:
        print ("The filename is valid.") 
        

       
# for ... else speciale contstructie in Python:
# De else wordt uitgevoerd alleen als de loop NIET is gestopt met break.

# Dus:

# Als een verboden teken wordt gevonden → break → else wordt overgeslagen.

# Als geen enkel verboden teken wordt gevonden → loop eindigt normaal → else wordt uitgevoerd.


# NB deze gaf meerdere keren "The filename is valid." omdat de else bij de for hoort, niet bij de if.
# filename = input ("Enter the filename: ")

# invalidCharacters = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
# for character in invalidCharacters:
#     if character in filename:
#         print ("The filename is invalid.")
#         break   
#     else: #ingesprongen else hoort bij if, niet bij for
#         print ("The filename is valid.") 

# !!!! vreemd genoeg werkte het wel prima met break eronder. Dan print hij "The filename is valid." maar een keer en haalt hij toch de foute filenames er uit????
# \