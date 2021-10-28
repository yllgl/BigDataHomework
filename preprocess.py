import os.path as path

from misspelling import kenlm_same, xpinyin_same, ppinyin_same, mac_bert_same, lower_same

xpinyin_same_line_number_file = "./xpinyin_same_line_number.txt"
ppinyin_same_line_number_file = "./ppinyin_same_line_number.txt"
lower_same_line_number_file = "./lower_same_line_number.txt"
kenlm_correct_same_line_number_file = "./kenlm_correct_same_line_number.txt"
mac_bert_correct_same_line_number_file = "./mac_bert_correct_same_line_number.txt"


def save_line_numbers(test_file_path):
    with open(test_file_path, 'r') as f:
        class CorrectOuter:
            def __init__(self, filepath, func, name):
                self.file_exists = False
                self.out = None
                if path.exists(filepath):
                    self.file_exists = True
                    return
                self.out = open(filepath, 'a+', encoding='utf8')
                self.func = func
                self.name = name

            def __del__(self):
                if self.out is not None:
                    self.out.close()

        outers = [
                  CorrectOuter(xpinyin_same_line_number_file, xpinyin_same, 'xpinyin'),
                  CorrectOuter(ppinyin_same_line_number_file, ppinyin_same, 'ppinyin'),
                  CorrectOuter(lower_same_line_number_file, lower_same, 'lower'),
                  CorrectOuter(kenlm_correct_same_line_number_file, kenlm_same, 'kenlm'),
                  CorrectOuter(mac_bert_correct_same_line_number_file, mac_bert_same, 'mac_bert')
        ]

        for i, line in enumerate(f):
            a, b = line.strip().split('\t')
            for outer in outers:
                if outer.file_exists:
                    continue
                if outer.func(a, b):
                    print(f"found same %s at line %d, a = %s, b = %s" % (outer.name, i + 1, a, b))
                    outer.out.write(str(i) + "\n")
            # if pinyin_correct_same(a, b):
            #     print("found same pinyin, a = ", a, "b = ", b)
            #     with open(pinyin_same_line_number_file, 'a+', encoding='utf8') as out:
            #         out.write(str(i) + "\n")
            # if kenlm_correct_same(a, b):
            #     print("found same kenlm, a = ", a, "b = ", b)
            #     with open(kenlm_correct_same_line_number_file, 'a+', encoding='utf8') as out:
            #         out.write(str(i) + "\n")
            # if mac_bert_correct_same()


def ensure_predict_preprocessed(test_file_path):
    save_line_numbers(test_file_path)


if __name__ == '__main__':
    ensure_predict_preprocessed("./test_A.tsv")
    # print(kenlm_correct_same("1", "2"))
