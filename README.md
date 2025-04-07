
---

## 🛠️ Custom Instruction for Equation: `z = (a - b) / (a + b)`

### 🎯 Objective  
The goal of this project is to design a custom instruction for the arithmetic equation:

```
z = (a - b) / (a + b)
```

within a mini compiler setup. The compiler:

- 🧠 Parses and understands the input expression
- ⚙️ Generates custom assembly instructions
- 🧮 Simulates register-level computation
- 📤 Displays:
  - ✅ Computed Result
  - 🧾 Lexical Tokens
  - 📋 Symbol Table
  - 🧮 Three-Address Code
  - 🌳 Parse Tree

This demonstrates how a specific arithmetic expression can be compiled and executed from high-level input to low-level execution.

---

### 🔄 Flow of Execution (from Input to Output)

When you run:

```bash
python3 main.py COMPUTE_Z 6 2
```

#### 1️⃣ User Input  
**File:** `main.py`  
Takes user input from the terminal (e.g., `a = 6`, `b = 2`)  
Passes values to other modules for compilation and code generation.

#### 2️⃣ Assembly Code Generation  
**File:** `compiler/input_writer.py`  
Creates `comp_div.asm`, which contains custom assembly for `z = (a - b) / (a + b)`  
Inserts values of `a` and `b` into the `.data` section.

#### 3️⃣ Assembling the Code  
**Tool:** NASM

```bash
nasm -f elf64 comp_div.asm -o comp_div.o
```

Compiles the assembly into an object file.

#### 4️⃣ Linking to Executable  
**Tool:** ld

```bash
ld -o comp_div comp_div.o
```

Links the object file into a binary executable.

#### 5️⃣ Execution of Custom Instruction  
**Command:**

```bash
./comp_div
```

Runs the binary that calculates `z = (a - b) / (a + b)` using registers.  
Displays result in the terminal.

#### 6️⃣ Compiler Backend Output  
**File:** `compiler/compiler_utils.py`

Python prints:
- 🧾 Lexical Tokens  
- 📋 Symbol Table  
- 🧮 Three-Address Code  

---

### 🔧 Prerequisites

Ensure these tools are installed:

#### ✅ 1. Python 3

```bash
python3 --version
pip install -r requirements.txt
```

#### ✅ 2. NASM

```bash
sudo apt update
sudo apt install nasm
```

#### ✅ 3. LD (Linker)

```bash
ld --version
sudo apt install binutils
```

#### ✅ 4. objdump

```bash
objdump --version
sudo apt install binutils
```

---

### 📁 Project Structure

```
mini_compiler/
├── comp_div.asm         # Custom assembly for (a-b)/(a+b)
├── comp_div.o           # Object file
├── comp_div             # Executable
├── main.py              # Python entry point
└── compiler/
    ├── input_writer.py   # Generates comp_div.asm
    ├── compiler_utils.py # Outputs tokens, symbol table, 3AC
```

---

### 🛠️ Register Pseudo Execution

```asm
mov    a, %eax        ; R1 = a
sub    b, %eax        ; R1 = a - b
mov    %eax, %r8d     ; R2 = numerator = a - b

mov    a, %eax        ; R1 = a
add    b, %eax        ; R1 = a + b
cdq                   ; Sign-extend for division
idiv   %r8d           ; eax = (a - b) / (a + b)
mov    %eax, z        ; store result
```

---

### 🌳 Parse Tree for `z = (a - b) / (a + b)`

```
       (=)
     /     \
   (z)     (/)
          /   \
       (-)     (+)
      /  \    /  \
    (a)  (b) (a)  (b)
```

---

### 🌟 Benefits of Custom Instruction

- ⚡ **Efficient Execution** – Clean and minimal instructions
- 🧠 **Educational** – Learn parsing, TAC, and register-level assembly
- 💡 **Real-World Insight** – Understand how compilers work under the hood

---

### 🧪 How to Run

```bash
nasm -f elf64 comp_div.asm -o comp_div.o
ld -o comp_div comp_div.o
python3 main.py COMPUTE_Z 6 2
objdump -d comp_div
```

---

### ✅ Conclusion

You've now created a custom mini compiler pipeline that:

- 🌳 Builds a parse tree
- 🧮 Generates Three-Address Code
- 🛠️ Produces and runs custom assembly
- 🔍 Offers insight into the final machine code with objdump

A perfect sandbox to learn how languages talk to hardware! 🔧💡

Let me know if you'd like a visual flowchart or want to extend this to handle other expressions!
If you want to add a custom instruction to a compiler, you typically need to modify the LLVM backend or GCC backend, depending on the compiler you’re working with. Below, I’ll break down the specific steps for LLVM (since it's more modular and widely used for custom instruction modifications).


---

Modifying the LLVM Backend for a Custom Instruction

Step 1: Set Up LLVM for Development

1. Clone the LLVM repository:

git clone https://github.com/llvm/llvm-project.git
cd llvm-project


2. Build LLVM:

mkdir build && cd build
cmake -G "Ninja" ../llvm -DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_BUILD_TYPE=Debug
ninja




---

Step 2: Define the Custom Instruction in LLVM Backend

1. Locate the Target Backend in LLVM

LLVM has a directory for each target architecture inside:

llvm/lib/Target/<YourTarget>/

For example, if you are modifying the X86 backend, go to:

llvm/lib/Target/X86/

If you’re working on a new processor, you may need to define a new backend.


---

2. Modify the Target’s Instruction Definitions (.td File)

Open XXXInstrFormats.td (for X86, it’s X86InstrFormats.td).

Add a new instruction for the equation .


Example for a MULADD instruction:

def MULADD : Instruction {
  let Opcode = 0xAB; // Assign an unused opcode
  let Format = (outs GR32:$dst), (ins GR32:$src1, GR32:$src2, GR32:$src3, GR32:$src4);
  let AsmString = "muladd $dst, $src1, $src2, $src3, $src4";
  let Constraints = "$dst = $src1";
}

This defines:

MULADD dst, src1, src2, src3, src4

Computes: dst = (src1 * src2) + (src3 * src4)



---

3. Modify the Instruction Selection (ISel) File

In:

llvm/lib/Target/<YourTarget>/<YourTarget>ISelDAGToDAG.cpp

Find the instruction selection logic and add pattern matching:

if (Node->getOpcode() == ISD::ADD) {
    SDValue Mul1 = Node->getOperand(0);
    SDValue Mul2 = Node->getOperand(1);

    if (Mul1.getOpcode() == ISD::MUL && Mul2.getOpcode() == ISD::MUL) {
        ReplaceNode(Node, CurDAG->getMachineNode(TargetOpcode::MULADD,
                  DL, VT, Mul1.getOperand(0), Mul1.getOperand(1),
                  Mul2.getOperand(0), Mul2.getOperand(1)));
        return;
    }
}

This matches (A * B) + (C * D) and replaces it with MULADD.


---

4. Define the Encoding for the Instruction

Modify:

llvm/lib/Target/<YourTarget>/<YourTarget>MCInstrDesc.td

Add:

let Opcode = 0xAB, Size = 4, Encoding = [0xAB, $dst, $src1, $src2, $src3, $src4];


---

5. Modify the Assembler & Disassembler

Assembler: Define parsing logic in:

llvm/lib/Target/<YourTarget>/<YourTarget>AsmParser.cpp

Example:

if (Mnemonic == "muladd") {
    Operands.push_back(Inst.getOperand(0));
    return Match_Mnemonic_Success;
}

Disassembler: Modify:

llvm/lib/Target/<YourTarget>/<YourTarget>Disassembler.cpp

Example:

case 0xAB:
    Inst.setOpcode(TargetOpcode::MULADD);
    break;



---

Step 3: Rebuild LLVM & Test the Instruction

1. Recompile LLVM:

ninja


2. Test using llc (LLVM’s assembly generator):

llc -march=<YourTarget> test.ll -o test.s

Where test.ll contains:

define i32 @test(i32 %a, i32 %b, i32 %c, i32 %d) {
    %1 = mul i32 %a, %b
    %2 = mul i32 %c, %d
    %3 = add i32 %1, %2
    ret i32 %3
}



Verify that the output assembly contains muladd instead of separate mul and add.



---

Step 4: Benchmark & Optimize

Run the compiled binary and check performance improvements.

Use llvm-mca to analyze instruction execution latency.



---

Conclusion

By following these steps, you integrate a custom instruction into LLVM, allowing your compiler to optimize specific equations. Let me know if you need help with any step! 🚀
