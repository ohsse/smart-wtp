import numpy as np


def get_max_amp_res(index, amp_data, res_data):
    try:
        amp = amp_data[:, index]
    except Exception:
        amp = np.array([0])
    
    try:
        res = res_data[:, index]
    except Exception:
        res = np.array([0])
    
    # amp가 비어있으면 기본값 0을 반환
    if amp.size == 0:
        return 0, 0
    
    try:
        max_index = np.argmax(amp)
        max_amp = amp[max_index]
    except Exception:
        max_amp = 0

    try:
        max_res = res[max_index]
    except Exception:
        max_res = 0

    return max_amp, max_res


import numpy as np

def merge_by_motor(motor_amp_info, motor_res_info, mergeMotorList):
    output = {}
    motors = mergeMotorList
    # motors = ["m_GM_1", "m_GM_2", "m_GM_3", "m_GM_4",]
    for i, motor in enumerate(motors):
        output[motor] = {}

        # amp_data: 최소 2행, 5열 (최소 DE_v_rms에 필요한 5번째 열까지 필요)
        try:
            amp_data = motor_amp_info[2 * i : 2 * i + 2]
            if amp_data.shape[0] != 2 or amp_data.shape[1] < 5:
                raise Exception("amp_data shape insufficient")
        except Exception:
            amp_data = np.zeros((2, 5))

        # res_data: 최소 2행, 8열 (최소 DE_v_rms alarm에 필요한 8번째 열까지 필요)
        try:
            res_data = motor_res_info[2 * i : 2 * i + 2]
            if res_data.shape[0] != 2 or res_data.shape[1] < 8:
                raise Exception("res_data shape insufficient")
        except Exception:
            res_data = np.zeros((2, 8))

        # unbalance
        amp, res = get_max_amp_res(0, amp_data, res_data)
        output[motor]["unbalance_amp"] = amp
        try:
            output[motor]["unbalance_alarm"] = np.array(res).astype(bool)
        except Exception:
            output[motor]["unbalance_alarm"] = False

        # misalignment
        amp, res = get_max_amp_res(1, amp_data, res_data)
        output[motor]["misalignment_amp"] = amp
        try:
            output[motor]["misalignment_alarm"] = np.array(res).astype(bool)
        except Exception:
            output[motor]["misalignment_alarm"] = False

        # rotor
        amp, res = get_max_amp_res(2, amp_data, res_data)
        output[motor]["rotor_amp"] = amp
        try:
            output[motor]["rotor_alarm"] = np.array(res).astype(bool)
        except Exception:
            output[motor]["rotor_alarm"] = False

        # DE bearing
        try:
            output[motor]["DE_amp"] = amp_data[0, 3]
        except Exception:
            output[motor]["DE_amp"] = 0
        try:
            output[motor]["DE_BPFO_alarm"] = np.array(res_data[0, 3]).astype(bool)
        except Exception:
            output[motor]["DE_BPFO_alarm"] = False
        try:
            output[motor]["DE_BPFI_alarm"] = np.array(res_data[0, 4]).astype(bool)
        except Exception:
            output[motor]["DE_BPFI_alarm"] = False
        try:
            output[motor]["DE_BSF_alarm"] = np.array(res_data[0, 5]).astype(bool)
        except Exception:
            output[motor]["DE_BSF_alarm"] = False
        try:
            output[motor]["DE_FTF_alarm"] = np.array(res_data[0, 6]).astype(bool)
        except Exception:
            output[motor]["DE_FTF_alarm"] = False

        # NDE bearing
        try:
            output[motor]["NDE_amp"] = amp_data[1, 3]
        except Exception:
            output[motor]["NDE_amp"] = 0
        try:
            output[motor]["NDE_BPFO_alarm"] = np.array(res_data[1, 3]).astype(bool)
        except Exception:
            output[motor]["NDE_BPFO_alarm"] = False
        try:
            output[motor]["NDE_BPFI_alarm"] = np.array(res_data[1, 4]).astype(bool)
        except Exception:
            output[motor]["NDE_BPFI_alarm"] = False
        try:
            output[motor]["NDE_BSF_alarm"] = np.array(res_data[1, 5]).astype(bool)
        except Exception:
            output[motor]["NDE_BSF_alarm"] = False
        try:
            output[motor]["NDE_FTF_alarm"] = np.array(res_data[1, 6]).astype(bool)
        except Exception:
            output[motor]["NDE_FTF_alarm"] = False

        # DE_v_rms
        try:
            output[motor]["DE_rms_amp"] = amp_data[0, 4]
        except Exception:
            output[motor]["DE_rms_amp"] = 0
        try:
            output[motor]["DE_rms_alarm"] = np.array(res_data[0, 7]).astype(bool)
        except Exception:
            output[motor]["DE_rms_alarm"] = False

        # NDE_v_rms
        try:
            output[motor]["NDE_rms_amp"] = amp_data[1, 4]
        except Exception:
            output[motor]["NDE_rms_amp"] = 0
        try:
            output[motor]["NDE_rms_alarm"] = np.array(res_data[1, 7]).astype(bool)
        except Exception:
            output[motor]["NDE_rms_alarm"] = False

    return output



def merge_by_pump(pump_amp_info, pump_res_info, mergePumpList):
    output = {}
    pumps = mergePumpList
    # pumps = ["p_GM_1", "p_GM_2", "p_GM_3", "p_GM_4",]

    for i, pump in enumerate(pumps):
        output[pump] = {}
        # 안전하게 amp_data, res_data 추출 (없을 경우 기본값 배열 사용)
        try:
            amp_data = pump_amp_info[2 * i : 2 * i + 2]
            # amp_data가 최소 (2,4) 형태인지 확인
            if amp_data.shape[0] != 2 or amp_data.shape[1] < 4:
                raise Exception("amp_data shape insufficient")
        except Exception:
            import numpy as np
            amp_data = np.zeros((2, 4))

        try:
            res_data = pump_res_info[2 * i : 2 * i + 2]
            # res_data가 최소 (2,7) 형태인지 확인
            if res_data.shape[0] != 2 or res_data.shape[1] < 7:
                raise Exception("res_data shape insufficient")
        except Exception:
            import numpy as np
            res_data = np.zeros((2, 7))

        # impeller
        amp, res = get_max_amp_res(0, amp_data, res_data)
        output[pump]["impeller_amp"] = amp
        try:
            output[pump]["impeller_alarm"] = np.array(res).astype(bool)
        except Exception:
            output[pump]["impeller_alarm"] = False

        # cavitation
        amp, res = get_max_amp_res(1, amp_data, res_data)
        output[pump]["cavitation_amp"] = amp
        try:
            output[pump]["cavitation_alarm"] = np.array(res).astype(bool)
        except Exception:
            output[pump]["cavitation_alarm"] = False

        # DE bearing
        try:
            output[pump]["DE_amp"] = amp_data[0, 2]
        except Exception:
            output[pump]["DE_amp"] = 0
        try:
            output[pump]["DE_BPFO_alarm"] = np.array(res_data[0, 2]).astype(bool)
        except Exception:
            output[pump]["DE_BPFO_alarm"] = False
        try:
            output[pump]["DE_BPFI_alarm"] = np.array(res_data[0, 3]).astype(bool)
        except Exception:
            output[pump]["DE_BPFI_alarm"] = False
        try:
            output[pump]["DE_BSF_alarm"] = np.array(res_data[0, 4]).astype(bool)
        except Exception:
            output[pump]["DE_BSF_alarm"] = False
        try:
            output[pump]["DE_FTF_alarm"] = np.array(res_data[0, 5]).astype(bool)
        except Exception:
            output[pump]["DE_FTF_alarm"] = False

        # NDE bearing
        try:
            output[pump]["NDE_amp"] = amp_data[1, 2]
        except Exception:
            output[pump]["NDE_amp"] = 0
        try:
            output[pump]["NDE_BPFO_alarm"] = np.array(res_data[1, 2]).astype(bool)
        except Exception:
            output[pump]["NDE_BPFO_alarm"] = False
        try:
            output[pump]["NDE_BPFI_alarm"] = np.array(res_data[1, 3]).astype(bool)
        except Exception:
            output[pump]["NDE_BPFI_alarm"] = False
        try:
            output[pump]["NDE_BSF_alarm"] = np.array(res_data[1, 4]).astype(bool)
        except Exception:
            output[pump]["NDE_BSF_alarm"] = False
        try:
            output[pump]["NDE_FTF_alarm"] = np.array(res_data[1, 5]).astype(bool)
        except Exception:
            output[pump]["NDE_FTF_alarm"] = False

        # DE_v_rms
        try:
            output[pump]["DE_rms_amp"] = amp_data[0, 3]
        except Exception:
            output[pump]["DE_rms_amp"] = 0
        try:
            output[pump]["DE_rms_alarm"] = np.array(res_data[0, 6]).astype(bool)
        except Exception:
            output[pump]["DE_rms_alarm"] = False

        # NDE_v_rms
        try:
            output[pump]["NDE_rms_amp"] = amp_data[1, 3]
        except Exception:
            output[pump]["NDE_rms_amp"] = 0
        try:
            output[pump]["NDE_rms_alarm"] = np.array(res_data[1, 6]).astype(bool)
        except Exception:
            output[pump]["NDE_rms_alarm"] = False

    return output


