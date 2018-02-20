# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Skrypt który czyta dane z plików txt, powstałych przy użyciu skrypyów testingModelPM10/testingModelPM25



file = open("err1hPM25.txt", "r")
arr = []
for line in file:
    if (float(line)< 20000):
      arr.append(float(line))

print "srednia 1sza"
avg = sum(arr)/len(arr)
print avg

centile_25th = np.percentile(arr, 25)
centile_50th = np.percentile(arr, 50)
centile_75th = np.percentile(arr, 75)

print "centyle 1sze:"
print centile_25th
print centile_50th
print centile_75th

print arr
sns.kdeplot(np.array(arr), cut= 0.0, shade=True)
plt.xlabel("Błąd względny [%]", fontsize = 20)
plt.ylabel("Gęstość prawdopodobieństwa", fontsize = 20)
plt.title("Rozkład względnego błędu predykcji stężenia pyłu $PM_{2.5}$", fontsize = 20)
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
plt.xlim(0, 150)

plt.show()
