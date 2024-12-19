# input & question can be found @ https://adventofcode.com/2024/day/19


from functools import lru_cache


def parse_input(directory):
    with open(directory, "r") as file:
        inp = file.read()

    towels, patterns = inp.split("\n\n")
    towels_list = towels.split(', ')
    pattern_list = patterns.split('\n')

    return towels_list, pattern_list


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def can_form_word(self, word):
        def dfs(index):
            if index == len(word):
                return True
            node = self.root
            for i in range(index, len(word)):
                if word[i] not in node.children:
                    return False
                node = node.children[word[i]]
                if node.is_end and dfs(i + 1):
                    return True
            return False

        return dfs(0)

    def count_combinations(self, word):
        @lru_cache(None)
        def dfs(index):
            if index == len(word):
                return 1
            node = self.root
            total_count = 0
            for i in range(index, len(word)):
                if word[i] not in node.children:
                    break
                node = node.children[word[i]]
                if node.is_end:
                    total_count += dfs(i + 1)
            return total_count

        return dfs(0)


def construct_towels(patterns, towels):
    trie = Trie()
    for pattern in patterns:
        trie.insert(pattern)

    count = 0
    all_combinations_count = 0
    for towel in towels:
        if trie.can_form_word(towel):
            count += 1
            all_combinations_count += trie.count_combinations(towel)

    return count, all_combinations_count


if __name__ == "__main__":
    input_dir = "inputfiles/day19.txt"
    patterns, towels = parse_input(input_dir)
    print(construct_towels(patterns, towels))
