import sys

import pycorrector
import xpinyin
import pypinyin
from pycorrector.macbert.macbert_corrector import MacBertCorrector

mac_bert_corrector = MacBertCorrector()
xpy = xpinyin.Pinyin()


def corrected(s, mode='kenlm'):
    return get_corrector(mode)(s)


def get_corrector(mode='kenlm'):
    if mode == 'kenlm':
        return pycorrector.correct
    elif mode == 'mac_bert':
        return mac_bert_corrector.macbert_correct
    else:
        sys.exit(-1)


def kenlm_same(stc_1, stc_2) -> bool:
    return _corrected_same(stc_1, stc_2, mode='kenlm')


def mac_bert_same(stc_1, stc_2) -> bool:
    return _corrected_same(stc_1, stc_2, mode='mac_bert')


def xpinyin_same(stc_1, stc_2) -> bool:
    return xpy.get_pinyin(stc_1) == xpy.get_pinyin(stc_2)


def ppinyin_same(stc_1, stc_2) -> bool:
    return pypinyin.slug(stc_1) == pypinyin.slug(stc_2)


def lower_same(stc_1, stc_2) -> bool:
    return stc_1.lower() == stc_2.lower()


def _corrected_same(stc_1, stc_2, mode='kenlm'):
    corrector = get_corrector(mode)
    corrected_1, _ = corrector(stc_1)
    corrected_2, _ = corrector(stc_2)
    return corrected_1 == corrected_2 \
           or stc_1 == corrected_2 \
           or stc_2 == corrected_1


def cal_misspelling_accuracy(file_with_ground_truth):
    class AccMetric:
        def __init__(self, func, name):
            self.func = func
            self.name = name
            self.corrected_same_count = 0
            self.corrected_acc_count = 0

        def get_acc(self):
            return 1. * self.corrected_acc_count / self.corrected_same_count

    metrics = [
        AccMetric(kenlm_same, 'kenlm'),
        AccMetric(xpinyin_same, 'xpinyin'),
        AccMetric(ppinyin_same, 'ppinyin'),
        AccMetric(lower_same, 'lower'),
        AccMetric(mac_bert_same, 'mac_bert')
    ]

    with open(file_with_ground_truth, 'r') as f:
        for i, line in enumerate(f):

            data = line.rstrip().split("\t")
            stc_1, stc_2, gt = data[0], data[1], int(data[2]) == 1
            for m in metrics:
                if m.func(stc_1, stc_2):
                    m.corrected_same_count += 1
                    m.corrected_acc_count += 1 if gt else 0
                    print(f"%s found same pair, line %d, stc_1 = %s, stc_2 = %s, groundtruth is %s" % (m.name, i + 1, stc_1, stc_2, gt))
    for m in metrics:
        print(f"%s same count = %d, acc count = %d, acc = %f" % (m.name, m.corrected_same_count, m.corrected_acc_count, m.get_acc()))


if __name__ == '__main__':
    # corrected_sent, detail = pycorrector.correct('少先队员因该为老人让坐', '少先队员因该为老人让坐')
    # print(corrected_sent, detail)
    cal_misspelling_accuracy("./train.txt")
    # print(mac_bert_correct_same('少先队员因该为老人让坐', '少先队员因该为老人让坐'))

    # stc_1 = "癌症会传染吗"
    # stc_2 = "癔症会传染吗"
    # print(xpy.get_pinyin(stc_1))
    # print(pypinyin.slug(stc_1))
    # print(pycorrector.correct(stc_1))
    # print(mac_bert_corrector.macbert_correct(stc_1))
    # print(xpy.get_pinyin(stc_2))
    # print(pypinyin.slug(stc_2))
    # print(pycorrector.correct(stc_2))
    # print(mac_bert_corrector.macbert_correct(stc_2))
    # print(xpinyin_correct_same(stc_1, stc_2))
    # print(ppinyin_correct_same(stc_1, stc_2))
    # print(kenlm_correct_same(stc_1, stc_2))
    # print(mac_bert_correct_same(stc_1, stc_2))
