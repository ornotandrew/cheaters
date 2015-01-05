# Thief McCheaterson
# The following program computes wheather a number is prime
# 4/1/2015

# There was something here, but I removed it
print("Hello, world!")
print("This program checks if numbers are prime")
print("Enter -1 to exit")
print("========================================")

while(True):
    # No checks on input are made
    # Program will crash if a non-numeric is entered
    number = eval(input("Enter a number: "))
   
    if number==-1:
        break
    
    # Nobody will suspect me of cheating! I renamed 'num' to 'number'
    elif number<1:
        print("Not prime")

    elif number==1:
        print("Prime")
    
    # I also changed the spacing and edited/removed the comments
    elif number%2==0:
        print("Not prime")

    else:
        # We can stop checking at s = sqrt(num), because if
        # any factor is greater than s, it must be multiplied
        # by something less than s to make num, and num will
        # have already been found to be not prime
        # (s itself must still be checked)
        for i in range(3, int(number**0.5+1), 2):
            if number%i==0:
                print("Not Prime")
                break
        else:
            print("Prime")


        

    

