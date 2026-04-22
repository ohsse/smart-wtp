from collections import deque


class bearingtemperature:
    def __init__(self, data: dict):
        self.data = data
        self.M_DE_bearing_temp_fail_value = deque(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10
        )
        self.M_NDE_bearing_temp_fail_value = deque(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10
        )
        self.P_DE_bearing_temp_fail_value = deque(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10
        )
        self.P_NDE_bearing_temp_fail_value = deque(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10
        )

        self.bearingtemp_dict = {
            "Time": 0,
            "M_DE_bearing_temp": 0,
            "M_NDE_bearing_temp": 0,
            "P_DE_bearing_temp": 0,
            "P_NDE_bearing_temp": 0,
            "M_DE_bearing_temp_fault": False,
            "M_NDE_bearing_temp_fault": False,
            "P_DE_bearing_temp_fault": False,
            "P_NDE_bearing_temp_fault": False,
            "alarm": False,
        }

    # bearing max temp = 80, 49.23 = bearingmaxtemp-max(air_temp)
    def get_bearingtempboundary(air_temp):
        """베어링 최대온도(제조사 기준)
        Parameters
        ----------
        air_temp : float
            외기온도 추정
        Returns
        -------
        T_max: float
            최대 베어링 온도
        """
        # 49.23 = bearing 최고온도-airtemp
        if air_temp < 5:
            air_temp = 5
        elif air_temp > 31:
            air_temp = 31
        
        T_max = air_temp + 49

        return T_max

    def calculate_tempthresholdbearing(
        self, time, sensitivity_bearing_temp, Mtemp_DE, Mtemp_NDE, Ptemp_DE, Ptemp_NDE
    ):
        """월/일/시간 시점의 외기온도 불러오기

        Parameters
        ----------
        time : datetime
            실시간 시간데이터
        data: dict
            월/일/시간에서의 외기온도 dictionary
        keys: str
            datetime 을 string으로 변환시킨 데이터
        sensitivity_bearing_temp: float
            베어링온도 Threshold 민감도
        th_factor: float
            Threshold를 1로 만들어주기위한 스케일링 factor

        Returns
        -------
        T_max : float
            표준기반 추정 베어링온도 Threshold
        M_DE_bearing_temp: float
            th_factor와 sensitivity 로 스케일링된 모터 베어링 DE 온도
        M_NDE_bearing_temp: float
            th_factor와 sensitivity 로 스케일링된 모터 베어링 NDE 온도
        P_DE_bearing_temp: float
            th_factor와 sensitivity 로 스케일링된 펌프 베어링 DE 온도
        P_NDE_bearing_temp: float
            th_factor와 sensitivity 로 스케일링된 펌프 베어링 DE 온도
        M_DE_bearing_temp_fault: float
            모터 DE 베어링온도 fault 유무
        M_NDE_bearing_temp_fault: float
            모터 NDE 베어링온도 fault 유무
        P_DE_bearing_temp_fault: float
            펌프 DE 베어링온도 fault 유무
        P_NDE_bearing_temp_fault: float
            펌프 NDE 베어링온도 fault 유무
        """
        t_ = str(time)
        month = t_[5:7]
        day = t_[8:10]
        hour = t_[11:13]
        keys = str(month) + "-" + str(day) + "-" + str(hour)
        T_max = self.get_bearingtempboundary(self.data[keys])

        th_factor = (1 / T_max) / 50
        M_DE_bearing_temp = Mtemp_DE * th_factor * sensitivity_bearing_temp
        M_NDE_bearing_temp = Mtemp_NDE * th_factor * sensitivity_bearing_temp
        P_DE_bearing_temp = Ptemp_DE * th_factor * sensitivity_bearing_temp
        P_NDE_bearing_temp = Ptemp_NDE * th_factor * sensitivity_bearing_temp

        if M_DE_bearing_temp > 1:
            M_DE_bearing_temp_fault = 1
        else:
            M_DE_bearing_temp_fault = 0

        if M_NDE_bearing_temp > 1:
            M_NDE_bearing_temp_fault = 1
        else:
            M_NDE_bearing_temp_fault = 0

        if P_DE_bearing_temp > 1:
            P_DE_bearing_temp_fault = 1
        else:
            P_DE_bearing_temp_fault = 0

        if P_NDE_bearing_temp > 1:
            P_NDE_bearing_temp_fault = 1
        else:
            P_NDE_bearing_temp_fault = 0

        return (
            M_DE_bearing_temp,
            M_NDE_bearing_temp,
            P_DE_bearing_temp,
            P_NDE_bearing_temp,
            M_DE_bearing_temp_fault,
            M_NDE_bearing_temp_fault,
            P_DE_bearing_temp_fault,
            P_NDE_bearing_temp_fault,
        )

    def check_bearingtempfailure(
        self,
        time,
        Mtemp_DE,
        Mtemp_NDE,
        Ptemp_DE,
        Ptemp_NDE,
        sensitivity_bearing_temp,
        maxfail_num,
    ):
        """권선온도고장

        Parameters
        ----------
        Mtemp_DE : float
            모터 베어링온도 DE
        Mtemp_NDE: float
            모터 베어링온도 NDE
        Ptemp_DE: float
            펌프 베어링온도 DE
        Ptemp_NDE
            펌프 베어링온도 NDE
        maxfail_num: int
            오류 개수 Threshold
        sensitivity_bearing_temp: float
            베어링온도 Threshold 민감도
        Returns
        -------
        if_M_DE_bearing_temp_fail: 1 or 0
            모터 DE 베어링온도가 10분동안 오류를 보내면 고장 alarm을 보냄
        if_M_NDE_bearing_temp_fail: 1 or 0
            모터 NDE 베어링온도가 10분동안 오류를 보내면 고장 alarm을 보냄
        if_P_DE_bearing_temp_fail: 1 or 0
            펌프 DE 베어링온도가 10분동안 오류를 보내면 고장 alarm을 보냄
        if_P_NDE_bearing_temp_fail: 1 or 0
            펌프 NDE 베어링온도가 10분동안 오류를 보내면 고장 alarm을 보냄
        if_alarm: bool
            4개의 베어링온도중 하나라도 고장이면 알람
        """

        (
            M_DE_bearing_temp,
            M_NDE_bearing_temp,
            P_DE_bearing_temp,
            P_NDE_bearing_temp,
            M_DE_bearing_temp_fault,
            M_NDE_bearing_temp_fault,
            P_DE_bearing_temp_fault,
            P_NDE_bearing_temp_fault,
        ) = self.calculate_tempthresholdbearing(
            time, sensitivity_bearing_temp, Mtemp_DE, Mtemp_NDE, Ptemp_DE, Ptemp_NDE
        )
        self.M_DE_bearing_temp_fail_value.append(M_DE_bearing_temp_fault)
        self.M_NDE_bearing_temp_fail_value.append(M_NDE_bearing_temp_fault)
        self.P_DE_bearing_temp_fail_value.append(P_DE_bearing_temp_fault)
        self.P_NDE_bearing_temp_fail_value.append(P_NDE_bearing_temp_fault)

        self.bearingtemp_dict["Time"] = time
        self.bearingtemp_dict["M_DE_bearing_temp"] = M_DE_bearing_temp
        self.bearingtemp_dict["M_NDE_bearing_temp"] = M_NDE_bearing_temp
        self.bearingtemp_dict["P_DE_bearing_temp"] = P_DE_bearing_temp
        self.bearingtemp_dict["P_NDE_bearing_temp"] = P_NDE_bearing_temp

        if_M_DE_bearing_temp_fail = (
            sum(self.M_DE_bearing_temp_fail_value) == maxfail_num
        )
        if_M_NDE_bearing_temp_fail = (
            sum(self.M_NDE_bearing_temp_fail_value) == maxfail_num
        )
        if_P_DE_bearing_temp_fail = (
            sum(self.P_DE_bearing_temp_fail_value) == maxfail_num
        )
        if_P_NDE_bearing_temp_fail = (
            sum(self.P_NDE_bearing_temp_fail_value) == maxfail_num
        )

        if_alarm = (
            if_M_DE_bearing_temp_fail
            + if_M_NDE_bearing_temp_fail
            + if_P_DE_bearing_temp_fail
            + if_P_NDE_bearing_temp_fail
        ) > 0
        self.bearingtemp_dict["M_DE_bearing_temp_fault"] = if_M_DE_bearing_temp_fail
        self.bearingtemp_dict["M_NDE_bearing_temp_fault"] = if_M_NDE_bearing_temp_fail
        self.bearingtemp_dict["P_DE_bearing_temp_fault"] = if_P_DE_bearing_temp_fail
        self.bearingtemp_dict["P_NDE_bearing_temp_fault"] = if_P_NDE_bearing_temp_fail
        self.bearingtemp_dict["alarm"] = if_alarm

        return self.bearingtemp_dict
