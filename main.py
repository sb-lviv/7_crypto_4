#!/usr/bin/env python3

from .rsa.main import RSA
import argparse
import random
from math import gcd


class Elgamal(RSA):

    def handle_input(self):
        if self.generate_key:
            p = random.randint(10 ** 20, 10 ** 50)
            q = random.randint(2, p)
            x = random.randint(2, p)
            y = Elgamal.power(q, x, p)

            output_file = self.output_file + '.pub'
            output_text = ('{}\n{}\n{}').format(p, q, y)
            RSA.save_to_file(output_file, output_text)

            output_file = self.output_file + '.prv'
            output_text = '{}\n{}'.format(p, x)
            RSA.save_to_file(output_file, output_text)

        elif self.file_to_encrypt is not None:
            keys = RSA.read_from_file(self.key_file_name + '.pub').split('\n')
            p, q, y = [int(x)for x in keys]

            data = RSA.read_from_file(self.file_to_encrypt)
            data, key = Elgamal.encrypt(data, p, q, y)

            with open(self.output_file, 'w') as f:
                for num in data:
                    f.write(str(num) + '\n')
                f.write(str(key))

        elif self.file_to_decrypt is not None:
            p, x = RSA.read_from_file(self.key_file_name + '.prv').split('\n')
            data = RSA.read_from_file(self.file_to_decrypt).split('\n')
            a = int(data[-1])
            data = [int(char) for char in data[:-1]]

            data = Elgamal.decrypt(data, a, int(x), int(p))

            RSA.save_to_file(self.output_file, ''.join(data))

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
            b = b // 2

        return x % c

    @staticmethod
    def encrypt(msg, p, q, y):

        k = random.randint(2, p)
        a = Elgamal.power(q, k, p)
        b = Elgamal.power(y, k, p)
        en_msg = [b * ord(char) for char in msg]

        return en_msg, a

    @staticmethod
    def decrypt(en_msg, a, x, p):

        h = Elgamal.power(a, x, p)
        dr_msg = [chr(int(char)//h) for char in en_msg]

        return dr_msg


if __name__ == "__main__":
    Elgamal().handle_input()
