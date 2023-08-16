import pyautogui
import random
import time
import pstats
import cProfile
import pstats

DURATION = 10  # Duration in seconds
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

start_time = time.time()
def monke_test():
    while time.time() - start_time < DURATION:
        # Random mouse movement
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        pyautogui.moveTo(x, y, duration=0.1)

        # Random click
        if random.random() < 0.1:
            pyautogui.click()

        # Random keypress
        if random.random() < 0.05:
            pyautogui.press(random.choice(['a', 'b', 'c', 'd', 'e']))

profile = cProfile.Profile()
profile.enable()

monke_test()

profile.disable()
stats = pstats.Stats(profile)
stats.dump_stats(filename='monke_test.prof')