import os
import time
import pyttsx3
import tkinter as tk
from tkinter import filedialog
import threading
from playsound import playsound
import configparser


import inspect
import ctypes
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
    _async_raise(thread.ident, SystemError)


global contents
global rate, vol, spdFactorEn, spdFactorCN
# 配置文件路径
config_dir = 'config'
config_path = os.path.join(config_dir, 'config.ini')
# 检查是否存在config_dir路径，如果没有，就创建
if not os.path.exists(config_dir):
    os.mkdir(config_dir)


# 保存设置
def save_settings():
    # 从 Entry 中获取数值并赋值给全局变量
    global rate, vol, spdFactorEn, spdFactorCN
    rate = int(rate_entry.get())
    vol = float(vol_entry.get())
    spdFactorEn = float(spdFactorEn_entry.get())
    spdFactorCN = float(spdFactorCN_entry.get())
    # 创建配置文件对象
    config = configparser.ConfigParser()
    # 添加节
    config.add_section('settings')

    # 添加配置项
    config.set('settings', 'rate', str(rate))
    config.set('settings', 'vol', str(vol))
    config.set('settings', 'spdFactorEn', str(spdFactorEn))
    config.set('settings', 'spdFactorCN', str(spdFactorCN))

    # 写入配置文件
    with open(config_path, 'w') as f:
        config.write(f)


# 加载设置
def load_settings():
    # 创建配置文件对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read(config_path)

    # 读取配置项并赋值给全局变量和 Entry 中
    global rate, vol, spdFactorEn, spdFactorCN
    rate = int(config.get('settings', 'rate'))
    vol = float(config.get('settings', 'vol'))
    spdFactorEn = float(config.get('settings', 'spdFactorEn'))
    spdFactorCN = float(config.get('settings', 'spdFactorCN'))

    rate_entry.delete(0, tk.END)
    rate_entry.insert(0, str(rate))
    vol_entry.delete(0, tk.END)
    vol_entry.insert(0, str(vol))
    spdFactorEn_entry.delete(0, tk.END)
    spdFactorEn_entry.insert(0, str(spdFactorEn))
    spdFactorCN_entry.delete(0, tk.END)
    spdFactorCN_entry.insert(0, str(spdFactorCN))


def choose_file():
    filepath = os.getcwd()  # 获取当前执行路径
    filepath = os.path.join(filepath, 'texts')
    filepath = filedialog.askopenfilename(title="选择文件", filetypes=[("Text Files", "*.txt")], initialdir=filepath)
    if filepath:
        file_path_var.set(filepath)
        load_contents(filepath)


def load_contents(filepath):
    global contents
    contents = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split('/')
            contents.append({
                'English': words[0],
                'Chinese': words[1]
            })
    main_list.delete(0, tk.END)
    spdFactorEn = float(spdFactorEn_entry.get())
    spdFactorCN = float(spdFactorCN_entry.get())
    for c in contents:
        en_cnt = len(c['English'])
        cn_cnt = len(c['Chinese'])
        pause_time = round(en_cnt * spdFactorEn + cn_cnt * spdFactorCN)
        new_text = " / " + f"en({en_cnt})- {en_cnt * spdFactorEn:.2f};  cn({cn_cnt})- {cn_cnt * spdFactorCN:.2f} " + \
                   f" ---{pause_time}"
        text = c['English'] + " / " + c['Chinese'] + new_text
        main_list.insert(tk.END, text)  # (c['English'], c['Chinese'])


def countdown(pause_time):
    while pause_time:
        if stop_event.is_set():
            raise KeyboardInterrupt
            return
        mins, secs = divmod(pause_time, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        countdown_text.set(timeformat)
        # test_beep(2, 1)
        if pause_time >= 3:
            beep_event.set()
        else:
            beep_event2.set()
        time.sleep(1)
        pause_time -= 1


def dictate():
    try:
        global contents, rate, vol, spdFactorEn, spdFactorCN
        rate = int(rate_entry.get())
        vol = float(vol_entry.get())
        spdFactorEn = float(spdFactorEn_entry.get())
        spdFactorCN = float(spdFactorCN_entry.get())
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)  # 设置语速
        engine.setProperty('volume', vol)  # 设置音量
        voices = engine.getProperty('voices')  # 获取当前语音的详细信息
        engine.setProperty('voice', voices[1].id)
        test_beep(2, 1)
        engine.say("attention, dictation begins now")
        engine.runAndWait()
        engine.setProperty('voice', voices[0].id)
        test_beep2(2, 1)
        engine.say("注意，听写开始")
        engine.runAndWait()
        engine.setProperty('voice', voices[1].id)
        for i, c in enumerate(contents):
            en_cnt = len(c['English'])
            cn_cnt = len(c['Chinese'])
            pause_time = round(en_cnt * spdFactorEn + cn_cnt * spdFactorCN)
            # original_text = main_list.get(i)
            # new_text = original_text + "  /  " +\
            #            f"en-{en_cnt}-{en_cnt * spdFactorEn:.2f}; cn-{cn_cnt}-{cn_cnt*spdFactorCN:.2f}"
            # main_list.delete(i)
            # main_list.insert(i, new_text)
            main_list.itemconfig(i, fg="red", bg="yellow")
            main_list.see(i)
            engine.say(c['English'])
            engine.runAndWait()
            countdown(pause_time)
            main_list.itemconfig(i, fg="black", bg="grey")
            time.sleep(1)  # 避免声音冲突

        engine.setProperty('voice', voices[0].id)
        engine.say("听写结束")
        engine.runAndWait()
        engine.setProperty('voice', voices[1].id)
        engine.say("dictation completed, please check your answers")
        engine.runAndWait()
        # engine.stop()
        # stop_event.set()
    finally:
        engine.stop()
        stop_event.set()


global thread_dictate, thread_mgr
stop_event = threading.Event()  # 事件对象，目前没用


def start_dictate():  # 供按钮调用
    global thread_mgr
    thread_mgr = threading.Thread(target=dictate_mgr, daemon=True)
    stop_event.clear()
    thread_mgr.start()

def dictate_mgr():
    global thread_dictate
    thread_dictate = threading.Thread(target=dictate, daemon=True)
    thread_dictate.start()
    # print("以下stop_event.wait()")
    stop_event.wait()
    # print("stop_event. 收到，线程完结")



def kill_dictate():
    stop_event.set()  # 目前不起作用
    # stop_thread(thread_dictate)  # 强行终止，还是不行，产生的异常会被忽略，只会在响音效时终止音效进程

# 创建主窗口
root = tk.Tk()
root.title("听写助手")

# 创建文件选择框
file_path_var = tk.StringVar()
file_select_frame = tk.Frame(root)
file_select_frame.pack(side="top", fill="x")
# file_select_label = tk.Label(file_select_frame, text="选择文件：")
# file_select_label.pack(side="left")
file_entry = tk.Entry(file_select_frame, textvariable=file_path_var, state="readonly")
file_entry.pack(side="left", fill="x", expand=True)
file_select_button = tk.Button(file_select_frame, text="打开", command=choose_file, width=10)
file_select_button.pack(side="left")

# 创建列表框
main_list_frame = tk.Frame(root)
main_list_frame.pack(side="top", fill="both", expand=True)
main_list_label = tk.Label(main_list_frame, text="听写内容：")
main_list_label.pack(side="top")
main_list = tk.Listbox(main_list_frame, width=50, height=20)
main_list.pack(side="left", fill="both", expand=True)
main_list_scrollbar = tk.Scrollbar(main_list_frame, orient="vertical")
main_list_scrollbar.pack(side="right", fill="y")
main_list.configure(yscrollcommand=main_list_scrollbar.set)
main_list_scrollbar.configure(command=main_list.yview)

# 创建参数输入框
default_width = 5
param_frame = tk.Frame(root)
param_frame.pack(side="top", fill="x", expand=True)
# param_frame.pack_propagate(False)
param_label = tk.Label(param_frame, text="设置：")
param_label.pack(side="left")
rate_label = tk.Label(param_frame, text="语速")
rate_label.pack(side="left")
rate_entry = tk.Entry(param_frame, width=default_width)
rate_entry.pack(side="left", fill="x", expand=True)
rate_entry.insert(0, "150")
vol_label = tk.Label(param_frame, text="音量（0-1）：")
vol_label.pack(side="left")
vol_entry = tk.Entry(param_frame, width=default_width)
vol_entry.pack(side="left", fill="x", expand=True)
vol_entry.insert(0, "1.0")
spdFactorEn_label = tk.Label(param_frame, text="英文每字符秒：")
spdFactorEn_label.pack(side="left")
spdFactorEn_entry = tk.Entry(param_frame, width=default_width)
spdFactorEn_entry.pack(side="left", fill="x", expand=True)
spdFactorEn_entry.insert(0, "0.3")
spdFactorCN_label = tk.Label(param_frame, text="中文每字符秒：")
spdFactorCN_label.pack(side="left")
spdFactorCN_entry = tk.Entry(param_frame, width=default_width)
spdFactorCN_entry.pack(side="left", fill="x", expand=True)
spdFactorCN_entry.insert(0, "1.0")

# 创建开始按钮
start_button = tk.Button(root, text="开始听写", command=start_dictate)
start_button.pack(side="left")
start_button = tk.Button(root, text="中止听写", command=kill_dictate)
start_button.pack(side="left")
start_button = tk.Button(root, text="保存设置", command=save_settings)
start_button.pack(side="right")
start_button = tk.Button(root, text="载入设置", command=load_settings)
start_button.pack(side="right")

# 创建倒计时文本框
countdown_frame = tk.Frame(root)
countdown_frame.pack(side="bottom")
countdown_label = tk.Label(countdown_frame, text="倒计时：")
countdown_label.pack(side="left")
countdown_text = tk.StringVar()
countdown_text.set("")
countdown_entry = tk.Entry(countdown_frame, textvariable=countdown_text, state="readonly")
countdown_entry.pack(side="left")


# 发音事件
def beep_task():
    while True:
        beep_event.wait()  # 等待事件
        playsound(".\\sounds\\start-13691.mp3")
        beep_event.clear()  # 重置事件状态


beep_event = threading.Event()  # 播放事件对象
beep_thread = threading.Thread(target=beep_task, daemon=True)
beep_thread.start()


# 发音事件2
def beep_task2():
    while True:
        beep_event2.wait()  # 等待事件
        playsound(".\\sounds\\stop-13692.mp3")
        beep_event2.clear()  # 重置事件状态


beep_event2 = threading.Event()  # 播放事件对象2
beep_thread2 = threading.Thread(target=beep_task2, daemon=True)
beep_thread2.start()


# 发音测试
def test_beep(cnt: int, interval: float):
    for i in range(cnt):
        beep_event.set()
        time.sleep(interval)


# 发音测试2
def test_beep2(cnt: int, interval: float):
    for i in range(cnt):
        beep_event2.set()
        time.sleep(interval)

# 加载设置
try:
    load_settings()
except Exception as e:
    print("错误：", e)
# 运行主循环
root.mainloop()
