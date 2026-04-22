import json
import os
import pickle
import sys
import time
from dateutil import tz

# sys.path.append(os.getcwd())
sys.path.append(
    os.path.dirname(
        os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    )
)

from datetime import datetime, timedelta

from util.utils.db import DBConnect

from Bearingtemperature import bearingtemperature
from config.config import config
from Windingtemperature import windingtemperature


def PMSpump():
    sensitivity_bearing_temp = 50
    sensitivity_winding_temp = 50
    maxfail_num = 10
    v_rated = 380
    I_rated = 97.3
    
    # 한국 시간대 설정
    KST = tz.gettz('Asia/Seoul')
    
    center_id = 'hakya'

    ip, port, name, id, pw = config.get_db_info()

    with open("hours0819.pkl", "rb") as fr:
        airtemp_dict = pickle.load(fr)

        # threshold

        # chaksoo
    # bearing_temp_algorithm = bearingtemperature(airtemp_dict)
    # winding_temp_algorithm = windingtemperature(airtemp_dict)

    algorithm_dict = {}
    algorithm_dict["pump_scada_01"] = bearingtemperature(airtemp_dict)
    algorithm_dict["pump_scada_02"] = bearingtemperature(airtemp_dict)
    algorithm_dict["pump_scada_03"] = bearingtemperature(airtemp_dict)
    algorithm_dict["pump_scada_04"] = bearingtemperature(airtemp_dict)
    algorithm_dict["pump_scada_05"] = bearingtemperature(airtemp_dict)
    algorithm_dict["pump_scada_06"] = bearingtemperature(airtemp_dict)

    ## sim
    ## db에 wind가 없음, wind:권선
    algorithm_dict["wind_pump_scada_01"] = windingtemperature(airtemp_dict)
    algorithm_dict["wind_pump_scada_02"] = windingtemperature(airtemp_dict)
    algorithm_dict["wind_pump_scada_03"] = windingtemperature(airtemp_dict)
    algorithm_dict["wind_pump_scada_04"] = windingtemperature(airtemp_dict)
    algorithm_dict["wind_pump_scada_05"] = windingtemperature(airtemp_dict)
    algorithm_dict["wind_pump_scada_06"] = windingtemperature(airtemp_dict)

    while True:
        try:
            conn = DBConnect(ip, id, pw, port, name)

            cur = conn.get_cursor()

            ## sim ## 안쓰는 코드
            # cur.execute(
            #     "SELECT threshold from TB_THRESHOLD where table_id = 'gac_backwash_pump'"
            # )
            # rows = cur.fetchall()
            # threshold_jObj = json.loads(rows[0][0])
            
            # 현재 시간을 한국 시간대로 변환
            current_time_korea = datetime.now(KST)
            # 원하는 형식으로 시간 포맷
            now_acq_date_time = current_time_korea.strftime('%Y-%m-%d %H:%M:00')
            
            # 2분 전의 시간 계산
            time_two_minutes_before = current_time_korea - timedelta(minutes=2)
            two_minutes_before_formatted = time_two_minutes_before.strftime('%Y-%m-%d %H:%M:%S')
            now_acq_date_time =  two_minutes_before_formatted
            print(now_acq_date_time)

            # 계산 안된 데이터들 있는지 조회
            cur.execute(
                f"SELECT acq_date from TB_PUMP_SCADA where proc_stat = 0 and acq_date > '{now_acq_date_time}' group by acq_date order by acq_date asc;"
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
                # 시간별로 모든 설비의 데이터를 가져와서 계산

                cur.execute(
                    f"""SELECT pump_scada_id, center_id, r_temp, s_temp, t_temp, brg_motor_de_temp, brg_motor_nde_temp
                    , brg_pump_de_temp, brg_pump_nde_temp from TB_PUMP_SCADA where proc_stat = 0 and acq_date = '{acq_date}' """
                )

                datas = cur.fetchall()
                for data in datas:
                    print(acq_date, data)
                    flag = False
                    try:
                        failure_dict = algorithm_dict[data[0]].check_bearingtempfailure(
                            acq_date,
                            data[5],
                            data[6],
                            data[7],
                            data[8],
                            sensitivity_bearing_temp,
                            maxfail_num,
                        )
                        conn.insert(
                            f"""INSERT INTO TB_DIAG_MOTOR_PUMP(center_id,pump_scada_id,acq_date,M_DE_bearing_temp,M_NDE_bearing_temp,P_DE_bearing_temp,P_NDE_bearing_temp
                        ,M_DE_bearing_temp_fault,M_NDE_bearing_temp_fault,P_DE_bearing_temp_fault,P_NDE_bearing_temp_fault) 
                        VALUES('{data[1]}','{data[0]}','{acq_date}',{failure_dict["M_DE_bearing_temp"]},{failure_dict["M_NDE_bearing_temp"]},{failure_dict["P_DE_bearing_temp"]}
                        ,{failure_dict["P_NDE_bearing_temp"]},{failure_dict["M_DE_bearing_temp_fault"]},{failure_dict["M_NDE_bearing_temp_fault"]}
                        ,{failure_dict["P_DE_bearing_temp_fault"]},{failure_dict["P_NDE_bearing_temp_fault"]});"""
                        )
                        '''
                        conn.insert(
                            f"UPDATE TB_PUMP_SCADA SET proc_stat = 1 where center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';"
                        )
                        '''
                        flag = True
                    except Exception as algorithm_ex:
                        print(acq_date, data, "PMSpump winding temp exception")
                        print(algorithm_ex)
                        '''
                        if new_data_flag is False:
                            conn.insert(
                                f"""UPDATE TB_PUMP_SCADA SET proc_stat = -1 where center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';"""
                            )
                        ''' 
                    try:
                        failure_dict = algorithm_dict[
                            f"wind_{data[0]}"
                        ].check_wingdingtempfailure(
                            acq_date,
                            data[2],
                            data[3],
                            data[4],
                            sensitivity_winding_temp,
                            maxfail_num,
                        )
                        # if flag is False:
                        conn.insert(
                            f"""INSERT INTO TB_DIAG_MOTOR_PUMP_WINDING(center_id,pump_scada_id,acq_date,winding_tempR,winding_tempS,winding_tempT
                            ,winding_tempR_fault,winding_tempS_fault,winding_tempT_fault) 
                            VALUES('{data[1]}','{data[0]}','{acq_date}',{failure_dict["winding_tempR"]},{failure_dict["winding_tempS"]},{failure_dict["winding_tempT"]}
                            ,{failure_dict["winding_tempR_fault"]},{failure_dict["winding_tempS_fault"]},{failure_dict["winding_tempT_fault"]}) 
                            ON DUPLICATE KEY UPDATE winding_tempR = {failure_dict['winding_tempR']},winding_tempS = {failure_dict['winding_tempS']}
                            ,winding_tempT = {failure_dict['winding_tempT']},winding_tempR_fault = {failure_dict['winding_tempR_fault']}
                            ,winding_tempS_fault = {failure_dict['winding_tempS_fault']},winding_tempT_fault = {failure_dict['winding_tempT_fault']};"""
                        )
                        # else:
                        # conn.insert(f"UPDATE TB_DIAG_MOTOR_PUMP SET winding_tempR = {failure_dict['winding_tempR']} WHERE center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';")
                        # conn.insert(f"UPDATE TB_DIAG_MOTOR_PUMP SET winding_tempS = {failure_dict['winding_tempS']} WHERE center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';")
                        # conn.insert(f"UPDATE TB_DIAG_MOTOR_PUMP SET winding_tempT = {failure_dict['winding_tempT']} WHERE center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';")
                        # conn.insert(f"UPDATE TB_DIAG_MOTOR_PUMP SET winding_tempR_fault = {failure_dict['winding_tempR_fault']} WHERE center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';")
                        # conn.insert(f"UPDATE TB_DIAG_MOTOR_PUMP SET winding_tempS_fault = {failure_dict['winding_tempS_fault']} WHERE center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';")
                        # conn.insert(f"UPDATE TB_DIAG_MOTOR_PUMP SET winding_tempT_fault = {failure_dict['winding_tempT_fault']} WHERE center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';")

                        conn.insert(
                            f"UPDATE TB_PUMP_SCADA SET proc_stat = 2 where center_id = '{data[1]}' AND pump_scada_id = '{data[0]}' AND acq_date = '{acq_date}';"
                        )
                        # flag = True
                    except Exception as algorithm_ex:
                        print(
                            acq_date, algorithm_ex, "PMSpump winding temp exception"
                        )

                    # print("")

        except Exception as main_ex:
            print(f"PMSpump main process down!! : {main_ex}")
        finally:
            try:
                conn.close()
            except Exception as close_ex:
                print(close_ex)
            time.sleep(5)


if __name__ == "__main__":
    PMSpump()
