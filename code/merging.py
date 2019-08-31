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
from matplotlib import cm

#%% [markdown]
# ### 카드 데이터

#%%
path = '../data/local_data/pkls/cardpkl/'

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
carddata['AGE_CD'] = carddata['AGE_CD'].astype('int')
carddata['age'] = np.round(carddata.AGE_CD / 10, 0) * 10

carddata['age'] = carddata['age'].astype('category')
del carddata['AGE_CD']
#%%
a = carddata.groupby(['STD_DD', 'GU_CD', 'DONG_CD', 'MCT_CAT_CD', 'SEX_CD', 'age']).sum()
a = a.fillna(0)
#%%
carddata.iloc[:, -7:].head()

#%% [markdown]
# ### 미세먼지 데이터

#%%
path = '../data/local_data/pkls/dustpkl/'
final_nowon = pd.read_pickle( path + 'nowon_365.pickle')
final_jongro = pd.read_pickle( path + 'jongro_365.pickle')

stations_nowon = list(set(final_jongro.serial.values))
stations_jong = list(set(final_jongro.serial.values))
#%%
path = '../data/local_data/pkls/dustpkl/'
jong_totalmean = pd.read_pickle( path + 'jongro_mean.pickle')
nowon_totalmean = pd.read_pickle( path + 'nowon_mean.pickle')
# finedust_mean = pd.read_pickle( path + 'finedust_mean.pickle')
jong_totalmean['GU_CD'] = '종로구'
nowon_totalmean['GU_CD'] = '노원구'
gu_totalmean = pd.concat([jong_totalmean, nowon_totalmean])
gu_totalmean = gu_totalmean.reset_index()
#%%
# pm10_class
gu_totalmean.loc[gu_totalmean['pm10']< 31.0 , 'pm10_class'] = 0                           # 좋음(0): 0 < pm10 < 30
gu_totalmean.loc[(gu_totalmean['pm10']< 81.0) & (gu_totalmean['pm10'] >= 31.0), 'pm10_class'] = 1    # 보통(1) :31 < pm10 < 80
gu_totalmean.loc[(gu_totalmean['pm10']< 151.0) & (gu_totalmean['pm10']>= 81.0) , 'pm10_class'] = 2   # 나쁨(2): 81 < pm10 < 150
gu_totalmean.loc[gu_totalmean['pm10']>= 151.0 , 'pm10_class'] = 3                         # 매우나쁨(3): pm10 >= 151

# pm25_class
gu_totalmean.loc[gu_totalmean['pm25']< 16.0 , 'pm25_class'] = 0
gu_totalmean.loc[(gu_totalmean['pm25']< 36.0) & (gu_totalmean['pm25'] >= 16.0), 'pm25_class'] = 1
gu_totalmean.loc[(gu_totalmean['pm25']< 76.0) & (gu_totalmean['pm25'] >= 36.0) , 'pm25_class'] = 2
gu_totalmean.loc[gu_totalmean['pm25']>= 76.0 , 'pm25_class'] = 3

#pm_class
gu_totalmean.loc[gu_totalmean['pm10_class']< gu_totalmean['pm25_class'] , 'pm_class'] = gu_totalmean['pm25_class']
gu_totalmean.loc[gu_totalmean['pm10_class']< gu_totalmean['pm25_class'] , 'pm_class_info'] ='pm25'

gu_totalmean.loc[gu_totalmean['pm10_class']>= gu_totalmean['pm25_class'] , 'pm_class'] = gu_totalmean['pm10_class']
gu_totalmean.loc[gu_totalmean['pm10_class']>= gu_totalmean['pm25_class'] , 'pm_class_info'] ='pm10'

#type 변경
gu_totalmean['pm10_class'] = gu_totalmean['pm10_class'].astype('category')
gu_totalmean['pm25_class'] = gu_totalmean['pm25_class'].astype('category')
gu_totalmean['pm_class'] = gu_totalmean['pm_class'].astype('category')


# 위코드는 기상전체최종으로 옮기기
#%%
# 구별 미세먼지 data
a = a.reset_index()
datagudust = a.copy()
datagudust = datagudust.set_index('STD_DD')
gu_totalmean = gu_totalmean.set_index('date')
datagudust.loc[datagudust['GU_CD'] == '노원구', 'pm_class_today'] = gu_totalmean.loc[gu_totalmean['GU_CD']=='종로구']['pm_class']
datagudust.loc[datagudust['GU_CD'] == '종로구', 'pm_class_today'] = gu_totalmean.loc[gu_totalmean['GU_CD']=='노원구']['pm_class']
# 아래코드 추가가 안됨
# datagudust.loc[datagudust['GU_CD'] == '노원구', 'pm_class_yesterday'] = gu_totalmean['pm_class'].shift(1)
# datagudust.loc[datagudust['GU_CD'] == '종로구', 'pm_class_yesterday'] = gu_totalmean['pm_class'].shift(1)

# 동별 미세먼지 data
datadongdust = a.copy()
final_dust = pd.concat([final_jongro, final_nowon])
final_dust.columns = ['DONG_CD', 'serial', 'STD_DD', 'pm10', 'pm10_class', 'pm25', 'pm25_class',
       'pm_class', 'pm_class_info']
datadongdust = pd.merge(left=datadongdust, right=final_dust, how='left', on=['STD_DD','DONG_CD'], sort=False)
# 같은 동끼리만 shift하고 싶은데 어떻게해야하나.. 지금 코드는 왜곡이 있음, 다른 동의 경계, 구의 경계 구분 없음
# datadongdust.loc[datadongdust['GU_CD'] == '노원구', 'pm_class_yesterday'] = datadongdust['pm_class'].shift(1)
# datadongdust.loc[datadongdust['GU_CD'] == '종로구', 'pm_class_yesterday'] = datadongdust['pm_class'].shift(1)
#%%
# datagudust.isnull().sum()
# datadongdust.isnull().sum()
# datadongdust.loc[datadongdust['serial'].isna()]
# 카드data에만 있는 행정동 삭제 (기상데이터가 없는 행정동)
datadongdust = datadongdust.dropna()

#%% [markdown]
# ### 유동인구 데이터

#%%
path = '../data/local_data/pkls/fppkl/'
sex_age_move = pd.read_pickle( path + 'sex_age_move.pkl')
timemove = pd.read_pickle( path + 'Timemove.pkl')


#%%
timemove['time_fp_sum'] = timemove.iloc[:, 2:].sum(axis=1)
timemove['time_fp_mean'] = timemove.iloc[:, 2:].mean(axis=1)
timemove = timemove.reset_index()
timemove['STD_YMD'] = pd.to_datetime(timemove['STD_YMD'], format='%Y%m%d', errors='ignore')
timemove = timemove.set_index('STD_YMD')

#%%
sex_age_move = sex_age_move.set_index('STD_YMD', 'HDONG_NM')
del sex_age_move['STD_YM']
del sex_age_move['HDONG_CD']
#%%
# floating_pop = pd.merge(timemove, sex_age_move, on=['STD_YMD', 'HDONG_NM'])
# sex_age_move.head()
sex_age_move = pd.DataFrame({'sex_age_fp':sex_age_move.reset_index().groupby(['STD_YMD', 'HDONG_NM']).sum().stack()})
sex_age_move = sex_age_move.reset_index()
sex_age_move['STD_YMD'] = pd.to_datetime(sex_age_move['STD_YMD'], format='%Y%m%d', errors='ignore')
sex_age_move = sex_age_move.set_index('STD_YMD')


# ---------------여기부터------------------------
# ---------------여기부터------------------------
# ---------------여기부터------------------------
# ---------------여기부터------------------------
# ---------------여기부터------------------------
#%%
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_00', 'AGE'] = 0
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_10', 'AGE'] = 10
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_20', 'AGE'] = 20
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_30', 'AGE'] = 30
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_40', 'AGE'] = 40
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_50', 'AGE'] = 50
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_60', 'AGE'] = 60
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_70U', 'AGE'] = 70

sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_00', 'AGE'] = 0
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_10', 'AGE'] = 10
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_20', 'AGE'] = 20
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_30', 'AGE'] = 30
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_40', 'AGE'] = 40
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_50', 'AGE'] = 50
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_60', 'AGE'] = 60
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_70U', 'AGE'] = 70

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
donglist = list(set(carddata.DONG_CD.values))
donglist


#%%
for i in donglist:
    carddata.loc[carddata['DONG_CD'] == str(i), 'time_fp_sum'] = timemove.loc[timemove['HDONG_NM']== str(i)]['time_fp_sum']
    carddata.loc[carddata['DONG_CD'] == str(i), 'time_fp_mean'] = timemove.loc[timemove['HDONG_NM']== str(i)]['time_fp_mean']


#%%
# sex_age_fp_sum	sex_age_fp_mean

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
# for row in temp.itertuples():
    


#%%
# for i in temp.STD_DD.values:
#     for z in temp.DONG_CD.values:
#         temp.loc[(temp.STD_DD == i) & (temp.DONG_CD == z), 'yt_total_amt'] = total_rp.loc[(total_rp.ADMD_NM == i) & (total_rp.date == z), 'Total Cost']


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



