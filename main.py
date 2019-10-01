#!/usr/bin/env python3

from rsa.main import RSA
import argparse
import random
from math import gcd


class Elgamal(RSA):

    def handle_input(self):
        if self.generate_key:
            pass

        elif self.file_to_encrypt is not None:
            pass

        elif self.file_to_decrypt is not None:
            pass

        else:
            raise RuntimeError('invalid input')

    @staticmethod
    def gen_key(q):

        key = random.randint(10 ** 20, q)
        while gcd(q, key) != 1:
            key = random.randint(10 ** 20, q)

        return key

    @staticmethod
    def power(a, b, c):
        x = 1
        y = a

        while b > 0:
            if b % 2 == 0:
                x = (x * y) % c
            y = (y * y) % c
            b = int(b / 2)

        return x % c

    @staticmethod
    def encrypt(msg, q, h, g):

        en_msg = []

        k = gen_key(q)  # Private key for sender
        s = power(h, k, q)
        p = power(g, k, q)

        for i in range(0, len(msg)):
            en_msg.append(msg[i])

        print("g^k used : ", p)
        print("g^ak used : ", s)
        for i in range(0, len(en_msg)):
            en_msg[i] = s * ord(en_msg[i])

        return en_msg, p

    @staticmethod
    def decrypt(en_msg, p, key, q):

        dr_msg = []
        h = power(p, key, q)
        for i in range(0, len(en_msg)):
            dr_msg.append(chr(int(en_msg[i]/h)))

        return dr_msg


if __name__ == "__main__":
    Elgamal().handle_input()
