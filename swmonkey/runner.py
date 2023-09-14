import subprocess
import os
import argparse
import time
from .main import run_monkey
import multiprocessing
from swmonkey.log.log import logger


def run_command(sudo=False, cmd=None, passwd=None):
    if sudo:
        if passwd is None:
            raise Exception('passwd is None')
        cmd = f'sudo -S {cmd}'
    subprocess.run(f'echo {passwd} | {cmd}', shell=True)


def run_monkey_test():
    duration = int(os.getenv('DURATION'))
    # check child process status every 5 seconds
    starttime = float(os.environ.get('START_TIME'))
    while time.time() - starttime < duration:
        logger.info(f'[Main process] start swmonkey {starttime}')
        # 使用multiprocessing的原因：
        #  1. subprocess.open在一些情况下会找不到swmonkey command/file，原因未知
        #  2. multiprocess.Process 子进程会继承父进程的环境变量，不需要再传入
        p = multiprocessing.Process(
            target=run_monkey, args=(duration,), daemon=True)
        p.daemon = True
        p.start()
        p.join()
        # 设定的时间没有执行完
        # Note:
        # 在openlylin压测过程中发现桌面环境会崩溃重置，这时如果配置了autostart smwonkey,
        # 相当于重新执行了一遍swmonkey, start_time将重置，~/.swmonkey会新建日志文件夹
        if time.time() - starttime < duration:
            logger.info(
                "[Main process]Monkey test stopped unexpectedly, restarting...")
        time.sleep(3)

        restart_x11 = os.environ.get('RESTART_X11')
        password = os.environ.get('PASSWORD')
        if restart_x11 is not None and password is not None:
            logger.info("[Main process]Restarting x11...")
            # WARNING
            # 执行这个命令会导致桌面环境重启，所有的应用都会关闭,包括swmonkey_runner
            run_command(sudo=True, cmd='systemctl restart lightdm',
                        passwd=password)
    logger.info("[Main process]Monkey test finished!")


def main():
    parser = argparse.ArgumentParser(
        description='A tool for monkey test on Linux GUI')

    parser.add_argument('-d', '--duration', type=int,
                        default=0, help='Duration in seconds')
    parser.add_argument('--restart-x11', dest='restartx11', action='store_true',
                        default=None, help='Restart x11 when x11 crashed.')
    parser.add_argument('--password', dest='password', type=str,
                        default=None, help='Password for sudo.')
    args = parser.parse_args()

    duration = args.duration
    assert duration > 0, 'Duration must be greater than 0'
    if duration is not None:
        os.environ['DURATION'] = str(duration)

    restartx11 = args.restartx11
    if restartx11 is not None:
        os.environ['RESTART_X11'] = str(restartx11)

    password = args.password
    if password is not None:
        os.environ['PASSWORD'] = password

    # 控制进程不需要传入starttime，默认为当前时间
    starttime = time.time()
    os.environ['START_TIME'] = str(starttime)

    run_monkey_test()


if __name__ == '__main__':
    main()
