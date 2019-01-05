# Add your phone to security System
import os
print("\n\033[1;31;47m --- Welcome to Phone Adding System ---\033[0m \n")
ser=["At&t","Tmobile","Verizon"]
ext=["txt.att.net","tmomail.net","vtext.com"]
number=raw_input("Please enter your phone number\n")

count =1
print "\n\033[1;30;47m index   Service\033[0m \n"

for x in ser:
    print  "  "+ str(count) + "  --  " + x
    count=count+1
index=int(raw_input("enter the index of service\n"))
value=str(number)+"@"+str(ext[index-1])

with open('phone.txt', 'a+') as file:
    if not any(value == x.rstrip('\r\n') for x in file):
        file.write(value + '\n')
        print "Adding succesfull"
    else:
        print (number + " exists")
print("\n\033[1;31;47m --- Available Phones ---\033[0m \n")
file=open("phone.txt","r")
for i,line in enumerate(file):
    data=line.split(" ")
    print(data[0])
file.close()

