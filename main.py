import bitstring as bs
import sha256 as sh
import header as hd
import datetime

if __name__ == '__main__':
    # Target
    max_value = 26959535291011309493156476344723991336010898738574164086137773096960
    difficulty = 13008091666971.90
    target = max_value / difficulty
    # Construction of block header
    # Block 600,000 is used as example
    version = '0x20000000'
    prev_hash = '0x00000000000000000003ecd827f336c6971f6f77a0b9fba362398dd867975645'
    merkle_root = '0x66b7c4a1926b41ceb2e617ddae0067e7bfea42db502017fde5b695a50384ed26'
    time = int(datetime.datetime(2019, 10, 18, 19, 4, 21).timestamp())
    bits = 387294044
    nonce = 1066642855
    header = hd.header(version, prev_hash, merkle_root, time, bits, nonce)
    # Looking for nonce to be under target
    block_hash = bs.BitString(uint=sh.sha256(sh.sha256(header)).uintle, length=256)
    while block_hash.uint > int(target):
        nonce += 1
        block_hash = bs.BitString(uint=sh.sha256(sh.sha256(header)).uintle, length=256)
    print('The nonce is: ' + str(nonce) + '\nThe hash is: ' + str(block_hash))
