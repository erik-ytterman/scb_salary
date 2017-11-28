import seaborn as sns
import matplotlib.pyplot as plt

import scb_dataproxy as scbdp

df = scbdp.get_dataframe()

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(35,20))
fig.suptitle("Income and Age Distribution", fontsize=30)
fig.patch.set_facecolor('white')

g1 = sns.barplot(x='age', y='median' , hue='gender', data=df, ax=ax1)
g1.set_xlabel("Age"   ,fontsize=25)
g1.set_ylabel("Median",fontsize=25)
g1.tick_params(labelsize=20)
g1.set_xticklabels(g1.get_xticklabels(), rotation=90)

g2 = sns.barplot(x='age', y='average', hue='gender', data=df, ax=ax2)
g2.set_xlabel("Age"   ,fontsize=25)
g2.set_ylabel("Average",fontsize=25)
g2.tick_params(labelsize=20)
g2.set_xticklabels(g2.get_xticklabels(), rotation=90)

g3 = sns.barplot(x='age', y='count'  , hue='gender', data=df, ax=ax3)
g3.set_xlabel("Age"   ,fontsize=25)
g3.set_ylabel("Individuals",fontsize=25)
g3.tick_params(labelsize=20)
g3.set_xticklabels(g3.get_xticklabels(), rotation=90)

sns.despine(fig)

plt.savefig('distribution.png')
