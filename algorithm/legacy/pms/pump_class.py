from typing import Tuple

import numpy as np
from diagnosis_algorithms import (
    check_rms_alarm,
    diagnose_bearing,
    diagnose_cavitation,
    diagnose_impeller,
)
from feature_extraction import (
    get_bearing_char_freqs,
    get_cavitation_features,
    get_iqr_threshold,
    get_rms_velocity,
    get_spectral_features,
)
from motor_status import get_motor_1x
from preprocess import do_preprocess#, do_preprocess_atg


class PumpDiagnosis:
    def __init__(self, f_rated: float, bpfs_r: list, n_blades: list, n_hist: int) -> None:
        # basic pump information
        self.f_rated = f_rated
        self.BPFs_r = bpfs_r

        # basic settings
        self.fs = 12800
        self.band_low = 2000
        self.band_high = 3500
        self.n_harmonics = 6
        self.n_poles = n_blades
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

        self.spectral_energies = None

        self.v_rms = None

        # historical_features
        self.history_nxs_val = np.zeros([n_hist, self.n_harmonics])
        self.history_nxs_is_peak = np.zeros([n_hist, self.n_harmonics])

        self.history_bpfs_raw_val = np.zeros([n_hist, 4 * self.n_harmonics])
        self.history_bpfs_raw_is_peak = np.zeros([n_hist, 4 * self.n_harmonics])

        self.history_bpfs_env_val = np.zeros([n_hist, 4 * self.n_harmonics])
        self.history_bpfs_env_is_peak = np.zeros([n_hist, 4 * self.n_harmonics])

        self.history_spectral_energies_val = np.zeros([n_hist, 10])
        self.history_v_rms = np.zeros([n_hist])

    # preprocess --> raw spectrum, env spectrum 추출
    def preprocess(self, timeseries: np.ndarray, f_line: float) -> None:
        self.timeseries = timeseries
        (
            self.f,
            self.x_mag,
            self.f_env,
            self.x_mag_env,
        ) = do_preprocess(timeseries, self.band_low, self.band_high, self.fs)
        self.f_line = f_line
        # (
        #     self.f_vg_atg,
        #     self.x_mag_vg_atg,
        # ) = do_preprocess_atg(timeseries, self.band_low, self.band_high, self.fs)

        return None

    # check_pump_status --> 펌프의 현재상태 (on 여부, 1x 성분) 확인
    def check_pump_status(self, on_tag) -> None:
        # self.if_on = check_if_motor_on(self.f, self.x_mag, 10)
        self.if_on = on_tag
        self.one_x = get_motor_1x(self.f, self.x_mag, self.f_rated, self.f_line)
        if self.if_on:
            self.run_steps = self.run_steps + 1

        return None

    # get_iqr_thresholds: 피크 추출을 위한 경계 설정
    def get_iqr_thresholds(self, N: float = 2.25, l_filter: int = 50) -> None:
        q1, q3, self.peak_threshold = get_iqr_threshold(self.x_mag, N, l_filter)
        q1_env, q3_env, self.peak_threshold_env = get_iqr_threshold(
            self.x_mag_env, N, l_filter
        )

        return None

    # get_feqtures: 펌프 관련 피쳐 추출
    def get_features(self) -> None:
        # prepare characteristic frequencies to be searched for
        nXs = self.one_x * np.array([i for i in range(1, self.n_harmonics + 1)])
        bearing_char_freqs = get_bearing_char_freqs(
            self.f, self.x_mag, self.one_x, self.BPFs_r, self.n_harmonics, self.n_poles
        )
        char_freqs_combined = np.hstack((nXs, bearing_char_freqs))

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

        # search & insert spectral energies, rms_velocity feature
        self.spectral_energies = get_cavitation_features(
            self.f, self.x_mag, [200 + i * 180 for i in range(11)]
        )

        # search & insert rms velocity feature
        self.v_rms = get_rms_velocity(self.timeseries, self.fs)

        return None

    # update --> 추출 된 피쳐 중 중요한 피쳐의 저장
    def update(self) -> None:
        if self.if_on:
            # update historical values of feature if pump is on
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

            self.history_spectral_energies_val[
                :-1
            ] = self.history_spectral_energies_val[1:]
            self.history_spectral_energies_val[-1] = self.spectral_energies

            self.history_v_rms[:-1] = self.history_v_rms[1:]
            self.history_v_rms[-1] = self.v_rms

        return None

    # 펌프 진단
    def diagnose(
        self,
        impeller_sensitivity: int,
        bearing_sensitivity: int,
        cavitation_sensitivity: int,
        rms_sensitivity: int,
    ) -> Tuple[float, bool, float, bool, float, bool, bool, bool, bool, float, bool]:
        if self.if_on and self.run_steps >= self.history_nxs_val.shape[0]:
            cavitation_amp, cavitation = diagnose_cavitation(
                self.history_spectral_energies_val, cavitation_sensitivity
            )
            impeller_amp, impeller = diagnose_impeller(self.v_rms,
                self.timeseries, self.one_x, self.n_poles, self.f_line, self.fs, impeller_sensitivity
            )
            # bearing_amp, bpfo, bpfi, bsf, ftf = diagnose_bearing(self.x_mag,
            #     self.history_bpfs_env_is_peak, self.v_rms, bearing_sensitivity, 6.1 #, self.f_vg_atg, self.x_mag_vg_atg
            # )
            bearing_amp, bpfo, bpfi, bsf, ftf = diagnose_bearing(self.x_mag,
                self.history_bpfs_raw_is_peak, self.v_rms, bearing_sensitivity, 6.1 #, self.f_vg_atg, self.x_mag_vg_atg
            )
            v_rms = self.v_rms
            rms_alarm = check_rms_alarm(self.v_rms, "pump", rms_sensitivity)

        else:
            cavitation_amp = 0
            cavitation = False
            impeller_amp = 0
            impeller = False
            bearing_amp = 0
            bpfo = False
            bpfi = False
            bsf = False
            ftf = False
            v_rms = 0
            rms_alarm = False

        return (
            cavitation_amp,
            cavitation,
            impeller_amp,
            impeller,
            bearing_amp,
            bpfo,
            bpfi,
            bsf,
            ftf,
            v_rms,
            rms_alarm,
        )
