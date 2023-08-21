import psutil
from log import logger


def monitor_system():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    net_info = psutil.net_io_counters()
    logger.info(
        f'CPU:  {cpu_usage}%; Memory: {mem_usage}%; Disk: {disk_usage}%; Net: {net_info.bytes_sent} bytes sent, {net_info.bytes_recv} bytes received')

if __name__ == '__main__':
    monitor_system()
    # Output: 'CPU:  0.0%; Memory: 0.0%; Disk: 0.0%; Net: 0 bytes sent, 0 bytes received