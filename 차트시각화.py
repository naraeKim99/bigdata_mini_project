import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 한글 및 그래프 크기 설정
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family']='Malgun Gothic'
plt.rcParams['figure.figsize'] = (12,5)


# 실업자 데이터
unempl=pd.read_csv('./data/실업자.csv').iloc[:,2:]
unempl=unempl.transpose().iloc[:,0]   # 행열을 바꿔준다
unempl.index=pd.to_datetime(unempl.index)   # 시계열 그래프를 그리기 위해 일자 행의 데이터를 datetime 형식으로 바꿔준다.
unempl= unempl.replace(',', '',regex=True)  # 모든 숫자들이 문자열로 되어있어 숫자로 변환하기 위해 문자 ','를 제거한다.
unempl=pd.to_numeric(unempl)   # 숫자로만 이루어진 문자열을 numeric으로 바꿔준다.
unempl=pd.DataFrame(unempl)    # 열이 하나인 series타입의 데이터를 편의를 위해 data frame형태로 변환한다.
unempl.columns=['계']   # 컬럼 명을 지정한다
# print(unempl.info())
# print(unempl.head())


# 취업자수 데이터
empl=pd.read_csv('./data/취업자수.csv')
empl=empl.set_index('업종별')   # 인덱스에 
empl=empl.transpose()
empl.index=pd.to_datetime(empl.index)
empl= empl.replace(',', '',regex=True)
for i in range(7):
    empl.iloc[:,i]=pd.to_numeric(empl.iloc[:,i])
empl=empl.loc['2019-06-01':'2021-06-01',:]
print(empl.info())
print(empl.head())


# 창업기업수 데이터
startsup=pd.read_csv('./data/창업기업수.csv')
startsup=startsup.set_index('업종별')
startsup=startsup.transpose()
startsup.index=pd.to_datetime(startsup.index)
startsup= startsup.replace(',', '',regex=True)
for i in range(5):
    startsup.iloc[:,i]=pd.to_numeric(startsup.iloc[:,i])
startsup=startsup.loc['2019-06-01':'2021-06-01',:]
print(startsup.info())
# print(startsup)

# startsup.boxplot()
# plt.show()
from commonutil import outfliers_iqr
lower, upper=outfliers_iqr(startsup['서비스업'])
startsup['서비스업'][startsup['서비스업']>upper]=upper
# startsup.boxplot()
# plt.show()


# 코로나 확진자 수
covid=pd.read_csv('./data/코로나확진자수.csv')
covid=covid.iloc[1:,:2]
covid=covid.set_index('일자')
covid.index=pd.to_datetime(covid.index)
covid.columns=['계']
covid.계= covid.계.str.replace(',','')
covid.계=pd.to_numeric(covid.계)
covid=covid.resample(rule='1M').sum()
covid=covid.reset_index()
covid.일자=covid.일자.astype(str)
covid.일자=covid.일자.str.slice(0,7)
covid=covid.set_index('일자')
covid.index=pd.to_datetime(covid.index)
covid=covid.iloc[:len(covid.index)-2,:]
# print(covid)


# 개업,폐업 사업장 수
busi=pd.read_csv('./data/성립소멸현황.csv')
busi.년월별=pd.to_datetime(busi.년월별)
busi.columns=['일자','개업수','폐업수']
busi=busi.set_index('일자')
busi_2020=busi.iloc[12:,:]
# print(busi_2020)




# 1. 개폐업률+확진자수, 보조y축
fig, ax1=plt.subplots()
ax1.set_xlabel('일자')
ax1.set_ylabel('개업/폐업수')
ax1.plot(busi_2020.index, busi_2020)
dateFmt = mdates.DateFormatter('%Y-%m')
ax1.xaxis.set_minor_formatter(dateFmt)
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=45)
plt.tick_params(axis='both', which='minor',rotation=45)
ax1.legend(['개업수','폐업수'])

ax2=ax1.twinx()
ax2.set_ylabel('확진자수')
ax2.bar(covid.index, covid.계, color='red',width=3)
ax2.legend(['확진자수'],loc='upper right')
plt.show()
'''
코로나 확진자 수가 증가함에 따라 거리두기 단계를 상향조정한 이후 약 한달정동의 기간을 두고 
폐업하는 사업장의 수가 증가함을 확인할 수 있다.
'''


# 2. 개폐업률+실업자수, 보조y축
fig, ax1=plt.subplots()
ax1.set_xlabel('일자')
ax1.set_ylabel('개업/폐업수')
ax1.plot(busi.index, busi)
dateFmt = mdates.DateFormatter('%Y-%m')
ax1.xaxis.set_minor_formatter(dateFmt)
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=45)
plt.tick_params(axis='both', which='minor',rotation=45)
ax1.legend(['개업수','폐업수'])

ax2=ax1.twinx()
ax2.set_ylabel('실업자 수')
ax2.plot(unempl.index, unempl, color='red')
ax2.legend(['실업자수'])
plt.show()
'''
폐업하는 사업장의 증가로 인해 실업자도 증가함을 확인할 수 있다.
'''


# 3-1. 업종별 창업수
fig, ax1=plt.subplots()
ax1.set_xlabel('일자')
ax1.set_ylabel('업종별창업수(개)')
ax1.plot(startsup.index, startsup.서비스업,color='purple')
dateFmt = mdates.DateFormatter('%Y-%m')
ax1.xaxis.set_minor_formatter(dateFmt)
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=45)
plt.tick_params(axis='both', which='minor',rotation=45)
ax1.legend(['서비스업'],loc='upper left')

ax2=ax1.twinx()
ax2.set_ylabel('업종별창업수(개)')
ax2.plot(startsup.index, startsup.iloc[:,1:])
ax2.legend(['건설업','제조업','전기,가스,증기및공기조절공급업','농업,임업,어업,광업'],loc='upper right')
plt.show()


# 3-2. 신규사업장수+업종별창업수(서비스업)(2019.06-2021.06)
new_busi=pd.DataFrame(busi.개업수)
new_busi=new_busi.loc['2019-06-01':'2021-06-01',:]

fig, ax1=plt.subplots()
ax1.set_xlabel('일자')
ax1.set_ylabel('업종별창업수(개)')
ax1.plot(startsup.index, startsup.iloc[:,0])
dateFmt = mdates.DateFormatter('%Y-%m')
ax1.xaxis.set_minor_formatter(dateFmt)
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=45)
plt.tick_params(axis='both', which='minor',rotation=45)
ax1.legend(['서비스업','건설업','제조업','전기,가스,증기및공기조절공급업','농업,임업,어업,광업'],loc='upper left')

ax2=ax1.twinx()
ax2.set_ylabel('신규사업장수(개)')
ax2.plot(new_busi.index, new_busi, color='darkred')
ax2.legend(['신규사업장수'],loc='upper right')
plt.grid(True)
plt.show()
'''
신규 사업장 수가 증가함에도 서비스업의 신규사업장은 즈
'''

# 3-3. 신규사업장수+업종별창업수(서비스 외)(2019.06-2021.06)
new_busi=pd.DataFrame(busi.개업수)
new_busi=new_busi.loc['2019-06-01':'2021-06-01',:]

fig, ax1=plt.subplots()
ax1.set_xlabel('일자')
ax1.set_ylabel('업종별창업수(개)')
ax1.plot(startsup.index, startsup.iloc[:,1:])
dateFmt = mdates.DateFormatter('%Y-%m')
ax1.xaxis.set_minor_formatter(dateFmt)
ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=45)
plt.tick_params(axis='both', which='minor',rotation=45)
ax1.legend(['서비스업','건설업','제조업','전기,가스,증기및공기조절공급업','농업,임업,어업,광업'],loc='upper left')

ax2=ax1.twinx()
ax2.set_ylabel('신규사업장수(개)')
ax2.plot(new_busi.index, new_busi, color='darkred')
ax2.legend(['신규사업장수'],loc='upper right')
plt.show()

'''
2020-3,4분기에 서비스업은 창업에서 많은 비중을 차지함에도 불구하고 하강세를 보이는 반면,
그럼에도 저렇게 '창업수'가 상승한것은 건설/전기가스 쪽이 증가한것이 큰 영향을 미친다고 볼 수 있다.
이는
1. 거리두기로 인해 사람들이 집에서 머무르는 시간이 증가함에따라 전기, 가스등의 자원 소모가 많아지고,
리모델링 등과 같이 집에 변화를 주는 투자를 많이 해 건설,제조업의 이용이 증가한다

2. # 총 창업수와 비교하였을때
1,2(생산업)차 산업에 비해 3차산업(서비스업)이 코로나로 인해 큰 타격을 입은 것을 알 수 있다.

'''