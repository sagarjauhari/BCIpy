import pandas as pd

aoa = pd.read_csv('published_data/AoA_51715_words.csv')
print aoa['AoA_Kup_lem']
print aoa['Freq_pm']
print aoa['Word']
