
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
