#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math
import collections

plt.rcParams['font.sans-serif'] = ['SimHei']   # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False     # 正常显示负号

# fin = open('./data.txt', 'r')
# datanum = int(fin.readline())
# data = []
# for i in range(datanum):
#     data.append([int(i) for i in fin.readline().split()][1:])
# print(data)

datafile = './data.txt'
# isUSTC: 1 for USTCers, 0 for other school
isUSTC = np.genfromtxt(datafile, delimiter=' ', usecols=(1,), dtype=int)
isUSTC = 2 - isUSTC
# grade: 1 for grade one, 0 for higher grade
grade = np.genfromtxt(datafile, delimiter=' ', usecols=(2,), dtype=int)
grade = np.array([0 if i > 1 else 1 for i in grade])
isknown = np.genfromtxt(datafile, delimiter=' ', usecols=(3,), dtype=int)
isknown = 2 - isknown
# others: 1 for yes(means bad), 0 for maybe, -1 for no(in good condition)
isselfOCD = np.genfromtxt(datafile, delimiter=' ', usecols=(4,), dtype=int)
isselfOCD = 2 - isselfOCD
isOCDbad = np.genfromtxt(datafile, delimiter=' ', usecols=(5,), dtype=int)
isOCDbad = 2 - isOCDbad
self_condition = np.genfromtxt(datafile, delimiter=' ', usecols=(6, 7, 8, 9, 10, 11), dtype=int)
self_condition = 2 - self_condition
self_condition_sum = np.array([i.sum() for i in self_condition])
self_condition_sum_yes = np.array([collections.Counter(i)[1] for i in self_condition])
test_result = np.genfromtxt(datafile, delimiter=' ', usecols=(i for i in range(12, 40 + 1)), dtype=int)
test_result = 2 - test_result
test_result_sum = np.array([i.sum() for i in test_result])
test_result_sum_yes = np.array([collections.Counter(i)[1] for i in test_result])
# print(test_result_sum)
# print(test_result_sum_yes)

total = len(isUSTC)
total_ustc = (isUSTC == 1).sum()
print('Total questionnaires: %d' % total)
print('USTC: %d' % total_ustc)
print('non-USTC: %d' % (total - total_ustc))
total_gradeone = (grade == 1).sum()
print('Grade one or lower: %d' % total_gradeone)
print('Grade two or higher: %d' % (total - total_gradeone))
print('Know about OCD: %f' % ((isknown == 1).sum() / total))
print('Know about OCD USTC: %f' % ((isknown[isUSTC == 1] == 1).sum() / total_ustc))
print('Know about OCD non-USTC: %f' % ((isknown[isUSTC == 0] == 1).sum() / (total - total_ustc)))
print('Think self has OCD: %f' % ((isselfOCD == 1).sum() / total))
print('Think self has OCD USTC: %f' % ((isselfOCD[isUSTC == 1] == 1).sum() / total_ustc))
print('Think self has OCD non-USTC: %f' % ((isselfOCD[isUSTC == 0] == 1).sum() / (total - total_ustc)))
print('Think self disturbed by OCD: %f' % ((isOCDbad == 1).sum() / total))
print('Think self disturbed by OCD USTC: %f' % ((isOCDbad[isUSTC == 1] == 1).sum() / total_ustc))
print('Think self disturbed by OCD non-USTC: %f' % ((isOCDbad[isUSTC == 0] == 1).sum() / (total - total_ustc)))

# 看相关系数
print('Correlation of self_condition: ')
self_condition_cor = np.corrcoef(self_condition.transpose())
# print(self_condition_cor)
# you can see all these elems are Positive

print('Correlation of test_result: ')
test_result_cor = np.corrcoef(test_result.transpose())
# print(test_result_cor)
# you can see all these elems are also Positive

self_and_test_cor = np.corrcoef([self_condition_sum, test_result_sum])
# print(self_and_test_cor)
# 0.689, seems strongly related
# 显著性检验 费希尔t检验
r = self_and_test_cor[0][1]
n = len(self_condition_sum)
t = math.fabs(r) * math.sqrt((n - 2) / (1 - r ** 2))
print("total: %d" % n)
print(t)
# 10.370, while t_100_0.005 = 2.626, t_125_0.005 = 2.616
# 在显著性水平0.01(99%)下认为二者有强相关关系

print("Average OCD tendency(by test table): total/USTC/non-USTC for all(yes, maybe, no) and specific(yes only)")
print(np.average(test_result_sum))
print(np.average(test_result_sum[isUSTC == 1]))
print(np.average(test_result_sum[isUSTC == 0]))
print(np.average(test_result_sum_yes))
print(np.average(test_result_sum_yes[isUSTC == 1]))
print(np.average(test_result_sum_yes[isUSTC == 0]))
# 看起来中科大的情况好于其他学校？
# -7.19834710744
# -8.52830188679
# -6.16176470588
# 5.76859504132
# 5.75471698113
# 5.77941176471

print("Average OCD tendency(by test table): total/grade-1/non-grade-1 for all(yes, maybe, no) and specific(yes only)")
print(np.average(test_result_sum))
print(np.average(test_result_sum[grade == 1]))
print(np.average(test_result_sum[grade == 0]))
print(np.average(test_result_sum_yes))
print(np.average(test_result_sum_yes[grade == 1]))
print(np.average(test_result_sum_yes[grade == 0]))
# -7.19834710744
# -5.47619047619
# -11.1081081081
# 5.76859504132
# 6.36904761905
# 4.40540540541
# 结果大一比大二上明显强迫严重

# 独立性检验
# >=8 认为强迫
a = isUSTC_OCD = sum(i >= 8 for i in test_result_sum[isUSTC == 1])
b = isUSTC_nonOCD = sum(not (i >= 8) for i in test_result_sum[isUSTC == 1])
c = nonUSTC_OCD = sum(i >= 8 for i in test_result_sum[isUSTC == 0])
d = nonUSTC_nonOCD = sum(not (i >= 8) for i in test_result_sum[isUSTC == 0])
Ksqr = total * (a * d - b * c) ** 2 / ((a + b) * (a + c) * (c + d) * (b + d))
print(a, b, c, d)
print("Ksqr: %f" % Ksqr)
# 0.141, <3.841, 认为无关

a = isgrade_OCD = sum(i >= 8 for i in test_result_sum[grade == 1])
b = isgrade_nonOCD = sum(not (i >= 8) for i in test_result_sum[grade == 1])
c = nongrade_OCD = sum(i >= 8 for i in test_result_sum[grade == 0])
d = nongrade_nonOCD = sum(not (i >= 8) for i in test_result_sum[grade == 0])
Ksqr = total * (a * d - b * c) ** 2 / ((a + b) * (a + c) * (c + d) * (b + d))
print(a, b, c, d)
print("Ksqr: %f" % Ksqr)
# 2.74, <3.841, >2.706, 认为90%有关， 但不能认为95%有关

# >=3 认为状况不好
a = isUSTC_OCD = sum(i >= 3 for i in self_condition_sum[isUSTC == 1])
b = isUSTC_nonOCD = sum(not (i >= 3) for i in self_condition_sum[isUSTC == 1])
c = nonUSTC_OCD = sum(i >= 3 for i in self_condition_sum[isUSTC == 0])
d = nonUSTC_nonOCD = sum(not (i >= 3) for i in self_condition_sum[isUSTC == 0])
Ksqr = total * (a * d - b * c) ** 2 / ((a + b) * (a + c) * (c + d) * (b + d))
print(a, b, c, d)
print("Ksqr: %f" % Ksqr)
# 0.141, <3.841, 认为无关

a = isgrade_OCD = sum(i >= 3 for i in self_condition_sum[grade == 1])
b = isgrade_nonOCD = sum(not (i >= 3) for i in self_condition_sum[grade == 1])
c = nongrade_OCD = sum(i >= 3 for i in self_condition_sum[grade == 0])
d = nongrade_nonOCD = sum(not (i >= 3) for i in self_condition_sum[grade == 0])
Ksqr = total * (a * d - b * c) ** 2 / ((a + b) * (a + c) * (c + d) * (b + d))
print(a, b, c, d)
print("Ksqr: %f" % Ksqr)
# 2.74, <3.841, >2.706, 认为90%有关， 但不能认为95%有关

plt.hist(test_result_sum, bins=10, facecolor='blue', edgecolor='black')
plt.title('强迫强度--是、或许、否')
plt.ylabel('人数')
plt.savefig('1.png')
plt.show()
plt.hist(test_result_sum_yes, bins=10, facecolor='orange', edgecolor='black')
plt.title('强迫强度--回答“是”的个数')
plt.ylabel('人数')
plt.savefig('2.png')
plt.show()
plt.hist(self_condition_sum, bins=10, facecolor='blue', edgecolor='black')
plt.title('自我状况，大表示糟糕，小表示良好（总）')
plt.ylabel('人数')
plt.savefig('3.png')
plt.show()
plt.hist(self_condition_sum_yes, bins=7, facecolor='orange', edgecolor='black')
# plt.scatter([i for i in range(0, 7)], [collections.Counter(self_condition_sum_yes)[i] for i in range(0, 7)])
plt.title('自我状况，大表示糟糕，小表示良好（回答是）')
plt.ylabel('人数')
plt.savefig('4.png')
plt.show()
