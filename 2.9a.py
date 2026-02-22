import math
angle = float(input('please enter the angle in degrees: '))
#radians = math.radians(angle)
#print(angle, "degrees is equal to", radians, "radians.")
#zou ik doen

radians = angle * math.pi / 180
print(angle, "degrees is equal to", radians, "radians.")

print("the sine of", angle, "degrees is", round(math.sin(radians), 3))
print("the cosine of", angle, "degrees is", round(math.cos(radians), 3))  
