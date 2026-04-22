# ********************************************
# * System      : EMS
# * Program ID  : PowerPrediction
# * Description : Power prediction model execution and scheduling
# * Execute Program : predict_func
# * Revision    :
# * 수정일      수정자        수정내용
# * 2024-09-15  최용성        Initial PEP8 Compliance and Code Commenting
# ********************************************

#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
import os
import numpy as np
import re
from datetime import datetime, timedelta
import pickle
from keras.models import load_model
import tensorflow as tf
from keras.losses import mean_squared_error
import time
import pymysql
from pymysql.cursors import DictCursor
import schedule
from pytz import timezone
from sqlalchemy import create_engine

# 모델 초기화
def initialization(model_name):
    """
    모델 초기화 함수
    지정된 모델 이름에 따라 모델과 관련된 스케일러를 로드하고 초기화 작업을 수행
    """
    print('initialization - model_name:', model_name)
    worksheet = pd.read_excel(r"/home/app/power/Gosan_taglist.xlsx")

    # 변수 목록 필터링
    df = worksheet.loc[(worksheet['비고'] != 'NU')].reset_index(drop=True)
    df_variable = worksheet.loc[(worksheet['비고'] == 'variable')].reset_index(drop=True)

    load_dir = r"/home/app/power/"

    try:
        # 모델 불러오기
        model = load_model(f"{load_dir}saved_model/{model_name}.keras", custom_objects={'custom_loss': custom_loss})
        print('model 1:', model)
    except:
        print(f'Failed to load {model_name}.keras file..., alternatively load {model_name}.h5 file ... ')
        try:
            # .h5 확장자로 모델 불러오기
            model = load_model(f"{load_dir}saved_model/{model_name}.h5", custom_objects={'custom_loss': custom_loss})
            print('model 2:', model)
        except:
            print(f'Failed to load {model_name}.keras or {model_name}.h5 file... please ask model developer...')
    
    # 스케일러 불러오기
    loaded_scalers = {}
    save_path = os.path.join(load_dir, f"saved_scaler/{model_name}/Power_tot_scaler.pkl")
    with open(save_path, "rb") as f:
        loaded_scalers['Power_tot'] = pickle.load(f)
    for feature in df_variable.변수명:
        save_path = os.path.join(load_dir, f"saved_scaler/{model_name}/{feature}_scaler.pkl")
        with open(save_path, "rb") as f:
            loaded_scalers[feature] = pickle.load(f)

    return df, df_variable, model, loaded_scalers

# 데이터베이스 연결 설정
def open_db():
    """
    MariaDB 연결 함수
    """
    print("open_db")
    with open(r'/home/app/connections.json') as f:
        connection = json.load(f)['maria-ems-db-gs']
        print('connection', connection)
        connection = pymysql.connect(**connection)
        print('connected', connection)
    return connection

# DB 설정 불러오기
def get_db_config():
    """
    데이터베이스 설정 반환 함수
    """
    db_config = {
        "host": "10.103.11.112",
        "port": 3306,
        "user": "ems_user",
        "password": "ems2023",
        "db": "EMS_DB"
    }
    return db_config

# 데이터 전처리
def clean_and_convert(df):
    """
    데이터 프레임을 숫자형으로 변환하고 불필요한 소수점 제거
    """
    for column in df.columns:
        df[column] = df[column].astype(str).apply(lambda x: re.sub(r'\.0000$', '', x))
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

# 데이터베이스에서 데이터 가져오기
def get_db_df(connection, tag_name, start_time, window_size):
    """
    지정된 태그의 데이터를 데이터베이스에서 가져옴
    """
    print(tag_name)
    cursor = connection.cursor(DictCursor)
    cursor.execute( 
        f"""
        SELECT TS AS 'Datetime', VALUE 
        FROM EMS_DB.TB_RAWDATA tr
        WHERE TAGNAME = '{tag_name}' AND TS <= '{start_time}' 
        AND TS >= DATE_SUB('{start_time}', INTERVAL 5 DAY) 
        ORDER BY TS DESC
        LIMIT {window_size * 60}
        """
    )
    data = cursor.fetchall()
    return data

# 데이터 프레임 인덱스 설정
def set_index_df(df):
    """
    데이터 프레임의 인덱스를 Datetime으로 설정하고 정렬
    """
    df = df.reset_index(drop=True)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.set_index('Datetime')
    df = df.sort_index()
    return df

# 사용자 정의 손실 함수
def custom_loss(y_true, y_pred):
    """
    커스텀 손실 함수: 주어진 마스크를 기준으로 손실 계산
    """
    mask = tf.reduce_any(tf.not_equal(y_true, 10), axis=-1, keepdims=True)
    mask = tf.cast(mask, tf.float32)

    y_true_masked = tf.multiply(y_true, mask)
    y_pred_masked = tf.multiply(y_pred, mask)

    loss = mean_squared_error(y_true_masked, y_pred_masked)

    return tf.reduce_sum(loss) / tf.reduce_sum(mask)

# ReLU 활성화 함수
def RELU(x):
    """
    ReLU 함수: 0보다 큰 값은 그대로 반환, 그렇지 않은 값은 0 반환
    """
    return np.maximum(0, x)

# 시간에 대한 사인, 코사인 값 계산
def cal_time(data_df):
    """
    주어진 데이터프레임의 시간 정보를 사인 및 코사인 값으로 변환
    """
    datetime_hours = data_df.index.hour
    hours_sin = np.sin(datetime_hours * (2 * np.pi / 24))
    data_df['hours_sin'] = hours_sin
    hours_cos = np.cos(datetime_hours * (2 * np.pi / 24))
    data_df['hours_cos'] = hours_cos
    return data_df

# 데이터 리샘플링
def resampling(data_df, resam_term='1H', method='mean'):
    """
    데이터를 주기별로 리샘플링
    """
    data_df_resam = data_df.copy()
    data_df_resam = data_df_resam.reset_index(drop=False)
    data_df_resam['Datetime'] = pd.to_datetime(data_df_resam['Datetime'])
    data_df_resam = data_df_resam.set_index('Datetime')
    
    if method == 'mean':
        data_df_resam = data_df_resam.resample(rule=resam_term, closed='right', origin='end').mean(numeric_only=True)
    elif method == 'sum':
        data_df_resam = data_df_resam.resample(rule=resam_term, closed='right', origin='end').sum(numeric_only=True)
    elif method == 'max':
        data_df_resam = data_df_resam.resample(rule=resam_term, closed='right', origin='end').max(numeric_only=True)
    
    return data_df_resam

# 예측 결과 데이터 생성
def create_tnk_df(df_result):
    """
    예측 결과 데이터프레임 생성 및 DB에 저장
    """
    timestamp = df_result.index
    current_time_str = datetime.now().strftime('%H%M')
    opt_idx_values = [f"701-367-FRI:{ts.strftime('%Y%m%d%H-')}{current_time_str}" for ts in timestamp]

    for col in df_result.columns:
        tnk_df = pd.DataFrame({
        'RGSTR_TIME': [datetime.now()] * len(df_result),
        'PRDCT_TIME': timestamp,
        'PRDCT_TIME_DIFF': [i+1 for i in range(len(df_result))],
        'PRDCT_MEAN': [0] * len(df_result),
        'PRDCT_STD': [0] * len(df_result),
        'TUBE_PRSR_PRDCT': [0] * len(df_result),
        'PUMP_GRP': [0] * len(df_result),
        'PWR_PRDCT': df_result[col].values,
        'ANLY_TIME': [datetime.now()] * len(df_result),
        'OPT_IDX': opt_idx_values
        })
        tnk_df.set_index(['RGSTR_TIME'])
        tnk_df.to_sql('TB_CTR_OPT_RST', engine, if_exists='append', index=False)


# 예측 함수
def Predict(model_name, window_size):
    """
    예측을 수행하는 함수
    지정된 모델을 사용하여 입력 데이터를 예측하고 결과를 DB에 저장
    """
    KST = timezone('Asia/Seoul')
    now = datetime.now().astimezone(KST)  # 현재 시간을 KST로 변환
    test_timestamp = now.replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M')

    # 모델 초기화 및 데이터 불러오기
    df, df_var, model, loaded_scalers = initialization(model_name)
    data_target = pd.DataFrame()
    data_var = pd.DataFrame()

    # DB 연결 설정
    db_connection = open_db()
    for i in range(len(df)):
        # 데이터 가져오기
        if df['변수명'][i][:5] == 'Power':
            data_target[f"{df.변수명[i]}"] = set_index_df(pd.DataFrame(get_db_df(db_connection, f"{df.태그명[i]}", test_timestamp, window_size)))
        else:
            data_var[f"{df.변수명[i]}"] = set_index_df(pd.DataFrame(get_db_df(db_connection, f"{df.태그명[i]}", test_timestamp, window_size)))
    db_connection.close()

    print(f"Successfully imported data ...")
    print('data_df:', data_target)

    # 데이터 정리 및 변환
    data_target = clean_and_convert(data_target)
    data_target = data_target.sum(axis=1).to_frame()
    data_target.columns = ['Power_tot']
    data_target = data_target.fillna(data_target.mean())
    target_resampled = resampling(data_target, resam_term='1H', method='mean')

    try:
        data_var = data_var.fillna(data_var.mean())
        var_resampled = resampling(df_var, resam_term='1H', method='mean')
        data_df = pd.concat([target_resampled, var_resampled], axis=1, join='inner')
    except:
        data_df = target_resampled.copy()

    data_df = cal_time(data_df)
    data_df = data_df.iloc[-window_size:]
    df_to_sequence = data_df.copy().reset_index(drop=True)

    print("------------------------------------------------------------")

    # 스케일러로 데이터 변환
    df_to_sequence['Power_tot'] = loaded_scalers['Power_tot'].transform(df_to_sequence[['Power_tot']])

    # 예측 수행
    testset = df_to_sequence.copy()
    testset = testset.fillna(testset.mean())
    try:
        d_testX = testset.copy()
        testPredict = model.predict(d_testX)
    except:
        d_testX = np.expand_dims(testset, axis=0)
        testPredict = model.predict(d_testX)

    # 예측 결과 처리
    testPredict_result = testPredict[:, -step_topredict:, :]
    if testPredict_result.ndim == 2:
        pass
    else:
        testPredict_result = np.expand_dims(testPredict_result, axis=0)

    print(f"예측 시점 : {test_timestamp} (KTC)")

    # 예측 결과 데이터 프레임 구성
    df_result = pd.DataFrame(index=[datetime.strptime(test_timestamp, '%Y-%m-%d %H:%M') + timedelta(hours=i+1) for i in range(step_topredict)])

    scaler = loaded_scalers['Power_tot']
    test_predict_result_numpy = testPredict_result
    inverse_transformed = scaler.inverse_transform(test_predict_result_numpy.reshape(-1, 1)).flatten()
    df_result[f"Power_tot_Predict"] = RELU(inverse_transformed)

    # 예측 결과 저장
    create_tnk_df(df_result)

    return None, df_result

# 전체 예측 수행 함수
def Predict_func(model_name, window_size):
    """
    예측 수행 및 로그 출력
    """
    KST = timezone('Asia/Seoul')
    start = time.time()
    print(f"실행 시작: {str(datetime.now().astimezone(KST)).split('.')[0]} (KTC)")

    # 예측 함수 호출
    Predict(model_name, window_size)

    print(f"실행 완료: {str(datetime.now().astimezone(KST)).split('.')[0]} (KTC)")
    print(f"실행 시간 : {time.time() - start :.2f} 초")
    return None

# 실행 설정
window_size = 120
step_topredict = 24  # 모델 자체 예측 시간 = 5분 but 사용은 1분
model_name = 'Powerprediction_DLinear_Gosan'

# DB 설정
db_config = get_db_config()
database_connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db']}"
engine = create_engine(database_connection_string)

# 스케줄 실행 (60분마다)
schedule.every(60).minute.do(Predict_func, model_name, window_size)
while True:
    schedule.run_pending()
    time.sleep(1)
