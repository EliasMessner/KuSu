import os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zipf

german_colors = ['Rot', 'Violett', 'Blau', 'Grün', 'Gelb', 'Orange', 'Schwarz', 'Weiß', 'Grau','Metallic','Braun','Türkis-Blaugrün','Pink-Rosa']

def count_occurences(path):
    color_counts = dict.fromkeys(german_colors, 0)
    for el in os.listdir(path):
        with open(path + "/" + el, 'r', encoding="ISO-8859-1") as file:
            lines = file.readlines()
            lines = [el for line in lines for el in line.split() if el != "\n"]
            line_dict = Counter(lines)
            color_counts = Counter(color_counts)
            color_counts = line_dict + color_counts
    sum_values = sum(color_counts.values())
    color_counts = {k:(v/sum_values)*100 for (k,v) in color_counts.items() if (v/sum_values)*100 >=1}
    return dict(sorted(color_counts.items(), key=lambda item: item[1], reverse=True))

def plot_plot(number,keys,values, quelle):
    plt.rcParams['text.usetex'] = True
    alpha = 2
    plt.subplot(3,1,number)
    plt.ylim([0, 100])
    width = [0.1 for el in range(0,len(keys))]
    x_axis = np.arange(len(keys))
    plot = plt.bar(x_axis-0.2, values,width = width, label = "reale Verteilung")
    total = sum(values)
    plt.bar(x_axis+0.2, [zipf.pmf(p, alpha) * total for p in range(1, len(keys) + 1)],width = width, label = r'erwartete Zipf-Verteilung für $\alpha = 2$')
    plt.ylabel('Häufigkeit in \%', fontsize=8)
    plt.xlabel('Häufigkeitsverteilung in Bildern aus '+quelle, fontsize=8)
    plt.legend(loc="upper right", prop={'size': 8})    
    plt.xticks(x_axis, keys)
    
## first plot westmuensterland
westmuensterland = '../images/westmuensterlandtext'
westmuensterland_counts = count_occurences(westmuensterland)
westmuensterland_keys = westmuensterland_counts.keys()
westmuensterland_values= westmuensterland_counts.values()
plot_plot(1, westmuensterland_keys, westmuensterland_values, "Westmünsterland")

## second plot muenchen
muenchen = '../images/muenchentext'
muenchen_counts = count_occurences(muenchen)
muenchen_keys = muenchen_counts.keys()
muenchen_values = muenchen_counts.values()
plot_plot(2, muenchen_keys, muenchen_values, " München")

## third plot all
all_counts = dict(Counter(westmuensterland_counts)+Counter(muenchen_counts))
sum_values = sum(all_counts.values())
all_counts = {k:(v/sum_values)*100 for (k,v) in all_counts.items() if (v/sum_values)*100 >=1}
all_counts = dict(sorted(all_counts.items(), key=lambda item: item[1], reverse=True) )
all_keys = all_counts.keys()
all_values = all_counts.values()
plot_plot(3, all_keys, all_values, " beiden Quellen")
plt.subplots_adjust(hspace=0.8)
plt.savefig("Häufigkeitsverteilungen")