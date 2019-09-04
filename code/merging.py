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
import seaborn as sns    
%matplotlib inline  
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

#%% [markdown]
# ### 카드 데이터

#%%
path = '../data/local_data/pkls/cardpkl/'

groupeddata = pd.read_pickle( path + 'groupeddata.pkl').reset_index()
dailyjong = pd.read_pickle( path + 'dailyjong.pkl').reset_index()
dailynowon = pd.read_pickle( path + 'dailynowon.pkl').reset_index()
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
del carddata['AMTperCNT']
#%%
a = carddata.groupby(['STD_DD', 'GU_CD', 'DONG_CD', 'age','MCT_CAT_CD',]).sum()
a = a.fillna(0)
#%%
a['AMTperCNT'] = a['USE_AMT'] / a['USE_CNT'] 
del a['USE_CNT']
a = a.unstack(-1).unstack(-1)

#%% [markdown]
# ### 미세먼지 데이터

#%%
path = '../data/local_data/pkls/dustpkl/'
# final_nowon = pd.read_pickle( path + 'nowon_365.pickle')
# final_jongro = pd.read_pickle( path + 'jongro_365.pickle')
gu_total = pd.read_pickle( path + 'gutotal_365.pickle')
# stations_nowon = list(set(final_jongro.serial.values))
# stations_jong = list(set(final_jongro.serial.values))
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
# a = a.reset_index()
datagudust = a.copy()
# datagudust = datagudust.set_index('STD_DD')
gu_totalmean = gu_totalmean.set_index('date')
datagudust = pd.merge(left=datagudust, right=gu_totalmean.reset_index(), how='left', left_on=['STD_DD','GU_CD'], right_on=['date', 'GU_CD'], sort=False)
del datagudust['date']
# 아래코드 추가가 안됨
# datagudust.loc[datagudust['GU_CD'] == '노원구', 'pm_class_yesterday'] = gu_totaoday'] = gu_totalmean.loc[gu_totalmean['GU_CD']=='노원구']['pm_cllmean['pm_class'].shift(1)
# datagudust.loc[datagudust['GU_CD'] == '종로구', 'pm_class_yesterday'] = gu_totalmean['pm_class'].shift(1)
#%%
# 동별 미세먼지 data
datadongdust = a.copy()
# final_dust = pd.concat([final_jongro, final_nowon])
gu_total.columns = ['DONG_CD', 'STD_DD', 'pm10', 'pm25', 'msg', 'pm10_class', 'pm25_class',
       'pm_class', 'pm_class_info', 'msg_yes']
datadongdust = pd.merge(left=datadongdust, right=gu_total, how='left', on=['STD_DD','DONG_CD'], sort=False)
# 같은 동끼리만 shift하고 싶은데 어떻게해야하나.. 지금 코 드는 왜곡이 있음, 다른 동의 경계, 구의 경계 구분없음
# 기상데이터에서 해줫음..
# datadongdust.loc[datadongdust['GU_CD'] == '노원구', 'pm_class_yesterday'] = datadongdust['pm_class'].shift(1)
# datadongdust.loc[datadongdust['GU_CD'] == '종로구', 'pm_class_yesterday'] = datadongdust['pm_class'].shift(1)
# 카드data에만 있는 행정동 삭제 (기상데이터가 없는 행정동)
datadongdust = datadongdust.dropna()

#%% [markdown]
# ### 유동인구 데이터
#%%
path = '../data/local_data/pkls/fppkl/'
timemove = pd.read_pickle( path + 'Timemove.pkl')

timemove['time_fp_sum'] = timemove.iloc[:, 2:].sum(axis=1)
timemove['time_fp_mean'] = timemove.iloc[:, 2:].mean(axis=1)

timemove['STD_YMD'] = pd.to_datetime(timemove['STD_YMD'], format='%Y%m%d', errors='ignore')
timemove = timemove.set_index('STD_YMD')

#%%
path = '../data/local_data/pkls/fppkl/'
sex_age_move = pd.read_pickle( path + 'sex_age_move.pkl')
del sex_age_move['STD_YM']
del sex_age_move['HDONG_CD']
sex_age_move['STD_YMD'] = pd.to_datetime(sex_age_move['STD_YMD'], format='%Y%m%d', errors='ignore')
#%%
sex_age_move = pd.DataFrame({'sex_age_fp':sex_age_move.groupby(['STD_YMD', 'HDONG_NM']).sum().stack()})
sex_age_move = sex_age_move.reset_index()
sex_age_move['sex'] = np.nan

#%%
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_00', 'AGE'] = 0
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_10', 'AGE'] = 10
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_20', 'AGE'] = 20
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_30', 'AGE'] = 30
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_40', 'AGE'] = 40
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_50', 'AGE'] = 50
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_60', 'AGE'] = 60
sex_age_move.loc[sex_age_move.level_2 == 'MAN_FLOW_POP_CNT_70U', 'AGE'] = 70

man = ['MAN_FLOW_POP_CNT_00',
 'MAN_FLOW_POP_CNT_10',
 'MAN_FLOW_POP_CNT_20',
 'MAN_FLOW_POP_CNT_30',
 'MAN_FLOW_POP_CNT_40',
 'MAN_FLOW_POP_CNT_50',
 'MAN_FLOW_POP_CNT_60',
 'MAN_FLOW_POP_CNT_70U']
sex_age_move['sex'].loc[sex_age_move['level_2'].isin(man)] = 'M'
    

sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_00', 'AGE'] = 0
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_10', 'AGE'] = 10
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_20', 'AGE'] = 20
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_30', 'AGE'] = 30
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_40', 'AGE'] = 40
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_50', 'AGE'] = 50
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_60', 'AGE'] = 60
sex_age_move.loc[sex_age_move.level_2 == 'WMAN_FLOW_POP_CNT_70U', 'AGE'] = 70
wman = ['WMAN_FLOW_POP_CNT_00',
 'WMAN_FLOW_POP_CNT_10',
 'WMAN_FLOW_POP_CNT_20',
 'WMAN_FLOW_POP_CNT_30',
 'WMAN_FLOW_POP_CNT_40',
 'WMAN_FLOW_POP_CNT_50',
 'WMAN_FLOW_POP_CNT_60',
 'WMAN_FLOW_POP_CNT_70U']
sex_age_move['sex'].loc[sex_age_move['level_2'].isin(wman)] = 'W'

sex_age_move = sex_age_move.dropna()
del sex_age_move['level_2']

#%%
path = '../data/local_data/pkls/fppkl/'
sex_age_move.to_pickle(path + 'SAfp')
timemove.to_pickle(path + 'tmfp')
#%%
datadongdustmove = datadongdust.merge(timemove,how='inner',left_on=['DONG_CD','STD_DD'],right_on=['HDONG_NM','STD_YMD'])
del datadongdustmove['HDONG_NM']
# result_move = result_move.rename(columns = {'SUM': 'MOVE','S-W':'MOVE-WORKER'})
#%%
# sex, age 빠져서 merge가 안됨 - 수정예정
# datadongdustmove = datadongdustmove.merge(sex_age_move,how='inner',left_on=['DONG_CD','STD_DD', 'SEX_CD', 'age'],right_on=['HDONG_NM','STD_YMD', 'sex', 'AGE'])
# del datadongdustmove['STD_YMD']
# del datadongdustmove['HDONG_NM']
# del datadongdustmove['sex']
# del datadongdustmove['AGE']

#%%
datadongdustmove.msg = datadongdustmove.msg.astype('float32')
datadongdustmove.msg_yes = datadongdustmove.msg_yes.astype('float32')
datadongdustmove.pm10_class = datadongdustmove.pm10_class.astype('float32')
datadongdustmove.pm25_class = datadongdustmove.pm25_class.astype('float32')
datadongdustmove.pm_class = datadongdustmove.pm_class.astype('float32')
datadongdustmove.pm_class_info = datadongdustmove.pm_class_info.astype('object')
# sex_age_fp_sum	sex_age_fp_mean
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
del datadongdustmove['TMST_05']
del datadongdustmove['TMST_06']
del datadongdustmove['TMST_07']
del datadongdustmove['TMST_08']
del datadongdustmove['TMST_09']
del datadongdustmove['TMST_10']
del datadongdustmove['TMST_11']
del datadongdustmove['TMST_12']
del datadongdustmove['TMST_13']
del datadongdustmove['TMST_14']
del datadongdustmove['TMST_15']
del datadongdustmove['TMST_16']
del datadongdustmove['TMST_17']
del datadongdustmove['TMST_18']
del datadongdustmove['TMST_19']
del datadongdustmove['TMST_20']
del datadongdustmove['TMST_21']
del datadongdustmove['TMST_22']
del datadongdustmove['TMST_23']
#%%

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


#%% [markdown]
# ### 유통데이터

#%%
path = '../data/local_data/pkls/'
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
# # 카드소비매출에 없는 항목 지우기
# yutong_ = yutong.copy()
# yutong_ = yutong_.reset_index()
# deleteCATE = ['임신/육아', '홈&리빙']
# for i in deleteCATE:
#     yutong_ = yutong_[yutong_.ANTC_ITEM_LCLS_NM != i]
#     yutong_['MCT_CAT_CD'] = np.nan
# yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '간식', ['MCT_CAT_CD']] = '음료식품'
# yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '마실거리', ['MCT_CAT_CD']] = '음료식품'
# yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '식사', ['MCT_CAT_CD']] = '음료식품'

# yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '사회활동', ['MCT_CAT_CD']] = '서적문구'

# yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '취미&여가활동', ['MCT_CAT_CD']] = '레저용품'

# yutong_.loc[yutong_['ANTC_ITEM_LCLS_NM'] == '헬스&뷰티', ['MCT_CAT_CD']] = '보건위생'
# yutong_ = yutong_.set_index('date')
# catlist = ['음료식품', '서적문구', '레저용품', '보건위생']
# yt_temp = pd.DataFrame()
# yutong_ = yutong_.reset_index()
# yt_temp['STD_DD'] = yutong_.date
# yt_temp['DONG_CD'] = yutong_.ADMD_NM
# yt_temp['MCT_CAT_CD'] = yutong_.MCT_CAT_CD
# yt_temp['yt_total_amt'] = yutong_.Total_Cost
# yt_temp['yt_cat_amt'] = yutong_.Cat_Cost
# yt_temp.head()
#%% [markdown]
# https://stackoverflow.com/questions/36909977/update-row-values-where-certain-condition-is-met-in-pandas


#%%
yutong = yutong.reset_index()
yutong.columns = ['date', 'ADMD_NM', 'MCT_CAT_CD', 'percentage', 'Total_Cost', 'Cat_Cost']

#%%
# 유통 항목앞에 유통이란 str 추가해서 카드소비 항목과 혼동 없도록 함
yutong['MCT_CAT_CD'] = '유통 ' + yutong['MCT_CAT_CD']
#%%
yutong_ = yutong.groupby(['ADMD_NM', 'date', 'MCT_CAT_CD']).mean().unstack(2)
yutong_ = yutong_.reset_index()
datadongdustmovert = datadongdustmove.merge(yutong_, how='inner',left_on=['DONG_CD','STD_DD'],right_on=['ADMD_NM','date'])





#%%
# datadongdustmovert.to_pickle(path + 'dongCardDustFpRtMergedUnstacked')
#%%
# final data 형식
path = '../data/local_data/pkls/'
datadongdustmovert = pd.read_pickle(path + 'dongCardDustFpRtMergedUnstacked')
#%%
# 평일
plt.figure(figsize=(50,50))
sns.heatmap(data = datadongdustmovert[~datadongdustmovert.STD_DD.isin(holiday_df)].corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap=sns.diverging_palette(20, 220, n=200),square=True)
#%%
# 휴일
plt.figure(figsize=(15,15))
sns.heatmap(data = datadongdustmovert[datadongdustmovert.STD_DD.isin(holiday_df)].corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap=sns.diverging_palette(20, 220, n=200),square=True)
#%%
# 전체
plt.figure(figsize=(15,15))
sns.heatmap(data = datadongdustmovert.corr(method = 'pearson'), annot=True, 
fmt = '.2f', linewidths=.5, cmap=sns.diverging_palette(20, 220, n=200),square=True)



#%%
