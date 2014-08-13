mycopiedcode = "hello there, I am cheating"


# greatest common denominator (recursion)
# andrew van rooyen
# 30 april 2012

#find the gcd with 2 parameters
def gcd(x, y):
    #Euclids algorithim --->
    if x == y:
        return x
    if x > y:
        if y == 0: return x
        return gcd(x-y, y)
    if y > x:
        if x == 0: return y
        return gcd(x, y-x)

#get input
i = input("Enter two numbers:\n")

#define temp holders for a and b
a1 = i[:i.find(" ")]
b1 = i[i.find(" ")+1:]

#make a the bigger number and b the smaller one
if a1 > b1:
    a, b = a1, b1
elif a1 < b1:
    a, b = b1, a1
else:
    a, b = a1, b1

#get gcd and print
ans = gcd(eval(a), eval(b))
print("The GCD is:",ans)