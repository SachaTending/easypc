from cpu import CPU
from struct import unpack, pack

def int_to_reg(val: int):
    return ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'RAX', 'RBX', 'RBP', 'RSP', 'RIP', 'RFLAGS', 'RVMM', 'RIDT'][val]

def parse_flags(flags: int):
    blen = [1, 2, 4, 8][flags & 0b11]
    bp = {1: 'b', 2: 'h', 4: 'i', 8: 'l'}[blen]
    is_reg = bool(flags&0b100)
    is_pointer = bool(flags&0b1000)
    plen = flags&0b110000
    plen = plen >> 4
    plen = [1, 2, 4, 8][plen]
    pp = {1: 'b', 2: 'h', 4: 'i', 8: 'l'}[plen]
    if bool(flags&0b1000000): bp = bp.capitalize()
    def get_val(cpu: CPU):
        v = cpu.mem[cpu.regs.RIP:cpu.regs.RIP+blen]
        cpu.regs.RIP+=blen
        v = bytearray(v)
        v = unpack(bp, v)[0]
        if is_reg:
            v = getattr(cpu.regs, int_to_reg(v))
        if is_pointer:
            v = unpack(pp, bytearray(cpu.mem[v:v+plen]))[0]
        return v
    def set_val(cpu: CPU, nwal: int):
        v = cpu.mem[cpu.regs.RIP:cpu.regs.RIP+blen]
        v = bytearray(v)
        v = unpack(bp, v)[0]
        if is_reg:
            if is_pointer:
                dest = getattr(cpu.regs, int_to_reg(v))
                dest = bytearray(cpu.mem[v:v+pp])
                dest = unpack(pp, dest)[0]
                cpu.mem[dest] = pack(pp, nwal)
            else:
                setattr(cpu.regs, int_to_reg(v), nwal)
        elif is_pointer:
            cpu.mem[v] = pack(pp, nwal)
    return get_val, set_val

def nop(cpu: CPU):
    cpu.regs.RIP+=1

def add(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    fr = pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf2 = parse_flags(f2)
    to = pf2[0](cpu)
    pf2[1](cpu, to+fr)

def sub(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    fr = pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf2 = parse_flags(f2)
    to = pf2[0](cpu)
    pf1[1](cpu, fr-to)

def mul(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    fr = pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf2 = parse_flags(f2)
    to = pf2[0](cpu)
    pf1[1](cpu, fr*to)

def div(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    fr = pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf2 = parse_flags(f2)
    to = pf2[0](cpu)
    pf1[1](cpu, fr/to)

def jmp(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    cpu.regs.RIP = pf1[0](cpu)

def cmp(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    v1 = pf1[0](cpu)
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf2 = parse_flags(f1)
    v2 = pf2[0](cpu)
    if v1 == v2:
        cpu.regs.RFLAGS |= 1
    else:
        cpu.regs.RFLAGS &= ~1

def jq(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    to = pf1[0](cpu)
    if cpu.regs.RFLAGS & 1:
        cpu.regs.RIP = to
        cpu.regs.RFLAGS &= ~1

def jeq(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    cpu.regs.RIP+=1
    pf1 = parse_flags(f1)
    to = pf1[0](cpu)
    if not (cpu.regs.RFLAGS & 1):
        cpu.regs.RIP = to

def call(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    pf1 = parse_flags(f1)
    to = pf1[0](cpu)
    cpu.mem[cpu.regs.RSP] = pack("L", cpu.regs.RIP)
    cpu.regs.RIP = to

def ret(cpu: CPU):
    cpu.regs.RIP+=1
    raddr = cpu.mem[cpu.regs.RSP-8]
    cpu.regs.RSP-=8
    cpu.regs.RIP=raddr

def and_op(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    pf1 = parse_flags(f1)
    val = pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    pf2 = parse_flags(f2)
    val2 = pf2[0](cpu)
    pf1[1](cpu, val&val2)

def or_op(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    pf1 = parse_flags(f1)
    val = pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    pf2 = parse_flags(f2)
    val2 = pf2[0](cpu)
    pf1[1](cpu, val|val2)

def xor(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    pf1 = parse_flags(f1)
    val = pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    pf2 = parse_flags(f2)
    val2 = pf2[0](cpu)
    pf1[1](cpu, val^val2)

def stop(cpu: CPU):
    cpu.running = False

def mov(cpu: CPU):
    cpu.regs.RIP+=1
    f1 = cpu.mem[cpu.regs.RIP]
    pf1 = parse_flags(f1)
    pf1[0](cpu)
    f2 = cpu.mem[cpu.regs.RIP]
    pf2 = parse_flags(f2)
    val2 = pf2[0](cpu)
    pf1[1](cpu, val2)

def setup_instr_set_0(cpu: CPU):
    cpu.op(0)(nop)
    cpu.op(1)(add)
    cpu.op(2)(sub)
    cpu.op(3)(mul)
    cpu.op(4)(div)
    cpu.op(5)(jmp)
    cpu.op(6)(cmp)
    cpu.op(7)(jq)
    cpu.op(8)(jeq)
    cpu.op(9)(call)
    cpu.op(10)(ret)
    cpu.op(11)(and_op)
    cpu.op(12)(or_op)
    cpu.op(13)(xor)
    cpu.op(14)(stop)
    cpu.op(15)(mov)