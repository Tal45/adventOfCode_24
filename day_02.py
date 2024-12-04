def is_safe(report):
    for i in range(1, len(report)):
        res = report[i] - report[i-1]
        if res <= 0 or 3 < res:
            return False
    return True


def is_safe2(report):
    for i in range(1, len(report)):
        res = report[i] - report[i-1]
        if res <= 0 or 3 < res:
            if is_safe(report[:i] + report[i + 1:]) or is_safe(report[:i - 1] + report[i:]):
                return True
            else:
                return False
    return True


if __name__ == '__main__':
    # replace with your input directory
    input_directory = "inputfiles/day2.txt"
    with open(input_directory, "r") as file:
        part_one, part_two = 0, 0
        for line in file:
            report = [int(x) for x in line.split()]

            if report[len(report)-1] < report[0]:
                report.reverse()

            if is_safe(report):
                part_one += 1
            elif is_safe2(report):
                part_two += 1
    print(part_one, part_one + part_two)


