import random
import sympy
import getpass
import bip_utils
import binascii
from mod import Mod
from bip_utils import (
    Bip39EntropyBitLen, Bip39EntropyGenerator, Bip39WordsNum, Bip39Languages, Bip39MnemonicGenerator, Bip39MnemonicEncoder
)
from bip_utils import Bip39Languages, Bip39WordsNum, Bip39MnemonicGenerator, Bip39SeedGenerator

def set_P():
    P = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',16)
    random_seed = int(bytes(input("Introduce any characters to generate a random P: "),'utf-8').hex(), 16)
    random.seed(random_seed)
    P = random.randint(P+1, P*16*16+15)
    P = sympy.nextprime(P)
    return P

def pool_keys():
    P = set_P()
    admin_key = 0;
    has_admin = input("Will you use an administrator key? [Y/N]: ")
    if has_admin == 'Y':
        admin_key = int("0x" + input("introduce the administrator key: "),16)
    num_keys = int(input("How many keys do you want to pool?"))
    keys = []
    for i in range(num_keys):
        num_key = int(input("Introduce your participant number(key number) :"))
        key = int("0x" + input("Introduce your key: "), 16)
        keys.append([num_key, key])
    secret_int = Mod(0,P)
    for key1 in keys:
        numeric_value = Mod(1,P)
        for key2 in keys:
            if(key1!=key2):
                numeric_value = numeric_value * ((-key2[0])*(Mod(key1[0]-key2[0], P))**(-1))
        numeric_value = numeric_value * key1[1]
        secret_int = secret_int + numeric_value
    secret_int = secret_int - admin_key
    print("")
    print(bytes.fromhex(hex(secret_int._value)[2:]).decode('utf-8'))
    print("")


def distribute_keys():
    P = set_P()
    random.seed(P)
    distributed_keys = []
    polinomial_factors = []
    has_admin = input("Do you want to generate an administrator key? [Y/N]: ")
    admin_key = 0
    if has_admin == 'Y':
        admin_key = random.randint(0,P)
    S = input("Introduce the twelve mnemonic words separated by spaces: ")
    mnemonic_code = int("0x" + S.encode().hex(), 16)
    secret = Mod(0,P)
    secret = secret + admin_key + mnemonic_code
    N = int(input("Introduce the number of keys: "))
    T = int(input("Introduce the threshold: "))

    for i in range(T-1):
        polinomial_factors.append(random.randrange(P-1))
    for i in range(1,N+1):
        key = Mod(0,P)
        for j in range(len(polinomial_factors)):
            key = key + i**(T-1-j)*polinomial_factors[j]
        key = key + secret
        distributed_keys.append([i,key._value])
    print("")
    print("keys:")
    for item in distributed_keys:

        print("")
        print(item[0])
        print(hex(item[1])[2:])
        print("")
    if(has_admin=='Y'):
        print("administrator key:")
        print(hex(admin_key)[2:])
        print("")


if __name__ == "__main__":
    while(1):
        print("Welcome to the bip-39 key splitter for shared holding. Please select one of the specified options:")
        print("P - Pool keys")
        print("D - Distribute keys")
        print("M - Manual")
        print("I - Information")
        print("Q - Quit")
        choice = input("Option: ")

        if choice == 'P':
            pool_keys()
        if choice == 'D':
            distribute_keys()
        if choice == 'Q':
            exit()

