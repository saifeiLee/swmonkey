import time
import pstats
import cProfile
import pstats

from first_monkey import monkey_test

start_time = time.time()

profile = cProfile.Profile()
profile.enable()

monkey_test()

profile.disable()
stats = pstats.Stats(profile)
stats.dump_stats(filename='./out/monkey_test.prof')