import os
from typing import Tuple

import joblib
import numpy as np
from feature_extraction import integrate
from numpy.fft import irfft, rfft, rfftfreq
from preprocess import do_butter_highpass_filter
from matplotlib import pyplot as plt

MODEL_PATH = "./ML_models"

# diagnose_unbalance
def diagnose_unbalance_misalignment(
    timeseries: np.ndarray,
    nxs_val_history: np.ndarray,
    v_rms: float,
    sensitivity: int,
    v_rms_threshold: float,
) -> Tuple[float, bool]:
    """
    Diagnose unbalance and misalignment.
    Diagnose if (unbalance/misalignment condition is met) and (rms velocity condition is met).
    Parameters
    ----------
    nxs_val_history: n-d array
        historical nX data
    v_rms: float
        current rms velocity
    sensitivity: int
        unbalnce/misalignment diagnosis sensitivity (1~10)
    v_rms_threshold: float
        rms velocity threshold
    Returns
    ----------
    unbalance_amp: float
        HI for unbalance
    misalignment_amp: float
        HI for misalignment
    unbalance: bool
        unbalance diagnosis result
    unbalance: bool
        misalignment diagnosis result
    """

    # sensitivity 가 1~10 이도록 변경
    sensitivity = np.clip(sensitivity, 1, 10)
    
    one_two_xs = nxs_val_history[:, 0:2]
    one_five_xs = nxs_val_history[:, 0:5]
    # rms_vibr = np.sqrt(np.mean(timeseries**2))
    rms_vibr = 0.01
    threshold_misal = 0.0005
    sums_xs = np.sum(one_five_xs[:, :-1], axis=1).reshape([-1, 1])
    allsum_xs = np.mean(sums_xs)

    # sums = np.sum(nxs_val_history[:, :-1], axis=1).reshape([-1, 1])
    # unbal_misalign_feature = one_two_xs / sums  # kim :one, two 성분의 평균
    unbal_misalign_feature = one_two_xs / allsum_xs  # kim :one, two 성분의 평균
    # print("Unbal, misalignment 1X and 2X : ", one_two_xs[0][0], one_two_xs[0][1], "// RMS_Vibr (unbal threshold) : ", rms_vibr)
    #model_path = os.path.join(        os.getcwd(), MODEL_PATH, "unbal_misalign_model_rbf_svm.pkl"    )
    model_path = "./ML_models/unbal_misalign_model_rbf_svm.pkl"
    # print("unbal_misal_feature : ", unbal_misalign_feature)
    
    model = joblib.load(model_path)
    historical_scores = model.predict_proba(unbal_misalign_feature) # kim : Model이 Unbalance 또는 Misalignment일 확률 출력
    mean_scores = np.mean(historical_scores, axis=0)[1:] # kim : historical_scores의 
    
    # calculate amps
    
    score_threshold = 1 - 0.04 * sensitivity  # 1일때 0.96, 5일때 0.8, 10일때 0.6
    score_part = np.clip(
        mean_scores / score_threshold, 0, 1.1
    )  # historical mean 이 score_threshold 도달 시 score part 충족
    # print("Unbalance_Misalignment M/L scores : ", score_part)
    
    rule = [one_two_xs[0][0]/rms_vibr, one_two_xs[0][1]/one_two_xs[0][0]]
    
    rule_part_unbal = np.clip(
        one_two_xs[0][0]/rms_vibr, 0, 1.1
    )

    rule_part_misalignment = np.clip(
        one_two_xs[0][1]/one_two_xs[0][0], 0, 1.1
    )
    # print(rule_part_misalignment)
    # print(one_two_xs[0][1], one_two_xs[0][0])
    # rule_part_misalignment = np.clip(
    #     one_two_xs[0][1]/threshold_misal, 0, 1.1
    # )
    # print(one_two_xs[0][0], one_two_xs[0][1])
    # rule_part = np.clip(
    #     rule, 0, 1.1
    # )
    rule_part = [rule_part_unbal, rule_part_misalignment]
    # print("rule_parts :", rule_part)
    
    # v_rms_part = np.clip(
    #     v_rms / (0.7 * v_rms_threshold), 0, 1.1
    # )  # rms가 threshold의 70% 도달시 충족

    #원본
    # amps = (0.6 * score_part) + (0.4 * v_rms_part)
    #조건 변경
    # amps = (0.1 * score_part) + (0.9 * v_rms_part)
    amps = []
    for i in range(2):
        amps.append(0.1 * score_part[i] + 0.9 * rule_part[i])

    unbalance_amp = amps[0] #1x
    misalignment_amp = amps[1] #2x
    ## unbalance_amp = (0.2 * score_part[1]) + (0.8 * rule_part[0])
    ## misalignment_amp = (0.2 * score_part[2]) + (0.8 * rule_part[1])

    #1이상이 결함으로 판단, 0.8이상은 경고

    # unbalance = score_part[0] >= 1 and unbalance_amp >= 1
    # misalignment = score_part[1] >= 1 and misalignment_amp >= 1
    v_rms_part = 0
    # print("v_RMS : ", v_rms)
    if v_rms > 3.5:
        v_rms_part = 0.8
    if v_rms > 6.5:
        v_rms_part = 1.1

    if unbalance_amp >= 0.95:
        if v_rms_part >= 0.8:
            if v_rms_part >= 1:
                unbalance = True
                unbalance_amp = 1.1
            else:
                # unbalance = False
                unbalance_amp = 0.8
                unbalance = True
                # unbalance_amp = 1.1
        else:
            unbalance = False
            unbalance_amp = 0
    else:
        unbalance = False
        unbalance_amp = 0
        
    if misalignment_amp >= 0.95:
        if v_rms_part >= 0.8:
            if v_rms_part >= 1:
                misalignment = True
                misalignment_amp = 1.1
            else:
                # misalignment = False
                misalignment_amp = 0.8
                misalignment = True
                # misalignment_amp = 1.1
        else:
            misalignment = False
            misalignment_amp = 0
    else:
        misalignment = False
        misalignment_amp = 0
    # unbalance = v_rms_part >= 1 and unbalance_amp >= 1
    # misalignment = v_rms_part >= 1 and misalignment_amp >= 1

    
    return unbalance_amp, unbalance, misalignment_amp, misalignment


# diagnose_bearing
def diagnose_bearing(
    x_mag,
    bpfs_env_is_peak_history: np.ndarray,
    v_rms: float,
    sensitivity: int,
    v_rms_threshold: float,
    # f_vg_atg: np.ndarray,
    # x_mag_vg_atg: np.ndarray,
) -> Tuple[float, bool, float, bool, bool, bool]:
    """
    Diagnose bearing. Diagnose if (bearing fault condition is met)
    and (rms velocity condition is met).
    Parameters
    ----------
    bpfs_env_is_peak_history: n-d array
        historical envelope BPFs peak data
    v_rms: float
        current rms velocity
    sensitivity: int
        bearing diagnosis sensitivity (1~10)
    v_rms_threshold: float
        rms velocity threshold
    Returns
    ----------
    bearing_amp: float
        HI for bearing
    bpfo: bool
        BPFO diagnosis result
    bpfi: bool
        BPFI diagnosis result
    bsf: bool
        BSF diagnosis result
    ftf: bool
        FTF diagnosis result
    """
    ## 'bearing_LR_model.pkl' : 과거 엔벨로프 BPF 피크 데이터를 기반으로 베어링 상태를 진단
    ## 임계값 : 현재 RMS 속도가 특정 수준을 초과하는지 여부를 결정
    x_mag_ = x_mag.copy()[2000:8000]

    white_noise = 0
    print("SUM of MAG : " , sum(x_mag_))
    if sum(x_mag_) > 50:
        white_noise = 1

    # 사용하는 harmonics 의 갯수 추정   하모닉이란 기본 주파수의 배수 1x 2x 3x ...
    n_harmonics = int(bpfs_env_is_peak_history.shape[1] / 4)
    n_hist = bpfs_env_is_peak_history.shape[0]

    # sensitivity 가 1~10 이도록 변경
    sensitivity = np.clip(sensitivity, 1, 10)

    bpfo_peaks = bpfs_env_is_peak_history[:, : 1 * n_harmonics]
    bpfi_peaks = bpfs_env_is_peak_history[:, 1 * n_harmonics : 2 * n_harmonics]
    bsf_peaks = bpfs_env_is_peak_history[:, 2 * n_harmonics : 3 * n_harmonics]
    ftf_peaks = bpfs_env_is_peak_history[:, 3 * n_harmonics : 4 * n_harmonics]
          
    ## BPF 엔벨로프 피크(BPFO, BPFI, BSF 및 FTF)를 추출하여 베어링 피처의 단일 매트릭스로 결합합
    bearing_feature_ml = np.vstack((bpfo_peaks, bpfi_peaks, bsf_peaks, ftf_peaks))[
        :, :-1
    ]  # 1~5 peak 이용
    bearing_feature_rule = np.vstack((bpfo_peaks, bpfi_peaks))[:,:2] # 1X와 2X만 사용
    
    # print("bearing_feature_rule : ", bearing_feature_rule)
    #model_name = os.path.join(os.getcwd(), MODEL_PATH, "bearing_LR_model.pkl")
    model_path = "./ML_models/bearing_LR_model.pkl"
    model = joblib.load(model_path)
    historical_scores = model.predict_proba(bearing_feature_ml)[:, 1]
    
    mean_scores = np.array(
        [
            np.mean(historical_scores[: 1 * n_hist]),
            np.mean(historical_scores[1 * n_hist : 2 * n_hist]),
            np.mean(historical_scores[2 * n_hist : 3 * n_hist]),
            np.mean(historical_scores[3 * n_hist : 4 * n_hist]),
        ]
    )

    # calculate amps
    score_threshold = 1 - 0.04 * sensitivity  # 1일때 0.96, 5일때 0.8, 10일때 0.6
    score_part = np.clip(
        mean_scores / score_threshold, 0, 1.1
    )  # historical mean 이 score_threshold 도달 시 score part 충족
    rule = np.clip(np.mean(bearing_feature_rule), 0, 1.1)

    print(f"1X and 2X BPFO, BPFI (rule) : {bearing_feature_rule}")
   
    v_rms_part = np.clip(
        v_rms / (0.7 * v_rms_threshold), 0, 1.1
    )  # rms가 threshold의 70% 도달시 충족

    #조건 원본
    # amps = 0.6 * score_part + 0.4 * v_rms_part

    if rule >=0.7 and white_noise == 1:
        rule_part = 1.13
    elif rule >= 0.7 and white_noise == 0:
        rule_part = 0.9
        # rule_part = 1.13
    else:
        rule_part = np.mean(score_part)
    # rule_part = rule >= 1 and v_rms_part >= 1
    
    # 조건 수정
    # amps = (0.1 * score_part) + (0.9 * v_rms_part) 
    amps = (0.1 * score_part) + (0.9 * rule_part) 

    bpfo_amp = amps[0]
    bpfi_amp = amps[1]
    bsf_amp = amps[2]
    ftf_amp = amps[3]
    bearing_amp = np.max([bpfo_amp, bpfi_amp])
    # bearing_amp = np.max([bpfo_amp, bpfi_amp, bsf_amp, ftf_amp])

    # bpfo = score_part[0] >= 1 and bpfo_amp >= 1
    # bpfi = score_part[1] >= 1 and bpfi_amp >= 1
    # bsf = score_part[2] >= 1 and bsf_amp >= 1
    # ftf = score_part[3] >= 1 and ftf_amp >= 1
    bpfo = score_part[0] >= 0.8 and bpfo_amp >= 0.8
    bpfi = score_part[1] >= 0.8 and bpfi_amp >= 0.8
    bsf = score_part[2] >= 0.8 and bsf_amp >= 0.8
    ftf = score_part[3] >= 0.8 and ftf_amp >= 0.8
    
    if bearing_amp >= 0.8:
        bpfo = True
    
    return bearing_amp, bpfo, bpfi, bsf, ftf

# diagnose_rotor
def diagnose_rotor(
    rotor_is_peak_history: np.ndarray,
    sensitivity: int,
) -> Tuple[float, bool]:
    """
    Diagnose rotor. Diagnose if more than 3 out of first 4 rotor components are detected.
    Parameters
    ----------
    rotor_is_peak_history: n-d array
        historical rotor peak data
    sensitivity: int
        rotor diagnosis sensitivity
    Returns
    ----------
    rotor_amp: float
        HI for rotor
    rotor: bool
        rotor diagnosis result
    """
    # sensitivity 가 1~10 이도록 변경
    sensitivity = np.clip(sensitivity, 1, 10)
    percentage_threshold = 1.0 - 0.04 * sensitivity  # 1일때 0.96, 5일때 0.8, 10일때 0.6
    
    # rotor 성분 별 percentage_threshold 넘는지 확인
    n_hist = rotor_is_peak_history.shape[0]
    rotor_over_percentage = (
        (np.sum(rotor_is_peak_history, axis=0) / n_hist) > percentage_threshold # 0.8
    ).astype(int)
    rotor_peak_number = np.sum(rotor_over_percentage)
    print("rotor peak number", rotor_peak_number)
    rotor_amp = rotor_peak_number / 4
    rotor = rotor_amp >= 1
    
    return rotor_amp, rotor


# diagnose_impeller
def diagnose_impeller(v_rms : float,
    timeseries: np.ndarray,
    one_x: float,
    n_blades: int,
    f_line: float,
    fs: float,
    sensitivity: int,
) -> Tuple[float, bool]:
    """
    Diagnose impeller. Diagnose if rms magnitude of impeller component is over threshold.
    Parameters
    ----------
    timeseries: 1-d array
        timeseries of acceleration
    one_x: float
        location of 1x component
    f_line: float
        line frequency
    fs: float
        sampling frequency
    sensitivity: int
        diagnosis sensitivity of impeller
    Returns
    ----------
    impeller_amp: float
        HI for impeller
    impeller: bool
        impeller diagnosis result
    """

    # sensitivity 가 1~10 이도록 변경
    # 민감도를 1에서 10 사이로 제한
    sensitivity = np.clip(sensitivity, 1, 10)

    # 저주파 잡음을 제거하기 위해 시계열 데이터에 고역 필터 적용
    acc_filtered = do_butter_highpass_filter(timeseries, 20, fs, 1)
    
    # 필터링된 가속도를 적분하여 속도 데이터 계산
    t = np.array([i / fs for i in range(acc_filtered.shape[0])])
    velocity = integrate(t, acc_filtered) * 9806 # 1G = 9806 mm/s^2

    # 속도 데이터의 푸리에 변환을 수행하여 주파수 구성 요소를 얻음
    vel_fourier = rfft(velocity)
    
    n = velocity.shape[0]  # 12800 by default # FFT 계산을 위한 기본 길이
    f = rfftfreq(n, d=1 / fs)
    
    # 주파수 분해능 계산
    del_f = f[1] - f[0]

    # delete 2x line frequency component # 2x 선 주파수 구성 요소 제거하여 그 영향을 배제
    f_to_be_deleted = f_line * 2
    to_be_deleted_ind = np.argmin(np.abs(f - f_to_be_deleted))
    vel_fourier[to_be_deleted_ind - 2 : to_be_deleted_ind + 3] = vel_fourier[
        to_be_deleted_ind + 3
    ]
    
    # print(f"vel_fourier (1) : {vel_fourier}")
    # leave impeller component only # 6x one_x 근처의 주파수 구성 요소만 남기고 모두 0으로 설정
    impeller_ind = np.argmin(np.abs(f - one_x * n_blades))
    vel_fourier_to_calc = vel_fourier[int(impeller_ind*0.9) : int(impeller_ind*1.1)]
    
    vel_fourier[: impeller_ind - int(impeller_ind/10)*int(1 / del_f)] = 0
    vel_fourier[impeller_ind + int(impeller_ind/10)*int(1 / del_f) :] = 0
    # print(f"vel_fourier (2) : ...{vel_fourier[vel_fourier != 0]}...")
    
    
    # return to timeseries
    # 주파수 구성 요소를 다시 시계열로 변환
    vel_impeller = irfft(vel_fourier)

    Limit_A = 3.5
    Limit_B = 5.0
    
    # 임펠러 시계열 데이터의 RMS 값을 계산
    impeller_rms = np.sqrt(np.mean(vel_impeller**2))
    
    # sensitivity = 1 일때 threshold = 6.4, sensitivity = 5 일때 threshold = 4.4 (3*(6.1/4.2)), sensitivity = 8  이상일 때 threshold = 3
    # 민감도에 따라 임계값을 계산하고 임펠러 상태가 임계값을 초과하는지 확인
    rms_threshold = np.clip((13.8 - sensitivity) / 2, 3, 10)
    # impeller_amp = 0.5 + impeller_rms / rms_threshold
    impeller_amp = impeller_rms / (Limit_A*Limit_B / v_rms)
    impeller = impeller_amp >= 1
    
    return impeller_amp, impeller

'''
# diagnose_cavitation 원본
def diagnose_cavitation(
    spectral_energy_history: np.ndarray,
    sensitivity: int,
) -> Tuple[float, bool]:
    """
    Diagnose cavitation. Diagnose if number of sections whose
    magnitude/historical_magnitude is over ratio_threshold is over number_threshold
    Parameters
    ----------
    spectral_energy_history: n-d array
        historical spectral energy data
    sensitivity: int
        diagnosis sensitivity of cavitation
    Returns
    ----------
    cavitation_amp: float
        HI for cavitation
    cavitation: bool
        cavitation diagnosis result
    """

    # sensitivity 가 1~10 이도록 변경
    sensitivity = np.clip(sensitivity, 1, 10)

    #조건 원본
    #ratio_threshold = 4
    #조건 수정 5배
    ratio_threshold = 5
    number_threshold = np.clip(9.5 - 0.5 * sensitivity, 1, 10)  # 1일때 9, 5일때 7, 10일때 4.5

    spectral_energy_median = np.median(spectral_energy_history[:-1], axis=0)
    last_spectral_energy = spectral_energy_history[-1]

    spectral_energy_ratio = last_spectral_energy / (spectral_energy_median + 1e-6)
    if_over_energy_ratio = (spectral_energy_ratio >= ratio_threshold).astype(int)

    number_over_ratio_threshold = np.sum(
        if_over_energy_ratio
    )  # ratio threshold 충족시킨 구간의 갯수

    cavitation_amp = number_over_ratio_threshold / number_threshold
    cavitation = cavitation_amp >= 1

    return cavitation_amp, cavitation
'''
def diagnose_cavitation(
    spectral_energy_history: np.ndarray,
    sensitivity: int,
) -> Tuple[float, bool]:
    # 주파수 범위 설정 (200~2000을 10개 구간으로 나눔)
    band_ranges = [(200 + i * 180, 200 + (i + 1) * 180) for i in range(10)]
    
    historical_energies = np.array([
        spectral_energy_history[:, i] for i in range(len(band_ranges))
    ]).T  # 각 열이 시간 포인트, 행이 구간 에너지임계값 계산
    # if len(spectral_energy_history) >= 20:
    #     thresholds = [5 * np.median(historical_energies[-20:, i]) for i in range(10)]
    #     print(f"{len(spectral_energy_history)}th threshold : ")
    #     print(thresholds)
    # else:
    #     thresholds = [5 * np.median(historical_energies[-len(spectral_energy_history):, i]) for i in range(10)]
    #     print(f"{len(spectral_energy_history)}th threshold : ")
    #     print(thresholds)

    # thresholds = [6.127391534651856e-05, 0.0006486610183231308, 0.0030704008020922533, 0.009782687639148949, 0.014783872542067054, 0.022018533710056576, 0.025568500457551175, 0.015551901217041825, 0.007375177034549384, 0.0011783950447042599] # 정상데이터에서의 20개 데이터 중간값의 5배 (설비마다 변경해야 함)
    thresholds = [6.127391534651856e-04, 0.006486610183231308, 0.030704008020922533, 0.09782687639148949, 0.14783872542067054, 
                  0.022018533710056576, 0.025568500457551175/2, 0.015551901217041825/4, 0.007375177034549384/5, 0.0011783950447042599/2] # 정상데이터에서의 20개 데이터 중간값의 5배 (설비마다 변경해야 함)
    
    # thresholds = [1.2296135470923805e-07, 8.822667957846524e-08, 1.2572528324687237e-07, 2.212754512145168e-07, 3.4837108889519976e-07, 5.321319638040826e-07, 6.954656178200027e-07, 0.03395396085820971, 9.971348416665665e-07, 1.0312708321898102e-06] # 이 값은 안씀
    # # 현재 에너지 계산 (마지막 시간 포인트)
    current_energies = historical_energies[-1]
    exc = current_energies > thresholds
    # 조건 검사
    exceedances = sum(current_energy > threshold for current_energy, threshold in zip(current_energies, thresholds))
    cavitation = exceedances > 7
    
    cavitation_amp = exceedances / 10

    return cavitation_amp, cavitation


# vibration level
def check_rms_alarm(
    v_rms: float,
    dev_type: str,
    sensitivity: int,
) -> bool:
    """
    give vibration severity level
    Parameters
    ----------
    v_rms: float
        rms velocity
    dev_type: str
        'motor' or 'pump'
    sensitivity: int
        sensitivity for rms alarm
    Returns
    ----------
    rms_alarm: bool
        alarm with rms
    """
    sensitivity = min(max(1, sensitivity), 10)

    rms_alarm = False

    if dev_type == "motor":
        # 1일때 6.26; 5일때 4.5; 10일때 2.3
        rms_threshold = -0.44 * sensitivity + 6.7 # 5.5
    else:
        # 1일때 7.62; 5일때 6.1; 10일때 4.2
        rms_threshold = -0.38 * sensitivity + 8 

    if v_rms > rms_threshold:
        rms_alarm = True

    return rms_alarm
