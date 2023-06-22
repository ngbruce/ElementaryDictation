''' 用于的格式：
第1单元Welcome to our school
1	have	有 /hæv; həv/
2	many	许多 /'meni/
3	like	像……那样 /laɪk/
4	music	音乐 /'mju:zɪk/
第2单元Can I help you?
1	car	小汽车 /kɑ:(r)/
2	plane	飞机 /pleɪn/
3	train	火车 /treɪn/
4	can	能 /kæn; kən/
'''


import os


def parse_raw_file(filename):
    list_raw = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            list_raw.append(line.rstrip())  # 去掉每行结尾的换行符，并添加到列表中

    list_splited = []  # 保存结果的列表
    current_unit = {}  # 当前处理的单元的信息
    for line in list_raw:
        if line.startswith("第"):  # 如果是标题行
            if current_unit:  # 如果当前有正在处理的单元，将其保存到结果列表中
                list_splited.append(current_unit)
            current_unit = {"title": line, "unit_content": []}  # 创建一个新的单元信息字典
        else:  # 如果是内容行
            parts = line.split("\t")  # 将每行内容按制表符分隔
            current_unit["unit_content"].append(parts)  # 将内容行添加到单元信息字典中

    # 处理最后一个单元
    if current_unit:
        list_splited.append(current_unit)

    return list_splited


# def save_files(list_splited):
#     # 定义不允许用作文件名或路径名的字符
#     invalid_chars = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
#     for unit in list_splited:
#
#         # 以标题为文件名创建文件，打开并以增加方式写入内容
#         with open(f"texts/{unit['title'].rstrip()}.txt", "a", encoding="utf-8") as f:
#             for content in unit["unit_content"]:
#                 # 读取字符串列表索引为[1]和[2]的内容，中间用“ / ”拼接
#                 line = f"{content[1]} / {content[2]}"
#                 f.write(line + "\n")  # 将内容写入文件，并添加一个换行符
def save_files(list_splited, save_path):
    # 定义不允许用作文件名或路径名的字符
    invalid_chars = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]

    for unit in list_splited:
        # 删除标题中不允许用作文件名或路径名的字符
        title = unit["title"].rstrip()
        for char in invalid_chars:
            title = title.replace(char, "")

        # 创建文件路径并创建文件
        file_path = os.path.join(save_path, f"{title}.txt")
        with open(file_path, "a", encoding="utf-8") as f:
            for content in unit["unit_content"]:
                # 读取字符串列表索引为[1]和[2]的内容，中间用“ / ”拼接
                line = f"{content[1]} / {content[2]}"
                f.write(line + "\n")  # 将内容写入文件，并添加一个换行符


result = parse_raw_file("texts_raw/raw_5d.txt")
save_files(result, "texts")
