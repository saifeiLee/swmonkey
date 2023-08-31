import pyautogui
import random
import time
import os

from swmonkey.util.util import KEY_NAMES
from swmonkey.data_structure.gui_action import GUIAction
from swmonkey.log.log import logger, get_out_dir
from swmonkey.monitor.monitor import monitor_system

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

class MonkeyTest():
    def __init__(self, duration):
        self.duration = duration
        self.actions = []

    def run(self):
        self.monkey_test()

    def record_action(self, action):
        self.actions.append(action.__dict__)

    def monkey_test(self):
        '''
        每次循环，随机生成一个动作，然后执行
        '''
        monitor_system()
        logger.info("Monkey started!")
        start_time = time.time()
        while time.time() - start_time < self.duration:
            # Random mouse movement
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)

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
        out_path = get_out_dir()
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        actions_json_file_path = os.path.join(out_path, 'actions.json')
        with open(actions_json_file_path, 'w') as f:
            f.write(str(self.actions))
        logger.info("Monkey finished!")
