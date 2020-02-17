import bitstring as bs


# Bitstring functions
def ch(x, y, z):
    return (x & y) ^ (~x & z)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def rotr(x, n):
    t1 = (x >> n)
    t2 = (x << (len(x) - n))
    return t1|t2


def up_sigma_0(x):
    t1 = rotr(x, 2)
    t2 = rotr(x, 13)
    t3 = rotr(x, 22)
    return t1 ^ t2 ^ t3


def up_sigma_1(x):
    t1 = rotr(x, 6)
    t2 = rotr(x, 11)
    t3 = rotr(x, 25)
    return t1 ^ t2 ^ t3


def lo_sigma_0(x):
    t1 = rotr(x, 7)
    t2 = rotr(x, 18)
    return t1 ^ t2 ^ (x >> 3)


def lo_sigma_1(x):
    t1 = rotr(x, 17)
    t2 = rotr(x, 19)
    return t1 ^ t2 ^ (x >> 10)


def bs_sum(*args):
    aux = 0
    for arg in args:
        w = len(arg)
        aux += arg.uint
        aux = aux % (2**w)
    return bs.BitString(uint=aux, length=w)


# Prime root constants
def isprime(n):
    aux = 0
    if n == 2:
        return True

    if n != 2 and n % 2 == 0:
        return False

    for i in range(1, n + 1, 2):
        if n % i == 0:
            aux += 1

    if aux == 2:
        return True
    else:
        return False


def prime_seq(n):
    p = [2]
    i = 1
    j = 3

    while i < n:
        if isprime(j):
            p.append(j)
            i +=1
        j += 2

    return p


def hex8(n, m):
    m = n ** (1/m)
    aux = int((m - int(m))*(16**8))
    return bs.BitString(uint=aux, length=32)


# Padding to 512 bits
def padding(x):
    l = len(x)
    bit = bs.BitString(bin = '0b1')
    x.append(bit)
    k1 = bs.BitString(uint = 0, length = (448 - len(x)) % 512)
    x.append(k1)
    k2 = bs.BitString(uint = l, length = 64)
    x.append(k2)
    return x


# Construction of 64 words
def word(x):
    w = []
    for i in range(0, 16):
        w.append(x[32 * i: 32 * (i + 1)])

    for i in range(16, 64):
        args = [lo_sigma_1(w[i - 2]), w[i - 7], lo_sigma_0(w[i - 15]), w[i - 16]]
        w.append(bs_sum(*args))
    return w


# Initial hash
def h0():
    n = 8
    h = prime_seq(n)
    h_0 = bs.BitString('')
    for i in range(0, n):
        h_0.append(hex8(h[i], 2))
    return h_0


# Initial constants
def k0():
    n = 64
    k_0 = prime_seq(n)
    for i in range(0, n):
        k_0[i] = hex8(k_0[i], 3)
    return k_0


# Working constants
def working_constants(x, sha):
    w = word(x)
    k_0 = k0()
    cons = sha
    for i in range(0, 64):
        args1 = [cons[7],  up_sigma_1(cons[4]),  ch(cons[4], cons[5], cons[6]),  k_0[i], w[i]]
        t1 = bs_sum(*args1)
        args2 = [up_sigma_0(cons[0]), maj(cons[0], cons[1], cons[2])]
        t2 = bs_sum(*args2)
        for j in range(7, 4, -1):
            cons[j] = cons[j - 1]
        args3 = [cons[3], t1]
        cons[4] = bs_sum(*args3)
        for k in range(3, 0, -1):
            cons[k] = cons[k - 1]
        args4 = [t1, t2]
        cons[0] = bs_sum(*args4)
    return cons


# Final hash
# Uses working constants
def final_hash(w, sha):
    res = bs.BitString('')
    for i in range(0, 8):
        res.append(bs_sum(sha[i], w[i]))
    return res


# Unpacking
def mesage_size(x):
    n = int(len(x) / 512)
    w = []
    for i in range(0, n):
        w.append(x[512 * i: 512 * (i + 1)])
    return w


def hash_size(sha):
    h =[]
    for i in range(0, 8):
        h.append(sha[32 * i: 32 * (i + 1)])
    return h


# Full sha256 implementation
def sha256(x):
    padding(x)
    m = mesage_size(x)
    sha = h0()
    for i in range(0, len(m)):
        w = working_constants(m[i], hash_size(sha))
        sha = final_hash(w, hash_size(sha))
    return sha
