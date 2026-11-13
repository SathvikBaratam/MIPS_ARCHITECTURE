#  MIPS Processor Simulator – Project

This project implements a **simplified MIPS processor simulator in Python** along with supporting assembly and test programs.  
It demonstrates instruction execution, register operations, memory access, branching, and system calls.

This project was developed as part of a **Computer Architecture / Processor Design Mini Project**.

---

## 📁 Project Folder Structure
```text
.
├── processor.py        # Main MIPS processor simulator
├── mip.asm             # MIPS assembly source program
├── assemble_code1.txt  # Hexadecimal machine code input (generated from MARS)
├── twosum.py           # Two Sum algorithm (Python demo)
├── REPORT.pdf          # Project report document
└── README.md           # Project documentation
```

##  Project Overview

The simulator emulates a basic **single-cycle MIPS processor**.  
It loads hexadecimal machine instructions from `assemble_code1.txt`, executes them sequentially, and displays each stage of execution.

Key components implemented:

- Program Counter (PC)
- 32 General Purpose Registers
- Byte-addressable Memory
- Instruction Fetch–Decode–Execute Cycle
- Branching and Jumping
- System Calls

---

##  processor.py

This is the core of the project.

### Features

- 32 MIPS registers
- 1 MB memory
- R, I, and J instruction formats
- Arithmetic and logical operations
- Load/store instructions
- Branch and jump control
- Syscall handling

---

##  Supported Instructions

### R-Type
- ADD  
- ADDU  
- SLL  
- SYSCALL  

### I / J Type
- ADDI  
- ADDIU  
- ORI  
- LUI  
- LW  
- SW  
- BEQ  
- BNE  
- J  

---

##  Memory Layout

| Segment | Address |
|--------|---------|
| Text Segment | `0x00400000` |
| Data Segment | `0x10010000` |
| Total Memory | 1 MB |

---

## ▶️ How to Run

Make sure Python 3 is installed.

Open terminal inside the project directory:

```bash
python processor.py