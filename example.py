from ahk import AHK
from time import time, sleep

ahk = AHK()
ahk.mouse_move(2600, 600, speed=10, blocking=True)
ahk.click()

# ahk.key_press('pgdn')
# sleep(1)

# win = ahk.active_window
# win.kill()

ahk.key_down('Control')
ahk.key_press('w')


