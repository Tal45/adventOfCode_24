def parseInput(file):
    list1, list2 = [], []
    with open(file, "r") as inputfile:
        for line in inputfile:
            tmp = line.split()
            list1.append(int(tmp[0]))
            list2.append(int(tmp[1]))
    return list1, list2

def countDiff(list1, list2):
    return sum(abs(x-y) for x, y in zip(list1, list2))

def calcOccr(list1, list2):
    return sum(x * list2.count(x) for x in list1)

if __name__ == "__main__":
    list1, list2 = parseInput("inputfiles/day1.txt")
    list1.sort()
    list2.sort()

    # part1
    print(countDiff(list1, list2))
    # part2
    print(calcOccr(list1, list2))