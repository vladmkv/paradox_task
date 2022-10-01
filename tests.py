if __name__ == '__main__':
    bits = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1]
    flip_bits = bits[8:0:-1]
    print(flip_bits)

    byte = 0

    for bit in flip_bits:
        byte = (byte << 1) + bit

    print(byte)