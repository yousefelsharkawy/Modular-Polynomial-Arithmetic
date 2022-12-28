# Modular-Polynomial-Arithmetic

## Overview on Galois fields of the form $GF(p^n)$
- in here, all the polynomials in the system have 2 properties 
  - the coefficients are always in $mod(p)$ range 
  - the polynomials are always in $mod(m(x))$ range
- we ensure that the above system is a field if 
  - **p** is a **prime** number 
  - **m(x)** is a prime polynomial or sometimes called **irreducable polynomial**, which means it can never result as a multiplication of 2 polynomials 

*** 

## what is a field ?
a field is an enclosed system where all the elements in that system are closed under the following operations 
- addition
- subtraction
- multiplication 
- division (by finding the inverse of the second element and multplying it with the first element)

therefore the above polynomial arithmetic module is field if given a prime p and irreducable m(x)

***

## installation steps 
- clone the library 
- pip install requirements.txt

***

## running and usage  

- this program is a **command line argument** program that recieves the inputs as per the following format 

`python polynomials.py first_polynomial [optional_second_polynomial] modular_polynomial_m(x) P [list of comma-separated operations to be done]`

- each polynomial has all of this its terms on this following convention: $ax^n$ as a is the coefficient of the term and n is the power 

- the list of the supported operations to be made 
  - in the case of inputing 2 polynomials
    - **add**: this adds the 2 polynomials given and returns the result in $mod m(x)$ and coefficients in mod p
    - **sub**: this subtracts  the 2 polynomials given and returns the result in $mod m(x)$ and coefficients in mod p
    - **mul**: this multiplies the 2 polynomials given and returns the result in $mod m(x)$ and coefficients in mod p
    - **div1**: this divides the second polynomial by the first polynomial returns the result in $mod m(x)$ and coefficients in mod p
    - **div2**: this divides the first polynomial by the second polynomial returns the result in $mod m(x)$ and coefficients in mod p
    - **gcd1**: this returns the greatest common divisor between the first polynomial and m(x), it also returns the inverse -if exixts according to the constarins we mentioned above-
    - **gcd2**: this returns the greatest common divisor between the second polynomial and m(x), it also returns the inverse -if exixts according to the constarins we mentioned above-
  - in case of specifying only 1 polynomial to the program 
    - **gcd1**: this returns the greatest common divisor between the first and only polynomial given and m(x), it also returns the inverse -if exixts according to the constarins we mentioned above-
    
