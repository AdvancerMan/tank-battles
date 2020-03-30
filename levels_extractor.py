# coding: utf-8

from os import listdir as os_listdir, \
    mkdir as os_mkdir
from levels import level_dict_


def levels_writing(lvl_dict):
    with open('levels.py', 'w', encoding='utf-8-sig') as f:
        f.write('# coding: utf-8\n\nlevel_dict_ = {}\n')
        L_number = '0'
        for name, level in lvl_dict.items():
            L_number = str(int(L_number) + 1)
            f.write('\nL' + L_number + ' = ')
            f.write(str(level).replace(',', ',\n   ').replace('[', '[\n    ').replace(']', '\n]'))
            f.write("\n\nlevel_dict_['" + name + "'] = L" + L_number)
            f.write('\n')


def extractor():
    try:
        os_mkdir('levels')
    except OSError:
        pass

    for name, level in level_dict_.items():
        with open('levels/' + name, 'w', encoding='utf-8-sig') as f:
            for line in level:
                f.write(line + '\n')


def compressor():
    try:
        files = os_listdir('levels')
    except FileNotFoundError:
        input('Папки levels не существует.')
        return

    for file in files:
        with open('levels/' + file, encoding='utf-8-sig') as f:
            level = [line.strip() for line in f]
        level_dict_[file] = level

    levels_writing(level_dict_)


if __name__ == '__main__':
    extractor()
    compressor()