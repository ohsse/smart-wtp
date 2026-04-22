from collections import deque


class windingtemperature:
    def __init__(
        self,
        data: dict,
    ):
        self.data = data
        self.winding_tempR_fail_value = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10)
        self.winding_tempS_fail_value = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10)
        self.winding_tempT_fail_value = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10)

        self.windingtemp_dict = {
            "Time": 0,
            "winding_tempR": 0,
            "winding_tempS": 0,
            "winding_tempT": 0,
            "winding_tempR_fault": False,
            "winding_tempS_fault": False,
            "winding_tempT_fault": False,
            "alarm": False,
        }

    def get_windingtempboundary(self, air_temp):
        """NEMA표준 최대 권선온도
        Parameters
        ----------

        Returns
        -------
        T_max : float

        """
        # windingtemp_th =105
        T_max = 105 + (40 - air_temp) * (1 - ((155 - (40 + 105)) / 80))

        return T_max

    def calculate_tempthreshold(
        self,
        time: float,
        winding_tempR,
        winding_tempS,
        winding_tempT,
        sensitivity_winding_temp,
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
        sensitivity_winding_temp: float
            권선온도 Threshold 민감도
        th_factor: float
            Threshold를 1로 만들어주기위한 스케일링 factor
        Returns
        -------
        T_max : float
            표준기반 추정 권선온도 Threshold
        ch_winding_tempR: float
            th_factor와 sensitivity 로 스케일링된 권선온도 R상
        ch_winding_tempS: float
            th_factor와 sensitivity 로 스케일링된 권선온도 S상
        ch_winding_tempT: float
            th_factor와 sensitivity 로 스케일링된 권선온도 T상
        winding_tempR_fault: float
            R상 권선온도 fault 유무
        winding_tempS_fault: float
            S상 권선온도 fault 유무
        winding_tempT_fault: float
            T상 권선온도 fault 유무
        """
        t_ = str(time)
        month = t_[5:7]
        day = t_[8:10]
        hour = t_[11:13]
        keys = str(month) + "-" + str(day) + "-" + str(hour)
        T_max = self.get_windingtempboundary(self.data[keys])

        th_factor = (1 / T_max) / 50
        ch_winding_tempR = winding_tempR * th_factor * sensitivity_winding_temp
        ch_winding_tempS = winding_tempS * th_factor * sensitivity_winding_temp
        ch_winding_tempT = winding_tempT * th_factor * sensitivity_winding_temp

        if ch_winding_tempR > 1:
            winding_tempR_fault = 1
        else:
            winding_tempR_fault = 0

        if ch_winding_tempS > 1:
            winding_tempS_fault = 1
        else:
            winding_tempS_fault = 0

        if ch_winding_tempT > 1:
            winding_tempT_fault = 1
        else:
            winding_tempT_fault = 0

        return ch_winding_tempR, ch_winding_tempS, ch_winding_tempT, winding_tempR_fault, winding_tempS_fault, winding_tempT_fault

    def check_wingdingtempfailure(
        self,
        time,
        winding_tempR,
        winding_tempS,
        winding_tempT,
        sensitivity_winding_temp,
        maxfail_num,
    ):
        """권선온도고장

        Parameters
        ----------
        time: datetime
            실시간 시간데이터
        winding_tempR: float
            R상 권선온도
        winding_tempS: float
            S상 권선온도
        winding_tempT: float
            T상 권선온도
        maxfail_num: int
            오류 개수 Threshold
        sensitivity_winding_temp: float
            권선온도 Threshold 민감도
        Returns
        -------
        ch_winding_tempR: float
            th_factor와 sensitivity 로 스케일링된 권선온도 R상
        ch_winding_tempS: float
            th_factor와 sensitivity 로 스케일링된 권선온도 S상
        ch_winding_tempT: float
            th_factor와 sensitivity 로 스케일링된 권선온도 T상
        if_windingtemp_tempR_fail: 1 or 0
            R상 권선온도가 10분동안 오류를 보내면 고장 alarm을 보냄
        if_windingtemp_tempS_fail: 1 or 0
            S상 권선온도가 10분동안 오류를 보내면 고장 alarm을 보냄
        if_windingtemp_tempT_fail: 1 or 0
            T상 권선온도가 10분동안 오류를 보내면 고장 alarm을 보냄
        """
        ch_winding_tempR, ch_winding_tempS, ch_winding_tempT, winding_tempR_fault, winding_tempS_fault, winding_tempT_fault = self.calculate_tempthreshold(
            time, winding_tempR, winding_tempS, winding_tempT, sensitivity_winding_temp
        )

        self.winding_tempR_fail_value.append(winding_tempR_fault)
        self.winding_tempS_fail_value.append(winding_tempS_fault)
        self.winding_tempT_fail_value.append(winding_tempT_fault)

        self.windingtemp_dict["Time"] = time
        self.windingtemp_dict["winding_tempR"] = ch_winding_tempR
        self.windingtemp_dict["winding_tempS"] = ch_winding_tempS
        self.windingtemp_dict["winding_tempT"] = ch_winding_tempT

        if_winding_tempR_fail = sum(self.winding_tempR_fail_value) == maxfail_num
        if_winding_tempS_fail = sum(self.winding_tempS_fail_value) == maxfail_num
        if_winding_tempT_fail = sum(self.winding_tempT_fail_value) == maxfail_num
        if_alarm = (if_winding_tempR_fail + if_winding_tempS_fail + if_winding_tempT_fail) > 0

        self.windingtemp_dict["winding_tempR_fault"] = if_winding_tempR_fail
        self.windingtemp_dict["winding_tempS_fault"] = if_winding_tempS_fail
        self.windingtemp_dict["winding_tempT_fault"] = if_winding_tempT_fail
        self.windingtemp_dict["alarm"] = if_alarm

        return self.windingtemp_dict
