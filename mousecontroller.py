# IMPORTS #
import ctypes
from typing import Union
import win32api
import win32con
import time
from random import choice
from keyboard import is_pressed

# VARS #
failsafe_enabled: bool = True
failsafe_key: str = 'esc'

recorded_moves: dict = {}

log: str = "mousecontroller debug log\n\n"

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# MOUSECONTROLS #
class FailSafe:
    @staticmethod
    def enable():
        global failsafe_enabled, log

        failsafe_enabled = True
        log += "FAILSAFE: enabled failsafe feature\n"

    @staticmethod
    def disable():
        global failsafe_enabled, log

        failsafe_enabled = False
        log += "FAILSAFE: disabled failsafe feature\n"

    @staticmethod
    def is_enabled() -> bool:
        return failsafe_enabled

    @staticmethod
    def set_key(key: str):
        global failsafe_key, log

        is_pressed(key)
        failsafe_key = key

        log += f"FAILSAFE: set failsafe activation key to {key}\n"


def get_pos() -> tuple[int, int]:
    return win32api.GetCursorPos()


def travel_to(target_pos: tuple[int, int], speed: Union[int, float], apply_jitter: bool = False,
              jitter_accuracy_px: int = 10):
    global log

    start_pos = get_pos()

    j_x = 0
    j_y = 0

    t_x, t_y = target_pos
    c_x, c_y = get_pos()

    x_dist = t_x - c_x
    y_dist = t_y - c_y

    x_vel = (x_dist / (1 / speed * 12000))
    y_vel = (y_dist / (1 / speed * 12000))

    tick = 0
    while (round(c_x), round(c_y)) != target_pos:
        tick += 1
        if is_pressed(failsafe_key) and failsafe_enabled:
            log += "FAILSAFE: failsafe trigger key pressed\n"
            print(FAIL + BOLD + f"Terminated Process As Failsafe Key '{failsafe_key}' Was Pressed." + END)
            log += "TERMINATED: process terminated due to failsafe activation.\n"
            quit()

        c_x += x_vel
        c_y += y_vel

        if apply_jitter and tick % 100 == 1:
            if choice([1, 0]):
                j_x += choice([1, -1])
            else:
                j_y += choice([1, -1])

            if j_x > jitter_accuracy_px:
                j_x -= 2
            if j_x < jitter_accuracy_px * -1:
                j_x += 2
            if j_y > jitter_accuracy_px:
                j_y -= 2
            if j_y < jitter_accuracy_px * -1:
                j_y += 2

        win32api.SetCursorPos((round(c_x) + j_x, round(c_y) + j_y))

    log += f"CURSOR: moved cursor from position {start_pos} to position {target_pos}\n"


def set_pos(target_pos: tuple[int, int]):
    global log

    win32api.SetCursorPos(target_pos)

    log += f"CURSOR: set position of cursor to {target_pos}\n"


def click():
    global log

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    log += f"CURSOR: left-clicked at position {get_pos()}"


def double_click():
    global log

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    log += f"CURSOR: double-clicked at position {get_pos()}"


def triple_click():
    global log

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    log += f"CURSOR: triple-clicked at position {get_pos()}"


def right_click():
    global log

    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

    log += f"CURSOR: right-clicked at position {get_pos()}"


def middle_click():
    global log

    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0)

    log += f"CURSOR: middle-clicked at position {get_pos()}"


def record_movements(recording_name: str, duration_seconds: Union[int, float]):
    global log

    start_t = time.time()

    recording = []
    log += f"RECORDING: started recording {recording_name} of duration {duration_seconds}\n"
    while time.time() - start_t < duration_seconds:
        if is_pressed(failsafe_key) and failsafe_enabled:
            log += "FAILSAFE: failsafe trigger key pressed\n"
            print(FAIL + BOLD + f"Terminated Process As Failsafe Key '{failsafe_key}' Was Pressed." + END)
            log += "TERMINATED: process terminated due to failsafe activation.\n"
            quit()
        recording.append(get_pos())

    recorded_moves[recording_name] = recording
    log += f"RECORDING: saved recording {recording_name} of duration {duration_seconds}\n"


def play_recorded_movements(recording_name: str):
    global log

    log += f"RECORDING: started playing recording {recording_name}\n"
    for pos in recorded_moves[recording_name]:
        if is_pressed(failsafe_key) and failsafe_enabled:
            log += "FAILSAFE: failsafe trigger key pressed\n"
            print(FAIL + BOLD + f"Terminated Process As Failsafe Key '{failsafe_key}' Was Pressed." + END)
            log += "TERMINATED: process terminated due to failsafe activation.\n"
            quit()
        win32api.SetCursorPos(pos)
        time.sleep(0)
    log += f"RECORDING: finished playing recording {recording_name}\n"


def is_clicked(mouse_button: int = 1, watch_time: int = 5) -> bool:
    if mouse_button == 1:
        b_num = 0x01
    elif mouse_button == 2:
        b_num = 0x02

    start = time.time()
    while 1:
        if ctypes.windll.user32.GetKeyState(b_num) not in [0, 1]:
            return True
        elif time.time() - start >= watch_time:
            break
        time.sleep(0.001)
    return False


class Log:
    @staticmethod
    def get_log() -> str:
        return log

    @staticmethod
    def save_log_to_file(filename: str = "mousecontroller-log.txt"):
        global log

        log += f"LOG: saved current log to file {filename}\n"

        with open(filename, "w") as File:
            File.write(log)
