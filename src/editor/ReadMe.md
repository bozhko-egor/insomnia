# insomnia level editor

## Keyboard bindings:
1. `c` - toggle collision
2. `w` - build walls on this screen
3. `g` - toggle grid
4. `z` - undo last action
5. `i` - place cursor into nearest 32p*32p tile
6. `t` - cursor moving in 32p increments (toggle)
7. `r` - select last used block
8. `F5` - quick save your work
9. `q`



## How to import level into the game
You need to specify name of the level you created in `/src/level_config.py`:

```python
levels = ['your_level',
          'another_one',
          'and_another_one']
``` - Append level names to the end of the array

## To Do:
1. Moving platforms
2. Teleports
3. Mouse-controls
