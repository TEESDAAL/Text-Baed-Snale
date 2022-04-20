import pyautogui
import os
import threading
from time import sleep
from random import randint


def press_enter():
    while True:
        sleep(0.01)
        pyautogui.press("enter")


NUM_ROWS = NUM_COLS = 20

VALID_KEYS = {"w", "a", "s", "d"}
direction = "d"
apple_on_board = False
apples_eaten = 0
NUM_APPLES = 5

snake_parts = [(0, 0)]
directions = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}
direction_inv = {"w": "s", "s": "w", "a": "d", "d": "a"}
apple_coords = set()

emoji_displayed = input("Does this character '🍎' display properly? (y/n)") in (
    "yes",
    "y",
)
# Note these are full width characters, not the normal ones
BACKGROUND = "⬛" if emoji_displayed else "- "
SNAKE_COLOR = "🟩" if emoji_displayed else "@ "
FOOD = "🍎" if emoji_displayed else "a "

print(
    f"The background colour is represented by the '{BACKGROUND}' character, "
    f"the snake is represented by the '{SNAKE_COLOR}' character, "
    f"and the food is represented by the '{FOOD}' character"
)

input("Press enter to start the game")


def add_apples(NUM_APPLES):
    apples_added = 0
    while len(apple_coords) < NUM_APPLES:
        test_coord = (randint(0, NUM_ROWS - 1), randint(0, NUM_COLS - 1))
        if test_coord not in apple_coords and test_coord not in snake_parts:
            apple_coords.add(test_coord)
            apples_added += 1


t = threading.Thread(target=press_enter)
t.start()

while (length := len(snake_parts)) == len(set(snake_parts)):
    add_apples(NUM_APPLES)

    y, x = snake_parts[0]
    sleep(0.05)
    user_input = input().lower()

    if user_input in VALID_KEYS and user_input != direction_inv[direction]:
        direction = user_input

    del snake_parts[length - 1]
    Δy, Δx = directions[direction]

    snake_parts.insert(0, ((y + Δy) % NUM_ROWS, (x + Δx) % NUM_COLS))

    y, x = snake_parts[0]

    if (y, x) in apple_coords:
        apple_coords.remove((y, x))
        apple_on_board = snake_parts.append(
            ((y + Δy) % NUM_ROWS, (x + Δx) % NUM_COLS)
        )

    str_board = []
    for row_num in range(NUM_ROWS):
        str_board.extend(
            [
                *[
                    SNAKE_COLOR
                    if (row_num, col_num) in snake_parts
                    else FOOD
                    if (row_num, col_num) in apple_coords
                    else BACKGROUND
                    for col_num in range(NUM_COLS)
                ],
                "\n",
            ]
        )
    os.system("cls" if os.name == "nt" else "clear")

    print("".join(str_board))
