import threading
from swmonkey.monitor.monitor import monkey_monitor

DURATION = 10  # Duration in seconds
# DURATION = 60 * 60 * 10  # Duration in seconds
TIME_DIFF_SCALE = 0.1


# Start monitor in a sperated thread
monitor_thread = threading.Thread(target=monkey_monitor, daemon=True)
monitor_thread.start()
