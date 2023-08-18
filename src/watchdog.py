import threading


def collect_system_logs():
    with open('/var/log/syslog', 'r') as f:
        logs = f.readlines()
    with open('out/syslog.txt', 'w') as f:
        LINES_COUNT = -200
        f.writelines(logs[LINES_COUNT:])


def watchdog(func, timeout, *args, **kwargs):
    test_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    test_thread.start()
    test_thread.join(timeout=timeout)

    if test_thread.is_alive():
        collect_system_logs()
        # raise TimeoutError(f'Test timed out after {timeout} seconds')
