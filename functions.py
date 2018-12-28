def grade2gpa(grade):
    if(grade >= 90):
        return 4
    elif(grade >= 85):
        return 3.75
    elif(grade >= 80):
        return 3.4
    elif(grade >= 75):
        return 3.1
    elif(grade >= 70):
        return 2.8
    elif(grade >= 65):
        return 2.5
    elif(grade >= 60):
        return 2.25
    elif(grade >= 50):
        return 2
    else:
        return 1
