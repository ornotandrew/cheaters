"""Assignment 8 Question 4
09 May 2014
Jordan Kadish, Recursive Palindromic Prime"""
import sys
import question1
import math
sys.setrecursionlimit (30000)

def PrimeNumber(StartNumber, Divide):
    #Checking from 2 up until the square root
    if StartNumber < 2:
        return False
    #2 is a prime
    elif StartNumber == 2:
        return True
    elif (math.sqrt(StartNumber) + 1) > Divide:
        if StartNumber % Divide == 0:
            return False
        else:
            return PrimeNumber(StartNumber, Divide +1)
    else:
        return True 
    
def counter(FirstNumber, LastNumber):
    #Base Check
    if FirstNumber <= LastNumber:
        #Pallindromic Prime check
        if PrimeNumber(FirstNumber, 2) and question1.PalinCheck(FirstNumber):
            print(FirstNumber)
        counter(FirstNumber+1, LastNumber)

FirstCheck = eval(input('Enter the starting point N: \n'))
LastCheck = eval(input('Enter the ending point M: \n'))    

print('The palindromic primes are: ')
counter(FirstCheck, LastCheck)
