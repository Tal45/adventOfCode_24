def isSafe(report):
    for i in range(1, len(report)):
        res = report[i] - report[i-1]
        if res <= 0 or 3 < res:
            return False
    return True

def isSafe2(report):
    for i in range(1, len(report)):
        res = report[i] - report[i-1]
        if res <= 0 or 3 < res:
            if isSafe(report[:i] + report[i+1:]) or isSafe(report[:i-1] + report[i:]):
                return True
            else:
                return False
    return True

if __name__ == '__main__':

    file = open("dayTwoInput.txt", "r")
    pOne, pTwo = 0, 0
    for line in file:
        report = [int(x) for x in line.split()]

        if report[len(report)-1] < report[0]:
            report.reverse()

        if isSafe(report):
            pOne += 1
        elif isSafe2(report):
            pTwo += 1

    print(pOne, pOne+pTwo)


