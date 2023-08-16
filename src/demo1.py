import pyautogui
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
print(screenWidth, screenHeight)
currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.
print(currentMouseX, currentMouseY)
pyautogui.moveTo(1100, 100) # Move the mouse to XY coordinates.

pyautogui.click()          # Click the mouse.
sunlogin_button_image_path = os.path.join(parent_dir, 'images/sunlogin_icon.png')
pyautogui.click(sunlogin_button_image_path) # Click the sunlogin icon.
pyautogui.doubleClick() # Click the sunlogin icon.
pyautogui.move(500, 500, duration=2, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
pyautogui.write('Hello world!', interval=0.25)  # Type with quarter-second pause in between each key.
pyautogui.press('esc')     # Simulate pressing the Escape key.
with pyautogui.hold('shift'):  # Press the Shift key down and hold it.
    pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left'])  # Press the left arrow key 6 times.

pyautogui.hotkey('ctrl', 'c') # Press the Ctrl-C hotkey combination.
pyautogui.alert('This is the message to display.') # Make an alert box appear and pause the program until OK is clicked.
pyautogui.press('enter') # Press the Enter key.