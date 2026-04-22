from typing import Tuple

import numpy as np
from diagnosis_algorithms import (check_rms_alarm, diagnose_bearing,
                                  diagnose_rotor,
                                  diagnose_unbalance_misalignment)
from feature_extraction import (get_bearing_char_freqs, get_iqr_threshold,
                                get_rms_velocity, get_rotor_char_freqs,
                                get_spectral_features)
from motor_status import get_motor_1x
from preprocess import do_preprocess#, do_preprocess_atg


class motorDiagnosis:
    def __init__(self, f_rated: float, bpfs_r: list, n_poles : int, n_hist: int) -> None:
        # basic motor information
        self.f_rated = f_rated
        self.bpfs_r = bpfs_r

        # basic settings
        self.fs = 12800  # sampling rate
        # 펌프 케비테이션 진단을 위한 주파수 대역대로 추정
        #원본 설정
        #self.band_low = 2000
        #self.band_high = 4000
        #수정된 조건
        self.band_low = 200
        self.band_high = 2000
        
        self.n_harmonics = 6
        self.n_poles = n_poles
        self.dev_limit = 1

        # current status
        self.f_line = None
        self.timeseries = None
        self.f = None
        self.x_mag = None
        self.f_env = None
        self.x_mag_env = None
        self.peak_threshold = None
        self.peak_threshold_env = None
        self.if_on = None
        self.one_x = None
        self.run_steps = 0
        self.f_vg_atg = None
        self.x_mag_vg_atg = None
        
        # current feature output
        self.nxs_val = None
        self.nxs_freq = None
        self.nxs_is_peak = None

        self.bpfs_raw_val = None
        self.bpfs_raw_freq = None
        self.bpfs_raw_is_peak = None

        self.bpfs_env_val = None
        self.bpfs_env_freq = None
        self.bpfs_env_is_peak = None

        self.rotors_val = None
        self.rotors_freq = None
        self.rotors_is_peak = None

        self.v_rms = None

        # historical features of previous n_hist steps
        self.history_nxs_val = np.zeros([n_hist, self.n_harmonics])
        self.history_nxs_is_peak = np.zeros([n_hist, self.n_harmonics])

        self.history_bpfs_raw_val = np.zeros([n_hist, 4 * self.n_harmonics])
        self.history_bpfs_raw_is_peak = np.zeros([n_hist, 4 * self.n_harmonics])

        self.history_bpfs_env_val = np.zeros([n_hist, 4 * self.n_harmonics])
        self.history_bpfs_env_is_peak = np.zeros([n_hist, 4 * self.n_harmonics])

        self.history_rotors_val = np.zeros([n_hist, 4])
        self.history_rotors_is_peak = np.zeros([n_hist, 4])

        self.history_v_rms = np.zeros([n_hist])

    # preprocess
    # --> timeseries에서 raw spectrum, env spectrum 계산
    def preprocess(self, timeseries: np.ndarray, f_line: float) -> None:
        self.timeseries = timeseries
        (
            self.f,
            self.x_mag,
            self.f_env,
            self.x_mag_env,
        ) = do_preprocess(self.timeseries, self.band_low, self.band_high, self.fs, False)
        self.f_line = f_line
        
        return None

    # check_motor_status --> 모터의 현재 상태 확인 (on 여부, 1x 성분) 확인
    def check_motor_status(self, on_tag) -> None:
        # self.if_on = check_if_motor_on(self.f, self.x_mag, 2)
        self.if_on = on_tag
        self.one_x = get_motor_1x(self.f, self.x_mag, self.f_rated, self.f_line)
        
        if self.if_on:
            self.run_steps = self.run_steps + 1

        return None

    # get_iqr_thresholds: 피크 추출을 위한 경계 설정
    def get_iqr_thresholds(self, n: float = 2.25, l_filter: int = 50) -> None:
        q1, q3, self.peak_threshold = get_iqr_threshold(self.x_mag, n, l_filter)
        q1_env, q3_env, self.peak_threshold_env = get_iqr_threshold(
            self.x_mag_env, n, l_filter
        )

        return None

    # get_feqtures: 모터 관련 피쳐 추출
    def get_features(self) -> None:
        # prepare characteristic frequencies to be searched for
        nXs = self.one_x * np.array([i for i in range(1, self.n_harmonics + 1)])
        rotor_char_freqs = get_rotor_char_freqs(
            self.one_x, self.f_line, self.n_poles
        )
        bearing_char_freqs = get_bearing_char_freqs(
            self.f, self.x_mag, self.one_x, self.bpfs_r, self.n_harmonics, self.n_poles
        )
        char_freqs_combined = np.hstack((nXs, bearing_char_freqs, rotor_char_freqs))

        # search for values at characteristic frequencies
        raw_mag, raw_f, raw_is_peak = get_spectral_features(
            self.f,
            self.x_mag,
            self.f_line,
            char_freqs_combined,
            self.dev_limit,
            self.peak_threshold,
            False,
        )
        env_mag, env_f, env_is_peak = get_spectral_features(
            self.f_env,
            self.x_mag_env,
            self.f_line,
            bearing_char_freqs,
            self.dev_limit,
            self.peak_threshold_env,
            True,
        )

        # insert searched values
        self.nxs_freq = raw_f[: self.n_harmonics]
        self.nxs_val = raw_mag[: self.n_harmonics]
        self.nxs_is_peak = raw_is_peak[: self.n_harmonics]

        self.bpfs_raw_freq = raw_f[self.n_harmonics : 5 * self.n_harmonics]
        self.bpfs_raw_val = raw_mag[self.n_harmonics : 5 * self.n_harmonics]
        self.bpfs_raw_is_peak = raw_is_peak[self.n_harmonics : 5 * self.n_harmonics]

        self.bpfs_env_freq = env_f
        self.bpfs_env_val = env_mag
        self.bpfs_env_is_peak = env_is_peak

        self.rotors_freq = raw_f[-4:]
        self.rotors_val = raw_mag[-4:]
        self.rotors_is_peak = raw_is_peak[-4:]

        # search & insert rms velocity feature
        self.v_rms = get_rms_velocity(self.timeseries, self.fs)
        #print('#@#@#@#@get_features:',self.v_rms)
        return None

    # 중요 피쳐의 history 업데이트
    def update(self) -> None:
        if self.if_on:
            # update historical values of feature if motor is on
            self.history_nxs_val[:-1] = self.history_nxs_val[1:]
            self.history_nxs_val[-1] = self.nxs_val
            self.history_nxs_is_peak[:-1] = self.history_nxs_is_peak[1:]
            self.history_nxs_is_peak[-1] = self.nxs_is_peak

            self.history_bpfs_raw_val[:-1] = self.history_bpfs_raw_val[1:]
            self.history_bpfs_raw_val[-1] = self.bpfs_raw_val
            self.history_bpfs_raw_is_peak[:-1] = self.history_bpfs_raw_is_peak[1:]
            self.history_bpfs_raw_is_peak[-1] = self.bpfs_raw_is_peak

            self.history_bpfs_env_val[:-1] = self.history_bpfs_env_val[1:]
            self.history_bpfs_env_val[-1] = self.bpfs_env_val
            self.history_bpfs_env_is_peak[:-1] = self.history_bpfs_env_is_peak[1:]
            self.history_bpfs_env_is_peak[-1] = self.bpfs_env_is_peak

            self.history_rotors_val[:-1] = self.history_rotors_val[1:]
            self.history_rotors_val[-1] = self.rotors_val
            self.history_rotors_is_peak[:-1] = self.history_rotors_is_peak[1:]
            self.history_rotors_is_peak[-1] = self.rotors_is_peak

            self.history_v_rms[:-1] = self.history_v_rms[1:]
            self.history_v_rms[-1] = self.v_rms

        return None

    # 모터 진단
    def diagnose(
        self,
        unbal_misalign_sensitivity: int,
        bearing_sensitivity: int,
        rotor_sensitivity: int,
        rms_sensitivity: int,
    ) -> Tuple[
        float,
        bool,
        float,
        bool,
        float,
        bool,
        float,
        bool,
        bool,
        bool,
        bool,
        float,
        bool,
    ]:
        #print('@#@#@#@@-self.if_on:',self.if_on)
        #print('@#@#@#@@-self.run_steps:',self.run_steps)
        #print('@#@#@#@@-self.history_nxs_val.shape[0]:',self.history_nxs_val.shape[0])
        if self.if_on and self.run_steps >= self.history_nxs_val.shape[0]:
            (
                unbalance_amp,
                unbalance,
                misalignment_amp,
                misalignment,
            ) = diagnose_unbalance_misalignment(self.timeseries,
                self.history_nxs_val, self.v_rms, unbal_misalign_sensitivity, 4.5
            )
            rotor_amp, rotor = diagnose_rotor(
                self.history_rotors_is_peak, rotor_sensitivity
            )
            # bearing_amp, bpfo, bpfi, bsf, ftf = diagnose_bearing(self.x_mag,
            #     self.history_bpfs_env_is_peak, self.v_rms, bearing_sensitivity, 4.5 #, self.f_vg_atg, self.x_mag_vg_atg
            # )
            bearing_amp, bpfo, bpfi, bsf, ftf = diagnose_bearing(self.x_mag,
                self.history_bpfs_raw_is_peak, self.v_rms, bearing_sensitivity, 4.5 #, self.f_vg_atg, self.x_mag_vg_atg
            )
            v_rms = self.v_rms
            rms_alarm = check_rms_alarm(self.v_rms, "motor", rms_sensitivity)
            #print('@#@#@#@@diagnose if')

        else:
            unbalance_amp = 0
            unbalance = False
            misalignment_amp = 0
            misalignment = False
            rotor_amp = 0
            rotor = False
            bearing_amp = 0
            bpfo = False
            bpfi = False
            bsf = False
            ftf = False
            v_rms = 0
            rms_alarm = False
            #print('@#@#@#@@diagnose else')

        return (
            unbalance_amp,
            unbalance,
            misalignment_amp,
            misalignment,
            rotor_amp,
            rotor,
            bearing_amp,
            bpfo,
            bpfi,
            bsf,
            ftf,
            v_rms,
            rms_alarm,
        )
