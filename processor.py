TEXT_BASE = 0x00400000
DATA_BASE = 0x10010000
MEMORY_SIZE = 1024 * 1024

memory = bytearray(MEMORY_SIZE)

OPCODES = {
    0x00: "R",
    0x08: "ADDI",
    0x09: "ADDIU",
    0x0D: "ORI",
    0x0F: "LUI",
    0x23: "LW",
    0x2B: "SW",
    0x04: "BEQ",
    0x05: "BNE",
    0x02: "J"
}

FUNCTS = {
    0x20: "ADD",
    0x21: "ADDU",
    0x00: "SLL",
    0x0C: "SYSCALL"
}

def load_machine_code(filename):
    ins = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                ins.append(int(line, 16))
    return ins

instructions = load_machine_code("assembly_code1.txt")

registers = [0] * 32
PC = TEXT_BASE
cycle = 0

INPUT_VALUES = [6, 3, 5, 1, 8, 4, 6, 9]
input_index = 0

def to_signed(val):
    val &= 0xFFFFFFFF
    return val - 0x100000000 if val & 0x80000000 else val

def address_to_index(addr):
    if DATA_BASE <= addr < DATA_BASE + MEMORY_SIZE:
        return addr - DATA_BASE
    return None

def read_word(addr):
    idx = address_to_index(addr)
    if idx is None:
        return 0
    val = (
        (memory[idx] << 24) |
        (memory[idx + 1] << 16) |
        (memory[idx + 2] << 8) |
        memory[idx + 3]
    )
    return to_signed(val)

def write_word(addr, value):
    idx = address_to_index(addr)
    if idx is None:
        return
    value &= 0xFFFFFFFF
    memory[idx]     = (value >> 24) & 0xFF
    memory[idx + 1] = (value >> 16) & 0xFF
    memory[idx + 2] = (value >> 8) & 0xFF
    memory[idx + 3] = value & 0xFF

print("Starting execution...\n")

while True:

    index = (PC - TEXT_BASE) // 4
    if index < 0 or index >= len(instructions):
        break

    cycle += 1
    print(f"=== Cycle {cycle} ===")

    instr = instructions[index]
    nextPC = PC + 4

    print(f"[IF] Fetched 0x{instr:08x} at PC {hex(PC)}")

    opcode = (instr >> 26) & 0x3F
    rs     = (instr >> 21) & 0x1F
    rt     = (instr >> 16) & 0x1F
    rd     = (instr >> 11) & 0x1F
    shamt  = (instr >> 6) & 0x1F
    funct  = instr & 0x3F
    imm    = instr & 0xFFFF
    addr   = instr & 0x3FFFFFF

    if imm & 0x8000:
        imm -= 0x10000

    read_data1 = registers[rs]
    read_data2 = registers[rt]

    RegWrite = False
    write_reg = None
    write_data = None
    action = ""

    if OPCODES.get(opcode) == "R":

        op = FUNCTS.get(funct)

        if op == "SYSCALL":
            v0 = registers[2]
            if v0 == 5:
                if input_index < len(INPUT_VALUES):
                    registers[2] = INPUT_VALUES[input_index]
                    input_index += 1
                else:
                    break
            elif v0 == 1:
                print(f"[OUTPUT] {registers[4]}")
            elif v0 == 10:
                break
            PC = nextPC
            print("-"*50)
            continue

        elif op == "ADD":
            action = "ADD"
            RegWrite = True
            write_reg = rd
            write_data = to_signed(read_data1) + to_signed(read_data2)

        elif op == "ADDU":
            action = "ADDU"
            RegWrite = True
            write_reg = rd
            write_data = (read_data1 + read_data2) & 0xFFFFFFFF

        elif op == "SLL":
            action = "SLL"
            RegWrite = True
            write_reg = rd
            write_data = read_data2 << shamt

    else:

        op = OPCODES.get(opcode)

        if op in ("ADDI", "ADDIU"):
            action = op
            RegWrite = True
            write_reg = rt
            write_data = to_signed(read_data1) + imm

        elif op == "ORI":
            action = "ORI"
            RegWrite = True
            write_reg = rt
            write_data = read_data1 | (imm & 0xFFFF)

        elif op == "LUI":
            action = "LUI"
            RegWrite = True
            write_reg = rt
            write_data = imm << 16

        elif op == "LW":
            action = "LW"
            RegWrite = True
            write_reg = rt
            write_data = read_word(to_signed(read_data1) + imm)

        elif op == "SW":
            action = "SW"
            write_word(to_signed(read_data1) + imm, read_data2)

        elif op == "BEQ":
            action = "BEQ"
            if read_data1 == read_data2:
                nextPC = nextPC + (imm << 2)

        elif op == "BNE":
            action = "BNE"
            if read_data1 != read_data2:
                nextPC = nextPC + (imm << 2)

        elif op == "J":
            action = "J"
            nextPC = (PC & 0xF0000000) | (addr << 2)

    print(f"[ID] {action}")

    if RegWrite and write_reg != 0:
        registers[write_reg] = write_data & 0xFFFFFFFF
        print(f"[WB] Wrote {write_data & 0xFFFFFFFF} to ${write_reg}")

    registers[0] = 0
    PC = nextPC
    print("-"*50)

print("\nExecution Finished")
print("Register $t9 (count) =", registers[25])