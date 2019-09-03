# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'code'))
	print(os.getcwd())
except:
	pass

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns    
%matplotlib inline  
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
#%%
#카드매출 불러오기
card_tem1=pd.read_pickle('../data/local_data/pkls/cardpkl/dailyjong.pkl')
card_tem2=pd.read_pickle('../data/local_data/pkls/cardpkl/dailynowon.pkl')
card_data=pd.concat([card_tem1,card_tem2],axis=0)

#%%
#유통이랑 카드매출 비교하기
#1번째 양으로 상관계수 구하기->cor찍어 봤지만 의미 없었다 
#but 카드매출 안에서의 상관관계는 보였다
cor_AMT=card_data.groupby(['DONG_CD','STD_DD','MCT_CAT_CD'])['USE_AMT'].sum().unstack(2).fillna(0)

#2번째 건수으로 상관계수 구하기
cor_CNT=card_data.groupby(['DONG_CD','STD_DD','MCT_CAT_CD'])['USE_CNT'].sum().unstack(2).fillna(0)

#3번째 양/건수으로 상관계수 구하기->상관관계가 가장 낮게나옴
cor_AMTperCNT=card_data.groupby(['DONG_CD','STD_DD','MCT_CAT_CD'])['AMTperCNT'].sum().unstack(2).fillna(0)
#%%
#유통 불러오기
suply_data=pd.read_pickle('../data/local_data/cat_cost.pickle')
suply_data.date=pd.to_datetime(suply_data.date,format='%Y%m%d')
#%%
cor_sup=suply_data.set_index(['ADMD_NM','date','ANTC_ITEM_LCLS_NM'])['cat_cost'].unstack(2)
#%% 양으로 상관계수 구하기--가장의미있다
cor_result=cor_sup.reset_index().merge(cor_AMT.reset_index(),how='inner',left_on=['ADMD_NM','date'],right_on=['DONG_CD','STD_DD'])
cor_result=cor_result.set_index(['ADMD_NM','date'])
del cor_result['DONG_CD'],cor_result['STD_DD']

plt.figure(figsize=(15,15))
sns.heatmap(data = cor_result.corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap='RdBu')
#%% 건수으로 상관계수 구하기
# cor_result=cor_sup.reset_index().merge(cor_CNT.reset_index(),how='inner',left_on=['ADMD_NM','date'],right_on=['DONG_CD','STD_DD'])
# cor_result=cor_result.set_index(['ADMD_NM','date'])

# plt.figure(figsize=(15,15))
# sns.heatmap(data = cor_result.corr(method = 'pearson'), annot=True, 
# fmt = '.2f', linewidths=.5, cmap='RdBu')
#%% 양/건수으로 상관계수 구하기
# cor_result=cor_sup.reset_index().merge(cor_AMTperCNT.reset_index(),how='inner',left_on=['ADMD_NM','date'],right_on=['DONG_CD','STD_DD'])
# cor_result=cor_result.set_index(['ADMD_NM','date'])

# plt.figure(figsize=(15,15))
# sns.heatmap(data = cor_result.corr(method = 'pearson'), annot=True, 
# fmt = '.2f', linewidths=.5, cmap='RdBu')
#%%
cor_result[:10]

#%%
#미세먼지 불러오기 같은 동에 다른 측정기는 평균으로 대체했음
dust_jongro=pd.read_pickle('../data/local_data/pkls/dustpkl/jongro_365.pickle')
dust_nowon=pd.read_pickle('../data/local_data/pkls/dustpkl/nowon_365.pickle')
dust_data=pd.concat([dust_jongro,dust_nowon],axis=0)

#%%

dust_data_mean=dust_data.groupby(['행정동','date']).mean()
dust_data_mean.pm_class=dust_data_mean.pm_class.round()
dust_data_mean.pm10_class=dust_data_mean.pm10_class.round()
dust_data_mean.pm25_class=dust_data_mean.pm25_class.round()


#%%
result_dust=cor_result.reset_index().merge(dust_data_mean.reset_index(),how='inner',left_on=['ADMD_NM','date'],right_on=['행정동','date'])
del result_dust['행정동']
#%%
result_dust
#%%
#유동인구 불러오기
move_data=pd.read_pickle('../data/local_data/pkls/movedata_worker')[['STD_YMD','HDONG_NM','SUM','WORKER','S-W']]
move_data.STD_YMD=pd.to_datetime(move_data.STD_YMD,format='%Y%m%d')

#%%
result_move=result_dust.merge(move_data,how='inner',left_on=['ADMD_NM','date'],right_on=['HDONG_NM','STD_YMD'])
del result_move['STD_YMD']
del result_move['HDONG_NM']
result_move = result_move.rename(columns = {'SUM': 'MOVE','S-W':'MOVE-WORKER'})

#%%
# result_move.to_pickle('final.pickle')

#%%
