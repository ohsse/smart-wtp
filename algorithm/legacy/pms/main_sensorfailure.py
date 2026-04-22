import base64
import gzip
import json
import os
import sys
import time
from dateutil import tz

import numpy as np

# sys.path.append(os.getcwd())
sys.path.append(
    os.path.dirname(
        os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    )
)

from datetime import datetime, timedelta

from  util.utils.db import DBConnect

from config.config import config
from vibrationsensor import check_vibrationsensor

def decompress(data):
     byte_data = gzip.decompress(base64.standard_b64decode(data))
     temp = byte_data.decode("utf-16")
     temp_jarr = json.loads(temp)
     return np.array(list(map(lambda x: float(x), temp_jarr)))

## sim  data 형태를 모름 ㅠ 임시로 처리
#def decompress(data):
#    temp_jarr = data[1:-1].replace("  ", " ").split(" ")
#    return np.array(list(map(lambda x: float(x), temp_jarr)))


def sensorfailure():
    maxfail_num = 10
    # sensorfailure_th = 0.1
    
    # 한국 시간대 설정
    KST = tz.gettz('Asia/Seoul')
    
    center_id = 'hakya'

    ip, port, name, id, pw = config.get_db_info()
    # sensorfailure_algorithm = check_vibrationsensor()
    algorithm_dict = {}
    algorithm_dict["motor_01"] = check_vibrationsensor()
    algorithm_dict["motor_02"] = check_vibrationsensor()
    algorithm_dict["motor_03"] = check_vibrationsensor()
    algorithm_dict["motor_04"] = check_vibrationsensor()
    algorithm_dict["motor_04"] = check_vibrationsensor()
    algorithm_dict["motor_06"] = check_vibrationsensor()
    while True:
        try:
            conn = DBConnect(ip, id, pw, port, name)

            cur = conn.get_cursor()
            cur.execute(
                "SELECT threshold from TB_THRESHOLD where table_id = 'songsusensor'"
            )
            rows = cur.fetchall()
            threshold_jObj = json.loads(rows[0][0])
            
             # 현재 시간을 한국 시간대로 변환
            current_time_korea = datetime.now(KST)
            # 원하는 형식으로 시간 포맷
            now_acq_date_time = current_time_korea.strftime('%Y-%m-%d %H:%M:%S')
            
            # 2분 전의 시간 계산
            time_two_minutes_before = current_time_korea - timedelta(minutes=2)
            two_minutes_before_formatted = time_two_minutes_before.strftime('%Y-%m-%d %H:%M:00')
            now_acq_date_time =  two_minutes_before_formatted
            print(now_acq_date_time)

            # 계산 안된 데이터들 있는지 조회
            cur.execute(
                f"SELECT acq_date from TB_MOTOR where proc_stat = 1 and acq_date > '{now_acq_date_time}' group by acq_date order by acq_date asc;"  ### sim TB_MOTOR
            )
            acq_date_rows = cur.fetchall()

            if len(acq_date_rows) > 0:
                last_acq_date = acq_date_rows[-1]

            for acq_datetime in acq_date_rows:
                new_data_flag = False
                if last_acq_date is acq_datetime:
                    new_data_flag = True
                    time.sleep(3)

                acq_date = datetime.strftime(acq_datetime[0], "%Y-%m-%d %H:%M:%S")
                # motor 별로 아이디 가져오기
                cur.execute(
                    f"SELECT DISTINCT motor_id from TB_MOTOR where acq_date = '{acq_datetime[0]}' ORDER BY motor_id;"  ### sim TB_MOTOR
                )
                motor_rows = cur.fetchall()

                # 데이터 계측 시점과 가장 가까운 시간 가져오기
                # cur.execute(f"SELECT func_get_abs_time('{acq_datetime[0]}', '', 1)")
                ####### sim ( *** 위 코드의 의도와 맞게 확인 필요 : scada_time 추출하는 sql *** )
                ## 위에 sql문이 func_get_abs_time가 정의되지 않아서 실행이 안되는데, 어디서 가져오지 ?
                cur.execute(
                    f"SELECT acq_date from TB_PUMP_SCADA WHERE acq_date = '{acq_datetime[0]}' order by acq_date desc"
                )  ### test sim
                scada_time = cur.fetchall()[0][0]
                # on 데이터 가져오기
                cur.execute(
                    f"SELECT pump_scada_id, eq_on, frequency FROM TB_PUMP_SCADA WHERE acq_date = '{scada_time}' order by acq_date desc"
                )
                on_rows = cur.fetchall()
                on_tags = {}
                for row in on_rows:
                    eq_on = row[1]
                    on_tags[row[0]] = eq_on

                for motor_row in motor_rows:
                    motor_id = motor_row[0]

                    # off 상태였는지 확인
                    if on_tags[config.get_on_off_id(motor_id)] == False:
                        query = f"INSERT INTO tb_diag_motor_sensor_failure(motor_id, center_id, acq_date, rms_ratio, vibsensor_fail) VALUES({motor_id}, 'gumi', '{acq_date}', 0, 0)"
                    else:
                        cur.execute(
                            f"SELECT center_id, channel_id, data_array from TB_MOTOR where acq_date = '{acq_datetime[0]}' AND motor_id = '{motor_id}' ORDER BY channel_id;"  ### sim TB_MOTOR
                        )
                        raws = cur.fetchall()

                        # P_DE, P_NDE, M_DE, M_NDE
                        raw_array = []
                        for raw in raws:
                            raw_array.append(decompress(raw[2]))

                        failure_dict = algorithm_dict[
                            motor_id
                        ].check_vibrationsensorfailure(
                            acq_date,
                            raw_array[3],  # M_NDE
                            raw_array[2],  # M_DE
                            raw_array[1],  # P_NDE
                            raw_array[0],  # P_DE
                            threshold_jObj["sensorfailure_th"],
                            maxfail_num,
                        )
                        query = f"""INSERT INTO tb_diag_motor_sensor_failure(motor_id, center_id, acq_date, rms_ratio, M_NDE_sensor_fault, M_DE_sensor_fault, P_NDE_sensor_fault
                            , P_DE_sensor_fault) VALUES('{motor_id}', '{center_id}', '{acq_date}', {failure_dict['min/max']}, {failure_dict['M_NDE_sensor_fault']}
                            , {failure_dict['M_DE_sensor_fault']}, {failure_dict['P_NDE_sensor_fault']}, {failure_dict['P_DE_sensor_fault']})"""
                    conn.insert(query)
                    #rawdata 지우는것은 보류
                    #conn.insert(
                    #     f"DELETE FROM TB_MOTOR WHERE acq_date = '{acq_datetime[0]}' AND motor_id = '{motor_id}';"  ### sim TB_MOTOR
                    #)
                    conn.insert(
                    f"UPDATE TB_MOTOR SET proc_stat = 2  WHERE acq_date = '{acq_datetime[0]}' AND motor_id = '{motor_id}';" 
                     )
                    # conn.insert(f"UPDATE TB_PUMP_SCADA SET proc_stat = 1 where center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';")
        except Exception as main_ex:
            print(f"sensorfailure main process down!! : {main_ex}")
        finally:
            try:
                conn.close()
            except Exception as close_ex:
                print(close_ex)
            time.sleep(5)


if __name__ == "__main__":
    sensorfailure()
