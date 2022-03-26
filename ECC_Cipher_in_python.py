import random

# a point on the elliptic curve
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ' - ' + str(self.y)


class Elliptic_Curve_Cryptography:
    def __init__(self, a, b):
        #y^2 = x^3 + ax + b
        # Bitcoin : a = 0 and b = 7 (y^2 = x^3 + 7)
        self.a = a
        self.b = b

    def point_addition(self, P, Q):
        x1, y1 = P.x, P.y
        x2, y2 = Q.x, Q.y
        # Sometimes we have to make a point addition and sometimes a point doubling (P=Q)
        if x1 == x2 and y1 == y2:
            # Point doubling operation
            m = (3*x1*x1+self.a) / (2*y1)
        else:
            # Point addition operation (P!=Q)
            m = (y2-y1)/ (x2-x1)
        # We have to update x3 and y3 coordinates accordingly
        x3 = m*m - x1 - x2
        y3 = m*(x1-x3) - y1
        return Point(x3, y3)
    
    # It has O(m) linear running time complexity
    def double_and_add(self, n, P):
        temp_point = Point(P.x, P.y)
        binary = bin(n)[3:]
        #print(binary)
        for binary_char in binary:
            # The point doubling operation
            temp_point = self.point_addition(temp_point, temp_point )
            if binary_char == '1':
                # The point addition operation
                temp_point = self.point_addition(temp_point, P)
        return temp_point


if __name__ == '__main__':
    ecc = Elliptic_Curve_Cryptography(-2, 2)
    # The E elleptic curve + the G generator is public
    generator_point = Point(-2, -1)
    #print(ecc.point_addition(generator_point, generator_point))
    #print(ecc.double_and_add(100, generator_point))
    # Alice's random number a
    alice_random = random.randint(2, 1e4)
    # Bob's random number b
    bob_random = random.randint(2, 1e4)
    # Public key with double and add algorithm
    alice_public = ecc.double_and_add(alice_random, generator_point)
    bob_public = ecc.double_and_add(bob_random, generator_point)
    # They can generate the private key which will be the same
    alice_secret_key = ecc.double_and_add(alice_random, bob_public)
    bob_secret_key = ecc.double_and_add(bob_random, alice_public)
    print("Alice secret key is : %s\n" % alice_secret_key)
    print("Bob secret key is : %s\n" % bob_secret_key)