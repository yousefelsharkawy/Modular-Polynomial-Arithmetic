import re
import numpy as np
import time

class polynomial:
    def __init__(self,p,**kwargs):
        self.p = p
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

    def __add__(self,other,modular=True):
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
        if modular:
            if self.p != other.p:
                raise ValueError('Cannot add polynomials with different modulus')
            coefficents = coefficents % self.p
        while 0.0 in coefficents:
            index = np.where(coefficents == 0.0)[0][0]
            coefficents = np.delete(coefficents,index)
            orders = np.delete(orders,index)
        kwargs = {'coffecients':coefficents,'orders':orders}
        return polynomial(p=self.p,**kwargs)

    def __sub__(self,other,modular=True):
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
        if modular:
            if self.p != other.p:
                raise ValueError('Cannot sub polynomials with different modulus')
            coefficents = coefficents % self.p
        while 0.0 in coefficents:
            index = np.where(coefficents == 0.0)[0][0]
            coefficents = np.delete(coefficents,index)
            orders = np.delete(orders,index)
        kwargs = {'coffecients':coefficents,'orders':orders}
        return polynomial(p=self.p,**kwargs)
    
    def __mul__(self,other,modular=True):
        coefficients = np.outer(other.coffecients,self.coffecients)
        orders = np.add.outer(other.orders,self.orders)
        output = polynomial(coffecients=[0],orders=[0],p=self.p)
        for i in range(coefficients.shape[0]):
            output += polynomial(coffecients=coefficients[i],orders=orders[i],p=self.p)
        if modular:
            if self.p != other.p:
                raise ValueError('Cannot mul polynomials with different modulus')
            output.coffecients = output.coffecients % self.p
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
    def __eq__(self,other):
        for i in range(len(self.orders)):
            if self.orders[i] != other.orders[i]:
                return False
            if self.coffecients[i] != other.coffecients[i]:
                return False
        return True

             

class modular_polynomial():
    def __init__(self,**kwargs):
        self.p = kwargs['p']
        if 'poly2' in kwargs:
            self.poly2 = polynomial(p=self.p,**kwargs['poly2'])
        self.poly1 = polynomial(p=self.p,**kwargs['poly1'])
        self.mod_ploy = polynomial(p=self.p,**kwargs['m(x)'])
    
    
    def add(self):
        if "poly2" not in self.__dict__:
            raise ValueError("No second polynomial to add")
        if self.poly1.p != self.poly2.p:
            raise ValueError('Cannot add polynomials with different modulus')
        return self.poly1 + self.poly2
    
    
    def sub(self):
        if "poly2" not in self.__dict__:
            raise ValueError("No second polynomial to sub")

        if self.poly1.p != self.poly2.p:
            raise ValueError('Cannot sub polynomials with different modulus')
        return self.poly1 - self.poly2
    
    def mul(self):
        if "poly2" not in self.__dict__:
            raise ValueError("No second polynomial to multiply")
        if self.poly1.p != self.poly2.p:
            raise ValueError('Cannot mul polynomials with different modulus')
        temp =  self.poly1 * self.poly2
        _, reminder =  temp / self.mod_ploy
        return reminder

    def extended_euclidean(self,poly):
        a1 = polynomial(coffecients=[1],orders=[0],p=self.p)
        a2 = polynomial(coffecients=[0],orders=[0],p=self.p)
        a3 = self.mod_ploy
        b1 = polynomial(coffecients=[0],orders=[0],p=self.p)
        b2 = polynomial(coffecients=[1],orders=[0],p=self.p)
        if poly == "first":
            b3 = self.poly1
        elif poly == "second":
            b3 = self.poly2
        else:
            raise ValueError("poly must be 'first' or 'second'")
        while b3.orders[0] != 0:
            q,r = a3/b3
            t1 = a1 - b1*q
            t2 = a2 - b2*q
            t3 = a3 - b3*q
            a1 = b1
            a2 = b2
            a3 = b3
            b1 = t1
            b2 = t2
            b3 = t3
        if b3 == polynomial(coffecients=[0],orders=[0],p=self.p):
            return a3,None
        elif b3 == polynomial(coffecients=[1],orders=[0],p=self.p):
            return b3,b2
        
    def inverse(self,poly="first"):
        if poly != "first" and poly != "second":
            raise ValueError("poly must be 'first' or 'second'")
        if poly == "first":
            if self.poly1.orders[0] == 0:
                raise ValueError("poly1 must be non-zero")
            gcd , inv = self.extended_euclidean(poly="first")
        elif poly == "second":
            if self.poly2.orders[0] == 0:
                raise ValueError("poly2 must be non-zero")
            gcd , inv = self.extended_euclidean(poly="second")
        return gcd,inv
        
    def div(self,poly="first"):
        if poly != "first" and poly != "second":
            raise ValueError("poly must be 'first' or 'second'")
        if poly == "first":
            if self.poly1.orders[0] == 0:
                raise ValueError("poly1 must be non-zero")
            gcd , inv = self.inverse(poly="first")
        elif poly == "second":
            if self.poly2.orders[0] == 0:
                raise ValueError("poly2 must be non-zero")
            gcd , inv = self.inverse(poly="second")
        if inv is not None:
            if poly == 'first':
                result = ((inv * self.poly2) / self.mod_ploy)
                return result[1] #return only the reminder of the division
            elif poly == 'second':
                result =  ((inv * self.poly1) / self.mod_ploy)
            return result[1]
        else:
            return "no inverse"
    
    def multiplicative_identity(self,poly="first"):
        gcd , inv = self.inverse(poly=poly)
        if inv is not None:
            if poly == 'first':
                return inv * self.poly1
            elif poly == 'second':
                result =  ((inv * self.poly2) / self.mod_ploy)
            return result[1]
        else:
            return "no inverse"
    def __str__(self):
        if 'poly2' in self.__dict__:
            return "First polynomial: " + str(self.poly1) + " Second polynomial: " + str(self.poly2) + " modular polynomial: " + str(self.mod_ploy) + " p: " + str(self.p)
        else:
            return "First polynomial: " + str(self.poly1) + " modular polynomial: " + str(self.mod_ploy) + " p: " + str(self.p)




import sys
import time

tic = time.time()
if len(sys.argv) == 1:
    print("No arguments given")
    sys.exit(0)
elif len(sys.argv) == 6:
    args = {'poly1':{'input':sys.argv[1]},'poly2':{'input':sys.argv[2]},'m(x)':{'input':sys.argv[3]},'p':int(sys.argv[4])}
    field = modular_polynomial(**args)
    operations  = sys.argv[5][1:-1]
    operations = operations.lower()
    operations = operations.split(',')
    #print(operations)
    print('The inputs to the program are: ' + str(field) )
    print('------------------------------------------------------------')
    for operation in operations:
        if operation == 'add':
            print('The result of the addition is: ' + str(field.add()))
        elif operation == 'sub':
            print('The result of the subtraction is: ' + str(field.sub()))
        elif operation == 'mul':
            print('The result of the multiplication is: ' + str(field.mul()))
        elif operation == 'div1':
            print('The division of the second polynomial on the first polynomil is: ' + str(field.div(poly="first")))
        elif operation == 'div2':
            print('The division of the first polynomial on the second polynomil is: ' + str(field.div(poly="second")))
        elif operation == 'gcd1':
            gcd1 , inv1 = field.inverse(poly="first")
            print('The result of the extended gcd of the first polynomial is: ' + str(gcd1) + ' and the inverse is: ' + str(inv1))
        elif operation == 'gcd2':
            gcd2 , inv2 = field.inverse(poly="second")
            print('The result of the extended gcd of the second polynomial is: ' + str(gcd2) + ' and the inverse is: ' + str(inv2))
        else:
            raise ValueError("Operation not found")
        print('------------------------------------------------------------')
    
elif len(sys.argv) == 5:
    args = {'poly1':{'input':sys.argv[1]},'m(x)':{'input':sys.argv[2]},'p':int(sys.argv[3])}
    field = modular_polynomial(**args)
    operations  = sys.argv[4][1:-1]
    operations = operations.lower()
    operations = operations.split(',')
    #print(operations)
    #print(field)
    print('The inputs to the program are: ' + str(field))
    for operation in operations:
        if operation == 'gcd1':
            gcd, inv = field.inverse(poly="first")
            print('The result of the extended gcd of the first polynomial is: ' + str(gcd) + ' and the inverse is: ' + str(inv))
        else:
            raise ValueError("Operation not found")
        print('------------------------------------------------------------')
else:
    raise ValueError("Wrong number of arguments")

toc = time.time()

print('The program took ' + str((toc-tic)*1000) + ' ms to run')