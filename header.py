import bitstring as bs


# Bitcoin header builder
def header(ver, prevh, merkle, time, bit, non):
    version = bs.BitString(ver)
    version = bs.BitString(uint=version.uintle, length=32)
    prevhash = bs.BitString(prevh)
    version.append(bs.BitString(uint=prevhash.uintle, length=256))
    merkle_root = bs.BitString(merkle)
    version.append(bs.BitString(uint=merkle_root.uintle, length=256))
    time_bit = bs.BitString(uint=time, length=32)
    version.append(bs.BitString(uint=time_bit.uintle, length=32))
    bits = bs.BitString(uint = bit, length=32)
    version.append(hex(bits.uintle))
    nonce = bs.BitString(uint=non, length=32)
    version.append(hex(nonce.uintle))
    return version
