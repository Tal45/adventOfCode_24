# question & input can be found @ https://adventofcode.com/2024/day/5
from collections import defaultdict


def parse_input(input_dir):
    rules, updates = [], []
    with open(input_dir, "r") as file:
        reading_rules = True
        for line in file:
            line = line.strip()
            if not line:
                reading_rules = False
                continue

            if reading_rules:
                rules.append(tuple(map(int, line.split("|"))))
            else:
                updates.append(list(map(int, line.split(","))))
    return rules, updates


def find_rules_for_update(update, rules):
    rule_list = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            rule_list.append(rule)
    return rule_list


def create_ranking(curr_rules):
    rank_map = defaultdict(int)
    changed = True

    while changed:
        changed = False
        for x, y in curr_rules:
            if rank_map[x] >= rank_map[y]:
                rank_map[y] = rank_map[x] + 1
                changed = True

    return rank_map


def sum_middle_sorted(rules, updates):
    total_sum_p1 = 0
    total_sum_p2 = 0
    for update in updates:
        current_rules = find_rules_for_update(update, rules)
        rank_map = create_ranking(current_rules)
        sorted_update = sorted(update, key=lambda x: rank_map.get(x, 0))
        if update == sorted_update:
            total_sum_p1 += update[len(update) // 2]
        else:
            total_sum_p2 += sorted_update[len(sorted_update) // 2]

    return total_sum_p1, total_sum_p2


if __name__ == '__main__':
    input_directory = "inputfiles/day5.txt"
    rules, updates = parse_input(input_directory)
    print(sum_middle_sorted(rules, updates))
