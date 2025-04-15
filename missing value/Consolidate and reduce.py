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

# 2. 데이터 통합 및 축소 예제

# 예시로 두 개의 데이터프레임을 합치기 (같은 열을 기준으로 merge)
# 데이터프레임 df_new의 'species'와 다른 예시 데이터프레임을 merge 하는 예시

# 새로운 데이터프레임 df2 생성
df2 = pd.DataFrame({
    'species': ['Adelie', 'Chinstrap', 'Gentoo'],
    'habitat': ['Tundra', 'Coastal', 'Coastal']
})

# 'species' 열을 기준으로 df_new와 df2를 병합
merged_df = pd.merge(df_new, df2, on='species', how='left')

# 데이터 축소: 필요한 열만 선택하여 새로운 데이터프레임 생성
reduced_df = merged_df[['species', 'bill_length_mm', 'habitat']]

# 결과 출력 (병합된 데이터프레임의 첫 5행을 출력)
print(reduced_df.head())
