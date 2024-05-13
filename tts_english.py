import tkinter as tk
from tkinter import scrolledtext, Entry, Label, messagebox
import pyttsx3
import threading

# 初始化Tkinter窗口
root = tk.Tk()
root.title("Text to Speech")

# 初始化pyttsx3引擎
engine = pyttsx3.init()

# 创建一个多行文本框
text_area = scrolledtext.ScrolledText(root, width=50, height=15)
text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# 增加一个标签和单行文本框用于输入语速
rate_label = Label(root, text="语速:")
rate_label.pack(pady=5)

rate_entry = Entry(root, width=5)
rate_entry.pack(pady=5)

# 设置默认语速
rate_entry.insert(0, "150")


# 定义朗读函数
def speak():
    # 获取文本框中的内容
    text = text_area.get("1.0", tk.END)

    # 获取语速输入框的内容，并尝试转换为整数
    try:
        rate = int(rate_entry.get())
    except ValueError:
        messagebox.showerror("错误", "语速必须是数字")
        return

    # 使用线程进行朗读，以避免阻塞主线程
    threading.Thread(target=say, args=(text, rate)).start()


# 定义清理换行函数，把text_area内容中换行符替换为空格
def clear_new_line():
    text = text_area.get("1.0", tk.END)
    text = text.replace('\n', ' ')
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", text)




# 定义使用pyttsx3引擎的say函数
def say(text, rate):
    # 设置语速
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')  # 获取当前语音的详细信息
    engine.setProperty('voice', voices[1].id)
    # 朗读文本
    engine.say(text)
    engine.runAndWait()


# 创建一个按钮，标题为“朗读”
speak_button = tk.Button(root, text="朗读", command=speak)
speak_button.pack(pady=10)

# 创建一个按钮，标题为“清理换行”
speak_button = tk.Button(root, text="清理换行", command=clear_new_line)
speak_button.pack(pady=10)

# 运行Tkinter主循环
root.mainloop()