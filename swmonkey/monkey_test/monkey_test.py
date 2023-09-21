import pyautogui
import random
import time
import os
import json
import pywinctl as pwc
from swmonkey.util.util import KEY_NAMES
from swmonkey.data_structure.gui_action import GUIAction
from swmonkey.log.log import logger, get_out_dir
from swmonkey.monitor.monitor import SystemMonitor
from swmonkey.error import AppWindowNotFoundError
import subprocess

pyautogui.FAILSAFE = False

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


def launch_app(app_exe_path):
    '''
    app_path: app的执行文件路径
    '''
    subprocess.Popen([app_exe_path])


class ViableAreaManager():
    '''
    管理Monkey事件的有效区域
    '''

    def __init__(self):
        # Dict of viable areas: id -> (x, y, width, height)
        self.viable_areas = {}
        app_path = os.environ.get('APP_PATH')
        if app_path is not None:
            all_windows_before_launch = pwc.getAllWindows()
            # 启动app
            launch_app(app_path)
            time.sleep(3)  # 等待app启动完成
            all_windows_after_launch = pwc.getAllWindows()
            new_app_window = None
            for window in all_windows_after_launch:
                if window not in all_windows_before_launch:
                    new_app_window = window
                    break
            # 如果指定了APP_PATH，则默认有效区域为APP窗口区域
            # exit(0)
            if new_app_window is not None:
                logger.info(
                    f"new_app_window: {new_app_window} {new_app_window._win.id} {new_app_window.left} {new_app_window.top} {new_app_window.width} {new_app_window.height}")
                self.add(new_app_window._win.id, new_app_window.left, new_app_window.top,
                         new_app_window.width, new_app_window.height)
            else:
                logger.error("获取应用窗口失败")
                raise AppWindowNotFoundError

    def get(self):
        pass

    def add(self, id, x, y, width, height):
        self.viable_areas[id] = (x, y, width, height)

    def update(self, id, x, y, width, height):
        if id not in self.viable_areas:
            logger.error(f"更新的有效区域不存在, id:{id}")
            return
        self.viable_areas[id] = (x, y, width, height)

    def restore_area(self):
        for id, area in self.viable_areas.items():
            x, y, width, height = area
            target_window = pwc.getWindow(id)
            pwc.moveWindow(id, x, y, width, height)

    def is_in(self, x, y):
        # check if the are has changed
        '''
        判断事件点是否在有效区域内
        '''
        windows_at_xy = pwc.getWindowsAt(x, y)
        if len(windows_at_xy) == 0:
            return False
        else:
            for window in windows_at_xy:
                if window._win.id in self.viable_areas:
                    return True
            return False

    def is_area_size_changed(self):
        active_window = pwc.getActiveWindow()
        if active_window is None:
            return False
        if active_window._win.id not in self.viable_areas:
            return False
        x, y, width, height = self.viable_areas[active_window._win.id]
        if active_window.width != width or active_window.height != height or active_window.left != x or active_window.top != y:
            return True

    def restore_area_size(self):
        active_window = pwc.getActiveWindow()
        if active_window is None:
            return
        if active_window._win.id not in self.viable_areas:
            return
        x, y, width, height = self.viable_areas[active_window._win.id]
        active_window.moveTo(x, y)
        active_window.resizeTo(width, height)


class MonkeyTest():
    def __init__(self, duration):
        self.duration = duration
        self.out_path = get_out_dir()
        self.actions_json_file_path = os.path.join(
            self.out_path, 'actions.json')
        self.viable_area_manager = ViableAreaManager()

    def run(self):
        self.monkey_test()

    def record_action(self, action):
        with open(self.actions_json_file_path, 'a') as f:
            f.write(json.dumps(action.__dict__) + '\n')

    def perform_action(self):
        '''
        随机生成一个动作，然后执行
        '''
        # Random mouse movement
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        if os.environ.get('APP_PATH') is not None:
            # 如果事件点不在有效区域内，则不执行
            if not self.viable_area_manager.is_in(x, y):
                return

        if random.random() < 0.1:
            gui_action = GUIAction(
                'click', time.time(), x, y, '', 'left', '')
        else:
            gui_action = GUIAction(
                'double_click', time.time(), x, y, '', 'left', '')
        gui_action.execute()
        self.record_action(gui_action)

        # Random keypress
        if random.random() < 0.5:
            gui_action = GUIAction(
                'key_press', time.time(), 0, 0, random.choice(KEY_NAMES), '', '')
        else:
            gui_action = GUIAction(
                'write', time.time(), 0, 0, '', '', random.choice(KEY_NAMES))
        gui_action.execute()
        self.record_action(gui_action)
        interval = float(os.environ.get('INTERVAL'))
        time.sleep(interval)  # 为了避免频繁的操作，每次操作后sleep一段时间

    def monkey_test(self):
        '''
        每次循环，随机生成一个动作，然后执行
        '''
        swmonitor = SystemMonitor()
        logger.info("Monkey started!")
        starttime = os.environ.get('START_TIME')
        assert starttime is not None
        start_time = float(starttime or time.time())
        keep_alive = os.environ.get('KEEP_ALIVE')
        while time.time() - start_time < self.duration:
            if keep_alive is not None and swmonitor.should_release_resource():
                logger.warning(
                    "System usage is over 90%. Ready to free some resource")
                swmonitor.free_resources()
            else:
                self.perform_action()
                if self.viable_area_manager.is_area_size_changed():
                    logger.info("面积改变了，需要恢复")
                    self.viable_area_manager.restore_area_size()
        logger.info("Monkey finished!")


if __name__ == '__main__':
    pinco_app_path = '/opt/seewoPincoGroup/run_pincogroup.sh'
    launch_app(pinco_app_path)
