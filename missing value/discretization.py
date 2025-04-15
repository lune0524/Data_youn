import numpy as np
import seaborn as sns
import pandas as pd

# 'penguins' 데이터셋 불러오기
df_new = sns.load_dataset('penguins')

# 1. 결측값 채우기 (각 열의 평균값으로 결측값을 채운다)
# 'bill_length_mm'의 결측값을 해당 열의 평균값으로 채우기
df_new['bill_length_mm'].fillna(df_new['bill_length_mm'].mean(), inplace=True)

# 'bill_depth_mm'의 결측값을 해당 열의 평균값으로 채우기
df_new['bill_depth_mm'].fillna(df_new['bill_depth_mm'].mean(), inplace=True)

# 'flipper_length_mm'의 결측값을 해당 열의 평균값으로 채우기
df_new['flipper_length_mm'].fillna(df_new['flipper_length_mm'].mean(), inplace=True)

# 'body_mass_g'의 결측값을 해당 열의 평균값으로 채우기
df_new['body_mass_g'].fillna(df_new['body_mass_g'].mean(), inplace=True)

# 'sex'의 결측값을 최빈값(모드)으로 채우기
df_new['sex'].fillna(df_new['sex'].mode()[0], inplace=True)

# 2. 이상치 식별 (IQR 방법을 사용하여 이상치를 찾는다)
# 'bill_length_mm' 열에서 이상치를 IQR (Interquartile Range) 방법으로 식별
Q1 = df_new['bill_length_mm'].quantile(0.25)  # 1사분위수
Q3 = df_new['bill_length_mm'].quantile(0.75)  # 3사분위수
IQR = Q3 - Q1  # IQR 계산

# 이상치 조건: IQR 값보다 크거나 작은 값이 이상치로 간주됨
outlier_condition = (df_new['bill_length_mm'] < (Q1 - 1.5 * IQR)) | (df_new['bill_length_mm'] > (Q3 + 1.5 * IQR))

# 이상치 식별 결과를 새로운 열 'bill_length_outlier'로 추가
df_new['bill_length_outlier'] = outlier_condition

# 3. 잡음 제거 (이상치 값을 NaN으로 처리하고 평균값으로 채운다)
# 이상치가 있는 값들을 NaN으로 변경
df_new.loc[outlier_condition, 'bill_length_mm'] = np.nan

# NaN으로 변경된 값을 해당 열의 평균값으로 채운다
df_new['bill_length_mm'].fillna(df_new['bill_length_mm'].mean(), inplace=True)

# 결과 출력 (처리된 데이터프레임의 첫 5행을 출력)
print(df_new.head())



# 3. 데이터 변환 및 이산화 예제

# 1. 데이터 변환 (스케일링) - MinMaxScaler를 사용하여 값을 0과 1 사이로 정규화
from sklearn.preprocessing import MinMaxScaler

# MinMaxScaler 객체 생성
scaler = MinMaxScaler()

# 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g' 열을 0과 1 사이로 정규화
df_new[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']] = scaler.fit_transform(
    df_new[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
)

# 2. 데이터 이산화 (이산화 함수 적용)
# 'body_mass_g' 열을 두 개의 범주('Low', 'High')로 이산화
bins = [0, 3500, 6000]  # 나누는 구간 (Low: 0~3500, High: 3500~6000)
labels = ['Low', 'High']  # 범주 이름
df_new['body_mass_category'] = pd.cut(df_new['body_mass_g'], bins=bins, labels=labels)

# 결과 출력 (이산화된 데이터를 포함한 데이터프레임의 첫 5행을 출력)
print(df_new[['species', 'body_mass_g', 'body_mass_category']].head())