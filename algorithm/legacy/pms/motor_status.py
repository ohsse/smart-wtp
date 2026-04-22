import numpy as np

from matplotlib import pyplot as plt
from scipy.signal import butter, lfilter, freqz

## 안쓰임
# check if motor is on --> 추후 scada 데이터에서 오는 ON 신호로 변경
def check_if_motor_on(f: np.ndarray, x_mag: np.ndarray, criteria: float = 2) -> bool:
    """
    Check if motor is running or not

    Parameters
    ----------
    f: 1-d array
        frequency domain of data

    x_mag: 1-d array
        magnitude of fourier series

    criteria: float
        criteria for checking if motor is on

    Returns
    ----------
    if_motor_on: bool
        if motor is running or not
    """

    f_3000_ind = np.argmin(np.abs(f - 3000))
    f_4000_ind = np.argmin(np.abs(f - 4000))
    if_motor_on = np.mean(x_mag[f_3000_ind:f_4000_ind]) > criteria / x_mag.shape[0]

    return if_motor_on

def butter_bandstop(lowcut, highcut, fs = 60, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a

def bandstop_filter(data, lowcut, highcut, fs = 60, order=5):
    b, a = butter_bandstop(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# get motor 1x component
def get_motor_1x(
    f: np.ndarray, x_mag: np.ndarray, f_rated: float, f_line: float = 60
) -> float:
    """
    Get motor running speed

    Parameters
    ----------
    f: 1-d array
        frequency domain of data

    x_mag: 1-d array
        magnitude of fourier series

    f_rated: float
        rated speed of motor at 60 Hz (eg. 1189/60 Hz)

    f_line: float
        line frequency (60 Hz by default)

    Returns
    ----------
    motor_1x: bool
        location of 1x component
    """
    x_mag_ = x_mag.copy()
    
    f_to_be_deleted = f_line * 2
    to_be_deleted_ind = np.argmin(np.abs(f - f_to_be_deleted))

    x_mag_[to_be_deleted_ind - 2 : to_be_deleted_ind + 3] = x_mag_[
        to_be_deleted_ind + 3
    ]  # 2x line frequency 제거
    
    # x_mag_ = bandstop_filter(x_mag, f_line * 2 * 0.98, f_line * 2 * 1.02, fs = 12800, order=6)

    one_x_assumed = f_rated * f_line / 60

    l_ind = np.argmin(np.abs(f - 0.98 * one_x_assumed))
    r_ind = np.argmin(np.abs(f - 1.02 * one_x_assumed))
    
    one_x_ind = np.argmax(x_mag_[l_ind : r_ind + 1]) + l_ind
    motor_1x = f[one_x_ind]
    
    print(f"line freq : {np.round(f_line,2)} Hz, rated freq : {np.round(f_rated,2)} Hz, one_x_assumed : {np.round(one_x_assumed,2)} Hz, detected : {np.round(motor_1x,2)} Hz")
    plt.figure(figsize = [20, 8])
    plt.subplot(2,1,1)
    plt.axvline(motor_1x, color = 'red', linestyle='-.', linewidth = 0.8, label = '1X (detected)')
    plt.axvline(2*motor_1x, color = 'black', linestyle='-.', linewidth = 0.8, label = '2X (detected)')
    plt.axvline(6*motor_1x, color = 'green', linestyle='-.', linewidth = 0.8, label = '6X (assumed)')
    plt.grid()
    plt.plot(f, x_mag, color = 'blue', linestyle = 'solid',linewidth = 1.0, label = 'FFT of the signal')

    plt.xlim([0, 200])
    plt.ylim([0, 0.1])
    plt.xticks(np.arange(0, 200, 20), rotation = 45)
    plt.xlabel('Freqency')
    plt.ylabel('Magnitude')
    plt.legend()
    
    plt.subplot(2,1,2)
    plt.plot(f, x_mag, color = 'blue', linestyle = 'solid',linewidth = 1.0, label = 'FFT of the signal')
    plt.xlim([0, 12800])
    plt.ylim([0, 0.1])
    plt.grid()
    plt.xticks(np.arange(0, 12800, 400), rotation = 45)
    plt.show()

    return motor_1x
