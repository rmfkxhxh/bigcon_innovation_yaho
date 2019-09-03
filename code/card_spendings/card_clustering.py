# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'code\\card_spendings'))
	print(os.getcwd())
except:
	pass
#%%
from IPython import get_ipython


#%%
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)


#%%
data=pd.read_pickle('../data/local_data/finaldata.pkl')
sns_count_data=pd.read_pickle('../data/local_data/sns_10totic_count_data').reset_index()[['DATE','topic']]


#%%
len(set(data['DONG_CD']))


#%%
fi_data=data.merge(sns_count_data,right_on='DATE',left_on='STD_DD',how='inner')


#%%
del fi_data['DATE']


#%%
fi_data[:10]


#%%
import matplotlib.pyplot as plt 
import seaborn as sns    
get_ipython().run_line_magic('matplotlib', 'inline')
plt.figure(figsize=(15,15))
sns.heatmap(data = fi_data.set_index(['GU_CD','DONG_CD','STD_DD']).corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap='RdBu')


#%%
del fi_data['SEX_CD'],fi_data['AGE_CD']


#%%

hi_data=fi_data.groupby(['DONG_CD','STD_DD','MCT_CAT_CD']).sum()['AMTperCNT'].unstack(2).fillna(0).groupby(['DONG_CD']).mean()


#%%
scaler=StandardScaler()
scaler.fit(fi_data.set_index(['GU_CD','DONG_CD','STD_DD','MCT_CAT_CD']))
x1=scaler.transform(fi_data.set_index(['GU_CD','DONG_CD','STD_DD','MCT_CAT_CD']))


#%%
x1[:10]


#%%
data_for_corr=pd.DataFrame(x1)
#%%
import matplotlib.pyplot as plt 
import seaborn as sns    
get_ipython().run_line_magic('matplotlib', 'inline')
plt.figure(figsize=(15,15))
sns.heatmap(data = data_for_corr.corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap='RdBu')


#%%
hi_data[:23]





#%%
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt


#%%
merge = linkage(hi_data, method='complete')


#%%
ax = plt.subplot(111)
dendrogram(merge, leaf_font_size=8, orientation='right')
# ax.set_xlim(xmin=0.03)
# ax.set_xscale('log')
plt.show()

#%%
R = dendrogram(
                merge,
                truncate_mode='lastp',  # show only the last p merged clusters
                p=4,  # show only the last p merged clusters
                no_plot=True,
                )


#%%
from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')
cluster.fit_predict(merge)[23]