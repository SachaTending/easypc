## Main information

# Registers
Register numeration starts from 0

Generic registers:
 - r0
 - r1
 - r2
 - r3
 - r4
 - r5
 - r6
 - r7
 - r8
 - r9
 - RAX
 - RBX
 - RBP

Special registers:
 - RSP(Stack pointer)
 - RIP(Instruction pointer)
 - RFLAGS(CPU Flags)
 - RVMM(VMM table pointer)

## Opcode encoding

# Basic structure of opcode
Each opcode is 1 byte long, if opcode is 0xFF, read another byte, but using diffeent instruction set(so technicaly, 0xFF is shift instruction set)

If opcode has operands, read operands

# Decoding operands
1. Read flags
    - Get how long is value, and read bytes specified in bits 0-1, check flags section for more info
    - If bit 2 was set, its a register, get register's value specified in value
    - If bit 3 was set, its a pointer, get value from that pointer(pointer is set via value(from register if bit 3 was set))
      - Get how long is pointer's value, and read bytes specified in bits 4-5, check flags section for more info
2. Read value
    - Read it using length specified in bits 0-1
3. Read register(IF BIT 2 WAS SET)
    - Get register's value(or write) by number specified in value
4. Read pointer(IF BIT 3 WAS SET), or write
    - Get pointer address from register(IF BIT 2 WAS SET)
    - Read bytes, how much bytes specified in bits 4-5, check flags section for more info
5. And thats all!
    - Seriously, value is read, what do you need now?

# Flags
 - bit 0-1: 2 bit long value
   - If value is 0, data is 1 bytes long(8 bit)
   - If value is 1, data is 2 bytes long(16 bit)
   - If value is 2, data is 4 bytes long(32 bit)
   - If value is 3, data is 8 bytes long(64 bit)
 - If bit 2 was set, its a register
 - If bit 3 was set, its a pointer, but how much bytes long is pointer? Answer contained in next 2 bits
 - bit 4-5: 2 bit long value
   - If value is 0, pointer's data is 1 bytes long(8 bit)
   - If value is 1, pointer's data is 2 bytes long(16 bit)
   - If value is 2, pointer's data is 4 bytes long(32 bit)
   - If value is 3, pointer's data is 8 bytes long(64 bit)
 - bit 6-8: reserved

## Opcodes

# NOP
 - Encoded: 0x00(nop)
 - Does nothing, entirely nothing.

# ADD (from), (to)
 - Encoded: 0x01(add) 0x00(flags_1) 0x00(data, length defined by flag) 0x00(flags_2) 0x00(data, length defined by flag)
 - Adds to destiniation

# SUB (from), (how much)
 - Encoded: 0x02(sub) 0x00(flags_1) 0x00(data, length defined by flag) 0x00(flags_2) 0x00(data, length defined by flag)
 - Substracts (how much) from (from)

# MUL (to), (by)
 - Encoded: 0x03(mul) 0x00(flags_1) 0x00(data, length defined by flag) 0x00(flags_2) 0x00(data, length defined by flag)
 - Multiples (to) by (by)

# DIV (to), (by)
 - Encoded: 0x04(div) 0x00(flags_1) 0x00(data, length defined by flag) 0x00(flags_2) 0x00(data, length defined by flag)
 - Divides (to) by (by)

# JMP (to)
 - Encoded: 0x05(jmp) 0x00(flags_1) 0x00(data, length defined by flag)
 - Jumps to (to), simple instruction

# CMP (val1), (val2)
 - Encoded: 0x06(cmp) 0x00(flags_1) 0x00(data, length defined by flag) 0x00(flags_2) 0x00(data, length defined by flag)
 - Compares val1 and val2
  - If val1 == val2:
   - Set flag 0 in RFLAGS
  - Else:
   - Clear flag 0 in RFLAGS

# LESS (val1), (val2)
 - Encoded: 0x07(less) 0x00(flags_1) 0x00(data, length defined by flag) 0x00(flags_2) 0x00(data, length defined by flag)
 - If val1 < val2:
  - Set flag 0 in RFLAGS
 - Else:
  - Clear flag 0 in RFLAGS

# JQ (to)
 - Encoded: 0x08(jq) 0x00(flags_1) 0x00(data, length defined by flag)
 - Jumps to (to) if bit 0 in rflags was set, and clears it

# JEQ (to)
 - Encoded: 0x09(jeq) 0x00(flags_1) 0x00(data, length defined by flag)
 - Same as jq but jumps if bit 0 in rflags not set

# CALL (what)
 - Encoded: 0x0a(call) 0x00(flags_1) 0x00(data, length defined by flag)
 - Calls (what), before calling, stores in stack return address(return address is addr of opcode+2(opcode and flags)+(data len)), addr in stack is 64 bit, and then, rsp = rsp+8

# RET
 - Encoded: 0x0b(ret)
 - Substracts from rsp 8, and then gets return address, then, it jumps to it

thats all, i think...