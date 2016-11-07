level_patterns = [["P                  P",
                   "P                  P",
                   "P                  P",
                   "P                  P",
                   "P   PPP            P"],
                  ["P                  P",
                   "P                  P",
                   "P                  P",
                   "PPPPPPPP           P",
                   "P                  P"]]


def Level_generate(width, height):
    from random import choice

    set = ['A', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    level = []
    skip = 3

    for k in range(height / 5 + skip):

        level.append(choice(level_patterns))

        for i in skip:
            string_val = "P" + "".join(choice(set) for i in range(width - 2)) + "P"
            level.append(string_val)

    return level
