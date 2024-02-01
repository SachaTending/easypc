from dataclasses import dataclass
from typing import Callable, Union
bytearray()

@dataclass
class mem_entry:
    get_data: Callable[[int], int]
    set_data: Callable[[int, int], None]
    start: int
    end: int

class Memory:
    mem: dict
    mmd: list[mem_entry] # memory mapped devices
    def __init__(self, size: int):
        self.mem = {}
        self.size = size
        self.mmd = []
    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, slice):
            r = []
            ind = key.start
            while ind < key.stop or ind != key.stop:
                r.append(self[ind])
                ind += key.step
            return r
        if key > self.size:
            print(f"Memory: Out Of Bounds reading: addr {hex(key)}")
            return 0
        for i in self.mmd:
            if key == i.start or key == i.end or i.start < key < i.end:
                return i.get_data(key-i.start)
        return self.mem.get(key, 0)
    def __setitem__(self, key: int, val: Union[list[int], int, bytes, bytearray]):
        v = val
        if type(val) in [bytes, bytearray]:
            v = []
            for i in val:
                v.append(i)
        if isinstance(v, int):
            v = [v]
        cont = False
        for i in range(len(v)):
            if i+key > self.size:
                continue
            for dev in self.mmd:
                if i+key == dev.start or i+key == dev.end or dev.start < i+key < dev.end:
                    dev.set_data((i+key)-dev.start, v[i])
                    cont = True
                    break
            if cont:
                cont = False
                continue
            if v[i] == 0:
                del self.mem[i+key]
            else: self.mem[i+key] = v[i]
    def map_dev(self, start: int, end: int, get_data: Callable[[int], int], set_data: Callable[[int, int], None]):
        dev = mem_entry(get_data, set_data, start, end)
        self.mmd.append(dev)
    def map_dev2(self, mmt: mem_entry):
        self.mmd.append(mmt)
    def __len__(self) -> int:
        return self.size