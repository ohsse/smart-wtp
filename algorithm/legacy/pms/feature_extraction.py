from typing import Tuple

import numpy as np
from numba import njit
from numpy.fft import irfft, rfft
from preprocess import do_butter_highpass_filter
from matplotlib import pyplot as plt

# get Q1, Q3 baselines and peak threshold
@njit
def get_iqr_threshold(
    spectrum: np.ndarray,
    n: float,
    l_filter: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Get baseline and iqr threshold of spectrum for peak detection.

    Parameters
    ----------
    spectrum: 1-d array
        magnitude of fourier series (x_mag)

    n: float
        multiplier of IQR threshold

    l_filter: int
        number of points to observe
        deciding baseline and threshold

    Returns
    ----------
    baseline_q1: 1-d array
        q1 baseline

    baseline_q3: 1-d array
        q3 baseline

    baseline_threshold: 1-d array
        baseline threshold for threshold
        (q3 baseline + 1.5iqr)

    """
    baseline_q1 = spectrum.copy()
    baseline_q3 = spectrum.copy()
    peak_threshold = spectrum.copy()
    
    for i in range(spectrum.shape[0]):
        if i < l_filter:
            section_spectrum = spectrum[0 : i + l_filter + 1]
        elif i > spectrum.shape[0] - l_filter:
            section_spectrum = spectrum[i - l_filter : spectrum.shape[0]]
        else:
            section_spectrum = spectrum[i - l_filter : i + l_filter + 1]

        q1 = np.percentile(section_spectrum, 25)
        q3 = np.percentile(section_spectrum, 75)
        iqr = q3 - q1
        outlier_threshold = q3 + n * iqr  # Tukey fence

        baseline_q1[i] = q1
        baseline_q3[i] = q3
        peak_threshold[i] = outlier_threshold
    return baseline_q1, baseline_q3, peak_threshold


# get broken rotor bar characteristic frequencies

''' Original code
def get_rotor_char_freqs(
    f_shaft: float,
    f_line: float,
    n_poles: int,
) -> np.ndarray:
    """
    Get rotor fault characteristic frequencies

    Parameters
    ----------
    f_shaft: float
        accurate 1x found from spectrum
        with 'get_motor_1x' function

    f_line: float
        line frequency (60 Hz by default)

    n_poles: int
        number of poles of the motor

    Returns
    ----------
    rotor_characteristic_freqs: 1-d array
        broken rotor bar fault frequencies

    """

    sync_speed = 60 * 2 * f_line / n_poles # 동기속도
    f_slip = sync_speed / 60 - f_shaft # 슬립주파수 : 라인주파수 - 회전주파수
    f_pole = f_slip * n_poles * 1.15  # 경험상 실제 pole frequency보다 더 떨어져 있으므로 15% 추가
    
    rotor_characteristic_freqs = np.array(
        [f_shaft - f_pole, f_shaft + f_pole, 2 * f_shaft - f_pole, 2 * f_shaft + f_pole]
    )
    print(f"sync_speed : {sync_speed}, f_slip : {f_slip}, f_pole : {f_pole}\n")
    print(f"1X slip freq : {f_shaft - f_pole}, {f_shaft + f_pole}, 2X slip freq : {2 * f_shaft - f_pole}, {2 * f_shaft + f_pole} ")

    return rotor_characteristic_freqs
'''

def get_rotor_char_freqs(
    f_shaft: float,
    f_line: float,
    n_poles: int,
) -> np.ndarray:
    """
    Get rotor fault characteristic frequencies

    Parameters
    ----------
    f_shaft: float
        accurate 1x found from spectrum
        with 'get_motor_1x' function

    f_line: float
        line frequency (60 Hz by default)

    n_poles: int
        number of poles of the motor

    Returns
    ----------
    rotor_characteristic_freqs: 1-d array
        broken rotor bar fault frequencies

    """
    sync_speed = 120 * f_line / n_poles # 동기속도
    f_slip = abs(sync_speed / 60 - f_shaft) # 슬립주파수 : 라인주파수 - 회전주파수
    f_pole = 1 + (f_slip * n_poles * 1.15)  # 경험상 실제 pole frequency보다 더 떨어져 있으므로 15% 추가
    
    rotor_characteristic_freqs = np.array(
        [f_shaft - f_pole, f_shaft + f_pole, 2 * f_shaft - f_pole, 2 * f_shaft + f_pole]
    )
    print("f_shaft : ", f_shaft, "f_line : ", f_line)
    print("rotor freqs : ", rotor_characteristic_freqs)
    print(f"sync_speed : {sync_speed} RPM, actual_speed : {f_shaft * 60} RPM, f_slip : {f_slip} Hz, f_pole : {f_pole} Hz\n")

    return rotor_characteristic_freqs

def get_peak_bearing(
    f: np.ndarray, 
    x_mag: np.ndarray,
    f_shaft : float,
    x_assumed : float,
) -> float:
    
    l_ind = np.argmin(np.abs(f - 0.97 * x_assumed))
    r_ind = np.argmin(np.abs(f - 1.03 * x_assumed))
    
    x_ind = np.argmax(x_mag[l_ind : r_ind + 1]) + l_ind
    x = f[x_ind]
    peak_mag = x_mag[x_ind]
    return x, peak_mag
    
# get broken rotor bar characteristic frequencies
def get_bearing_char_freqs(
    f: np.ndarray, 
    x_mag: np.ndarray,
    f_shaft: float,
    bpfs_r: list,
    n_harmonics: int,
    n_poles: int,
) -> np.ndarray:
    """
    Get bearing fault characteristic frequencies

    Parameters
    ----------
    f_shaft: float
        accurate 1x found from spectrum
        with 'get_motor_1x' function

    BPFs_r: list
        list containing BPFO_r, BPFI_r, BSF_r, FTF_r

    n_harmonics: int
        number of harmonics to search for

    Returns
    ----------
    bearing_characteristic_freqs: 1-d array
        bearing fault frequencies

    """

    to_n = np.array([i + 1 for i in range(n_harmonics)])
    bpfo = bpfs_r[0]*f_shaft
    bpfi = bpfs_r[1]*f_shaft
    bsf = bpfs_r[2]*f_shaft
    ftf = bpfs_r[3]*f_shaft
    
    bpfo, mag_bpfo = get_peak_bearing(f, x_mag, f_shaft, bpfo)
    bpfi, mag_bpfi = get_peak_bearing(f, x_mag, f_shaft, bpfi)
    bsf, mag_bsf = get_peak_bearing(f, x_mag, f_shaft, bsf)
    ftf, mag_ftf = get_peak_bearing(f, x_mag, f_shaft, ftf)
    
    # bpfo = bpfs_r[0]*f_shaft
    # bpfi = bpfs_r[1]*f_shaft
    # bsf = bpfs_r[2]*f_shaft
    # ftf = bpfs_r[3]*f_shaft
    # print(f"bpfo : {bpfo}, bpfi : {bpfi}, bsf : {bsf}, ftf : {ftf}")
    # print(f"mag bpfo : {mag_bpfo}, bpfi : {mag_bpfi}, bsf : {mag_bsf}, ftf : {mag_ftf}")
    
    # 1*bpfo, 2*bpfo, 3*bpfo ... 1*bpfi, 2*bpfi, 3*bpfi...
    bearing_characteristic_freqs = np.hstack(
        (bpfo * to_n, bpfi * to_n, bsf * to_n, ftf * to_n)
    )

    return bearing_characteristic_freqs

'''
# get spectral features
def get_spectral_features(
    f: np.ndarray,
    x_mag: np.ndarray,
    f_line: float,
    feature_freqs: np.ndarray,
    dev_limit: float,
    peak_threshold: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Get spectral_features

    Parameters
    ----------
    f: 1-d array
        frequency domain of data

    x_mag: 1-d array
        magnitude of fourier series

    f_line: float
        line frequency

    feature_freqs: 1-d array
        array containing feature
        frequencies; eg)[1x, 2x, 3x, 6x, etc...]

    dev_limit: float
        deviation limit for searching

    peak_threshold: 1-d array
        spectral threshold got from
        'get_peak_threshold' function

    Returns
    ----------
    feature_mag: 1-d array
        feature magnitudes

    real_f_values: 1-d array
        real feature frequencies considering deviation

    is_peak: 1-d array
        if each feature is peak or not
    """
    x_mag_ = x_mag.copy()
#     print(f"featrue freqs : {feature_freqs}")

    # negative frequency 제거
    zero_mask = feature_freqs > 0
    feature_freqs = feature_freqs[zero_mask]
    
    # line frequency 제거
    f_to_be_deleted = f_line * 2
    to_be_deleted_ind = np.argmin(np.abs(f - f_to_be_deleted))
    x_mag_[to_be_deleted_ind - 2 : to_be_deleted_ind + 3] = x_mag_[to_be_deleted_ind + 3
    ]  # 2x line frequency 제거

    # sort features (ascending)
    print(feature_freqs)
    sort = np.argsort(feature_freqs)
    rev_sort = np.argsort(sort)
    feature_freqs_sorted = feature_freqs[sort]
    # print(feature_freqs_sorted)
    
    # calculate max_boundary, max_deviation
    # (피쳐위치 계산값들간의 차이를 고려하여 실제값 탐색의 범위 상한을 결정하기 위함)
    max_deviation_temp = np.zeros_like(feature_freqs_sorted)
    max_deviation = np.zeros_like(feature_freqs_sorted)

    for i in range(feature_freqs_sorted.shape[0] - 1):
        a = feature_freqs_sorted[i]
        b = feature_freqs_sorted[i + 1]
        k = 100 * (b - a) / (a + b + 1e-6)
        max_deviation_temp[i] = np.min([k, dev_limit])
#     print(f"max_deviation : {max_deviation_temp}")
    max_deviation_temp[-1] = max_deviation_temp[-2]

    max_deviation[0] = max_deviation_temp[0]
    for i in range(1, max_deviation.shape[0] - 1):
        max_deviation[i] = np.min(max_deviation_temp[i - 1 : i + 2])

    max_deviation[-1] = max_deviation[-2]
    # rev_sort features
    max_deviation = max_deviation[rev_sort]
#     print("max_deviation:", max_deviation)
#    
    # calculate feature_values
    feature_mag = np.zeros_like(feature_freqs)
    real_f_values = np.zeros_like(feature_freqs)
    thresholds = np.zeros_like(feature_freqs)
    is_peak = np.zeros_like(feature_freqs)

    # 전체 상한선을 반영하여 탐색 범위 결정
    j = 0
    for i, freq in enumerate(feature_freqs):
#         print(i)
        max_dev = max_deviation[i]
#         print(f"frequency : {freq}")
#         print(f"max_dev : {max_dev}")
        freq_below = (1 - 0.01 * max_dev) * freq
        freq_above = (1 + 0.01 * max_dev) * freq
        below_index = np.argmin(np.abs(f - freq_below))
        above_index = np.argmin(np.abs(f - freq_above))

        targets_mag = x_mag_[below_index : above_index + 1]
        target_index = below_index + np.argmax(targets_mag)

        feature_mag[i] = x_mag_[target_index]
        real_f_values[i] = f[target_index]
        thresholds[i] = peak_threshold[
            target_index]
        print(f"feature mag {i} : {feature_mag[i]}, real f value : {real_f_values[i]}, threshold : {thresholds[i]}")
        if feature_mag[i] > thresholds[i]:
            is_peak[i] = 1
            j += 1
    print("total no. of feature > thresholds :", j)
    
    return feature_mag, real_f_values, is_peak
'''

def get_spectral_features(
    f: np.ndarray,
    x_mag: np.ndarray,
    f_line: float,
    feature_freqs: np.ndarray,
    dev_limit: float,
    peak_threshold: np.ndarray,
    mode_env: False
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Get spectral_features

    Parameters
    ----------
    f: 1-d array
        frequency domain of data

    x_mag: 1-d array
        magnitude of fourier series

    f_line: float
        line frequency

    feature_freqs: 1-d array
        array containing feature
        frequencies; eg)[1x, 2x, 3x, 6x, etc...]

    dev_limit: float
        deviation limit for searching

    peak_threshold: 1-d array
        spectral threshold got from
        'get_peak_threshold' function

    Returns
    ----------
    feature_mag: 1-d array
        feature magnitudes

    real_f_values: 1-d array
        real feature frequencies considering deviation

    is_peak: 1-d array
        if each feature is peak or not
    """
    x_mag_ = x_mag.copy()
    # negative frequency 제거
    for i in range(len(feature_freqs)):
        if feature_freqs[i] < 0:
            feature_freqs[i] = 0
    
    # line frequency 제거
    f_to_be_deleted = f_line * 2
    to_be_deleted_ind = np.argmin(np.abs(f - f_to_be_deleted))
    x_mag_[to_be_deleted_ind - 2 : to_be_deleted_ind + 3] = x_mag_[to_be_deleted_ind + 3]  # 2x line frequency 제거

    # sort features (ascending)
    # print(feature_freqs)
    sort = np.argsort(feature_freqs)
    rev_sort = np.argsort(sort)
    feature_freqs_sorted = feature_freqs[sort]
    
    # calculate max_boundary, max_deviation
    max_deviation_temp = np.zeros_like(feature_freqs_sorted)
    max_deviation = np.zeros_like(feature_freqs_sorted)

    for i in range(feature_freqs_sorted.shape[0] - 1):
        a = feature_freqs_sorted[i]
        b = feature_freqs_sorted[i + 1]
        k = 100 * (b - a) / (a + b + 1e-6)
        max_deviation_temp[i] = np.min([k, dev_limit])
    max_deviation_temp[-1] = max_deviation_temp[-2]

    max_deviation[0] = max_deviation_temp[0]
    for i in range(1, max_deviation.shape[0] - 1):
        max_deviation[i] = np.min(max_deviation_temp[i - 1 : i + 2])

    max_deviation[-1] = max_deviation[-2]
    # rev_sort features
    max_deviation = max_deviation[rev_sort]
    
    # calculate feature_values
    feature_mag = np.zeros_like(feature_freqs)
    real_f_values = np.zeros_like(feature_freqs)
    thresholds = np.zeros_like(feature_freqs)
    is_peak = np.zeros_like(feature_freqs)

    # 전체 상한선을 반영하여 탐색 범위 결정
    j = 0
    threshold_index_to_control_list = []
    for i, freq in enumerate(feature_freqs):
        max_dev = max_deviation[i]
        freq_below = (1 - 0.02 * max_dev) * freq
        freq_above = (1 + 0.02 * max_dev) * freq
        below_index = np.argmin(np.abs(f - freq_below))
        above_index = np.argmin(np.abs(f - freq_above))

        targets_mag = x_mag_[below_index : above_index + 1]
        target_index = below_index + np.argmax(targets_mag)

        feature_mag[i] = x_mag_[target_index]
        real_f_values[i] = f[target_index]
        thresholds[i] = peak_threshold[target_index]
        
        # print((i) // 6)
        if not mode_env: # 베어링 아닐때
            if (i+1)%6 == 1 or (i+1)%6 == 2:
                if i//6 > 0:
                    # threshold_index_to_control_list.append(i)
                    thresholds[i] = 0.005
            if i >= 30:
                if feature_mag[0] > 0.01:
                    thresholds[i] = feature_mag[0] * 0.05
                else:
                    thresholds[i] = 0.005
        else:
            if (i+1)%6 == 1 or (i+1)%6 == 2:
                # threshold_index_to_control_list.append(i)
                thresholds[i] = 0.005
            if i >= 24:
                if feature_mag[0] > 0.01:
                    thresholds[i] = feature_mag[0] * 0.05
                else:
                    thresholds[i] = 0.005
        # print(f"{i+1}th value : {feature_mag[i]}, threshold : {thresholds[i]}")
        if feature_mag[i] > thresholds[i]:
            is_peak[i] = 1
            j += 1
    # print("total no. of feature > thresholds :", j)
    # from matplotlib import pyplot as plt
    # plt.figure(figsize = [20, 8])
    # plt.plot(f, x_mag)
    # plt.xlim([0, 200])
    # plt.ylim([0, 0.1])
    # plt.xticks(np.arange(0, 200, 10), rotation = 45)
    # plt.show()
    return feature_mag, real_f_values, is_peak

# trapzoidal integration
def integrate(
    x: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:
    """
    Trapzoidal integrate series

    Parameters
    ----------
    x: 1-d array
        series domain

    y: 1-d array
        series magnitude

    Returns
    ----------
    integrated: 1-d array
        trapzoidal integration of x and y
    """

    integrated = np.cumsum(0.5 * ((x[1:] - x[:-1]) * (y[1:] + y[:-1])))
    return integrated


# trapzoidal integration
def integrate_in_f(
    x: np.ndarray,
    fs: float,
) -> np.ndarray:
    """
    integrate in frequency domain

    Parameters
    ----------
    x: 1-d array
        series domain

    fs: float
        sampling freq

    Returns
    ----------
    integrated: 1-d array
        integration of x
    """
    x_len = x.shape[0]
    x_padded = np.hstack((x, np.zeros_like(x))).reshape([-1])
    x_k = rfft(x_padded)

    w_k = np.array([2 * np.pi * k * fs / (2 * x_len + 1e-6) for k in range(x_len + 1)])
    w_k[0] = 1
    h_i = 1 / (w_k * 1j)
    h_i[0] = 0

    y = x_k * h_i
    integrated = irfft(y)[:x_len]

    return integrated


# get_cavitation_features
def get_cavitation_features(
    f: np.ndarray,
    x_mag: np.ndarray,
    section_list: list = [200 + i * 180 for i in range(11)],
) -> np.ndarray:
    """
    Get spectral energy features for detection of pump cavitation

    Parameters
    ----------
    f: 1-d array
        frequency domain of data

    x_mag: 1-d array
        magnitude of fourier series

    section_list: list
        list condtaining section information;
        eg) [1000, 2000, 3000] for section 1000~2000, 2000~3000

    Returns
    ----------
    spectral_energy: 1-d array
        spectral energy for each section
    """
    spectral_power = x_mag**2
    spectral_energy = np.zeros([len(section_list) - 1])

    for i in range(len(section_list) - 1):
        start_ind = np.argmin(np.abs(f - section_list[i]))
        end_ind = np.argmin(np.abs(f - section_list[i + 1]))
        spectral_energy[i] = integrate(
            f[start_ind:end_ind], spectral_power[start_ind:end_ind]
        )[-1]
    
    return spectral_energy

# get_rms_velocity
def get_rms_velocity(
    acc_timeseries: np.ndarray,
    fs: float,
) -> float:
    """
    Get rms velocity

    Parameters
    ----------
    acc_timeseries: 1-d array
        accelertion in g

    fs: float
        sampling frequency

    Returns
    ----------
    rms_velocity: float
        rms velocity in mm/s
    """

    acc_filtered = do_butter_highpass_filter(acc_timeseries, 20, fs, 1)
    t = np.array([i / fs for i in range(acc_filtered.shape[0])])
    velocity = integrate(t, acc_filtered) * 9806  # g --> mm/s  , twkim  Acceleration of gravity = g (input이 가속도로 들어옴)
    velocity = velocity - np.mean(velocity)
    rms_velocity = np.sqrt(np.mean(velocity**2))

    return rms_velocity

'''

# get_rms_velocity (new_version)
def get_rms_velocity(acc_timeseries: np.ndarray, fs: float) -> float:

    """
    Get rms velocity

    Parameters
    ----------
    acc_timeseries: 1-d array
        accelertion in g

    fs: float
        sampling frequency

    Returns
    ----------
    rms_velocity: float
        rms velocity in mm/s
    """

    acc_filtered = do_butter_highpass_filter(acc_timeseries, 10, fs, 5)
    velocity = integrate_in_f(acc_filtered, fs) * 9806 # g --> mm/s
    velocity = velocity-np.mean(velocity)
    rms_velocity = np.sqrt(np.mean(velocity ** 2))

    return rms_velocity

'''
