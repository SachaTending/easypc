from memory import Memory
from cpu import CPU
from arch import setup_instr_set_0

mem = Memory(4096)
mem[0] = 0x0e
cpu = CPU(mem)
setup_instr_set_0(cpu)
cpu.run()