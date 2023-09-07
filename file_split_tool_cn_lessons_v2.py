import os

filepath = "texts_raw/cn_6_1.txt"
texts_cn_dir = "texts_out_cn/六上"

if not os.path.exists(texts_cn_dir):
    os.makedirs(texts_cn_dir)

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

lesson = []
lesson_name = ""

for line in lines:
    if line.startswith("第一课"):
        # 遇到新课程,保存上一个课程
        if lesson:
            with open(f"{texts_cn_dir}/{lesson_name}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(lesson))
            print(f"已保存 {lesson_name}")

        # 开始新课程
        lesson_name = line
        lesson = []

    elif line == "":
        # 空行,跳过
        continue

    else:
        # 普通行,提取词语
        words = line.split()
        lesson.extend(words)

# 保存最后一个课程
if lesson:
    with open(f"{texts_cn_dir}/{lesson_name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lesson))
    print(f"已保存 {lesson_name}")