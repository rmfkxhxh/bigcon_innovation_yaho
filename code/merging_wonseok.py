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
holiday2=['20180401','20180407','20180408','20180414','20180415','20180421','20180422','20180428','20180429','20180505',
          '20180506','20180512','20180513','20180519','20180520','20180521','20180522','20180526','20180527','20180602',
          '20180603','20180606','20180609','20180610','20180616','20180617','20180623','20180624','20180630','20180701',
          '20180707','20180708','20180714','20180715','20180721','20180722','20180728','20180729','20180804','20180805',
          '20180811','20180812','20180815','20180818','20180819','20180825','20180826','20180901','20180902','20180908',
          '20180909','20180915','20180916','20180922','20180923','20180924','20180925','20180926','20180927','20180928',
          '20180929','20180930','20181003','20181006','20181007','20181009','20181013','20181014','20181020','20181021',
          '20181027','20181028','20181103','20181104','20181110','20181111','20181117','20181118','20181124','20181125',
          '20181201','20181202','20181208','20181209','20181215','20181216','20181222','20181223','20181224','20181225',
          '20181229','20181230','20181231','20190101','20190105','20190106','20190112','20190113','20190119','20190120',
          '20190126','20190127','20190202','20190203','20190204','20190205','20190206','20190207','20190208','20190209',
          '20190210','20190216','20190217','20190223','20190224','20190301','20190302','20190303','20190309','20190310',
          '20190316','20190317','20190323','20190324','20190330','20190331']
holiday_df=pd.to_datetime(pd.Series(holiday2))
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
 
 
plt.figure(figsize=(15,15))
sns.heatmap(data = result_move[result_move.date.isin(holiday_df)].corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap='RdBu')

#%%
plt.figure(figsize=(15,15))
sns.heatmap(data = result_move[~result_move.date.isin(holiday_df)].corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap=sns.diverging_palette(20, 220, n=200),square=True)


#%%
result_move[:10]

#%%


#%%


#%%
