import os, re
import csv,codecs

# 要求：把需要词频统计的文件都放在 "文件" 文件夹

current_files = os.listdir(".")

if "文件" not in current_files:
    raise RuntimeError("必须把需要词频统计的文件都放在 \"文件\" 文件夹")

files = os.listdir("文件")

if "词频统计(2字)" not in current_files:
    os.mkdir("词频统计(2字)")
if "词频统计(4字)" not in current_files:
    os.mkdir("词频统计(4字)")

def remove_punctuation(text):
    return ''.join(re.findall(u'[\u4e00-\u9fa5]+',text))

def count(text, skip, word_bank):
    result = dict()
    i = 0
    while i <= len(text) - skip:
        word = text[i:i+skip]
        if word in word_bank:
            if word not in result:
                result[word] = 1
            else:
                result[word] += 1
        i += 1
    return result

def load_dictionary():
    dictionary = set()
    print("加载词库...")
    with open('dict.txt', 'r') as file:
        word = file.readline()
        while word is not '':
            dictionary.add(word.strip().replace('n', ''))
            word = file.readline()
    print("加载完毕...")
    return dictionary


def write_result(dictionary, skip, name):
    with codecs.open('词频统计({0}字)/{1}'.format(skip, name.replace('txt', 'csv')), 'w', 'utf_8_sig') as file:
        file = csv.writer(file)
        for key in dictionary.keys():
            file.writerow([key, dictionary[key]]) # "{0},{1}\n".format(key, dictionary[key])

word_bank = load_dictionary()

total = len(files)
for i, name in enumerate(files):
    if '.txt' in name:
        with open('文件/{0}'.format(name), 'r') as file:
            try:
                text = file.read()
                text = remove_punctuation(text)
                text = ''.join(text.split())
                print(" 处理进度: {0:.2f}%".format(i / total * 100), end="\r")
                write_result(count(text, 2, word_bank), 2, name)
                write_result(count(text, 4, word_bank), 4, name)
            except Exception as e:
                print("处理失败：{0}".format(name))

        

