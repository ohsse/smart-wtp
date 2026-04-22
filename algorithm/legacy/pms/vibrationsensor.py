from collections import deque

import numpy as np


class check_vibrationsensor:
    def __init__(self):

        # self.vibrationsensorfailure_value = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10)
        self.M_NDE_sensorfailure_value = deque([0, 0, 0, 0, 0], maxlen=5)
        self.M_DE_sensorfailure_value = deque([0, 0, 0, 0, 0], maxlen=5)
        self.P_NDE_sensorfailure_value = deque([0, 0, 0, 0, 0], maxlen=5)
        self.P_DE_sensorfailure_value = deque([0, 0, 0, 0, 0], maxlen=5)
        self.vibrationsensorfailure_dict = {
            "Time": 0,
            "min/max": 0,
            "sensorfailure_th": 0,
            "M_NDE_sensor_fault": False,
            "M_DE_sensor_fault": False,
            "P_NDE_sensor_fault": False,
            "P_DE_sensor_fault": False,
        }

    def check_vibrationsensorfailure(
        self,
        Time,
        M_NDE: np.ndarray,
        M_DE: np.ndarray,
        P_NDE: np.ndarray,
        P_DE: np.ndarray,
        sensorfailure_th,
        maxfail_num: int,
    ):
        """진동 센서 고장진단

        Parameters
        ----------
        vibrationdata: np.ndarray
            진동데이터
        sensorfailure_th: float
            센서고장 횟수 Threshold
        if_vibrationsensor_fail: True/False
            센서 고장 유무
        maxfail_num:int
            센서고장 횟수

        Returns
        -------
        self.vibrationsensorfailure_dict["min/max"]: float
            Rms 최소/ 최대값 Ratio
        self.vibrationsensorfailure_dict["sensorfailure_th"]: float
            센서고장 Threshold
        self.vibrationsensorfailure_dict["vibsensor_fail"]: True/ False
            센서고장 유무


        """
        # maxfail_num = 10
        # sensorfailure_th = 0.1
        eps = 1e-6
        N = M_NDE.shape[0]
        M_NDE_rms = np.sqrt(np.sum((M_NDE ** 2)) / N) + eps
        M_DE_rms = np.sqrt(np.sum((M_DE ** 2)) / N) + eps
        P_NDE_rms = np.sqrt(np.sum((P_NDE ** 2)) / N) + eps
        P_DE_rms = np.sqrt(np.sum((P_DE ** 2)) / N) + eps
        all_sensor = np.array([M_NDE_rms, M_DE_rms, P_NDE_rms, P_DE_rms])
        max_rms = max(M_NDE_rms, M_DE_rms, P_NDE_rms, P_DE_rms)
        min_rms = min(M_NDE_rms, M_DE_rms, P_NDE_rms, P_DE_rms)
        all_sensor_bool = 1 * (all_sensor == min_rms)
        if_sensor_problem = min_rms < max_rms * sensorfailure_th

        if if_sensor_problem:
            self.M_NDE_sensorfailure_value.append(all_sensor_bool[0])
            self.M_DE_sensorfailure_value.append(all_sensor_bool[1])
            self.P_NDE_sensorfailure_value.append(all_sensor_bool[2])
            self.P_DE_sensorfailure_value.append(all_sensor_bool[3])
        else:
            self.M_NDE_sensorfailure_value.append(0)
            self.M_DE_sensorfailure_value.append(0)
            self.P_NDE_sensorfailure_value.append(0)
            self.P_DE_sensorfailure_value.append(0)

        if_M_NDE_sensorfailure_fail = sum(self.M_NDE_sensorfailure_value) == maxfail_num
        if_M_DE_sensorfailure_fail = sum(self.M_DE_sensorfailure_value) == maxfail_num
        if_P_NDE_sensorfailure_fail = sum(self.P_NDE_sensorfailure_value) == maxfail_num
        if_P_DE_sensorfailure_fail = sum(self.P_DE_sensorfailure_value) == maxfail_num

        # self.vibrationsensorfailure_value.append(if_sensor_problem)
        # if_alarm = (if_voltagevariation_fail + if_overcurrent_fail + if_currentunbalance_fail + if_voltageunbalance_fail + backwash_I_fault) > 0
        # if_vibrationsensor_fail = sum(self.vibrationsensorfailure_value) == maxfail_num
        self.vibrationsensorfailure_dict["Time"] = Time
        self.vibrationsensorfailure_dict["min/max"] = min_rms / max_rms
        self.vibrationsensorfailure_dict["sensorfailure_th"] = sensorfailure_th
        self.vibrationsensorfailure_dict["M_NDE_sensor_fault"] = if_M_NDE_sensorfailure_fail
        self.vibrationsensorfailure_dict["M_DE_sensor_fault"] = if_M_DE_sensorfailure_fail
        self.vibrationsensorfailure_dict["P_NDE_sensor_fault"] = if_P_NDE_sensorfailure_fail
        self.vibrationsensorfailure_dict["P_DE_sensor_fault"] = if_P_DE_sensorfailure_fail

        # self.vibrationsensorfailure_dict["vibsensor_fail"] = if_vibrationsensor_fail

        return self.vibrationsensorfailure_dict



"""
min 10
max 500

max 1/10   50

4개 센서 전부랑 min 비교
rms + 0.00001

min 값이랑 비교하는데 
min 값이 max 의 1/10 보다 크면 센서 문제가 없다 그래서 else문으로 빠진다
만약 작으면 if_sensor_problem이 True고 all_sensor_bool 값이 전달이 된다.
"""