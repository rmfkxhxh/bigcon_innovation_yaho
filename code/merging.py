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
import pandas as pd
import numpy as np

#%% [markdown]
# ### 카드 데이터

#%%
path = '../../data/local_data/pkls/cardpkl/'

groupeddata = pd.read_pickle( path + 'groupeddata.pkl').reset_index()
dailyjong = pd.read_pickle( path + 'dailyjong.pkl').reset_index()
dailynowon = pd.read_pickle( path + 'dailyjong.pkl').reset_index()
groupeddata.tail()


#%%
set(groupeddata.reset_index().MCT_CAT_CD.values)


#%%
cols = groupeddata.columns
cols = ['STD_DD', 'GU_CD', 'DONG_CD', 'SEX_CD', 'AGE_CD', 'MCT_CAT_CD',
       'USE_CNT', 'USE_AMT', 'AMTperCNT']
carddata = groupeddata[cols]
carddata['AGE_CD'] = data['AGE_CD'].astype('category')
carddata.tail()


#%%
carddata.iloc[:, -7:].head()

#%% [markdown]
# ### 미세먼지 데이터

#%%
path = '../../data/local_data/pkls/dustpkl/'
final_nowon = pd.read_pickle( path + 'nowon_365.pickle')
final_jongro = pd.read_pickle( path + 'jongro_365.pickle')
final_nowon['pm10_class'] = final_nowon['pm10_class']/2
final_jongro['pm10_class'] = final_jongro['pm10_class']/2


stations_nowon = list(set(final_jongro.serial.values))
stations_jong = list(set(final_jongro.serial.values))
#%%
jong_totalmean = pd.read_pickle( path + 'jongro_mean.pickle')
nowon_totalmean = pd.read_pickle( path + 'nowon_mean.pickle')
# pm10_class
jong_totalmean.loc[jong_totalmean['pm10']< 31.0 , 'pm10_class'] = 0                           # 좋음(0): 0 < pm10 < 30
jong_totalmean.loc[(jong_totalmean['pm10']< 81.0) & (jong_totalmean['pm10'] >= 31.0), 'pm10_class'] = 1    # 보통(1) :31 < pm10 < 80
jong_totalmean.loc[(jong_totalmean['pm10']< 151.0) & (jong_totalmean['pm10']>= 81.0) , 'pm10_class'] = 2   # 나쁨(2): 81 < pm10 < 150
jong_totalmean.loc[jong_totalmean['pm10']>= 151.0 , 'pm10_class'] = 3                         # 매우나쁨(3): pm10 >= 151

# pm25_class
jong_totalmean.loc[jong_totalmean['pm25']< 16.0 , 'pm25_class'] = 0
jong_totalmean.loc[(jong_totalmean['pm25']< 36.0) & (jong_totalmean['pm25'] >= 16.0), 'pm25_class'] = 1
jong_totalmean.loc[(jong_totalmean['pm25']< 76.0) & (jong_totalmean['pm25'] >= 36.0) , 'pm25_class'] = 2
jong_totalmean.loc[jong_totalmean['pm25']>= 76.0 , 'pm25_class'] = 3

# pm10_class
nowon_totalmean.loc[nowon_totalmean['pm10']< 31.0 , 'pm10_class'] = 0                           # 좋음(0): 0 < pm10 < 30
nowon_totalmean.loc[(nowon_totalmean['pm10']< 81.0) & (nowon_totalmean['pm10'] >= 31.0), 'pm10_class'] = 1    # 보통(1) :31 < pm10 < 80
nowon_totalmean.loc[(nowon_totalmean['pm10']< 151.0) & (nowon_totalmean['pm10']>= 81.0) , 'pm10_class'] = 2   # 나쁨(2): 81 < pm10 < 150
nowon_totalmean.loc[nowon_totalmean['pm10']>= 151.0 , 'pm10_class'] = 3                         # 매우나쁨(3): pm10 >= 151

# pm25_class
nowon_totalmean.loc[nowon_totalmean['pm25']< 16.0 , 'pm25_class'] = 0
nowon_totalmean.loc[(nowon_totalmean['pm25']< 36.0) & (nowon_totalmean['pm25'] >= 16.0), 'pm25_class'] = 1
nowon_totalmean.loc[(nowon_totalmean['pm25']< 76.0) & (nowon_totalmean['pm25'] >= 36.0) , 'pm25_class'] = 2
nowon_totalmean.loc[nowon_totalmean['pm25']>= 76.0 , 'pm25_class'] = 3

# pm_class(pm10과 pm25중 더 안좋은 것)
jong_totalmean.loc[nowon_totalmean['pm10_class']< jong_totalmean['pm25_class'] , 'pm_class'] = jong_totalmean['pm25_class']
jong_totalmean.loc[nowon_totalmean['pm10_class']>= jong_totalmean['pm25_class'] , 'pm_class'] = jong_totalmean['pm10_class']

# pm_class_info
jong_totalmean.loc[jong_totalmean['pm10_class']< jong_totalmean['pm25_class'] , 'pm_class_info'] ='pm25'
jong_totalmean.loc[jong_totalmean['pm10_class']>= jong_totalmean['pm25_class'] , 'pm_class_info'] ='pm10'

#
jong_totalmean['pm10_class'] = jong_totalmean['pm10_class'].astype('int')
jong_totalmean['pm25_class'] = jong_totalmean['pm25_class'].astype('int')
jong_totalmean['pm_class'] = jong_totalmean['pm_class'].astype('int')


# pm_class(pm10과 pm25중 더 안좋은 것)
nowon_totalmean.loc[nowon_totalmean['pm10_class']< nowon_totalmean['pm25_class'] , 'pm_class'] = nowon_totalmean['pm25_class']
nowon_totalmean.loc[nowon_totalmean['pm10_class']>= nowon_totalmean['pm25_class'] , 'pm_class'] = nowon_totalmean['pm10_class']

# pm_class_info
nowon_totalmean.loc[nowon_totalmean['pm10_class']< nowon_totalmean['pm25_class'] , 'pm_class_info'] ='pm25'
nowon_totalmean.loc[nowon_totalmean['pm10_class']>= nowon_totalmean['pm25_class'] , 'pm_class_info'] ='pm10'

#
nowon_totalmean['pm10_class'] = nowon_totalmean['pm10_class'].astype('int')
nowon_totalmean['pm25_class'] = nowon_totalmean['pm25_class'].astype('int')
nowon_totalmean['pm_class'] = nowon_totalmean['pm_class'].astype('int')

# 위코드는 기상전체최종으로 옮기기
#%%
datagudust = carddata.copy()
datagudust = datagudust.set_index('STD_DD')
datagudust.loc[data['GU_CD'] == '노원구', 'pm_class_today'] = nowon_totalmean['pm_class']
datagudust.loc[data['GU_CD'] == '종로구', 'pm_class_today'] = jong_totalmean['pm_class']
datagudust.loc[data['GU_CD'] == '노원구', 'pm_class_yesterday'] = nowon_totalmean['pm_class'].shift(1)
datagudust.loc[data['GU_CD'] == '종로구', 'pm_class_yesterday'] = jong_totalmean['pm_class']
# data
datadongdust = carddata.copy()
final_dust = pd.concat([final_jongro, final_nowon])
final_dust.columns = ['DONG_CD', 'serial', 'STD_DD', 'pm10', 'pm10_class', 'pm25', 'pm25_class',
       'pm_class', 'pm_class_info']
datadongdust = pd.merge(left=datadongdust, right=final_dust, how='left', on=['STD_DD','DONG_CD'], sort=False)
#%%
index = datadongdust['serial'].index[datadongdust['serial'].apply(np.isnan)]
datadongdust['DONG_CD'].ix[index[0]]
#%% [markdown]
# ### 유동인구 데이터

#%%
path = '../../data/local_data/pkls/fppkl'
sex_age_move = pd.read_pickle( path + 'sex_age_move.pkl')
timemove = pd.read_pickle( path + 'Timemove.pkl')


#%%
timemove['time_fp_sum'] = timemove.iloc[:, 2:].sum(axis=1)
timemove['time_fp_mean'] = timemove.iloc[:, 2:].mean(axis=1)


#%%
timemove = timemove.set_index('STD_YMD', 'HDONG_NM')
sex_age_move = sex_age_move.set_index('STD_YMD', 'HDONG_NM')
del sex_age_move['STD_YM']
del sex_age_move['HDONG_CD']
sex_age_move.head()


#%%
floating_pop = pd.merge(timemove, sex_age_move, on=['STD_YMD', 'HDONG_NM'])


#%%
floating_pop = floating_pop.reset_index()
floating_pop['STD_YMD'] = pd.to_datetime(floating_pop['STD_YMD'], format='%Y%m%d', errors='ignore')
floating_pop = floating_pop.set_index('STD_YMD')


#%%
temp_w = floating_pop.iloc[:,-10:-2]
temp_m = floating_pop.iloc[:,-18:-10]
floating_pop


#%%
temp_m = temp_m.reset_index()
temp_w = temp_w.reset_index()


#%%
temp_m = temp_m.set_index('STD_YMD')


#%%
temp_m['male_sum'] = temp_m.sum(axis=1)
temp_m['male_mean'] = temp_m.mean(axis=1)
temp_w['female_sum'] = temp_w.sum(axis=1)
temp_w['female_mean'] = temp_w.mean(axis=1)


#%%
temp_w


#%%
donglist = list(set(data.DONG_CD.values))
donglist


#%%
for i in donglist:
    data.loc[data['DONG_CD'] == str(i), 'time_fp_sum'] = floating_pop.loc[floating_pop['HDONG_NM']== str(i)]['time_fp_sum']
    data.loc[data['DONG_CD'] == str(i), 'time_fp_mean'] = floating_pop.loc[floating_pop['HDONG_NM']== str(i)]['time_fp_mean']


#%%
sex_age_fp_sum	sex_age_fp_mean

#%% [markdown]
# for i in donglist:
#     if data.SEX_CD = 'F':
#          data.loc[data['DONG_CD'] == str(i), 'sex_age_fp_sum'] = floating_pop.loc[floating_pop['HDONG_NM']== str(i)]['time_fp_sum']

#%%
# del data['time_fp_sum']
# del data['time_fp_mean']
# del data['sex_age_fp_sum']
# del data['sex_age_fp_mean']
data.groupby(['GU_CD', 'DONG_CD', 'STD_DD','time_fp_sum', 'time_fp_mean' ,'MCT_CAT_CD','pm_class_today','pm_class_yesterday']).sum()['USE_CNT'].unstack()


#%%
import matplotlib.pyplot as plt


#%%
from matplotlib import cm
color = cm.inferno_r(np.linspace(.4,.8, 30))
# 그래프에서 한글 사용 세팅
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7
plt.rcParams['lines.antialiased'] = True


#%%
data


#%%
# plot data
fig, ax = plt.subplots(figsize=(15,7))
# use unstack()
data.groupby(['GU_CD', 'DONG_CD', 'STD_DD','time_fp_sum', 'time_fp_mean' ,'MCT_CAT_CD','pm_class_today','pm_class_yesterday']).sum()['USE_CNT'].unstack(-6).plot(ax=ax)


#%%



#%%
# data.loc[data['DONG_CD'] == '청운효자동', 'time_fp_sum'] = floating_pop.loc[floating_pop['HDONG_NM']=='청운효자동']['time_fp_sum']


#%%
data.GU_CD.values


#%%
data.to_pickle(path + 'card_dust_yudong.pkl')

#%% [markdown]
# load data.pkl

#%%
path = '../../data/local_data/pkls/'
data = pd.read_pickle(path + 'card_dust_yudong.pkl')

#%% [markdown]
# ### 유통데이터

#%%
path = '../../data/local_data/pkls/'
yutong = pd.read_pickle( path + 'cat_cost.pickle')


#%%
yutong['date'] = pd.to_datetime(yutong['date'], format='%Y%m%d', errors='ignore')
yutong = yutong.set_index('date')

#%% [markdown]
# 카드 소비 카테고리와 유통매출 카테고리을 통일시켜야함
#%% [markdown]
# 없는 항목: 임신/육아, 홈&리빙  
# 
# 음료식품: 마실거리, 간식, 식사  
# 서적문구: 사회활동  
# 가전, 레저용품 : 취미&여가활동  
# 보건위생 : 헬스&뷰티
# 

#%%
yutong_ = yutong.copy()
yutong_ = yutong_.reset_index()
deleteCATE = ['임신/육아', '홈&리빙']
for i in deleteCATE:
    yutong_ = yutong_[yutong_.ANTC_ITEM_LCLS_NM != i]
    yutong_['MCT_CAT_CD'] = np.nan

#%% [markdown]
# https://stackoverflow.com/questions/36909977/update-row-values-where-certain-condition-is-met-in-pandas

#%%
yutong_.head()


#%%
yutong_.columns = ['ADMD_NM', 'percentage', 'Total_Cost', 'Cat_Cost', 'MCT_CAT_CD']


#%%
yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '간식', ['MCT_CAT_CD']] = '음료식품'
yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '마실거리', ['MCT_CAT_CD']] = '음료식품'
yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '식사', ['MCT_CAT_CD']] = '음료식품'

yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '사회활동', ['MCT_CAT_CD']] = '서적문구'

yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '취미&여가활동', ['MCT_CAT_CD']] = '레저용품'

yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '헬스&뷰티', ['MCT_CAT_CD']] = '보건위생'
yutong_ = yutong_.set_index('date')
yutong_.head()


#%%
del yutong_['ANTC_ITEM_LCLS_NM']


#%%
catlist = ['음료식품', '서적문구', '레저용품', '보건위생']


#%%
yt_temp = pd.DataFrame()
yutong_ = yutong_.reset_index()
yt_temp['STD_DD'] = yutong_.date
yt_temp['DONG_CD'] = yutong_.ADMD_NM
yt_temp['MCT_CAT_CD'] = yutong_.MCT_CAT_CD
yt_temp['yt_total_amt'] = yutong_.Total_Cost
yt_temp['yt_cat_amt'] = yutong_.Cat_Cost
yt_temp.head()


#%%
temp = yt_temp.groupby(['STD_DD','DONG_CD', 'MCT_CAT_CD']).sum()


#%%
temp.new = yt_temp.groupby(['STD_DD','DONG_CD', 'MCT_CAT_CD'])['yt_cat_amt'].sum()


#%%
total_rp = pd.read_pickle(path + '유통RP')
total_rp.reset_index()


#%%
total_rp = total_rp.reset_index()


#%%
total_rp


#%%
temp = temp.reset_index()


#%%
temp.groupby
total_rp.groupby


#%%
for row in temp.itertuples():
    


#%%
for i in temp.STD_DD.values:
    for z in temp.DONG_CD.values:
        temp.loc[(temp.STD_DD == i) & (temp.DONG_CD == z), 'yt_total_amt'] = total_rp.loc[(total_rp.ADMD_NM == i) & (total_rp.date == z), 'Total Cost']


#%%
total_rp.loc[total_rp.date['가회동']]


#%%
yt_temp.to_csv(path + 'yt_temp.csv')


#%%
yt_temp = yt_temp.set_index('index')
data = data.set_index('index')


#%%



#%%
row1idx = []
row2idx = []
for row1 in data.itertuples():
    for row2 in yt_temp.itertuples():
        if row1.DONG_CD == '하계2동' and row2.DONG_CD == '하계2동':
            if row1.MCT_CAT_CD == '음료식품' and row2.MCT_CAT_CD == '음료식품':
                row1idx.append(row1.Index)
                row2idx.append(row2.Index)
#                 data.iloc[row1.Index].yt_total_amt = row2.yt_total_amt
#                 data.iloc[row1.Index].yt_cat_amt = row2.yt_cat_amt
#         else:
#             data['yt_total_amt'] = np.nan
#             data['yt_cat_amt'] = np.nan


#%%
for row1 in data.itertuples():
    for row2 in yt_temp.itertuples():
        for i in donglist:
            for z in catlist:
                if row1.DONG_CD == str(i) and row2.DONG_CD == str(i):
                    if row1.MCT_CAT_CD == str(z) and row2.MCT_CAT_CD == str(z):
                        data.iloc[row1.Index].yt_total_amt = row2.yt_total_amt
                        data.iloc[row1.Index].yt_cat_amt = row2.yt_cat_amt
#         else:
#             data['yt_total_amt'] = np.nan
#             data['yt_cat_amt'] = np.nan


#%%
data.loc[data['DONG_CD'] == '하계2동']


#%%
data.isna().sum()

#%% [markdown]
# for i in donglist:
#     for z in catlist:
#         if data.DONG_CD == str(i) and yt_temp.DONG_CD == str(i):
#             if data.MCT_CAT_CD == str(z) and yt_temp.MCT_CAT_CD == str(z):
#                 data['yt_total_amt'] = yt_temp.yt_total_amt
#                 data['yt_cat_amt'] = yt_temp.yt_cat_amt

#%%
yt_temp = yt_temp.sort_index(axis=1)

if yt_temp['STD_DD'] == data['STD_DD'] and yt_temp['DONG_CD'] == data['DONG_CD'] and yt_temp['MCT_CAT_CD'] == data['MCT_CAT_CD']:
    data['yt_total_amt'] = yt_temp.yt_total_amt
    data['yt_cat_amt'] = yt_temp.yt_cat_amt


#%%
def preprocess(x):
    df = pd.merge(data, x, on=['STD_DD','DONG_CD', 'MCT_CAT_CD'], how='left')
    df.to_csv("final.csv", mode="a", header=False, index=False)

reader = pd.read_csv(path + "yt_temp.csv", chunksize=1000)

for r in reader:
    preprocess(r) 

#%% [markdown]
# 

#%%
yt_temp


#%%



#%%
data.to_pickle(path + 'finaldata.pkl')


#%%
path = '../../data/local_data/pkls/'
data = pd.read_pickle(path + 'finaldata.pkl')


#%%
data.head()


#%%



