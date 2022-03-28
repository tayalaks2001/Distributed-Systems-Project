from enum import Enum

class tester(Enum):
    apple = 1
    banana = 2
    citrus = 3

    @staticmethod
    def object_type():
        return 10


fruit = 'apple'
a = tester[fruit]
enumclass = type(a)

# printing enum member as string
print ("The string representation of enum member is : ",end="")
print (a)
 
# printing enum member as repr
print ("The repr representation of enum member is : ",end="")
print (a.value)
 
# printing the type of enum member using type()
print ("The type of enum member is : ",end ="")
print (type(a))
 
# printing name of enum member using "name" keyword
print ("The name of enum member is : ",end ="")
print (a.name)

print("Type: ", type(a).object_type())