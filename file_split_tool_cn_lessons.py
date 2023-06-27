filepath = "texts_raw/words_cn.txt"  # 替换为实际的文件路径
texts_cn_dir = "texts_out_cn"  # 替换为实际的目录路径

# 读取文件的所有内容
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 读取每一行，取出头尾的空格
lines_stripped = [line.strip() for line in lines]

# 定义列表列表，表示每一课的中文词语列表
list_lessons = []

# 遍历所有内容，按照数字开头的行划分为不同的课
lesson_index = -1
for line in lines_stripped:
    if line and line[0].isdigit():
        # 如果这一行以数字开头，表示这是一课
        lesson_index += 1
        list_lessons.append([])

        # 读取这一课的内容，使用空格划分中文词语，并添加到列表中
        words = line.split()[1:]
        for word in words:
            list_lessons[lesson_index].append(word)

    else:
        # 如果这一行不以数字开头，表示这是这一课的一部分
        # 将这一行使用空格划分中文词语，并添加到列表中
        words = line.split()
        for word in words:
            list_lessons[lesson_index].append(word)

# 遍历所有课程，保存为文件
for i, lesson in enumerate(list_lessons):
    filename = f"{i}.txt"
    filepath = f"{texts_cn_dir}/{filename}"
    with open(filepath, "w", encoding="utf-8") as f:
        for word in lesson:
            f.write(f"{word}\n")
    print(f"已保存第 {i} 课的内容到文件 {filename}。")