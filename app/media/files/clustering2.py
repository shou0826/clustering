import pandas as pd
import csv
import codecs
import numpy as np
from sklearn.cluster import KMeans

with codecs.open("data.csv", "r", "utf-8", "ignore") as f:
	df = pd.read_csv(f)

#文字列を数値に変換
df['plan_id'] = pd.to_numeric(df['plan_id'], errors='coerce')
df['selling_method_code'] = pd.to_numeric(df['selling_method_code'], errors='coerce')

#文字列を排除したdfをdata_dfへ代入
data_df = df.drop(columns=['id', 'phone_career', 'phone_name', 'region_code',
	'plan_category', 'campaign_code', 'campaign_code_2', 'campaign_code_3',
	'campaign_code_4', 'channel', 'Unnamed: 24'])

#NaNを0に置き換える
#data_df.isnull().sum()
data_df = data_df.fillna(0)

#Numpy行列に変換
df_array = np.array([data_df['age'].tolist(), data_df['sex'].tolist(),
 data_df['kei_kikan'].tolist(),data_df['plan_id'].tolist(),
 data_df['sales_1'].tolist(), data_df['sales_2'].tolist()])
df_array = df_array.T

#クラスタ実行
kmeans = KMeans(n_clusters=5).fit_predict(df_array)
data_df['cluster'] = kmeans

data_df['cluster'].value_counts()


