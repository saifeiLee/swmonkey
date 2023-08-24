import pyautogui
import random
import time
from ..util import KEY_NAMES
from swmonkey.data_structure.gui_action import GUIAction


SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


class MonkeyTest():
    def __init__(self, duration):
        self.duration = duration
        self.actions = []

    def run(self):
        self.monkey_test()

    def record_action(self, action_type, x, y, key, button, text):
        action = GUIAction(action_type, time.time(), x, y, key, button, text)
        self.actions.append(action)

    def monkey_test(self):
        '''
        每次循环，随机生成一个动作，然后执行
        '''
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

            # Random keypress
            if random.random() < 0.5:
                gui_action = GUIAction(
                    'key_press', time.time(), 0, 0, random.choice(KEY_NAMES), '', '')
            else:
                gui_action = GUIAction(
                    'write', time.time(), 0, 0, '', '', random.choice(KEY_NAMES))
            gui_action.execute()
