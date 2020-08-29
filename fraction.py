########################################################
#                     Fractions                        #
########################################################

def gcd(m, n):
    while m % n != 0:
        oldm = m
        oldn = n
        m = oldn
        n = oldm % oldn
    return n

class Fraction:

    def __init__(self, top, bottom):

        self.num = top
        self.den = bottom

    
    def __str__(self):

        fraction = str(self.num) + '/' + str(self.den)
        return fraction


    def __add__(self, f2):

        newnum = self.num * f2.den + self.den * f2.num
        newden = self.den * f2.den
        
        common = gcd(newnum, newden)
        
        return Fraction(newnum//common, newden//common)
    
    
    def __sub__(self, f2):
        
        newnum = self.num * f2.den - self.den * f2.num
        newden = self.den * f2.den
        
        common = gcd(newnum, newden)
        
        return Fraction(newnum//common, newden//common)
    
    def __eq__(self, other):
        
        firstnum = self.num * other.den
        secondnum = other.num * self.den
        
        return firstnum == secondnum

    def __lt__(self, other):
        
        firstnum = self.num * other.den
        secondnum = other.num * self.den
        
        return firstnum < secondnum

    def __gt__(self, other):
        
        firstnum = self.num * other.den
        secondnum = other.num * self.den
        
        return firstnum > secondnum

f1 = Fraction(1, 2)
f2 = Fraction(1, 3)

print(f1 - f2)