''' 用于的格式：
第一课
colourful [klfl] 多彩的

prefer [prf:(r)] 选择；宁愿要

winter [wnt(r)] 冬天

第二课

middle [mdl] 中间的；中等的

classmate [klɑ:smet] 同班同学

Australia ['strel] 澳大利亚

answer [ɑ:ns(r)] 回答
China ['tan] 中国

'''


import os


def is_blank(line):
    """
    判断一行是否为空行
    """
    stripped_line = line.strip()
    return len(stripped_line) == 0


def parse_text(text):
    if "[" in text and "]" in text:  # 判断字符串是否包含 "[" 和 "]" 字符
        # 如果存在 "[" 和 "]" 字符，判定为第一种格式
        start_index = text.index("[")  # 获取 "[" 字符的索引位置
        end_index = text.index("]")  # 获取 "]" 字符的索引位置
        tmp_en = text[:start_index].strip()  # 获取 "[" 字符前面的部分
        tmp_cn = text[end_index+1:].strip()  # 获取 "]" 字符后面的部分
        parts = [tmp_en, tmp_cn]  # 生成临时列表
    else:
        # 如果不存在 "[" 和 "]" 字符，判定为第二种格式
        for i, c in enumerate(text):
            if '\u4e00' <= c <= '\u9fa5':  # 判断字符是否为中文字符
                tmp_en = text[:i].strip()  # 获取中文字符前面的部分
                tmp_cn = text[i:].strip()  # 获取中文字符和后面的部分
                parts = [tmp_en, tmp_cn]  # 生成临时列表
                break

    return parts

def parse_raw_file(filename):
    list_raw = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if not is_blank(line):
                list_raw.append(line.rstrip())  # 去掉每行结尾的换行符，并添加到列表中

    list_splited = []  # 保存结果的列表
    current_unit = {}  # 当前处理的单元的信息
    for line in list_raw:
        if line.startswith("第"):  # 如果是标题行
            if current_unit:  # 如果当前有正在处理的单元，将其保存到结果列表中
                list_splited.append(current_unit)
            current_unit = {"title": line, "unit_content": []}  # 创建一个新的单元信息字典
        else:  # 如果是内容行
            # parts = line.split("\t")  # 将每行内容按制表符分隔
            _parts = parse_text(line)
            current_unit["unit_content"].append(_parts)  # 将内容行添加到单元信息字典中

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
                line = f"{content[0]} / {content[1]}"
                f.write(line + "\n")  # 将内容写入文件，并添加一个换行符


result = parse_raw_file("texts_raw/kj_5d.txt")
save_files(result, "texts")
