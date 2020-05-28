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

    csv_file = codecs.open(os.path.join(abs_path, str(file.file)), "r", "utf-8", "ignore")
    df_copy = pd.read_csv(csv_file, dtype={'phone_name': str})
    

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

    df_columns = ['phone_name' ,'plan_id', 'plan_category', 'campaign_code', 'campaign_code_2', 'campaign_code_3', 'campaign_code_4', 
             'channel']
    data_df[df_columns] = df_copy[df_columns]


    age_dict = {}
    age_count = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    age_key = ['10歳未満', '10~19歳','20~29歳','30~39歳','40~49歳','50~59歳','60~69歳','70~79歳','80~89歳','90歳以上']
    age_value = []

    kei_kikan_dict = {}
    kei_kikan_count = [50, 100, 150, 200, 250]
    kei_kikan_key = ['平均', '50未満', '50~99', '100~149', '150~199', '200以上']
    kei_kikan_value = []

    sex_dict = {}
    sex_count = [0, 1]
    sex_key = ['男性', '女性']
    sex_value = []

    kaku_type_code_dict = {}
    kaku_type_code_count = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    kaku_type_code_key = []
    kaku_type_code_value = []

    phone_career_dict = {}
    phone_career_count = [0, 1, 2, 3, 4]
    phone_career_key = ['#', '11', '12', '15', '16']
    phone_career_value = []

    taino_count_dict = {}
    taino_count_count = [0, 3, 6, 9, 10]
    taino_count_key = ['0', '1~3', '4~6', '7~9', '10']
    taino_count_value = []

    taino_month_dict = {}
    taino_month_count = list(range(12))
    taino_month_key = list(range(1,13))
    taino_month_value = []

    bill_change_count_dict = {}
    bill_change_count_count = list(range(6))
    bill_change_count_key = ['0回', '1回', '2回', '3回', '4回', '5回以上']
    bill_change_count_value = []

    phone_name_dict = {}
    AQUOS = 'AQ|SH'
    Xperie = 'Xperi|Xpr|SO'
    DIGNO = 'DIGNO|K'
    phone_name_count = ['iP', AQUOS, Xperie, DIGNO, 'Galaxy', 'Nexus', 'HTC', 'その他']
    phone_name_key = ['iPhone', 'AQUOS', 'Xperia', 'DIGNO', 'Galaxy', 'Nexus', 'HTC', 'その他']
    phone_name_value = []

    region_code_dict = {}
    region_code_count = list(range(9))
    region_code_key = ['東海', '北海道', '東北', '関西', '中国', '九州・沖縄', '北陸', '四国', '関東・甲信', ]
    region_code_value = []

    entry_age_dict = {}
    entry_age_count = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    entry_age_key = ['10歳未満', '10~19歳','20~29歳','30~39歳','40~49歳','50~59歳','60~69歳','70~79歳','80~89歳',
            '90歳以上']
    entry_age_value = []

    #_countと_keyの値が同じなため、_countを_keyに統合
    plan_id_dict = {}
    plan_id_rows_dict = dict(data_df['plan_id'].value_counts())
    plan_id_key = list(plan_id_rows_dict.keys())
    plan_id_value = []

    plan_category_dict = {}
    plan_category_rows_dict = dict(data_df['plan_category'].value_counts())
    plan_category_key = list(plan_category_rows_dict.keys())
    plan_category_value = []

    installment_count_dict = {}
    installment_count_count = list(range(11))
    installment_count_key = list(range(10))
    installment_count_key.append('10回以上')
    installment_count_value = []

    campaign_code_dict = {}
    campaign_code_rows_dict = dict(data_df['campaign_code'].value_counts())
    campaign_code_key = list(campaign_code_rows_dict.keys())
    campaign_code_value = []

    campaign_code_2_dict = {}
    campaign_code_2_rows_dict = dict(data_df['campaign_code_2'].value_counts())
    campaign_code_2_key = list(campaign_code_2_rows_dict.keys())
    campaign_code_2_value = []

    campaign_code_3_dict = {}
    campaign_code_3_rows_dict = dict(data_df['campaign_code_3'].value_counts())
    campaign_code_3_key = list(campaign_code_3_rows_dict.keys())
    campaign_code_3_value = []

    campaign_code_4_dict = {}
    campaign_code_4_rows_dict = dict(data_df['campaign_code_4'].value_counts())
    campaign_code_4_key = list(campaign_code_4_rows_dict.keys())
    campaign_code_4_value = []

    channel_dict = {}
    channel_rows_dict = dict(data_df['channel'].value_counts())
    channel_key = list(channel_rows_dict.keys())
    channel_value = []

    selling_method_code_dict = {}
    selling_method_code_key = list(range(4))
    selling_method_code_value = []

    pay_way_code_dict = {}
    pay_way_code_count = list(range(5))
    pay_way_code_key = ['コンビニ', 'ゆうちょ', '銀行', 'クレジットカード', 'その他']
    pay_way_code_value = []


    for i in range(5):
        cluster = data_df[data_df['cluster'] == i]
        
        #年齢を集計
        for age_i in age_count:
            len_age = len(cluster['age'])
            if age_i == 10:
                age_value.append(round(len(cluster[cluster['age'] < age_i]) / len_age * 100,1))
            elif age_i == 100:
                age_value.append(round(len(cluster[cluster['age'] >= age_i - 10]) / len_age * 100,1))
                age_dict[i] = dict(zip(age_key, age_value))
                age_value = []
            else:
                minus = len(cluster['age']) - len(cluster[cluster['age'] >= age_i - 10])
                age_value.append(round((len(cluster[cluster['age'] < age_i]) - minus) / len_age * 100,1))
                
        #kei_kikanを集計
        for kei_kikan_i in kei_kikan_count:
            len_all = len(cluster['kei_kikan'])
            if kei_kikan_i == 50:
                kei_kikan_value.append(round(cluster['kei_kikan'].mean()))
                kei_kikan_value.append(round(len(cluster[cluster['kei_kikan'] < kei_kikan_i]) / len_all * 100,1))
            elif kei_kikan_i == 250:
                kei_kikan_value.append(round(len(cluster[cluster['kei_kikan'] >= kei_kikan_i - 50]) / len_all * 100,1))
                kei_kikan_dict[i] = dict(zip(kei_kikan_key, kei_kikan_value))
                kei_kikan_value = []
            else:
                minus = len(cluster['kei_kikan']) - len(cluster[cluster['kei_kikan'] >= kei_kikan_i -50])
                kei_kikan_value.append(round((len(cluster[cluster['kei_kikan'] < kei_kikan_i]) - minus) / len_all * 100,1))
                
        #性別を集計
        for sex_i in sex_count:
            len_all = len(cluster['sex'])
            if sex_i == 0:
                sex_value.append(round(len(cluster[cluster['sex'] == 0]) / len_all * 100, 2))
            else:
                sex_value.append(round(len(cluster[cluster['sex'] == 1]) / len_all * 100, 2))
                sex_dict[i] = dict(zip(sex_key, sex_value))
                sex_value = []

        #kaku_type_codeを集計
        for kaku_type_code_i in kaku_type_code_count:
            len_all = len(cluster['kaku_type_code'])
            if kaku_type_code_i == 24:
                kaku_type_code_value.append(round(len(cluster[cluster['kaku_type_code'] == kaku_type_code_i]) / len_all * 100, 1))
                kaku_type_code_dict[i] = dict(zip(kaku_type_code_count, kaku_type_code_value))
                kaku_type_code_value = []
            else:
                kaku_type_code_value.append(round(len(cluster[cluster['kaku_type_code'] == kaku_type_code_i]) / len_all * 100, 1))
            
        #phone_careerを集計
        for phone_career_i in phone_career_count:
            len_all = len(cluster['phone_career'])
            if phone_career_i == 4:
                phone_career_value.append(round(len(cluster[cluster['phone_career'] == phone_career_i]) / len_all * 100, 1))
                phone_career_dict[i] = dict(zip(phone_career_key, phone_career_value))
                phone_career_value = []
            else:
                phone_career_value.append(round(len(cluster[cluster['phone_career'] == phone_career_i]) / len_all * 100, 1))
                
        #taino_countを集計
        for taino_count_i in taino_count_count:
            len_all = len(cluster['taino_count'])
            if taino_count_i == 0:
                taino_count_value.append(round(len(cluster[cluster['taino_count'] == taino_count_i]) / len_all * 100,1))
            elif taino_count_i == 10:
                taino_count_value.append(round(len(cluster[cluster['taino_count'] == taino_count_i]) / len_all * 100,1))
                taino_count_dict[i] = dict(zip(taino_count_key, taino_count_value))
                taino_count_value = []
            else:
                minus = len_all - len(cluster[cluster['taino_count'] >= taino_count_i - 2])
                taino_count_value.append(round((len(cluster[cluster['taino_count'] <= taino_count_i]) - minus) / len_all * 100,1))
                
        #taino_monthを集計
        for taino_month_i in taino_month_count:
            len_all = len(cluster['taino_month'])
            if taino_month_i == 11:
                taino_month_value.append(round(len(cluster[cluster['taino_month'] == taino_month_i]) / len_all * 100,1))
                taino_month_dict[i] = dict(zip(taino_month_key, taino_month_value))
                taino_month_value = []
            else:
                taino_month_value.append(round(len(cluster[cluster['taino_month'] == taino_month_i]) / len_all * 100,1))
                
        #bill_change_countを集計
        for bill_change_count_i in bill_change_count_count:
            len_all = len(cluster['bill_change_count'])
            if bill_change_count_i == 5:
                bill_change_count_value.append(round(len(cluster[cluster['bill_change_count'] >= bill_change_count_i]) / len_all * 100,2))
                bill_change_count_dict[i] = dict(zip(bill_change_count_key, bill_change_count_value))
                bill_change_count_value = []
            else:
                bill_change_count_value.append(round(len(cluster[cluster['bill_change_count'] == bill_change_count_i]) / len_all * 100,2))
        
        #phone_nameを集計
        for phone_name_i in phone_name_count:
            len_all = len(cluster['phone_name'])
            if phone_name_i == 'その他':
                phone_name_value.append(round(minus / len_all * 100, 2))
                phone_name_dict[i] = dict(zip(phone_name_key, phone_name_value))
                phone_name_value = []
            elif phone_name_i == 'iP':
                phone_name_value.append(round(len(cluster[cluster['phone_name'].str.contains(phone_name_i)]) / len_all * 100, 2))
                minus = len_all - len(cluster[cluster['phone_name'].str.contains(phone_name_i)])
            else:
                phone_name_value.append(round(len(cluster[cluster['phone_name'].str.contains(phone_name_i)]) / len_all * 100, 2))
                minus -= len(cluster[cluster['phone_name'].str.contains(phone_name_i)])
                
        #region_codeを集計
        for region_code_i in region_code_count:
            len_all = len(cluster['region_code'])
            if region_code_i == 8:
                region_code_value.append(round(len(cluster[cluster['region_code'] == region_code_i]) / len_all * 100, 2))
                region_code_dict[i] = dict(zip(region_code_key, region_code_value))
                region_code_value = []
            else:
                region_code_value.append(round(len(cluster[cluster['region_code'] == region_code_i]) / len_all * 100, 2))
                
        #entry_ageを集計
        for entry_age_i in entry_age_count:
            len_all = len(cluster['entry_age'])
            if entry_age_i == 10:
                entry_age_value.append(round(len(cluster[cluster['entry_age'] < entry_age_i]) / len_all * 100,2))
            elif entry_age_i == 100:
                entry_age_value.append(round(len(cluster[cluster['entry_age'] >= entry_age_i - 10]) / len_all * 100,2))
                entry_age_dict[i] = dict(zip(entry_age_key, entry_age_value))
                entry_age_value = []
            else:
                minus = len(cluster['entry_age']) - len(cluster[cluster['entry_age'] >= entry_age_i - 10])
                entry_age_value.append(round((len(cluster[cluster['entry_age'] < entry_age_i]) - minus) / len_all * 100,2))
                
        #plan_idを集計
        for plan_id_i in plan_id_key:
            len_all = len(cluster['plan_id'])
            plan_id_value.append(round(len(cluster[cluster['plan_id'] == plan_id_i]) / len_all * 100,2))
        plan_id_dict[i] = dict(zip(plan_id_key, plan_id_value))
        plan_id_value = []
        
        #plan_categoryを集計
        for plan_category_i in plan_category_key:
            len_all = len(cluster['plan_category'])
            plan_category_value.append(round(len(cluster[cluster['plan_category'] == plan_category_i]) / len_all * 100,2))
        plan_category_dict[i] = dict(zip(plan_category_key, plan_category_value))
        plan_category_value = []
        
        #installment_countを集計
        for installment_count_i in installment_count_count:
            len_all = len(cluster['installment_count'])
            if installment_count_i == 10:
                installment_count_value.append(round(len(cluster[cluster['installment_count'] >= installment_count_i]) / len_all * 100,2))
                installment_count_dict[i] = dict(zip(installment_count_key, installment_count_value))
                installment_count_value = []
            else:
                installment_count_value.append(round(len(cluster[cluster['installment_count'] == installment_count_i]) / len_all * 100,2))
                
        #campaign_codeを集計
        for campaign_code_i in campaign_code_key:
            len_all = len(cluster['campaign_code'])
            campaign_code_value.append(round(len(cluster[cluster['campaign_code'] == campaign_code_i]) / len_all * 100,2))
        campaign_code_dict[i] = dict(zip(campaign_code_key, campaign_code_value))
        campaign_code_value = []
        
        #campaign_code_2を集計
        for campaign_code_2_i in campaign_code_2_key:
            len_all = len(cluster['campaign_code_2'])
            campaign_code_2_value.append(round(len(cluster[cluster['campaign_code_2'] == campaign_code_2_i]) / len_all * 100,2))
        campaign_code_2_dict[i] = dict(zip(campaign_code_2_key, campaign_code_2_value))
        campaign_code_2_value = []
        
        #campaign_code_3を集計
        for campaign_code_3_i in campaign_code_3_key:
            len_all = len(cluster['campaign_code_3'])
            campaign_code_3_value.append(round(len(cluster[cluster['campaign_code_3'] == campaign_code_3_i]) / len_all * 100,2))
        campaign_code_3_dict[i] = dict(zip(campaign_code_3_key, campaign_code_3_value))
        campaign_code_3_value = []
        
        #campaign_code_4を集計
        for campaign_code_4_i in campaign_code_4_key:
            len_all = len(cluster['campaign_code_4'])
            campaign_code_4_value.append(round(len(cluster[cluster['campaign_code_4'] == campaign_code_4_i]) / len_all * 100,2))
        campaign_code_4_dict[i] = dict(zip(campaign_code_4_key, campaign_code_4_value))
        campaign_code_4_value = []
        
        #channelを集計
        for channel_i in channel_key:
            len_all = len(cluster['channel'])
            channel_value.append(round(len(cluster[cluster['channel'] == channel_i]) / len_all * 100,2))
        channel_dict[i] = dict(zip(channel_key, channel_value))
        channel_value = []
        
        #selling_method_codeを集計
        for selling_method_code_i in selling_method_code_key:
            len_all = len(cluster['selling_method_code'])
            selling_method_code_value.append(round(len(cluster[cluster['selling_method_code'] == selling_method_code_i]) / len_all * 100,2))
        selling_method_code_dict[i] = dict(zip(selling_method_code_key, selling_method_code_value))
        selling_method_code_value = []
        
        #pay_way_codeを集計
        for pay_way_code_i in pay_way_code_count:
            len_all = len(cluster['pay_way_code'])
            pay_way_code_value.append(round(len(cluster[cluster['pay_way_code'] == pay_way_code_i]) / len_all * 100,2))
        pay_way_code_dict[i] = dict(zip(pay_way_code_key, pay_way_code_value))
        pay_way_code_value = []
        
    data_key = ['age', 'kei_kikan', 'sex', 'kaku_type_code', 'phone_career', 'taino_count', 'taino_month', 'bill_change_count', 
        'phone_name', 'region_code', 'entry_age', 'plan_id', 'plan_category', 'installment_count', 'campaign_code', 'campaign_code_2',
        'campaign_code_3', 'campaign_code_4', 'channel', 'selling_method_code', 'pay_way_code']
    data_value = [age_dict, kei_kikan_dict, sex_dict, kaku_type_code_dict, phone_career_dict, taino_count_dict, 
        taino_month_dict, bill_change_count_dict, phone_name_dict, region_code_dict, entry_age_dict, plan_id_dict, 
        plan_category_dict, installment_count_dict, campaign_code_dict, campaign_code_2_dict,campaign_code_3_dict, 
        campaign_code_4_dict, channel_dict, selling_method_code_dict, pay_way_code_dict]
    cluster_dict = dict(zip(data_key, data_value))
    num = [0,1,2,3,4]    

    context = {
        'category_data': category_data,

        'cluster_dict': cluster_dict,
        'num': num,
    }

    return render(request, 'clustering/result.html', context)