from typing import Tuple

import numpy as np
# from numba import jit
from numpy.fft import fft, fftfreq
from scipy.signal import butter, hilbert, lfilter
from sklearn.linear_model import LinearRegression

## 특정 주파수 대역 분리
## Butterworth 대역통과 필터를 생성하고, 적용하여 특정 주파수 대역을 분리, 필터링된 출력 신호(시계열)를 반환
## Butterworth 필터는 통과대역에서 최대로 평탄한 응답을 갖고 정지대역으로 부드럽게 롤오프되는 일종의 무한 임펄스 응답(IIR) 필터
# bandpass filter
def do_butter_bandpass_filter(
    timeseries: np.ndarray, lowcut: float, highcut: float, fs: float, order: int = 1
) -> np.ndarray:
    """
    Bandpass filter

    Parameters
    ----------
    data: 1-d array
        timeseries data

    lowcut: float
        lowcut of band

    highcut: float
        highcut of band

    fs: float
        sampling frequency

    order: int
        order of butterworth bandpass filter

    Returns
    ----------
    y: 1-d array
        bandpassed timeseries data
    """

    nyq = 0.5 * fs     # scipy.signal.butter 함수에 따른 parameter (N, Wn, btype='Low', analog=False, output='ba', fs= None) 
                       # fs를 지정하면 Wn과 동일한 단위가 되지만 현재 코드에서는 지정하지 않았기 때문에 
                       # 디지털 필터의 경우 fs를 지정하지 않으면 Wn 단위는 0~1까지 정규화되며, 여기서 1은 나이퀴스트 주파수임
                       # 따라서 Wn은 반주기/샘플단위임 2*임계주파수/fs 로 정의됨 
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype="band")
    bandpass_filtered = lfilter(b, a, timeseries)
    ## butter : 필터 차수(order), 주파수 범위([low, high]) 및 필터 유형(btype)을 이용하여 -> 필터계수 생성
    ## lfilter : 필터링된 출력 신호(bandpass_filtered)를 반환

    return bandpass_filtered


# highpass filter
def do_butter_highpass_filter(
    timeseries: np.ndarray, cutoff: float, fs: float, order: int = 1
) -> np.ndarray:
    """
    Highpass filter

    Parameters
    ----------
    data: 1-d array
        timeseries data

    cutoff: float
        cutoff point

    fs: float
        sampling frequency #twkim defalut : 12800 , but sample data sampling rate 1000

    order: int
        order of bandpass filter

    Returns
    ----------
    y: 1-d array
        highpassed timeseries data
    """

    nyq = 0.5 * fs
    high = cutoff / nyq # 0.003125

    b, a = butter(order, high, btype="high", analog=False)
    highpass_filtered = lfilter(b, a, timeseries)

    return highpass_filtered


## 엔벨로프 스펙트럼을 얻기 위해 Hilbert 변환을 적용
# hilbert transform
def do_hilbert_transform(timeseries: np.ndarray) -> np.ndarray:
    """
    Bandpass filter and hilbert transform

    Parameters
    ----------
    timeseries: 1-d array
        timeseries data

    Returns
    ----------
    envelope: 1-d array
        timeseries bandpassed and hilbert transformed
    """

    envelope = np.abs(hilbert(timeseries))

    return envelope


## 'timeseries' 입력 신호를 매끄럽게 하고 스펙트럼 누출을 감소
## 입력 시계열에 해닝 윈도우를 적용하여 신호를 평활화하고 주파수 영역에서 스펙트럼 누출 감소
## 해닝 윈도우는 푸리에 변환을 수행하기 전에 신호에 적용되는 가중 코사인 함수.
## 창은 입력 시계열의 중앙을 중심으로 하고 길이는 입력과 동일합니다. 이 함수는 기간이 있는 시계열을 반환
# hanning window
def do_hanning_window(timeseries: np.ndarray) -> np.ndarray:
    """
    Return hanning windowed version of timeseries

    Parameters
    ----------
    timeseries: 1-d array
        timeseries data

    Returns
    ----------
    windowed: 1-d array
        hanning winodwed version of timeseries
    """

    windowed = timeseries * np.hanning(timeseries.shape[0])
    return windowed

## hanned을 FFT(고속 푸리에 변환)에 통과시켜, 주파수 영역(f)과 푸리에 급수의 크기(x_mag)를 생성
##'fft' : fft(Fast Fourier Transform)는 복소수 값 입력 신호에도 적용
##'rfft' : 고속 푸리에 변환(FFT) 알고리즘을 사용하여 실제 입력 신호의 1차원 이산 푸리에 변환(DFT)을 계산
##'rfftfreq' : rfft 출력(양의 주파수 성분)의 해당 주파수를 포함하는 입력 신호와 동일한 길이의 배열을 반환
# FFT
def do_fft(
    timeseries: np.ndarray, fs: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fast fourier transform

    Parameters
    ----------
    timeseries: 1-d array
        timeseries data

    fs: float
        sampling frequency

    Returns
    ----------
    f: 1-d array
        frequency domain

    x_mag: 1-d array
        magnitude of fourier series

    x_phase: 1-d array
        phase of fourier series
    """

    # x = rfft(timeseries)
    # n = timeseries.shape[0]  # 12800 by default
    # f = rfftfreq(n, d=1 / fs)
    
    x = fft(timeseries)
    n = timeseries.shape[0]
    f = fftfreq(n, d=1 / fs)  # Complete frequency range including negative frequencies

    x_mag = np.abs(x)
    x_mag = x_mag / (n / 2)

    return f, x_mag


# @jit
def get_merged_array(timeseries: np.ndarray, p: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    get merged array for get_AR_residual function

    Parameters
    ----------
    timeseries: 1-d array
        timeseries data

    p: int
        p term for autoregressive modeling

    Returns
    ----------
    X_train: n-d array
        p dimensional train array for get_AR_residual function

    Y_train: 1-d array
        p dimensional label array for get_AR_residual function
    """

    merged = np.zeros((timeseries.shape[0], p + 1))
    merged[:, 0:1] = timeseries

    for i in range(1, p + 1):
        merged[i:, i] = timeseries[:-i, 0]

    X_train = merged[p:, 1:]
    Y_train = merged[p:, 0]

    return X_train, Y_train


def get_AR_residual(timeseries: np.ndarray, p: int) -> np.ndarray:
    """
    get residual term from AR model

    Parameters
    ----------
    timeseries: 1-d array
        timeseries data

    p: int
        p term for autoregressive modeling

    Returns
    ----------
    residual: 1-d array
        residual from AR model
    """

    X_train, Y_train = get_merged_array(timeseries.reshape([-1, 1]), p)

    lr = LinearRegression()
    lr.fit(X_train, Y_train)

    prediction = X_train.dot(lr.coef_.T) + lr.intercept_
    prediction = np.hstack((timeseries[:p], prediction))
    residual = timeseries - prediction

    return residual


# # 'do_preprocess'
# # - input : 진동 데이터를 나타내는 1-d array timeseries,매개변수
# # 	timeseries: 진동 센서의 시계열 데이터를 나타내는 1차원 numpy 배열입니다. 결함을 분석하고 진단하기 전에 전처리가 필요한 원시 데이터입니다
# # 	env_lowcut: 엔벨로프 스펙트럼을 얻기 위해 Hilbert 변환을 적용하기 전에 대역 통과 필터에 대한 낮은 주파수 컷오프를 나타내는 플로트 값
# # 	env_highcut: 엔벨로프 스펙트럼을 얻기 위해 Hilbert 변환을 적용하기 전에 대역 통과 필터에 대한 더 높은 주파수 컷오프를 나타내는 부동 소수점 값
# # 	fs: 시계열 데이터의 샘플링 빈도(주파수)를 나타내는 float 값
# # 	AR: autoregressive(AR) 필터 사용 여부를 나타내는 boolean 값. True인 경우 함수는 원시 데이터에 AR 필터를 적용하여 데이터의 추세나 노이즈를 제거

# # - output : f, x_mag, f_env, x_mag_env, x_phase, 및 x_phase_env. (x_phase 및 x_phase_env 변수는 함수에서 반환되지 않음)
# # 	f: 전처리된 데이터의 푸리에 스펙트럼의 주파수 영역을 나타내는 1차원 numpy 배열.
# # 	x_mag: 전처리된 데이터의 푸리에 시리즈의 크기를 나타내는 1차원 numpy 배열.
# # 	f_env: 전처리된 데이터의 포락선 스펙트럼의 주파수 영역을 나타내는 1차원 numpy 배열.
# # 	x_mag_env: 전처리된 데이터의 포락선 스펙트럼의 푸리에 시리즈의 크기를 나타내는 1차원 numpy 배열.

## - 'do_hanning_window'  : 'timeseries' 입력의 스펙트럼 누출을 감소
## - 'do_fft' : hanned을 FFT(고속 푸리에 변환)에 통과시켜, 주파수 영역(f)과 푸리에 급수의 크기(x_mag)를 생성

## - 'get_AR_residual'  : 자동회귀(AR) 필터를 통과, 신호에서 고정 요소를 제거, 필터링된 시계열을 생성하는

## - 'do_butter_bandpass_filter' : timeseries를 Butterworth 대역 통과 필터에 통과 -> 대역 통과 필터링된 신호가 생성
## - 'do_hilbert_transform' 함수를 통해 Hilbert 변환을 통과하여 신호의 포락선을 생성


# preprocess
def do_preprocess(
    timeseries: np.ndarray,
    env_lowcut: float,
    env_highcut: float,
    fs: float,
    AR: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Preprocess data
    timeseries -> hanned -> fft
    timeseries -> bandpassfilter -> hilbert -> env_fft

    Parameters
    ----------
    timeseries: 1-d array
        timeseries data

    env_lowcut: float
        lowcut for bandpass filter before hilbert transform

    env_highcut: float
        highcut for bandpass filter before hilbert transform

    fs: float
        sampling frequency of timeseries

    AR: bool
        option whether to use AR filter or not

    Returns
    ----------
    f: 1-d array
        frequency domain

    x_mag: 1-d array
        magnitude of fourier series

    # x_phase: 1-d array
    #     phase of fourier series

    f_env: 1-d array
        frequency domain of env spectrum

    x_mag_env: 1-d array
        magnitude of fourier series of env spectrum

    # x_phase_env: 1-d array
    #     phase of fourier series of env spectrum
    """

    hanned = do_hanning_window(timeseries)
    f, x_mag = do_fft(hanned, fs)
    
    if AR is True:
        timeseries = get_AR_residual(timeseries, 40)
    
     # ------ f, x_mag 전처리 루트, f_env, x_mag_env 전처리 루트로 나눠짐
    
    bandpassed = do_butter_bandpass_filter(timeseries, env_lowcut, env_highcut, fs, 1) # (2 ~ 4 kHz)
    envelope = do_hilbert_transform(bandpassed)
    hanned_env = do_hanning_window(envelope)
    f_env, x_mag_env = do_fft(hanned_env, fs)

    return f, x_mag, f_env, x_mag_env


# # preprocess
# def do_preprocess_atg(
#     timeseries: np.ndarray,
#     env_lowcut: float,
#     env_highcut: float,
#     fs: float,
#     AR: bool = False,
# ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
#     """
#     Preprocess data
#     timeseries -> hanned -> fft
#     timeseries -> bandpassfilter -> hilbert -> env_fft

#     Parameters
#     ----------
#     timeseries: 1-d array
#         timeseries data

#     env_lowcut: float
#         lowcut for bandpass filter before hilbert transform

#     env_highcut: float
#         highcut for bandpass filter before hilbert transform

#     fs: float
#         sampling frequency of timeseries

#     AR: bool
#         option whether to use AR filter or not

#     Returns
#     ----------
#     f: 1-d array
#         frequency domain

#     x_mag: 1-d array
#         magnitude of fourier series

#     # x_phase: 1-d array
#     #     phase of fourier series

#     f_env: 1-d array
#         frequency domain of env spectrum

#     x_mag_env: 1-d array
#         magnitude of fourier series of env spectrum

#     # x_phase_env: 1-d array
#     #     phase of fourier series of env spectrum
#     """

#     t = np.array([i / fs for i in range(timeseries.shape[0])])
#     velocity = np.cumsum(0.5 * ((t[1:] - t[:-1])*(timeseries[1:] + timeseries[:-1]))) * 9806
#     velocity_g = integrate(t[:], timeseries[:]) * 9806

#     windowed_vg = do_hanning_window(velocity_g)
#     f_vg, x_mag_vg = do_fft(windowed_vg, fs)
    

#     return f_vg, x_mag_vg
