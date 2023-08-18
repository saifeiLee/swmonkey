import time
import pstats
import cProfile
import pstats

from first_monkey import monkey_test
from watchdog import watchdog

DURATION = 10  # Duration in seconds
# DURATION = 60 * 60 * 10  # Duration in seconds
TIME_DIFF_SCALE = 0.1


start_time = time.time()

profile = cProfile.Profile()
profile.enable()

# monkey_test()
watchdog(monkey_test, DURATION + TIME_DIFF_SCALE * DURATION, DURATION)

profile.disable()
stats = pstats.Stats(profile)
stats.dump_stats(filename='./out/monkey_test.prof')
