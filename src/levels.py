from random import choice

def level_generate(width, height):

    level_patterns = [['P             UUU  P',
                       'P                  P',
                       'P        AAA       P',
                       'P                  P',
                       'P   UUU            P'],
                      ['P                  P',
                       'P   A          A   P',
                       'P        UU        P',
                       'P   A          A   P',
                       'P                  P'],
                      ['P                  P',
                       'P   U          U   P',
                       'P        AA        P',
                       'P   U          U   P',
                       'P                  P'],
                      ['P                  P',
                       'PA  U   A   U   A  P',
                       'P A  U   A   U   A P',
                       'P  A  U   A   U   AP',
                       'P                  P']]


    set_of_elements = ['A', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    level = ['PPPPPPPPPPPPPPPPPPPP',
             'P                  P',
             'P                  P',
             'P                  P',
             'P                  P']
    skip = 3

    for k in range(height // (5 + skip)):

        level += choice(level_patterns)

        for i in range(skip):
            string_val = 'P' + ''.join(choice(set_of_elements) for i in range(width - 2)) + 'P'
            level.append(string_val)

    return level

level1 = level_generate(20,1000)
