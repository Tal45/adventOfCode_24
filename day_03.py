import re


def parse_input(filename):
    total_sum = 0
    pattern = re.compile(r"mul\((\d+),(\d+)\)")

    with open(filename, "r") as file:
        for line in file:
            matches = pattern.findall(line)
            for x, y in matches:
                total_sum += int(x) * int(y)

    return total_sum


def parse_with_enablers(filename):
    total_sum = 0
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
    do_pattern = re.compile(r"do\(\)")
    dont_pattern = re.compile(r"don't\(\)")

    with open(filename, "r") as file:
        input_text = file.read()
    all_matches = []
    all_matches += [(match.start(), "do") for match in do_pattern.finditer(input_text)]
    all_matches += [(match.start(), "dont") for match in dont_pattern.finditer(input_text)]
    all_matches += [(match.start(), "mul", match.groups()) for match in mul_pattern.finditer(input_text)]
    all_matches.sort(key=lambda b: b[0])

    mul_enabled = True
    for match in all_matches:
        if match[1] == "mul" and mul_enabled:
            x, y = map(int, match[2])
            total_sum += x * y
        elif match[1] == "do":
            mul_enabled = True
        else:
            mul_enabled = False

    return total_sum


if __name__ == "__main__":
    print(parse_input("inputfiles/day3.txt"))
    print(parse_with_enablers("inputfiles/day3.txt"))
