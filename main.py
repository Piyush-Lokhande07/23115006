# main.py
import sys
import subprocess
from compiler.input_writer import write_values_to_asm
from compiler.compiler_utils import generate_tokens, generate_three_address_code, generate_symbol_table

def run_comp_div(a, b):
    tokens = generate_tokens(a, b)
    symbol_table = generate_symbol_table(a, b)
    tac = generate_three_address_code(a, b)

    write_values_to_asm(a, b)
    subprocess.run(["as", "comp_div.asm", "-o", "comp_div.o"], check=True)
    subprocess.run(["ld", "comp_div.o", "-o", "comp_div"], check=True)
    result = subprocess.check_output(["./comp_div"]).decode("utf-8").strip()

    print("Computed result:", result)

    print("\nTokens:")
    tokens_array = [f"{token['value']} ({token['type']})" for token in tokens]
    print(f"[{', '.join(tokens_array)}]")

    print("\nSymbol Table:")
    print(f"{'Name':<10} | {'Type':<10} | {'Value'}")
    print("-" * 30)
    for entry in symbol_table:
        print(f"{entry['name']:<10} | {entry['type']:<10} | {entry['value']}")

    print("\nThree-Address Code:")
    for line in tac:
        print(line)

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py COMP_DIV <a> <b>")
        sys.exit(1)
    
    command = sys.argv[1]
    a = int(sys.argv[2])
    b = int(sys.argv[3])

    if command == "COMP_DIV":
        run_comp_div(a, b)
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
