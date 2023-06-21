import os
import time
import pyttsx3
import tkinter as tk
from tkinter import filedialog
import threading

global contents


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
    for c in contents:
        text = c['English']+" / "+ c['Chinese']
        main_list.insert(tk.END, text)  # (c['English'], c['Chinese'])


def countdown(pause_time):
    while pause_time:
        mins, secs = divmod(pause_time, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        countdown_text.set(timeformat)
        time.sleep(1)
        pause_time -= 1


def dictate():
    global contents
    rate = int(rate_entry.get())
    vol = float(vol_entry.get())
    spdFactorEn = float(spdFactorEn_entry.get())
    spdFactorCN = float(spdFactorCN_entry.get())
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # 设置语速
    engine.setProperty('volume', vol)  # 设置音量
    voices = engine.getProperty('voices')  # 获取当前语音的详细信息
    # print (voices)
    engine.setProperty('voice', voices[1].id)
    engine.say("dictation begins now")
    engine.runAndWait()
    for i, c in enumerate(contents):
        en_cnt = len(c['English'])
        cn_cnt = len(c['Chinese'])
        pause_time = round(en_cnt * spdFactorEn + cn_cnt*spdFactorCN)
        original_text = main_list.get(i)
        new_text = original_text + "  /  " + f"en-{en_cnt}-{en_cnt * spdFactorEn:.2f}; cn-{cn_cnt}-{cn_cnt*spdFactorCN:.2f}"
        main_list.delete(i)
        main_list.insert(i, new_text)
        main_list.itemconfig(i, fg="red")  # , font=('Arial', 11, 'bold')
        main_list.see(i)
        engine.say(c['English'])
        engine.runAndWait()
        countdown(pause_time)
        main_list.itemconfig(i, fg="black")  # , font=('Arial', 11, 'normal')

    engine.say("dictation finished")
    engine.runAndWait()
    engine.setProperty('voice', voices[0].id)
    engine.say("听写结束")
    engine.runAndWait()
    engine.stop()


def start_dictate():
    t = threading.Thread(target=dictate)
    t.start()


# 创建主窗口
root = tk.Tk()
root.title("听写助手")

# 创建文件选择框
file_path_var = tk.StringVar()
file_select_frame = tk.Frame(root)
file_select_frame.pack(side="top", fill="x")
file_select_label = tk.Label(file_select_frame, text="选择文件：")
file_select_label.pack(side="left")
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
spdFactorEn_label = tk.Label(param_frame, text="英文字符每秒：")
spdFactorEn_label.pack(side="left")
spdFactorEn_entry = tk.Entry(param_frame, width=default_width)
spdFactorEn_entry.pack(side="left", fill="x", expand=True)
spdFactorEn_entry.insert(0, "0.3")
spdFactorCN_label = tk.Label(param_frame, text="中文字符每秒：")
spdFactorCN_label.pack(side="left")
spdFactorCN_entry = tk.Entry(param_frame, width=default_width)
spdFactorCN_entry.pack(side="left", fill="x", expand=True)
spdFactorCN_entry.insert(0, "1.0")

# 创建开始按钮
start_button = tk.Button(root, text="开始听写", command=start_dictate)
start_button.pack(side="bottom")

# 创建倒计时文本框
countdown_frame = tk.Frame(root)
countdown_frame.pack(side="bottom")
countdown_label = tk.Label(countdown_frame, text="倒计时：")
countdown_label.pack(side="left")
countdown_text = tk.StringVar()
countdown_text.set("")
countdown_entry = tk.Entry(countdown_frame, textvariable=countdown_text, state="readonly")
countdown_entry.pack(side="left")

# 运行主循环
root.mainloop()
