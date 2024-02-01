class Flags:
    is_reg: bool = False
    is_pointer: bool = False
    pointer_size: int = 1

SIZE_CAST: list[int] = [0b0, 0b01, 0b10, 0b11]
PSIZE_CAST: list[int] = [0b0, 0b010000, 0b100000, 0b110000]

POINTER_SIZE_CAST: dict[int, int] = {1: 0, 2: 1, 4: 2, 8: 3}

REGISTER = 0b100
POINTER = 0b1000
SIGNED_VALUE = 0b1000000

"""
dict[int, int] contains relocation info
{pos in bytearray: value needs to be relocated}
"""

def gen_flags(fl: Flags, n: int):
    f = 0
    if n.bit_count() > 31:
        f |= SIZE_CAST[3]
    elif n.bit_count() > 15:
        f |= SIZE_CAST[2]
    elif n.bit_count() > 7:
        f |= SIZE_CAST[1]
    # if n below 256, no bit setting needed.
    if fl.is_reg: f |= REGISTER
    if fl.is_pointer: f |= POINTER
    if n < 0: f |= SIGNED_VALUE
    f |= PSIZE_CAST[POINTER_SIZE_CAST[fl.pointer_size]]
    return f

def add(num1: tuple[int, Flags], num2: tuple[int, Flags]) -> tuple[dict[int, int], bytearray]:
    pass