from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import FileForm
from .models import File
import os

import pandas as pd
import csv
import codecs
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder




def file_list(request):
    files = File.objects.all()
    return render(request, 'clustering/file_list.html', {
        'files': files
    })


def upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'clustering/upload.html', {
        'form': form
    })


def result(request, number):
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


    cluster_int_dict = {}
    cluster_category_dict1 = {}
    cluster_category_dict2 = {}
    cluster_category_dict3 = {}
    cluster_category_dict4 = {}
    cluster_category_dict5 = {}

    #カテゴリデータの割合をカウント
    cluster_data1 = data_df[data_df['cluster'] == 0]
    cluster_len1 = len(cluster_data1)
    for category_name in category_data:
        unique_count = data_df[category_name].nunique()
        for num in range(unique_count):
            cluster_category_list = round(cluster_data1[cluster_data1[category_name] == num].loc[:, category_name].count() / len(cluster_data1) * 100, 2)
            cluster_category_dict1[category_name] = cluster_category_list

    cluster_data2 = data_df[data_df['cluster'] == 1]
    cluster_len2 = len(cluster_data2)
    for category_name in category_data:
        unique_count = data_df[category_name].nunique()
        for num in range(unique_count):
            cluster_category_list = round(cluster_data2[cluster_data2[category_name] == num].loc[:, category_name].count() / len(cluster_data2) * 100, 2)
            cluster_category_dict2[category_name] = cluster_category_list

    cluster_data3 = data_df[data_df['cluster'] == 2]
    cluster_len3 = len(cluster_data3)
    for category_name in category_data:
        unique_count = data_df[category_name].nunique()
        for num in range(unique_count):
            cluster_category_list = round(cluster_data3[cluster_data3[category_name] == num].loc[:, category_name].count() / len(cluster_data3) * 100, 2)
            cluster_category_dict3[category_name] = cluster_category_list

    cluster_data4 = data_df[data_df['cluster'] == 3]
    cluster_len4 = len(cluster_data4)
    for category_name in category_data:
        unique_count = data_df[category_name].nunique()
        for num in range(unique_count):
            cluster_category_list = round(cluster_data4[cluster_data4[category_name] == num].loc[:, category_name].count() / len(cluster_data4) * 100, 2)
            cluster_category_dict4[category_name] = cluster_category_list

    cluster_data5 = data_df[data_df['cluster'] == 4]
    cluster_len5 = len(cluster_data5)
    for category_name in category_data:
        unique_count = data_df[category_name].nunique()
        for num in range(unique_count):
            cluster_category_list = round(cluster_data5[cluster_data5[category_name] == num].loc[:, category_name].count() / len(cluster_data5) * 100, 2)
            cluster_category_dict5[category_name] = cluster_category_list
        



    #数値データの平均を計算
    int_data = ['age', 'kei_kikan', 'taino_count', 'taino_month', 'bill_change_count', 'entry_age', 'installment_count', 'sales_1', 'sales_2']
    for i in range(5):
        cluster_data = data_df[data_df['cluster'] == i]
        print(len(cluster_data))
        for integer_name in int_data:
            cluster_int_list = round(cluster_data[integer_name].mean(), 1)
            cluster_int_dict[integer_name] = cluster_int_list

    whole_category_dict = {}

    #全体のカテゴリデータの割合
    print(len(data_df))
    for category_name in category_data:
        unique_count = data_df[category_name].nunique()
        for num in range(unique_count):
            whole_category_list = round(data_df[data_df[category_name] == num].loc[:, category_name].count() / len(data_df) * 100, 2)
            whole_category_dict[category_name] = whole_category_list

    whole_int_dict = {}

    #全体の数値データの平均
    print(len(data_df))
    for integer_name in int_data:
        whole_int_list = round(data_df[integer_name].mean(), 1)
        whole_int_dict[integer_name] = whole_int_list


    fivenum = [0, 1, 2, 3, 4]
    test_dict = [
        {1: 'a', 2: 'b'},
        {1: 'A', 2: 'B'},
    ]

    cluster_group_dict = {}
    cluster_shere = {}
    sale1sum = {}
    sale2sum = {}
    sale1shere = {}
    sale2shere = {}
    age_dict = {}
    age_data = []
    for i in range(5):
        #クラスタ人数を計算
        a_cluster = data_df[data_df['cluster'] == i]
        cluster_group = len(a_cluster)
        cluster_group_dict[i] = cluster_group
        #クラスタのシェアを計算
        cluster_division = round(cluster_group / len(data_df) * 100, 1)
        cluster_shere[i] = cluster_division
        #商品１、２の購入金額を計算
        sale1sum[i] = a_cluster['sales_1'].sum()
        sale2sum[i] = a_cluster['sales_2'].sum()
        #商品１、２のシェアを計算
        sale1shere[i] = round(sale1sum[i] / data_df['sales_1'].sum() * 100,1)
        sale2shere[i] = round(sale2sum[i] / data_df['sales_2'].sum() * 100,1)
        #年齢を集計
        age_num = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for age in age_num:
            len_age = len(a_cluster['age'])
            if age == 10:
                age_data.append(round(len(a_cluster[a_cluster['age'] < age]) / len_age * 100,1))
            elif age == 100:
                age_data.append(round(len(a_cluster[a_cluster['age'] >= age - 10]) / len_age * 100,1))
                age_dict[i] = age_data
                age_data = []
            else:
                minus = len(a_cluster['age']) - len(a_cluster[a_cluster['age'] >= age - 10])
                age_data.append(round((len(a_cluster[a_cluster['age'] < age]) - minus) / len_age * 100,1))
        

    #ageデータをテンプレートで表示するために加工         
    c1_age = age_dict[0]
    c2_age = age_dict[1]
    c3_age = age_dict[2]
    c4_age = age_dict[3]
    c5_age = age_dict[4]
    ten_dict = {
        0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [],
    }
    age_list = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {},]
    for i in range(10):
        ten_dict[i].append(c1_age[i])
        ten_dict[i].append(c2_age[i])
        ten_dict[i].append(c3_age[i])
        ten_dict[i].append(c4_age[i])
        ten_dict[i].append(c5_age[i])
    for num in range(10):
        ten_list_select = age_list[num]
        ten_dict_select = ten_dict[num]
        for i in range(5):
            ten_list_select[i] = ten_dict_select[i]
    







    


    context = {
        'file': file,
        'int_data': int_data,
        'category_data': category_data,
        'cluster_category_dict1': cluster_category_dict1,
        'cluster_category_dict2': cluster_category_dict2,
        'cluster_category_dict3': cluster_category_dict3,
        'cluster_category_dict4': cluster_category_dict4,
        'cluster_category_dict5': cluster_category_dict5,
        'cluster_int_dict': cluster_int_dict,
        'whole_int_dict': whole_int_dict,
        'whole_category_dict': whole_category_dict,
        'cluster_len1': cluster_len1,
        'cluster_len2': cluster_len2,
        'cluster_len3': cluster_len3,
        'cluster_len4': cluster_len4,
        'cluster_len5': cluster_len5,
        'fivenum': fivenum,
        'cluster_group_dict': cluster_group_dict,
        'cluster_shere': cluster_shere,
        'sale1sum': sale1sum,
        'sale2sum': sale2sum,
        'sale1shere': sale1shere,
        'sale2shere': sale2shere,
        'test_dict': test_dict,
        'age_dict': age_dict,
        'c1_age': c1_age,
        'c2_age': c2_age,
        'c3_age': c3_age,
        'c4_age': c4_age,
        'c5_age': c5_age,
        'age_num': age_num,
        'age_list': age_list

    }

    return render(request, 'clustering/result.html', context)