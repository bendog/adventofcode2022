from dataclasses import dataclass


@dataclass
class Tree:
    x: int
    y: int
    height: int
    left: list[int]
    right: list[int]
    up: list[int]
    down: list[int]

    @property
    def is_visible(self):
        if self.left == [] or self.right == [] or self.up == [] or self.down == []:
            return True
        return (
            max(self.left) < self.height
            or max(self.right) < self.height
            or max(self.up) < self.height
            or max(self.down) < self.height
        )

    ### ADDED FOR PART 2 ###
    def get_score(self, tree_heights):
        """this is messy because i assumed elves wouldn't be able to see through trees"""
        if len(tree_heights) <= 1:
            return len(tree_heights)
        score = 0
        # highest_tree = trees[0]
        for tree_height in tree_heights:
            # don't actually skip these trees because these elves have magic eyes
            # if tree_height < highest_tree:
            #     # skip trees that are obscured
            #     continue
            if tree_height >= self.height:
                # stop when you find a tall tree
                score += 1
                break
            else:
                # if this tree is visible count it
                # highest_tree = tree_height
                score += 1
        return score

    @property
    def view_score(self):
        """part 2"""
        score_left = self.get_score(self.left)
        score_right = self.get_score(self.right)
        score_up = self.get_score(self.up)
        score_down = self.get_score(self.down)
        return score_left * score_right * score_up * score_down


# import input
with open("day8-input.txt") as f:
    rows = [[int(x) for x in list(row.replace("\n", ""))] for row in f]
    cols = [[] for _ in rows[0]]
    for row in rows:
        for idx, val in enumerate(row):
            cols[idx].append(val)

# create trees
trees: list[Tree] = []
for idy, row in enumerate(rows):
    for idx, value in enumerate(row):
        left = row[:idx]
        left.reverse()
        right = row[idx + 1 :]
        up = cols[idx][:idy]
        up.reverse()
        down = cols[idx][idy + 1 :]
        trees.append(Tree(idx, idy, value, left, right, up, down))

print("visible trees")
print(len([tree for tree in trees if tree.is_visible]))

### part 2 ###
print("max score")
scores = sorted([tree.view_score for tree in trees])
# correct_tree = [tree for tree in trees if tree.x == 56 and tree.y == 22]
print(max(scores))
