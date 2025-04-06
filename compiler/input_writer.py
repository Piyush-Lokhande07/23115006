def write_values_to_asm(a, b):
    with open("comp_div.asm", "r") as file:
        lines = file.readlines()

    with open("comp_div.asm", "w") as file:
        for line in lines:
            if line.strip().startswith("a:"):
                file.write(f"    a: .long {a}\n")
            elif line.strip().startswith("b:"):
                file.write(f"    b: .long {b}\n")
            else:
                file.write(line)
