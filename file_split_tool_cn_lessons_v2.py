'''
用于的格式：
绿毯 线条 柔美 惊叹 回味 乐趣
目的地 洒脱 衣裳 彩虹 马蹄 热乎乎
礼貌 拘束 举杯 感人 会心 微笑

宅院
幽雅 伏案 浑浊 笨拙 眼帘 参差 单薄
文思 梦想 迷蒙 模糊 花蕾 衣襟 恍然
愁怨 顺心 平淡
'''

import os

filepath = "texts_raw/cn_6_1.txt"  # 替换为实际的文件路径
texts_cn_dir = "texts_out_cn/六上"  # 替换为实际的目录路径

# 读取文件的所有内容
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 按空行分割内容为不同的课文
lessons = content.strip().split("\n\n")

# 遍历每个课文
for i, lesson in enumerate(lessons):
    # 去除课文中的空行，并按空格分割为词语列表
    words = lesson.strip().split()

    # 创建课文对应的目录
    # lesson_dir = f"{texts_cn_dir}/课文{i + 1}"
    # os.makedirs(lesson_dir, exist_ok=True)

    # 保存词语到文件
    save_path = f"{texts_cn_dir}/词语{i + 1}.txt"
    # with open(f"{lesson_dir}/词语.txt", "w", encoding="utf-8") as f:
    with open(save_path, "w", encoding="utf-8") as f:
        for word in words:
            f.write(f"{word}\n")

    print(f"已保存第 {i + 1} 课的内容到文件 {save_path}。")