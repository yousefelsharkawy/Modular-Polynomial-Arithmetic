import re
import numpy as np
import time

class polynomial:
    def __init__(self,**kwargs):
        self.p = kwargs['p']
        if 'coffecients' in kwargs and 'orders' in kwargs:
            coffecients = np.array(kwargs['coffecients'])
            orders = np.array(kwargs['orders'])
        elif 'input' in kwargs:
            input = kwargs['input']
            input = input.lower()
            input = input.replace(' ','')
            if input[0] != '-':
                input = '+' + input
            coffecients = []
            orders = []
            x = re.findall(r'([+-]?\d*)x\^(\d+)',input)
            for term in x:
                coffecients.append(float(term[0]))
                orders.append(float(term[1]))
        coupled = zip(coffecients,orders)
        coupled = sorted(coupled,key=lambda x: x[1],reverse=True)
        self.coffecients = []
        self.orders = []
        for item in coupled:
            self.coffecients.append(item[0])
            self.orders.append(item[1])
        self.coffecients = np.array(self.coffecients)
        self.orders = np.array(self.orders)

    def __add__(self,other):
        coefficents = []
        orders = []
        for i in range(len(self.orders)):
            if self.orders[i] in other.orders:
                index = np.where(other.orders == self.orders[i])[0][0]
                coefficents.append(self.coffecients[i]+other.coffecients[index])
                orders.append(self.orders[i])
            else:
                coefficents.append(self.coffecients[i])
                orders.append(self.orders[i])
        for i in range(len(other.orders)):
            if other.orders[i] not in self.orders:
                coefficents.append(other.coffecients[i])
                orders.append(other.orders[i])
        coefficents = np.array(coefficents)
        orders = np.array(orders)
        while 0.0 in coefficents:
            index = np.where(coefficents == 0.0)[0][0]
            coefficents = np.delete(coefficents,index)
            orders = np.delete(orders,index)
        kwargs = {'coffecients':coefficents,'orders':orders,'p':self.p}
        return polynomial(**kwargs)

    def __sub__(self,other):
        coefficents = []
        orders = []
        for i in range(len(self.orders)):
            if self.orders[i] in other.orders:
                index = np.where(other.orders == self.orders[i])[0][0]
                coefficents.append(self.coffecients[i]-other.coffecients[index])
                orders.append(self.orders[i])
            else:
                coefficents.append(self.coffecients[i])
                orders.append(self.orders[i])
        for i in range(len(other.orders)):
            if other.orders[i] not in self.orders:
                coefficents.append(-other.coffecients[i])
                orders.append(other.orders[i])
        coefficents = np.array(coefficents)
        orders = np.array(orders)
        while 0.0 in coefficents:
            index = np.where(coefficents == 0.0)[0][0]
            coefficents = np.delete(coefficents,index)
            orders = np.delete(orders,index)
        kwargs = {'coffecients':coefficents,'orders':orders,'p':self.p}
        return polynomial(**kwargs)
    def __mul__(self,other):
        coefficients = np.outer(other.coffecients,self.coffecients)
        orders = np.add.outer(other.orders,self.orders)
        output = polynomial(coffecients=[0],orders=[0],p=self.p)
        for i in range(coefficients.shape[0]):
            output += polynomial(coffecients=coefficients[i],orders=orders[i],p=self.p)
        return output
    
    def __truediv__(self,other):
        if other.coffecients[0] == 0:
            raise ValueError('Division by zero')        
        if self.orders[0] < other.orders[0]:
            quotient =  polynomial(coffecients=[0],orders=[0],p=self.p)
            remainder = self
            return quotient,remainder
        else:
            quotient = polynomial(coffecients=[0],orders=[0],p=self.p)
            remainder = self
            while remainder.orders[0] >= other.orders[0]:
                coefficent = remainder.coffecients[0]/other.coffecients[0]
                order = remainder.orders[0]-other.orders[0]
                term = polynomial(coffecients=[coefficent],orders=[order],p=self.p)
                quotient += term
                remainder -= term*other
            return quotient,remainder
    
    def __str__(self):
        output = ''
        for i in range(len(self.orders)):
            if self.coffecients[i] > 0:
                output += '+' + str(self.coffecients[i]) + 'x^' + str(int(self.orders[i])) + ' '
            else:
                output += str(self.coffecients[i]) + 'x^' + str(int(self.orders[i])) + ' '
        return output
             


tic = time.time()
kwargs_a = {'input':'1x^0+2x^1+4x^7+2x^3+5x^6', 'p':4}
a = polynomial(**kwargs_a)
kwargs_b = {'input':'1x^1-10x^0', 'p':4}
b = polynomial(**kwargs_b)

c = a + b
d = a - b
x = a * b
quotient,reminder = a / b
toc = time.time()
print("a = "  + str(a))
print("b = " + str(b))
print("a + b = " + str(c))
print("a - b = " + str(d))
print("a * b = " + str(x))
print("a / b = " + str(quotient) + " remainder " + str(reminder))
print("time = " + str((toc-tic)*1000) + " ms")