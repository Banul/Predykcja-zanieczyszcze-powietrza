#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [2, 7, 8, 9, 8, 13, 14, 15, 27, 21]
twoX = result = map(lambda i: i * 2, x)


plt.scatter(x,y)
plt.xlabel("x",fontsize = 24)
plt.ylabel("y", fontsize = 24)
plt.title("Przykład przetrenowania algorytmu", fontsize = 20)
plt.plot(x,y, color = 'g', label = "algorytm przetrenowany")
plt.plot(x, twoX, color = 'r', label = "algorytm dobrze dopasowujący się")
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend( prop={'size': 16})
plt.show()