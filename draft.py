'''
# define class polynomial that stores a polynomial as a list of coffecients and order pairs
# define methods to add, subtract, multiply, and divide polynomials
class polynomial:
    def __init__(self,coffecients,order):
        self.coffecients = coffecients
        self.order = order
    def __add__(self,other):
        # add two polynomials
        # return a new polynomial
        coffecients = []
        order = []
        for i in range(max(self.order)+1):
            coffecients.append(0)
            order.append(i)
        for i in range(len(self.order)):
            coffecients[self.order[i]] += self.coffecients[i]
        for i in range(len(other.order)):
            coffecients[other.order[i]] += other.coffecients[i]
        return polynomial(coffecients,order)
    def __sub__(self,other):
        # subtract two polynomials
        # return a new polynomial
        coffecients = []
        order = []
        for i in range(max(self.order)+1):
            coffecients.append(0)
            order.append(i)
        for i in range(len(self.order)):
            coffecients[self.order[i]] += self.coffecients[i]
        for i in range(len(other.order)):
            coffecients[other.order[i]] -= other.coffecients[i]
        return polynomial(coffecients,order)
    def __mul__(self,other):
        # multiply two polynomials
        # return a new polynomial
        coffecients = []
        order = []
        for i in range(max(self.order)+max(other.order)+1):
            coffecients.append(0)
            order.append(i)
        for i in range(len(self.order)):
            for j in range(len(other.order)):
                coffecients[self.order[i]+other.order[j]] += self.coffecients[i]*other.coffecients[j]
        return polynomial(coffecients,order)
    def __truediv__(self,other):
        # divide two polynomials
        # return a new polynomial
        coffecients = []
        order = []
        for i in range(max(self.order)+1):
            coffecients.append(0)
            order.append(i)
        for i in range(len(self.order)):
            coffecients[self.order[i]] += self.coffecients[i]
        for i in range(len(other.order)):
            coffecients[other.order[i]] -= other.coffecients[i]
        return polynomial(coffecients,order)


polynomial1 = polynomial([1,2,3],[0,1,2])
polynomial2 = polynomial([1,2,3],[0,1,2])
polynomial3 = polynomial1 * polynomial2
print(polynomial3.coffecients)
'''

x = "5x^2-3x+2"
# extract the coefficients and order pairs fro x
def extract(x):
    # extract the coefficients and order pairs from x
    # return a list of coefficients and a list of order pairs
    coffecients = []
    order = []
    for i in range(len(x)):
        if x[i] == 'x':
            if x[i+1] == '^':
                coffecients.append(int(x[i-1]))
                order.append(int(x[i+2]))
            else:
                coffecients.append(int(x[i-1]))
                order.append(1)   
    return coffecients, order

print(extract(x))
