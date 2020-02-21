# encoding=utf-8
import os

import imageio
import jieba
from wordcloud import WordCloud


def cut_word(file_path):
    txt = ''
    with open(file_path, 'r') as f:
        line = f.readline()
        while line:
            txt += line
            line = f.readline()

    words = jieba.cut_for_search(txt)
    word_dict = dict()
    stop_word_set = get_stop_word_set()
    # print('舍弃的词: \n')
    for word in words:
        if len(word) < 2 or word in stop_word_set:
            # print(word)
            continue

        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] += 1

    return word_dict


def get_stop_word_set():
    stop_word_set = set()
    txt = ''
    with open('/home/john/tmp/words/wordcloud/txt/stop_words', 'r') as f:
        line = f.readline()
        while line:
            txt += line
            line = f.readline()

    for word in txt.split('\n'):
        stop_word_set.add(word)
    return stop_word_set


def save_cut_word(sort_list, file_path):
    with open(file_path, 'w') as f:
        for word in sort_list:
            f.write('%s %s\n' % (word[0], str(word[1])))


def get_sort_dict(word_dict):
    return sorted(word_dict.items(), key=lambda x: x[1], reverse=True)


def get_cut_words(sort_list, counts):
    sort_word_list = sort_list[:counts]
    print('分析的词: \n')
    ret_list = list()
    i = 1
    for word_tuple in sort_word_list:
        print('%s:%d:%d' % (word_tuple[0], word_tuple[1], i))
        ret_list.append(word_tuple[0])
        i += 1
    return ret_list


def generate_word_img(word_list, save_img_path):
    color_mask = imageio.imread('/home/john/tmp/words/wordcloud/background/hongxin.jpeg')
    wc = WordCloud(
        background_color='black',
        max_words=len(word_list),
        font_path='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        min_font_size=15,
        max_font_size=50,
        width=400,
        height=860,
        mask=color_mask
    )
    word_str = ''
    for word in word_list:
        word_str += word + ' '

    word_str = word_str.rstrip()
    wc.generate(word_str)
    wc.to_file(save_img_path)


def generate_new_word_cloud_img():
    word_dict = cut_word('/home/john/tmp/words/wordcloud/txt/hongloumeng.txt')
    sort_word_list = get_sort_dict(word_dict)
    save_cut_word_path = '/home/john/tmp/words/wordcloud/dict/hongloumeng'
    if not os.path.exists(save_cut_word_path):
        save_cut_word(sort_word_list, save_cut_word_path)
    word_list = get_cut_words(sort_word_list, 200)
    generate_word_img(word_list, '/home/john/tmp/words/wordcloud/hongloumeng.jpeg')


def test_generate_word_img():
    wl = ['一书', '故曰', '云云', '但书中', '所记', '何事', '何人']
    generate_word_img(wl, '/home/john/tmp/words/wordcloud/hongloumeng.jpeg')


if __name__ == '__main__':
    generate_new_word_cloud_img()
    # test_generate_word_img()
