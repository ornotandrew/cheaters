# Andrew van Rooyen
# The following program computes wheather a number is prime
# 4/1/2015

if __name__ == "__main__":
    
    print("Hello, world!")
    print("This program checks if numbers are prime")
    print("Enter -1 to exit")
    print("========================================")
    
    while(True):
        # No checks on input are made
        # Program will crash if a non-numeric is entered
        num = eval(input("Enter a number: "))
        
        if num == -1:
            break
        
        # All negative numbers are not prime
        # They are divisible by themselves, 1 and -1
        # Zero is also prime, as 0/x is always 0
        elif num < 1:
            print("Not prime")

        elif num == 1:
            print("Prime")
        
        # No even number is prime
        elif num%2 == 0:
            print("Not prime")

        else:
            # We can stop checking at s = sqrt(num), because if
            # any factor is greater than s, it must be multiplied
            # by something less than s to make num, and num will
            # have already been found to be not prime
            # (s itself must still be checked)
            for i in range(3, int(num**0.5+1), 2):
                if num%i == 0:
                    print("Not Prime")
                    break
            else:
                print("Prime")


        

    

