courses = {"0HV10" : "Introduction to psychology and technology", "0HV20" : "Perception and motor control", "0HV30" : "Social psychology and consumer behavior", "0HV40" : "Brain, body & behaviour", "0HV50" : "Programming for psychology and technology"}
print(courses["0HV30"])

codeCourse = input("Enter course code: ")
if codeCourse in courses:
    print("The name of course code " + codeCourse + " is " + courses[codeCourse])   
else:    print("Course code not found.")
