import base64
import gzip
import json
import os
import sys
import warnings
from dateutil import tz

import numpy as np
import pandas as pd

sys.path.append(os.getcwd())
# sys.path.append(
#     os.path.dirname(
#         os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#     )
# )

import time
from datetime import datetime, timedelta

from merge_by_device import merge_by_motor, merge_by_pump
from motor_class import motorDiagnosis
from pump_class import PumpDiagnosis

from config.config import config
from util.utils.db import DBConnect

warnings.filterwarnings(action="ignore")


# n_hist: number of recent feature sets to be saved in motor/pump class
########## 입력 1. n_hist (int, 12 이상) ##########
def decompress(data):
    byte_data = gzip.decompress(base64.standard_b64decode(data))
    temp = byte_data.decode("utf-16")
    temp_jarr = json.loads(temp)
    return np.array(list(map(lambda x:float(x), temp_jarr)))
    
def compress(json_data):
    # numpy 배열을 리스트로 변환하고, 이를 JSON 문자열로 인코딩
    #json_data = json.dumps(array.tolist())
    # JSON 문자열을 UTF-16으로 인코딩
    byte_data = json_data.encode("utf-16")
    # gzip을 사용하여 데이터 압축
    gzipped_data = gzip.compress(byte_data)
    # 결과를 Base64로 인코딩하여 리턴
    return base64.standard_b64encode(gzipped_data).decode()

def compress_array(array_list):
    # 배열 리스트의 각 항목을 UTF-16으로 인코딩하고 개행 문자로 연결
    byte_data = "\n".join([str(item) for item in array_list]).encode("utf-16")
    # gzip을 사용하여 데이터 압축
    gzipped_data = gzip.compress(byte_data)
    # 결과를 Base64로 인코딩하여 리턴
    return base64.standard_b64encode(gzipped_data).decode()

def fetch_device_info_from_db():
    try:
        # db connection
        ip, port, name, id, pw = config.get_db_info() # 디비 연결
        conn = DBConnect(ip, id, pw, port, name)
        cur = conn.get_cursor()
            
        # SQL 쿼리 실행 - 모든 그룹의 데이터를 가져오기
        sql = """
        SELECT GRP_ID, MOTOR_ID, EQ_TYPE, CHANNEL_NM, PARM_NM, PARM_VALUE
        FROM TB_AL_SETTING
        ORDER BY GRP_ID, MOTOR_ID, EQ_TYPE, CHANNEL_NM;
        """
        cur.execute(sql)
        result = cur.fetchall()
        print('result:', result)

        # 데이터 구조화
        device_info = {"n_poles": {}}
        sensors_data = {}

        # 그룹 ID 수 파악
        groups = set(row[0] for row in result)
        single_group = len(groups) == 1

        motor_counter = 1
        pump_counter = 1

        for row in result:
            grp_id = row[0]
            motor_or_pump = row[1]
            eq_type = row[2]
            channel = row[3]
            param_name = row[4]
            param_value = float(row[5])

            # 그룹별 데이터 초기화
            if grp_id not in sensors_data:
                sensors_data[grp_id] = {"motor_sensors": {}, "pump_sensors": {}}

            # MOTOR_ID 형식 변환
            if single_group:
                motor_or_pump = motor_or_pump.replace('motor_', 'motor_0')
            else:
                if grp_id == '1':
                    motor_or_pump = motor_or_pump.replace('motor_', 'motor_o_')
                elif grp_id == '2':
                    motor_or_pump = motor_or_pump.replace('motor_', 'motor_n_')

            if eq_type == 'MOTOR':
                if motor_or_pump not in sensors_data[grp_id]['motor_sensors']:
                    sensors_data[grp_id]['motor_sensors'][motor_or_pump] = {}

                if channel not in sensors_data[grp_id]['motor_sensors'][motor_or_pump]:
                    sensors_data[grp_id]['motor_sensors'][motor_or_pump][channel] = {}

                sensors_data[grp_id]['motor_sensors'][motor_or_pump][channel][param_name] = param_value

            elif eq_type == 'PUMP':
                if motor_or_pump not in sensors_data[grp_id]['pump_sensors']:
                    sensors_data[grp_id]['pump_sensors'][motor_or_pump] = {}

                if channel not in sensors_data[grp_id]['pump_sensors'][motor_or_pump]:
                    sensors_data[grp_id]['pump_sensors'][motor_or_pump][channel] = {}

                sensors_data[grp_id]['pump_sensors'][motor_or_pump][channel][param_name] = param_value

        for grp_id, grp_data in sensors_data.items():
            for motor_id, channels in grp_data['motor_sensors'].items():
                for channel, params in channels.items():
                    rated_freq = params['RPM'] / params['Cycle']
                    brg_ball = params['BRG(BALL)']
                    bpf_r = [
                        (brg_ball / 2) - 1.2,
                        (brg_ball / 2) + 1.2,
                        0.5 * ((brg_ball / 2) - (1.2 / brg_ball)),
                        0.5 - (1.2 / brg_ball)
                    ]

                    motor_de_key = f"P_motor_{motor_counter}_DE"
                    motor_nde_key = f"P_motor_{motor_counter}_NDE"

                    motor_sensors_key = f"motor_sensors_{grp_id}"
                    device_info.setdefault(motor_sensors_key, {})[motor_de_key] = {"rated_freq": rated_freq, "BPF_r": bpf_r}
                    device_info[motor_sensors_key][motor_nde_key] = {"rated_freq": rated_freq, "BPF_r": bpf_r}

                device_info['n_poles'][motor_sensors_key] = int(params['Pole'])
                motor_counter += 1  # motor_counter 증가

            for pump_id, channels in grp_data['pump_sensors'].items():
                for channel, params in channels.items():
                    rated_freq = params['RPM'] / params['Cycle']
                    brg_ball = params['BRG(BALL)']
                    bpf_r = [
                        (brg_ball / 2) - 1.2,
                        (brg_ball / 2) + 1.2,
                        0.5 * ((brg_ball / 2) - (1.2 / brg_ball)),
                        0.5 - (1.2 / brg_ball)
                    ]

                    pump_de_key = f"P_pump_{pump_counter}_DE"
                    pump_nde_key = f"P_pump_{pump_counter}_NDE"

                    pump_sensors_key = f"pump_sensors_{grp_id}"
                    device_info.setdefault(pump_sensors_key, {})[pump_de_key] = {"rated_freq": rated_freq, "BPF_r": bpf_r}
                    device_info[pump_sensors_key][pump_nde_key] = {"rated_freq": rated_freq, "BPF_r": bpf_r}

                device_info['n_poles'][pump_sensors_key] = int(params['Vane'])
                pump_counter += 1  # pump_counter 증가

        return device_info

    finally:
        cur.close()
 
def main():
    n_hist = 1 # 운행 스텝 변수
    center_id = 'hakya'

    ip, port, name, id, pw = config.get_db_info() # 디비 연결
    
    # 한국 시간대 설정
    KST = tz.gettz('Asia/Seoul')
    
    
    # load rated frequencies, BPFO_r, BPFI_r, BSF_r, FTF_r of each motor/pump sensor
    # json파일에서 센서 주파수 불러옴
    '''
    with open(
        os.path.join(os.getcwd(), "device_info.json"), "r"
    ) as device_info_json:
        device_info = json.load(device_info_json)
    '''    
    #DB의 설정값 획득
    device_info = fetch_device_info_from_db()

    # Initialization for each motor/pump sensor
    device_dict = {}
    motor_sensor_list = list(device_info["motor_sensors"].keys())
    pump_sensor_list = list(device_info["pump_sensors"].keys())

    # 여기서 Dignosis를 통해 motor_class.py의 init설정, rated_frequency는(부하 정격 주파수) 정상 정격 작동 주파수를 의미
    # get_motor_1x 성분을 추출할때 사용함
    for motor_sensor in motor_sensor_list:
        rated_frequency = device_info["motor_sensors"][motor_sensor]["rated_freq"]
        BPF_r = device_info["motor_sensors"][motor_sensor]["BPF_r"]
        device_dict[motor_sensor] = motorDiagnosis(rated_frequency, BPF_r, n_hist)

    for pump_sensor in pump_sensor_list:
        rated_frequency = device_info["pump_sensors"][pump_sensor]["rated_freq"]
        BPF_r = device_info["pump_sensors"][pump_sensor]["BPF_r"]
        device_dict[pump_sensor] = PumpDiagnosis(rated_frequency, BPF_r, n_hist)

    # prepare arrays to save result from this step
    motor_amp_this_run = np.zeros(
        [len(motor_sensor_list), 5]
    )  # motor amp: [unbalance_amp, misalignment_amp, rotor_amp, bearing_amp, rms]
    motor_res_this_run = np.zeros(
        [len(motor_sensor_list), 8]
    )  # motor res: [unbalance, misalignment, rotor, or_fault, ir_fault, ball_fault, train_fault]
    pump_amp_this_run = np.zeros(
        [len(pump_sensor_list), 4]
    )  # pump amp: [impeller_amp, cavitation_amp, bearing_amp, rms]
    pump_res_this_run = np.zeros(
        [len(pump_sensor_list), 7]
    )  # pump res: [impeller, cavitation, or_fault, ir_fault, ball_fault, train_fault]

    # run each step

    while True:
        try:
            # db connection
            conn = DBConnect(ip, id, pw, port, name)
            cur = conn.get_cursor()
            
            # 현재 시간을 한국 시간대로 변환
            current_time_korea = datetime.now(KST)
            # 원하는 형식으로 시간 포맷
            now_acq_date_time = current_time_korea.strftime('%Y-%m-%d %H:%M:%S')

            # 2분 전의 시간 계산
            time_two_minutes_before = current_time_korea - timedelta(minutes=10)
            two_minutes_before_formatted = time_two_minutes_before.strftime('%Y-%m-%d %H:%M:00')
            now_acq_date_time =  two_minutes_before_formatted

            #수동 시간 조절
            #now_acq_date_time = '2024-07-25 13:00:27.000'
            print(now_acq_date_time)
            
            #start_dt = '2024-03-17 09:50:00.000'
            #end_dt = '2024-03-17 09:55:00.000'

            #print( f"SELECT acq_date from TB_MOTOR where proc_stat = 0 and acq_date > '{start_dt}' and acq_date < '{end_dt}' group by acq_date order by acq_date asc;")
            #cur.execute(
            #    f"SELECT acq_date from TB_MOTOR where proc_stat = 0 group by acq_date order by acq_date asc;"  ### sim TB_MOTOR
            #)
            cur.execute(
                f"SELECT acq_date from TB_MOTOR where proc_stat = 0 and center_id='{center_id}' and acq_date > '{now_acq_date_time}' group by acq_date order by acq_date asc;"  ### sim TB_MOTOR
            )
            '''
            cur.execute(
                f"SELECT acq_date from TB_MOTOR where proc_stat = 0 and acq_date > '{now_acq_date_time}' group by acq_date order by acq_date asc;"  ### sim TB_MOTOR
            )
            '''
            acq_date_rows = cur.fetchall()
            #print(acq_date_rows)
            print("acq_date_rows len", len(acq_date_rows))
            if len(acq_date_rows) > 0:
                last_acq_date = acq_date_rows[-1]

            cur.execute(f"SELECT threshold FROM TB_THRESHOLD WHERE table_id = 'motor'")
            motor_threshold_jObj = json.loads(cur.fetchall()[0][0])
            #print('motor_threshold_jObj:', motor_threshold_jObj)
            cur.execute(f"SELECT threshold FROM TB_THRESHOLD WHERE table_id = 'pump'")
            pump_threshold_jObj = json.loads(cur.fetchall()[0][0])
            #print('pump_threshold_jObj:', pump_threshold_jObj)
            for acq_datetime in acq_date_rows:
                print('acq_datetime[0]')
                print(acq_datetime[0])
                cur.execute(
                    f"SELECT count(channel_id) from TB_MOTOR where DATE_FORMAT(ACQ_DATE, '%Y-%m-%d %H:%i:%S') >= DATE_SUB(DATE_FORMAT('{acq_datetime[0]}','%Y-%m-%d %H:%i:%S'), INTERVAL 1 MINUTE ) AND DATE_FORMAT(ACQ_DATE, '%Y-%m-%d %H:%i:%S') <= DATE_ADD(DATE_FORMAT('{acq_datetime[0]}','%Y-%m-%d %H:%i:%S'), INTERVAL 1 MINUTE );"
                )
                '''
                cur.execute(
                    f"SELECT count(channel_id) from TB_MOTOR where DATE_FORMAT(ACQ_DATE, '%Y-%m-%d %H:%i:%S') >= DATE_SUB(DATE_FORMAT('{acq_datetime[0]}','%Y-%m-%d %H:%i:%S'), INTERVAL 1 MINUTE );"
                )
                '''
                
                # 모든 데이터가 다 저장되는지 확인
                count = cur.fetchall()[0][0]
                print(f"#channel count = {count}")
                #if count != ((len(motor_sensor_list) + len(pump_sensor_list))):
                #    if last_acq_date is not acq_datetime:
                #        conn.insert(
                #            f"UPDATE TB_MOTOR SET proc_stat = -1 WHERE acq_date = '{acq_datetime[0]}'"
                #        )
                #        continue

                start = time.time()
                sql = f"SELECT motor_id, equipment_id, center_id, channel_id, data_array from TB_MOTOR where DATE_FORMAT(ACQ_DATE, '%Y-%m-%d %H:%i:%S') >= DATE_SUB(DATE_FORMAT('{acq_datetime[0]}','%Y-%m-%d %H:%i:%S'), INTERVAL 1 MINUTE );"  ### sim TB_MOTOR

                cur.execute(
                    f"SELECT motor_id, equipment_id, center_id, channel_id, data_array from TB_MOTOR where acq_date = '{acq_datetime[0]}' and center_id='{center_id}';"  ### sim TB_MOTOR
                )
                rows = cur.fetchall()
                end = time.time()
                row_count = len(rows)
                print("Number of rows", row_count)
                print(f"end read data time = {end - start}")

                ### diagnose motors ###
                # run through each motor sensor
                ########## 입력 2. 모터 진단 sensitivity (int, 1~10) ##########
                # threshold value get
                # m_sensitivity = [5, 5, 5, 5, 5]  # motor sensitivity: [unbalance, misalignment, bearing, rotor, rms]

                ########## 입력 2. 이번 step 모터/펌프들의 on tag ##########
                # index: PTK1 DE/NDE:0~1; PTK2 DE/NDE:2~3; PTK3 DE/NDE:4~5; PTK4 DE/NDE:6~7; SSN2 DE/NDE:8~9; SSN1 DE/NDE:10~11
                # on_tags = np.ones([12])

                ########## 입력 3. 이번 step 모터/펌프들의 line frequency(전원 주파수) ##########
                # index: PTK1 DE/NDE:0~1; PTK2 DE/NDE:2~3; PTK3 DE/NDE:4~5; PTK4 DE/NDE:6~7; SSN2 DE/NDE:8~9; SSN1 DE/NDE:10~11
                # value: PTK1~PTK4: 60; SSN2:745-617-CTI-4260; SSN1:745-617-SPI-4213
                line_frequencies = 60 * np.ones([12])
                tag_sql = f"SELECT pump_scada_id, eq_on FROM TB_PUMP_SCADA WHERE acq_date = func_get_abs_time('{acq_datetime[0]}', '', 1) order by acq_date desc"
                cur.execute(f"SELECT func_get_abs_time('{acq_datetime[0]}', '', 1)") ## sim 실행안됨 ㅠ # kim 이제 실행가능
                
                scada_time = cur.fetchall()[0][0] ## sim 실행안됨 ㅠ # kim 이제 실행가능
                #scada_time = '2023-12-18 13:00:00.000'

                cur.execute(
                    f"SELECT pump_scada_id, eq_on, frequency FROM TB_PUMP_SCADA WHERE acq_date = '{scada_time}' order by acq_date desc"
                )
                on_rows = cur.fetchall()

                print('EQ ON rows:', on_rows)

                on_tags = {}
                freq_tags = {}
                for row in on_rows:
                    pump_scada_id = row[0]
                    eq_on = row[1]
                    on_tags[row[0]] = eq_on

                for row in on_rows:
                    pump_scada_id = row[0]
                    if not row[2]:
                        freq_tags[pump_scada_id] = config.get_frequency_value(
                            pump_scada_id
                        ) ### kim : pump scada에 frequency 가 null (none) 값인 경우 config에 있는 데이터를 입력 (60)
                        continue
                    freq_tags[pump_scada_id] = row[2]

                print(datetime.strftime(acq_datetime[0], "%Y-%m-%d %H:%M:%S"))
                #print('motor_sensor_list:',motor_sensor_list)
                for i, motor_sensor_name in enumerate(motor_sensor_list):
                    # sample data 준비 --> 추후 실제 모터 센서 데이터를 순서대로 불러오도록 변경
                    # data_folder = os.path.join("X:\\수자원공사\\diagnosis_test_data", motor_sensor_name)
                    # data_name = os.listdir(data_folder)[np.random.randint(0, len(os.listdir(data_folder)) - 1, 1)[0]]
                    # data_motor = pd.read_csv(os.path.join(data_folder, data_name), header=None)
                    ########## 입력 3. motor vibration data (개개 모터에 대하여) ##########
                    # raw data decompress zip base64 to ndarray
                    
                    for row in rows:
                        #print('Motor row[3]:',row[3])
                        #print('config.get_mapping_id(row[3]):',config.get_mapping_id(row[3]))
                        if config.get_mapping_id(row[3]) in motor_sensor_name:
                            #print('Now motor_sensor_name:',motor_sensor_name)
                            #print('decompress data')
                            timeseries_motor = decompress(row[4])
                            motor_id = row[0]
                            print('##################')
                            #타임웨이브
            
                            # 2초 데이터를 1초만 추출
                            timeseries_subset = timeseries_motor[:12800]
                            df = pd.DataFrame(timeseries_subset, columns=['y'])

                            # 인덱스를 'x'로 지정
                            df['y'] = df['y'].apply(lambda x: round(x, 10))
                            y_list = ["{:.10f}".format(float(value)) for value in df['y']]
                            print(motor_id)
                            print(motor_sensor_name)
                            tsql = f"INSERT IGNORE INTO TB_TIMEWAVE(MOTOR_ID, CHANNEL_ID, ACQ_DATE, DATA_ARRAY) VALUES( '{motor_id}', '{motor_sensor_name}', '{acq_datetime[0]}', '{compress_array(y_list)}' ) "
                            #print(tsql)
                            conn.insert(tsql)
                            print('##################')

                    ########## 입력 4. line frequency ##########
                    # 평택 1~4 f_line: 60 고정; 송산 1 f_line: 745-617-SPI-4213; 송산 2 f_line: 745-617-CTI-4260
                    f_line = 60
                    
                    #print('Now motor_id:',motor_id)

                    # preprocess ~ diagnose for each motor sensor
                    device_dict[motor_sensor_name].preprocess(
                        timeseries_motor, freq_tags[config.get_on_off_id(motor_id)]
                    )
                    device_dict[motor_sensor_name].check_motor_status(
                        on_tags[config.get_on_off_id(motor_id)]
                    )
                    device_dict[motor_sensor_name].get_iqr_thresholds(2.25, 50)
                    device_dict[motor_sensor_name].get_features()
                    device_dict[motor_sensor_name].update()
                    # 설비가 꺼져있거나, 설비의 run_step < n_hist 일 시 결과로 0, False 을 줌
                    (
                        unbalance_amp,  #
                        unbalance,
                        misalignment_amp,
                        misalignment,
                        rotor_amp,
                        rotor,
                        bearing_amp,
                        or_fault,
                        ir_fault,
                        ball_fault,
                        train_fault,
                        motor_rms, # v_rms
                        motor_rms_alarm, # rms_alarm 단순 ISO threshold 4.5
                    ) = device_dict[motor_sensor_name].diagnose(
                        motor_threshold_jObj["unbalance"],
                        motor_threshold_jObj["bearing"],
                        motor_threshold_jObj["rotor"],
                        motor_threshold_jObj["rms"],
                    )
                    #print('device_dict:',device_dict)
                    motor_amp_this_run[i] = [
                        unbalance_amp,
                        misalignment_amp,
                        rotor_amp,
                        bearing_amp,
                        motor_rms,  # v_rms
                    ]
                    #print('motor_amp_this_run[i]',motor_amp_this_run[i])
                    motor_res_this_run[i] = [
                        unbalance,
                        misalignment,
                        rotor,
                        or_fault,
                        ir_fault,
                        ball_fault,
                        train_fault,
                        motor_rms_alarm, # rms_alarm 단순 ISO threshold 4.5
                    ]
                    #RMS 추출
                    rSql = f"INSERT IGNORE INTO TB_RMS(MOTOR_ID, CHANNEL_ID, ACQ_DATE, RMS) VALUES( '{motor_id}', '{motor_sensor_name}', '{acq_datetime[0]}', '{device_dict[motor_sensor_name].v_rms}' ) "
                    conn.insert(rSql)
                    #RMS 추출
                                        
                    #스펙트럼 데이터
                    y_list = ["{:.10f}".format(float(mag)) for mag in device_dict[motor_sensor_name].x_mag]
                    spSql = f"INSERT IGNORE INTO TB_SPECTRUM(MOTOR_ID, CHANNEL_ID, ACQ_DATE, DATA_ARRAY) VALUES('{motor_id}', '{motor_sensor_name}', '{acq_datetime[0]}', '{compress_array(y_list)}')"
                    conn.insert(spSql)
                    #스펙트럼 데이터
                    
                    #1x device_dict[motor_sensor_name].nxs_freq[1]
                    f1xSql = f"INSERT IGNORE INTO TB_FREQ(MOTOR_ID, CHANNEL_ID, ACQ_DATE, FREQ_TYPE, FREQ_VALUE) VALUES('{motor_id}', '{motor_sensor_name}', '{acq_datetime[0]}', '1', '{device_dict[motor_sensor_name].nxs_freq[1]}')"
                    conn.insert(f1xSql)
                    
                    #2x device_dict[motor_sensor_name].nxs_freq[1]
                    f2xSql = f"INSERT IGNORE INTO TB_FREQ(MOTOR_ID, CHANNEL_ID, ACQ_DATE, FREQ_TYPE, FREQ_VALUE) VALUES('{motor_id}', '{motor_sensor_name}', '{acq_datetime[0]}', '2', '{device_dict[motor_sensor_name].nxs_freq[2]}')"
                    conn.insert(f2xSql)
                    
                    #3x device_dict[motor_sensor_name].nxs_freq[1]
                    f3xSql = f"INSERT IGNORE INTO TB_FREQ(MOTOR_ID, CHANNEL_ID, ACQ_DATE, FREQ_TYPE, FREQ_VALUE) VALUES('{motor_id}', '{motor_sensor_name}', '{acq_datetime[0]}', '3', '{device_dict[motor_sensor_name].nxs_freq[3]}')"
                    conn.insert(f3xSql)
                    # print(f'end {motor_sensor_name}')
                ### diagnose pumps ###
                # run through each pump sensor
                ########## 입력 5. 진단 sensitivity (int, 1~10) ##########
                p_sensitivity = [
                    5,
                    5,
                    5,
                    5,
                ]  # pump sensitivity: [impeller, bearing, cavitation, rms]
                print("end motor")
                for i, pump_sensor_name in enumerate(pump_sensor_list):
                    # sample data 준비 --> 추후 실제 펌프 센서 데이터를 순서대로 불러오도록 변경
                    # data_folder = os.path.join("X:\\수자원공사\\diagnosis_test_data", pump_sensor_name)
                    # data_name = os.listdir(data_folder)[np.random.randint(0, len(os.listdir(data_folder)) - 1, 1)[0]]
                    # data_pump = pd.read_csv(os.path.join(data_folder, data_name), header=None)
                    # ########## 입력 6. pump vibration data (개개 펌프에 대하여) ##########
                    # timeseries_pump = np.asarray(data_pump).reshape([-1])

                    # raw data decompress zip base64 to ndarray
                    for row in rows:
                        #print('pump row[3]:',row[3])
                        #print('config.get_mapping_id(row[3]):',config.get_mapping_id(row[3]))
                        if config.get_mapping_id(row[3]) in pump_sensor_name:
                            #print('Now pump_sensor_name:'+pump_sensor_name)
                            timeseries_pump = decompress(row[4])
                            #print('timeseries_pump',timeseries_pump)
                            motor_id = row[0]
                            #타임웨이브
                            # 2초 데이터를 1초만 추출
                            timeseries_subset = timeseries_pump[:12800]
                            df = pd.DataFrame(timeseries_subset, columns=['y'])
                            # 인덱스를 'x'로 지정
                            df['y'] = df['y'].apply(lambda x: round(x, 10))
                            y_list = ["{:.10f}".format(float(value)) for value in df['y']]
                            tsql = f"INSERT IGNORE INTO TB_TIMEWAVE(MOTOR_ID, CHANNEL_ID, ACQ_DATE, DATA_ARRAY) VALUES( '{motor_id}', '{pump_sensor_name}', '{acq_datetime[0]}', '{compress_array(y_list)}' ) "
                            conn.insert(tsql)
                            #타임웨이브

                    ########## 입력 7. line frequency ##########
                    # 평택 1~4 f_line: 60 고정; 송산 1 f_line: 745-617-SPI-4213; 송산 2 f_line: 745-617-CTI-4260
                    f_line = 60

                    # preprocess ~ diagnose for each pump sensor
                    device_dict[pump_sensor_name].preprocess(
                        timeseries_pump, freq_tags[config.get_on_off_id(motor_id)]
                    )
                    device_dict[pump_sensor_name].check_pump_status(
                        on_tags[config.get_on_off_id(motor_id)]
                    )
                    device_dict[pump_sensor_name].get_iqr_thresholds(2.25, 50)
                    device_dict[pump_sensor_name].get_features()
                    device_dict[pump_sensor_name].update()
                    # 설비가 꺼져있거나, 설비의 run_step < n_hist 일 시 결과로 0, False 을 줌
                    (
                        cavitation_amp,
                        cavitation,
                        impeller_amp,
                        impeller,
                        bearing_amp,
                        or_fault,
                        ir_fault,
                        ball_fault,
                        train_fault,
                        pump_rms,
                        pump_rms_alarm,
                    ) = device_dict[pump_sensor_name].diagnose(
                        pump_threshold_jObj["impeller"],
                        pump_threshold_jObj["bearing"],
                        pump_threshold_jObj["cavitation"],
                        pump_threshold_jObj["rms"],
                    )
                    pump_amp_this_run[i] = [
                        impeller_amp,
                        cavitation_amp,
                        bearing_amp,
                        pump_rms,
                    ]
                    pump_res_this_run[i] = [
                        impeller,
                        cavitation,
                        or_fault,
                        ir_fault,
                        ball_fault,
                        train_fault,
                        pump_rms_alarm,
                    ]
                    #RMS 추출
                    rSql = f"INSERT IGNORE INTO TB_RMS(MOTOR_ID, CHANNEL_ID, ACQ_DATE, RMS) VALUES( '{motor_id}', '{pump_sensor_name}', '{acq_datetime[0]}', '{device_dict[pump_sensor_name].v_rms}' ) "
                    conn.insert(rSql)
                    #RMS 추출

                    #스펙트럼 데이터
                    y_list = ["{:.10f}".format(float(mag)) for mag in device_dict[pump_sensor_name].x_mag]

                    spSql = f"INSERT IGNORE INTO TB_SPECTRUM(MOTOR_ID, CHANNEL_ID, ACQ_DATE, DATA_ARRAY) VALUES('{motor_id}', '{pump_sensor_name}', '{acq_datetime[0]}', '{compress_array(y_list)}')"
                    conn.insert(spSql)
                    #스펙트럼 데이터
                    
                    #1x device_dict[pump_sensor_name].nxs_freq[1]
                    f1xSql = f"INSERT IGNORE INTO TB_FREQ(MOTOR_ID, CHANNEL_ID, ACQ_DATE, FREQ_TYPE, FREQ_VALUE) VALUES('{motor_id}', '{pump_sensor_name}', '{acq_datetime[0]}', '1', '{device_dict[pump_sensor_name].nxs_freq[1]}')"
                    conn.insert(f1xSql)
                    
                    #2x device_dict[pump_sensor_name].nxs_freq[1]
                    f2xSql = f"INSERT IGNORE INTO TB_FREQ(MOTOR_ID, CHANNEL_ID, ACQ_DATE, FREQ_TYPE, FREQ_VALUE) VALUES('{motor_id}', '{pump_sensor_name}', '{acq_datetime[0]}', '2', '{device_dict[pump_sensor_name].nxs_freq[2]}')"
                    conn.insert(f2xSql)
                    
                    #3x device_dict[pump_sensor_name].nxs_freq[1]
                    f3xSql = f"INSERT IGNORE INTO TB_FREQ(MOTOR_ID, CHANNEL_ID, ACQ_DATE, FREQ_TYPE, FREQ_VALUE) VALUES('{motor_id}', '{pump_sensor_name}', '{acq_datetime[0]}', '3', '{device_dict[pump_sensor_name].nxs_freq[3]}')"
                    conn.insert(f3xSql)
                print("end pump")
                # integrate diagnosis result for each motor/pump

                #print('motor_amp_this_run',motor_amp_this_run)
                #print('motor_res_this_run',motor_res_this_run)
                
                motor_result = merge_by_motor(motor_amp_this_run, motor_res_this_run)
                pump_result = merge_by_pump(pump_amp_this_run, pump_res_this_run)

                motor_rms_threshold = -0.44 * motor_threshold_jObj["rms"] + 6.7  # 4.5
                pump_rms_threshold = -0.38 * pump_threshold_jObj["rms"] + 8     # 6.1

                print('motor_result', motor_result)
                print('pump_result', pump_result)
                
                print(f"{acq_datetime[0]} end")
                keys = list(motor_result.keys())
                for key in keys:
                    print('{} motor_result - unbalance_amp:{} misalignment_amp:{} rotor_amp:{} NDE_amp{} NDE_rms_amp{}'.format(key, motor_result[key]['unbalance_amp'], motor_result[key]['misalignment_amp'],motor_result[key]['rotor_amp'], motor_result[key]['NDE_amp'],motor_result[key]['NDE_rms_amp']))
                    sql = f"""INSERT INTO TB_AI_DIAG_MOTOR(motor_id, center_id, acq_date, unbalance_amp,unbalance_alarm,misalignment_amp,misalignment_alarm,rotor_amp
                    ,rotor_alarm,de_amp,DE_rms_amp,de_bpfo_alarm,DE_BPFI_alarm,DE_BSF_alarm,DE_FTF_alarm,DE_rms_alarm,NDE_amp,NDE_rms_amp,NDE_BPFO_alarm,NDE_BPFI_alarm
                    ,NDE_BSF_alarm,NDE_FTF_alarm,NDE_rms_alarm) VALUES('{config.get_motor_id(key)}','{center_id}','{acq_datetime[0]}',{motor_result[key]['unbalance_amp']}
                    ,{motor_result[key]['unbalance_alarm']},{motor_result[key]['misalignment_amp']},{motor_result[key]['misalignment_alarm']},{motor_result[key]['rotor_amp']}
                    ,{motor_result[key]['rotor_alarm']},{motor_result[key]['DE_amp']},{motor_result[key]['DE_rms_amp']},{motor_result[key]['DE_BPFO_alarm']}
                    ,{motor_result[key]['DE_BPFI_alarm']},{motor_result[key]['DE_BSF_alarm']},{motor_result[key]['DE_FTF_alarm']},{motor_result[key]['DE_rms_alarm']}
                    ,{motor_result[key]['NDE_amp']},{motor_result[key]['NDE_rms_amp']},{motor_result[key]['NDE_BPFO_alarm']},{motor_result[key]['NDE_BPFI_alarm']}
                    ,{motor_result[key]['NDE_BSF_alarm']},{motor_result[key]['NDE_FTF_alarm']},{motor_result[key]['NDE_rms_alarm']})"""
                    #print('Motor sql:',sql)
                    conn.insert(sql)

                keys = list(pump_result.keys())
                for key in keys:
                    sql = f"""INSERT INTO TB_AI_DIAG_PUMP(pump_id, center_id, acq_date, impeller_amp,impeller_alarm,cavitation_amp,cavitation_alarm,de_amp,DE_rms_amp
                    ,de_bpfo_alarm,DE_BPFI_alarm,DE_BSF_alarm,DE_FTF_alarm,DE_rms_alarm,NDE_amp,NDE_rms_amp,NDE_BPFO_alarm,NDE_BPFI_alarm
                    ,NDE_BSF_alarm,NDE_FTF_alarm,NDE_rms_alarm) VALUES('{config.get_pump_id(key)}','{center_id}','{acq_datetime[0]}',{pump_result[key]['impeller_amp']}
                    ,{pump_result[key]['impeller_alarm']},{pump_result[key]['cavitation_amp']},{pump_result[key]['cavitation_alarm']},{pump_result[key]['DE_amp']}
                    ,{pump_result[key]['DE_rms_amp']},{pump_result[key]['DE_BPFO_alarm']}
                    ,{pump_result[key]['DE_BPFI_alarm']},{pump_result[key]['DE_BSF_alarm']},{pump_result[key]['DE_FTF_alarm']},{pump_result[key]['DE_rms_alarm']}
                    ,{pump_result[key]['NDE_amp']},{pump_result[key]['NDE_rms_amp']},{pump_result[key]['NDE_BPFO_alarm']},{pump_result[key]['NDE_BPFI_alarm']}
                    ,{pump_result[key]['NDE_BSF_alarm']},{pump_result[key]['NDE_FTF_alarm']},{pump_result[key]['NDE_rms_alarm']})"""
                    #print('Pump sql:',sql)
                    conn.insert(sql)
                conn.insert(
                    f"UPDATE TB_MOTOR SET proc_stat = 1 WHERE acq_date = '{acq_datetime[0]}';" 
                )
                print(f"{acq_datetime[0]} data insert end")
                end2 = time.time()
                print(f"end diagnosis time = {end2 - end}")
                print("### END ###")
                # update step number
        #conn.close()
        #exit()
        
        except Exception as main_ex:
            print(f"main MainProcess Down!! : {main_ex}")
        finally:
            try:
                conn.close()
            except Exception as close_ex:
                print(close_ex)
        time.sleep(5)


if __name__ == "__main__":
    main()
