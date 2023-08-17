import pyautogui
import random
import time
import pstats
import cProfile
import pstats
from util import KEY_NAMES

DURATION = 10  # Duration in seconds
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

start_time = time.time()
def monkey_test():
    while time.time() - start_time < DURATION:
        # Random mouse movement
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        pyautogui.moveTo(x, y, duration=0.1)

        # Random click
        if random.random() < 0.1:
            pyautogui.click()
        else:
            pyautogui.doubleClick()

        # Random keypress
        if random.random() < 0.5:
            pyautogui.press(random.choice(KEY_NAMES))

profile = cProfile.Profile()
profile.enable()

monkey_test()

profile.disable()
stats = pstats.Stats(profile)
stats.dump_stats(filename='monkey_test.prof')