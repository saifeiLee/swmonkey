import threading
import argparse
from swmonkey.monitor.monitor import monkey_monitor
from swmonkey.monkey_test.monkey_test import MonkeyTest

DURATION = 10  # Duration in seconds
# DURATION = 60 * 60 * 10  # Duration in seconds
TIME_DIFF_SCALE = 0.1


# Start monitor in a sperated thread
# monitor_thread = threading.Thread(target=monkey_monitor, daemon=True)
# monitor_thread.start()


def swmonkey():
    parser = argparse.ArgumentParser(
        description='A tool for monkey test on Linux GUI')
    parser.add_argument('-d', '--duration', type=int,
                        default=DURATION, help='Duration in seconds')
    args = parser.parse_args()

    duration = args.duration
    print(f'Duration: {duration} seconds')
    monkey_test = MonkeyTest(duration=duration)
    monkey_test.run()


if __name__ == '__main__':
    swmonkey()
