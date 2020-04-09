from django import template
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from ..forms import FileForm
from ..models import File
from ..views import result
import os

import pandas as pd
import csv
import codecs
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

register = template.Library()

@register.simple_tag
def read():
    number = 1
    files = File.objects.all()
    file_id = number - 1
    file = files[file_id]
    abs_path = os.path.join("media")
    csv_file = codecs.open(os.path.join(abs_path, str(file.file)), "r", "utf-8", "ignore")
    df = pd.read_csv(csv_file)
    category_data = ['sex', 'kaku_type_code', 'phone_career', 'phone_name', 'region_code', 'plan_id', 'plan_category', 'campaign_code', 'campaign_code_2',
    'campaign_code_3', 'campaign_code_4', 'channel', 'selling_method_code', 'pay_way_code']
    i = 0
    labels = {}
    le = LabelEncoder()
    for data in category_data:
        category = df.loc[:, data ]
        category_array = np.array(category, dtype=str)
        labels[i] = le.fit_transform(category_array)
        df[data] = labels[i]
        i += 1

    data_df = df.drop(columns=['id', 'Unnamed: 24'])

    #NaNを0に置き換える
    #data_df.isnull().sum()
    data_df = data_df.fillna(0)

    #Numpy行列に変換
    df_array = np.array(data_df)

    #クラスタ実行
    kmeans = KMeans(n_clusters=5).fit_predict(df_array)
    data_df['cluster'] = kmeans

    print(data_df['cluster'].value_counts())

    for i in range(5):
        cluster_data = data_df[data_df['cluster'] == i]
        print(len(cluster_data))
        for category_name in category_data:
            print(category_name)
            unique_count = data_df[category_name].nunique()
            for num in range(unique_count):
                return round(cluster_data[cluster_data[category_name] == num].loc[:, category_name].count() / len(cluster_data) * 100, 2)

