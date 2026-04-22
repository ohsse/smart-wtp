#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import json
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
import pickle
from keras.models import load_model
import time
import pymysql
from pymysql.cursors import DictCursor
import schedule
from pytz import timezone
from sqlalchemy import create_engine
import openpyxl

import threading
from concurrent.futures import ThreadPoolExecutor

# ===== Logging 설정 시작 =====
import logging
from logging.handlers import RotatingFileHandler
import subprocess

# log_file_path = "/home/app/pump3/predict_log.txt"
log_file_path = "./log/log.txt"
log_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
# ===== Logging 설정 끝 =====


# Initialize a thread pool executor with a maximum number of workers
executor = ThreadPoolExecutor(max_workers=100)

MAX_EXEC_TIME = 300  # 최대 허용 시간 (초)

def run_subprocess_with_timeout(command, timeout=MAX_EXEC_TIME):
    # 외부 명령을 백그라운드 스레드에서 실행하고 제한 시간을 넘기면 종료한다.
    def target():
        print(f"[{datetime.now()}] Subprocess 시작: {command}")
        process = subprocess.Popen(command, shell=True)
        try:
            process.wait(timeout=timeout)
            print(f"[{datetime.now()}] Subprocess 정상 종료: {command}")
        except subprocess.TimeoutExpired:
            print(f"[{datetime.now()}] [TIMEOUT] Subprocess 강제 종료: {command}")
            process.kill()
            print(f"[{datetime.now()}] [KILLED] Subprocess 종료 완료: {command}")

    threading.Thread(target=target).start()

def open_db():
    # JSON 설정 파일을 읽어 pymysql 연결을 생성한다.
    print("open_db")
    try:
        with open(r'./libs/connections.json') as f:
            # 커넥션 정보를 불러옴
            connection = json.load(f)['maria-ems-db-dev']
            print('connection', connection)
            connection = pymysql.connect(**connection)
            print('connected', connection)
        return connection
    except Exception as e:
        logger.exception("DB 연결 실패")
        return None

def get_db_config():
    # 결과 업로드용 SQLAlchemy 엔진 생성에 사용할 DB 설정값을 반환한다.
    db_config = {               ## DB 연결정보 #--#
        "host": "10.103.11.112",
        "port": 3306,
        "user": "ems_user",
        "password": "ems2023",
        "db": "EMS_DB"
    }
    return db_config
    

def get_db_df(connection, tag_name, start_time):
    # 특정 태그의 과거 데이터 최대 1440건을 기준 시각 이전으로 조회한다.
    print(tag_name)
    cursor = connection.cursor(DictCursor)
    try:
        cursor.execute(
            f"""
            SELECT TS AS 'Datetime', VALUE 
            FROM EMS_DB.TB_RAWDATA tr 
            WHERE TAGNAME = '{tag_name}' AND TS <= '{start_time}' 
            ORDER BY TS DESC
            LIMIT 1440
            """
        )
        data = cursor.fetchall()
        print(tag_name+"["+str(len(data))+"] end") # for debug
        if len(data) == 0:
            logger.warning(f"[데이터 없음] {tag_name} - {start_time}")
        return data
    except Exception as e:
        logger.exception(f"DB 조회 실패 - {tag_name}")
        return []

def set_index_df(df, window_size = 30):
    # Datetime을 인덱스로 맞추고 VALUE를 수치형으로 정리한다.
    df = df.reset_index(drop=True)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.set_index('Datetime')
    df = df.sort_index()
    try:
        df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
    except:
        pass
    return df

def custom_loss(y_true, y_pred):
    # 값 10으로 마스킹된 위치를 제외하고 MSE를 계산하는 사용자 정의 loss.
    import tensorflow as tf
    from keras.losses import mean_squared_error
    mask = tf.reduce_any(tf.not_equal(y_true, 10), axis=-1, keepdims=True)
    mask = tf.cast(mask, tf.float32)

    y_true_masked = tf.multiply(y_true, mask)
    y_pred_masked = tf.multiply(y_pred, mask)

    loss = mean_squared_error(y_true_masked, y_pred_masked)

    return tf.reduce_sum(loss) / tf.reduce_sum(mask)

def RELU(x):
    # 예측값이 음수가 되지 않도록 0 이하를 절삭한다.
    return np.maximum(0, x)

def initialization(sheetname, model_name, mode):
    # 태그 정의, 모델, scaler를 읽어 예측에 필요한 메타데이터를 구성한다.
    # worksheet = pd.read_excel('C://Users//MINDONE//KMJ//2025//1. EMS//EMS_GS//MAIN//GS_taglist_250904.xlsx', sheet_name = sheetname, header=0)
    worksheet = pd.read_excel(r'/home/app/pump3/GS_taglist.xlsx', sheet_name = sheetname, header=0)
    
    if mode == 'PRES':
        df = worksheet.loc[
            (worksheet['비고'] != 'NU') & (worksheet['사용'] == 'Y') & (worksheet['변수명'].str[0] == 'P')
        ].reset_index(drop=True)

    elif mode == 'FLUX':
        df = worksheet.loc[
            (worksheet['비고'] != 'NU') & (worksheet['사용'] == 'Y') & (worksheet['변수명'].str[0] != 'P')
        ].reset_index(drop=True)

    elif mode == 'BOTH':
        df = worksheet.loc[
            (worksheet['비고'] != 'NU') & (worksheet['사용'] == 'Y')
        ].reset_index(drop=True)

    # load_dir ="C://Users//MINDONE//KMJ//2025//1. EMS//EMS_GS//MAIN//"
    load_dir ="/home/app/pump3/"
    
    keras_file = f"{load_dir}saved_model/250903/{model_name}.keras"
    
    if os.path.exists(keras_file):
        print(f"파일이 존재합니다: {keras_file}")
    else:
        print(f"파일이 존재하지 않습니다: {keras_file}")
        
    try:
        model = load_model(f"{load_dir}saved_model/250903/{model_name}.keras", custom_objects={'custom_loss': custom_loss})
    except Exception as e:
        print(f'Failed to load {model_name}.keras file..., alternatively load {model_name}.h5 file ..., error: {e} ')
        logger.warning(f"{model_name}.keras 로드 실패, h5 로드 시도: {e}")
        try:
            model = load_model(f"{load_dir}saved_model/250903/{model_name}.h5", custom_objects={'custom_loss': custom_loss})
        except Exception as e:
            print(f'Failed to load {model_name}.keras or {model_name}.h5 file... please ask model developer..., error: {e}')
            logger.exception(f"{model_name} 모델 로드 실패 (keras, h5 모두)")
            raise
    model.summary()    
    loaded_scalers = {}
    var_list = df['변수명'].tolist()
    target_list = df.loc[df['비고'] == 'target'].변수명.tolist()

    var_list_height = [s for s in var_list if s[0] == 'H']
    var_first_two = [s.split('_')[0] for s in var_list_height]
    var_list_height_unique = list(set(var_first_two))
    if len(var_list_height_unique) != len(var_list_height):
        # 'H1_1', 'H1_2', 'H1_3' 등 높이별로 여러 개가 있을 때, sum으로 합침
        # '합쳐진 변수는 H1, H2, ...로 명명하며, 기존 변수는 삭제'
        for prefix in var_list_height_unique:
            height_cols = [s for s in var_list_height if s.startswith(prefix)]
            if len(height_cols) > 1:
                print(f"Variables {height_cols} summed into {prefix} and original columns dropped.")
                for col in height_cols:
                    var_list.remove(col)
                var_list.append(prefix)

    for feature in var_list:
        save_path = os.path.join(load_dir, f"./saved_scaler/250903/{model_name}/{feature}_scaler.pkl")
        try:
            with open(save_path, "rb") as f:
                loaded_scalers[feature] = pickle.load(f)
        except Exception as e:
            logger.exception(f"스케일러 로드 실패: {feature} ({save_path})")
            raise
  
    return df, model, loaded_scalers, var_list, target_list

def Predict_5min_test(name, model_name, mode='FLUX'):
    # 공통 예측 파이프라인: 데이터 조회, 전처리, 스케일링, 모델 추론, 역변환을 수행한다.
    # 현재 시간의 초를 구합니다.
    current_seconds = time.localtime().tm_sec
    # 10초 이전이면 10초까지 대기
    if current_seconds < 10:
        time_to_wait = 10 - current_seconds
        print(f"Waiting for {time_to_wait} seconds...")
        time.sleep(time_to_wait)
    
    KST = timezone('Asia/Seoul')
    now = datetime.now().astimezone(KST)
    test_timestamp = now.strftime('%Y-%m-%d %H:%M:00')  # 문자열로 현재 시간 포맷
    # test_timestamp = '2025-01-01 00:00:00'  # 테스트용
    print('######test_timestamp:', test_timestamp)
    
    try:
        df, model, loaded_scalers, var_list, target_list = initialization(name, model_name, mode=mode)
    except Exception as e:
        logger.exception(f"모델 및 스케일러 초기화 실패: {name}/{model_name}")
        return None, None, None
    
    data_df = pd.DataFrame()
    db_connection = open_db()
    if not db_connection:
        logger.error("DB 연결 실패 - 예측 중단")
        return None, None, None

    try:
        # 태그 정의서에 있는 모든 입력 태그를 순회하며 시계열 데이터를 적재한다.
        for i in range(len(df)):
            data_df[f"{df.변수명[i]}"] = set_index_df(
                pd.DataFrame(get_db_df(db_connection, f"{df.태그명[i]}", test_timestamp))
            )
    finally:
        db_connection.close()

    print("Successfully imported data ...")
    
    print("------------------------------------------------------------")
    var_list_2 = df['변수명'].tolist()
    var_list_height = [s for s in var_list_2 if s[0] == 'H']
    var_first_two = [s.split('_')[0] for s in var_list_height]
    var_list_height_unique = list(set(var_first_two))
    if len(var_list_height_unique) != len(var_list_height):
        # 'H1_1', 'H1_2', 'H1_3' 등 높이별로 여러 개가 있을 때, sum으로 합침
        # '합쳐진 변수는 H1, H2, ...로 명명하며, 기존 변수는 삭제'
        for prefix in var_list_height_unique:
            height_cols = [s for s in var_list_height if s.startswith(prefix)]
            if len(height_cols) > 1:
                data_df[prefix] = data_df[height_cols].sum(axis=1)
                data_df.drop(columns=height_cols, inplace=True)
                print(f"Variables {height_cols} summed into {prefix} and original columns dropped.")
                for col in height_cols:
                    var_list_2.remove(col)
                var_list_2.append(prefix)

    if set(var_list) != set(var_list_2):
        logger.error(f"변수 불일치 - 모델 변수: {var_list}, 데이터 변수: {var_list_2}")
        return None, None, None
    # 학습 입력과 동일한 시간 단위로 맞추기 위해 10분 평균값을 사용한다.
    data_df = data_df.resample('10min', origin ='end').mean()

    df_to_sequence = data_df.copy().reset_index(drop=True)


    try:
        # 학습 시 저장한 scaler를 변수별로 다시 적용한다.
        for feature in var_list:
            df_to_sequence[feature] = loaded_scalers[feature].transform(df_to_sequence[[feature]])
    except Exception as e:
        logger.exception("스케일러 적용 오류")
        return None, None, None

    testset = df_to_sequence.copy()


    if testset.isnull().values.any():
        logger.warning(f"[NaN 포함] 예측 입력 데이터 - {name}/{model_name}")

    testset = testset.fillna(testset.mean())

    try:
        # 전체 시계열을 하나의 배치로 넣고, 마지막 예측 시점의 결과를 사용한다.
        d_testX = np.expand_dims(np.array(testset[var_list]), axis=0)
        testPredict = model.predict(d_testX)
        testPredict_result = testPredict[:, -5, :]  # 마지막 시간 인덱스 (00분) 결과만 사용
    except Exception as e:
        logger.exception(f"모델 예측 실패: {name}/{model_name}")
        return None, None, None

    if testPredict_result.ndim == 2:
        pass
    else:
        testPredict_result = np.expand_dims(testPredict_result, axis=0)
    
    # 예측 시점 출력
    start_time_predict_str = test_timestamp
    print(f"예측 시점 : {start_time_predict_str} (KTC)")

    # 예측 결과 데이터 프레임 구성

    # 1. 가장 마지막 인덱스(예: DatetimeIndex) 를 문자열로 변환
    last_str = data_df.index[-1].strftime('%Y-%m-%d %H:%M:%S')

    # 2. 문자열을 datetime 객체로 다시 파싱
    last_dt = datetime.strptime(last_str, '%Y-%m-%d %H:%M:%S')

    # 3. 1분 뒤 시각 계산
    future_time = last_dt + timedelta(minutes=1)
    df_result = pd.DataFrame(index=[future_time.strftime('%Y-%m-%d %H:%M:%S')])

    try:
        # 예측 결과를 원래 단위로 복원한 뒤 음수는 0으로 보정한다.
        for k in range(testPredict_result.shape[1]):
            scaler_key = var_list[k]
            inverse_transformed = loaded_scalers[scaler_key].inverse_transform(
                testPredict_result[:, k].reshape(-1, 1)
            ).flatten()
            df_result[f"{scaler_key}_Predict"] = RELU(inverse_transformed)
    except Exception as e:
        logger.exception("역변환 실패 - 예측 결과 생성 중")
        return None, None, None

    print(f"1분 후 예측 : ")
    df_result_str = df_result.copy()
    df_result_str.columns = [df.loc[df['비고'] == 'target']['태그 설명']]

    print('df_result:', df_result)
    
    return df_result_str, df_result, data_df.iloc[-1]

def create_pump_df(timestamp, Q_pred, P_pred, pump_idxs, pump_yn, freqs, pump_grp):
    # 펌프 그룹별 운전 여부와 예측값을 업로드용 DataFrame으로 변환한다.
    pump_df =  pd.DataFrame({
        'RGSTR_TIME': [timestamp] * len(pump_idxs),
        'pump_idx': list(pump_idxs),
        'pump_yn': pump_yn,
        'FREQ': freqs,
        'PUMP_GRP': pump_grp,
        'TUBE_PRSR_PRDCT' : Q_pred,
        'PRDCT_MEAN' : P_pred,
        'PRDCT_TIME_DIFF' : 5
    })
    timestamp_fmt = '%Y-%m-%d %H:%M:%S'
    timestamp_temp = datetime.strptime(timestamp, timestamp_fmt)
    pump_df['OPT_IDX'] = f'701-367-FRI-{pump_grp}:{timestamp_temp.strftime("%Y%m%d%H-")}-{datetime.now().strftime("%H%M")}'
    return pump_df

def pred_pump(df_result, mode):
    # 예측된 유량/압력으로 펌프 운전 조합을 계산한다.
    if mode == 'OLD':
        pump_dfs = []
        print('####pred_pump')
        
        columns_checked = {'Q_GS_OLD_Predict': 'Q_GS_OLD_Predict' in df_result.columns,
                           'P_GS_OLD_Predict': 'P_GS_OLD_Predict' in df_result.columns} # 예측값 존재여부 확인
        print(f"{df_result['Q_GS_OLD_Predict']}")
        print(f"{df_result['P_GS_OLD_Predict']}")

        for timestamp, row in df_result.iterrows():
            print('row', row)
            pump_yn = []
            if all(columns_checked.values()):
                freqs = [None, None, None, None, None, None, None]
                Q = row['Q_GS_OLD_Predict']
                P = row['P_GS_OLD_Predict']
                print('Q:', Q)
                print('P:', P)
                if P >= 58.6613373258886 - 0.00527586346649821*Q + 1.2957874682855E-07*Q**2:
                    pump_yn = [0, 0, 0, 1, 1, 1, 1]
                elif -3.43193582761012 + 0.00120472303735243*Q - 4.08245928068585E-08*Q**2 <= P < 58.6613373258886 - 0.00527586346649821*Q + 1.2957874682855E-07*Q**2:
                    pump_yn = [0, 1, 0, 1, 0, 1, 1]
                elif 2.95 + 0.000497*Q - 0.0000000229*Q**2 <= P < -3.43193582761012 + 0.00120472303735243*Q - 4.08245928068585E-08*Q**2:
                    pump_yn = [0, 1, 0, 1, 1, 0, 1]
                elif 0.120821964429389 + 0.000853219487279097*Q - 3.52433865423429E-08*Q**2 <= P < 2.95 + 0.000497*Q - 0.0000000229*Q**2:
                    pump_yn = [0, 0, 0, 1, 1, 1, 0]
                elif 0.46770987097162 + 0.000872862970476709*Q - 3.89262100721736E-08*Q**2 <= P < 0.120821964429389 + 0.000853219487279097*Q - 3.52433865423429E-08*Q**2:
                    pump_yn = [0, 0, 0, 1, 1, 0, 1]
                elif -0.759451815235986 + 0.0010218039074961*Q - 4.43777727901476E-08*Q**2 <= P < 0.46770987097162 + 0.000872862970476709*Q - 3.89262100721736E-08*Q**2:
                    pump_yn = [0, 1, 0, 1, 0, 1, 0]
                elif P < -0.759451815235986 + 0.0010218039074961*Q - 4.43777727901476E-08*Q**2:
                    pump_yn = [0, 1, 0, 0, 1, 0, 1]
                
                if P < 0:
                    print(f"WARNING: Predicted pressure has negative value of {P}")
                print('pump_yn:', pump_yn)
                pump_df = create_pump_df(timestamp, Q, P, range(1, 8), pump_yn, freqs, 1)
                pump_dfs.append(pump_df)
                print('*'*30 + 'pump_dfs' + '*'*30)
                print(pump_dfs)

    elif mode == 'NEW':
        pump_dfs = []
        columns_checked = {'Q_GS_NEW_Predict': 'Q_GS_NEW_Predict' in df_result.columns,
                           'P_GS_NEW_Predict': 'P_GS_NEW_Predict' in df_result.columns}
        for timestamp, row in df_result.iterrows():
            print('row', row)
            if all(columns_checked.values()):
                freqs, pump_yn = [None, None, None, None], [0, 0, 1, 0]
                pump_df = create_pump_df(timestamp, row['Q_GS_NEW_Predict'], row['P_GS_NEW_Predict'], range(1, 5), pump_yn, freqs, 2)
                pump_dfs.append(pump_df)
    return pump_dfs

def create_tnk_df(df_result, test_timestamp):
    # 예측 결과를 탱크/배수지 결과 테이블 형식으로 변환해 DB에 저장한다.
    for col in df_result.columns:
        tnk_df = pd.DataFrame({
            'DSTRB_ID': [col] * len(df_result),
            'PRDCT_VALUE': df_result[col].fillna(0).values,
            # 'RGSTR_TIME': df_result.index
            'RGSTR_TIME': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(df_result)
        })
        tnk_df.set_index(['DSTRB_ID', 'RGSTR_TIME'])        
        print(tnk_df)
        try:
            tnk_df.to_sql('EMS_DB.TB_CTR_TNK_RST', engine, if_exists='append', index=False)
        except Exception as e:
            logger.exception(f"{col} 저장 중 오류 발생")

    return

def pred_and_upload_gs_test():  # 고산정수장 예측(구,신)
    # 고산 정수장의 유량/압력 예측 후, 실측 기반 보정과 업로드를 수행한다.
    try:
        _, df_result_flux, cur_flux = Predict_5min_test('Gosan','Gosan_test_ss_XGBoost', mode='FLUX')
        _, df_result_pres, cur_pres = Predict_5min_test('Gosan','Gosan_test_ss_XGBoost', mode='PRES')

        cur_flux = cur_flux.to_frame().T
        cur_flux = cur_flux.iloc[:, :2].reset_index(drop=True)
        cur_flux.columns = ['Q_GS_NEW_Predict', 'Q_GS_OLD_Predict']
        cur_flux.index = df_result_flux.index
        cur_flux = cur_flux.astype(float)

        cur_pres = cur_pres.to_frame().T
        cur_pres = cur_pres.iloc[:, :2].reset_index(drop=True)
        cur_pres.columns = ['P_GS_NEW_Predict', 'P_GS_OLD_Predict']
        cur_pres.index = df_result_pres.index
        cur_pres = cur_pres.astype(float)

        error_flux = abs((df_result_flux - cur_flux) / cur_flux)
        beta_features = error_flux.mean(axis=0)
        corrected_df_result_flux = pd.DataFrame(columns=df_result_flux.columns)
        for feature in df_result_flux.columns:
            beta = beta_features[feature]
            # 상대오차가 크면 실측값 비중을 높여 보수적으로 보정한다.
            if beta > 0.2:
                corrected_df_result_flux[feature] = (1-beta)*df_result_flux[feature] + beta*cur_flux[feature]
            else:
                corrected_df_result_flux[feature] = 0.8*df_result_flux[feature] + 0.2*cur_flux[feature]

        error_pres = abs((df_result_pres - cur_pres) / cur_pres)
        beta_features = error_pres.mean(axis=0)
        corrected_df_result_pres = pd.DataFrame(columns=df_result_pres.columns)
        for feature in df_result_pres.columns:
            beta = beta_features[feature]
            if beta > 0.2:
                corrected_df_result_pres[feature] = (1-beta)*df_result_pres[feature] + beta*cur_pres[feature]
            else:
                corrected_df_result_pres[feature] = 0.8*df_result_pres[feature] + 0.2*cur_pres[feature]

        df_result_old = pd.concat([corrected_df_result_flux['Q_GS_OLD_Predict'], corrected_df_result_pres['P_GS_OLD_Predict']], axis=1)
        df_result_new = pd.concat([corrected_df_result_flux['Q_GS_NEW_Predict'], corrected_df_result_pres['P_GS_NEW_Predict']], axis=1)

        create_tnk_df(df_result_old, df_result_old.index)
        create_tnk_df(df_result_new, df_result_new.index)
        pred_pump(df_result_old, 'OLD')
        pred_pump(df_result_new, 'NEW')

        logger.info("pred_and_upload_gs_test 실행 완료")

        return df_result_old, df_result_new
    except Exception as e:
        logger.exception("pred_and_upload_gs_test 예외 발생")
        return None, None

def predict_and_upload_flux_test(taglist):  # 하위 배수지 예측
    # 태그 정의서의 하위 배수지 시트들을 순회하며 예측 후 DB에 적재한다.
    i = 0
    for sheetname in taglist.sheetnames[2:]:
        print(f"---Predicting {sheetname}---")
        _, df_result, _ = Predict_5min_test(sheetname, f'{sheetname}_250904', mode='BOTH')

        create_tnk_df(df_result, df_result.index)
        i += 1
    return

def schedule_job(taglist):
    # 스케줄러가 직접 실행하지 않고 스레드풀에 전체 예측 작업을 제출한다.
    executor.submit(predict_gs_test, taglist)

def predict_gs_test(taglist):  # 전체 예측
    # 고산 정수장과 하위 배수지를 포함한 전체 예측 사이클 1회를 수행한다.
    KST = timezone('Asia/Seoul')
    start = time.time()
    print(f"실행 시작: {str(datetime.now().astimezone(KST)).split('.')[0]} (KTC)")

    try:
        pred_and_upload_gs_test()              # 241011 유량 및 압력을 각각 따로 예측하는 방식(기존)
        predict_and_upload_flux_test(taglist)
    except Exception as e:
        logger.exception("predict_gs_test 예외 발생")

    print(f"실행 완료: {str(datetime.now().astimezone(KST)).split('.')[0]} (KTC)")
    print(f"실행 시간 : {time.time() - start :.2f} 초")

# 설정 값
window_size = 144
# 현재 구현은 5분 앞 예측 결과를 사용하도록 맞춰져 있다.
step_topredict = 5  # 예측할 시간 = 5분

taglist_name = r"/home/app/pump3/GS_taglist.xlsx"
# 태그 정의서와 업로드 엔진을 시작 시점에 미리 준비해 재사용한다.
taglist = openpyxl.load_workbook(taglist_name)
db_config = get_db_config()
database_connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db']}"
engine = create_engine(database_connection_string)

# 매 분마다 전체 예측 작업을 실행하도록 등록한다.
schedule.every().minute.do(schedule_job, taglist)

# while True:
#     try:
#         # schedule.run_pending()
#         predict_gs_test(taglist)
#     except Exception as e:
#         logger.exception("스케줄러 실행 중 예외 발생")
#     time.sleep(1)
