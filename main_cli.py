import time
import pyttsx3
import sys


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print("\r"+timeformat, end='')
        sys.stdout.flush()
        # print(timeformat)
        time.sleep(1)
        t -= 1
    print("\r>")


def dictate(filepath: str, rate: int, vol: float, spdFactorEn: float, spdFactorCN: float):
    contents = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split('/')
            contents.append({
                'English': words[0],
                'Chinese': words[1]
            })
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # 设置语速
    engine.setProperty('volume', vol)  # 设置音量
    voices = engine.getProperty('voices')  # 获取当前语音的详细信息
    # print (voices)
    engine.setProperty('voice', voices[1].id)
    for c in contents:
        en_cnt = len(c['English'])
        cn_cnt = len(c['Chinese'])
        print(f"{en_cnt * spdFactorEn} + {cn_cnt*spdFactorCN}")
        pause_time = round(en_cnt * spdFactorEn + cn_cnt*spdFactorCN)
        print(f"Say: {c['English']} / {c['Chinese']} / {pause_time}秒 for {en_cnt}字符, {cn_cnt}中文")
        engine.say(c['English'])
        engine.runAndWait()
        countdown(pause_time)
    engine.say("dictation finished")
    engine.runAndWait()
    engine.setProperty('voice', voices[0].id)
    engine.say("听写结束")
    engine.runAndWait()
    engine.stop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dictate('texts\\dictation.txt', 150, 1.0, 0.3, 1.0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
