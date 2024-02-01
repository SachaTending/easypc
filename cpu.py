from memory import Memory
from typing import Callable

from dataclasses import dataclass

@dataclass
class Registers:
    r0: int = 0
    r1: int = 0
    r2: int = 0
    r3: int = 0
    r4: int = 0
    r5: int = 0
    r6: int = 0
    r7: int = 0
    r8: int = 0
    r9: int = 0

    RAX: int = 0
    RBX: int = 0
    RBP: int = 0

    RSP: int = 0
    RIP: int = 0
    RFLAGS: int = 0
    RVMM: int = 0
    RIDT: int = 0

class CPU:
    pass

class CPU:
    mem: Memory
    instruction_sets: dict[int, dict[int, Callable[[CPU], None]]] = {0: {}}
    instruction_set: int = 0
    mem: Memory
    regs: Registers
    def __init__(self, mem: Memory) -> None:
        self.mem = mem
        self.regs = Registers()
        self.running = False
    def op(self, op: int):
        def a(func: Callable[[CPU], None]):
            isn = int(op/256)
            o = op%256
            if self.instruction_sets.get(isn, None) == None:
                self.instruction_sets[isn] = {}
            self.instruction_sets[isn][o] = func
            #print(f"CPU: Registered opcode {hex(o)} at instruction set {isn}")
        return a
    def step(self):
        instr = self.mem[self.regs.RIP]
        if instr == 0xFF:
            self.instruction_set+=1
            if self.instruction_sets.get(self.instruction_set, None) == None:
                print(f"CPU: At RIP {hex(self.regs.RIP)}: Tried to switch to non-existent instruction set({self.instruction_set})")
                # We cannow trigger ints, so just stop
                self.running = False
                return
        else:
            handl = self.instruction_sets[self.instruction_set].get(instr, None)
            if handl == None:
                print(f"CPU: At RIP {hex(self.regs.RIP)}: Unknown instruction {hex(instr)}")
                # We cannow trigger ints, so just stop
                self.running = False
                return
            before = self.regs.RIP
            self.instruction_set = 0
            handl(self)
            if self.regs.RIP == before:
                self.regs.RIP+=1
    def run(self):
        self.running = True
        while self.running: self.step()