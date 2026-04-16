# MariaDB DDL Export

- Database: `EMS_DB_GS_DUMP_241113`
- Generated at: `2026-04-09 17:36:39`
- Table count: `95`

## Table List

- `TB_AI_MODE_RST`
- `TB_AVL_GRP`
- `TB_BASE_SAVINGS_TARGET`
- `TB_BASE_SAVING_CHART`
- `TB_CTR_OPT_RST`
- `TB_CTR_OPT_RST2`
- `TB_CTR_PRF_PUMPMST_INF`
- `TB_CTR_PUMPYN_INQUIRY`
- `TB_CTR_PUMPYN_RST`
- `TB_CTR_PUMP_OPT_LOG`
- `TB_CTR_PUMP_REQ_OPT`
- `TB_CTR_TNK_INF`
- `TB_CTR_TNK_INF_1119`
- `TB_CTR_TNK_RST`
- `TB_EMS_ALR`
- `TB_EPA_PUMP_FLOW`
- `TB_EPA_SIM_RESV_FLOW`
- `TB_EPA_TAG_INFO`
- `TB_FAC`
- `TB_FAC_OLD`
- `TB_FP_SI_VAL`
- `TB_FP_VAL`
- `TB_FR_SI_VAL`
- `TB_FR_VAL`
- `TB_GOALSETTING`
- `TB_HMI_ALR_TAG`
- `TB_HMI_CTR_LOG`
- `TB_HMI_CTR_TAG`
- `TB_HMI_TRNSP_TAG`
- `TB_LINK_GRP`
- `TB_LOG_TABLE`
- `TB_MERGE`
- `TB_MNL_CHN_LOG`
- `TB_MONTHLY_PEAK`
- `TB_NODE_TAG`
- `TB_NODE_TAG_11190`
- `TB_OPER_INF`
- `TB_PEAK_GNRTD_RST`
- `TB_PEAK_LOG`
- `TB_PEAK_PRDCT_RST`
- `TB_PEAK_PRTCP_INF`
- `TB_PEAK_PWR_PRDCT_RST`
- `TB_PEAK_RT_TAGHRR_INF`
- `TB_PEAK_RT_TAG_INF`
- `TB_PEAK_SCHDL_RST`
- `TB_PEAK_TAG_INF`
- `TB_PEAK_TAG_INF_GM_250725`
- `TB_PEAK_TAG_INF_HP_250725`
- `TB_PRF_INVRT_RST`
- `TB_PRF_PRFRM_RST`
- `TB_PRF_PUMPYN_RST`
- `TB_PRODUCER_DATA`
- `TB_PTR_CTR_ANLY_RST`
- `TB_PTR_CTR_INF`
- `TB_PTR_HALF_CTR_TAG`
- `TB_PTR_ORC_RST`
- `TB_PTR_STRTG_INF`
- `TB_PUMP_CAL`
- `TB_PUMP_CAL_0718`
- `TB_PUMP_CAL_20250418`
- `TB_PUMP_CAL_20250528`
- `TB_PUMP_CAL_250718`
- `TB_PUMP_CAL_250812`
- `TB_PUMP_CAL_260324`
- `TB_PUMP_CAL_BACKUP`
- `TB_PUMP_CAL_OLD`
- `TB_PUMP_COMBINATION`
- `TB_PUMP_COMBINATION_INF`
- `TB_PUMP_COMBINATION_INF_OLD`
- `TB_PUMP_COMBINATION_OLD`
- `TB_PUMP_COMB_POWER`
- `TB_PUMP_CTR_RTM`
- `TB_RAWDATA`
- `TB_RAWDATA_15MIN`
- `TB_RAWDATA_DAY`
- `TB_RAWDATA_DAY_INGRT`
- `TB_RAWDATA_HOUR`
- `TB_RAWDATA_HOUR_INGRT`
- `TB_RAWDATA_MONTH`
- `TB_RAWDATA_MONTH_INGRT`
- `TB_RAWDATA_PMB_HOUR`
- `TB_RST_SAVINGS_TARGET`
- `TB_RT_JOB_INF`
- `TB_RT_MSTR_INF`
- `TB_RT_POWER_RST`
- `TB_RT_RATE_INF`
- `TB_RT_RATE_RST`
- `TB_TAGINFO`
- `TB_TAG_UNIT_INFO`
- `TB_TNK_GRP_INF`
- `TB_TOT_ALG`
- `TB_TOT_GRP`
- `TB_WPP_TAG_CODE`
- `TB_WPP_TAG_INF`
- `TB_ZONE`

## `TB_AI_MODE_RST`

```sql
CREATE TABLE `TB_AI_MODE_RST` (
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록시간',
  `PUMP_GRP` varchar(1) NOT NULL COMMENT '펌프그룹',
  `AI_MODE` varchar(10) DEFAULT '2' COMMENT 'AI모드',
  `IS_WORK` varchar(1) DEFAULT '0' COMMENT '실제 동작 여부',
  `CUR_PUMP` varchar(100) DEFAULT NULL COMMENT '실제 가동 펌프 이력',
  `PRE_PUMP` varchar(100) DEFAULT NULL COMMENT ' 예측 펌프 조합',
  `FLOW_CTR` varchar(100) DEFAULT NULL COMMENT '증감운전 여부',
  PRIMARY KEY (`RGSTR_TIME`,`PUMP_GRP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='AI 모드 결과'
```

## `TB_AVL_GRP`

```sql
CREATE TABLE `TB_AVL_GRP` (
  `STN_FLW_VAL` int(11) NOT NULL COMMENT '기준유량값',
  `GRP_A_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_A_여부',
  `GRP_B_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_B_여부',
  `GRP_C_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_C_여부',
  `GRP_D_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_D_여부',
  `GRP_E_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_E_여부',
  `GRP_F_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_F_여부',
  `GRP_G_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_G_여부',
  `GRP_H_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_H_여부',
  `GRP_I_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_I_여부',
  `GRP_J_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_J_여부',
  `GRP_K_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_K_여부',
  `GRP_L_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_L_여부',
  `GRP_M_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_M_여부',
  `GRP_N_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_N_여부',
  `GRP_V_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_V_여부',
  `GRP_X_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_X_여부',
  `GRP_Z_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_Z_여부',
  `GRP_DD_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_DD_여부',
  `GRP_GG_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_GG_여부',
  `GRP_HH_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_HH_여부',
  `GRP_MM_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_MM_여부',
  `GRP_NN_YN` tinyint(1) NOT NULL DEFAULT 0 COMMENT '그룹_NN_여부',
  PRIMARY KEY (`STN_FLW_VAL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='사용가능그룹'
```

## `TB_BASE_SAVINGS_TARGET`

```sql
CREATE TABLE `TB_BASE_SAVINGS_TARGET` (
  `TYPE` varchar(50) DEFAULT NULL COMMENT '타입',
  `MNTH` varchar(3) DEFAULT NULL COMMENT '월',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값',
  `UNIT` varchar(10) DEFAULT NULL COMMENT '단위'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='전력 절감 결과'
```

## `TB_BASE_SAVING_CHART`

```sql
CREATE TABLE `TB_BASE_SAVING_CHART` (
  `TIME` datetime DEFAULT NULL COMMENT '일시',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='일별 전력 절감량'
```

## `TB_CTR_OPT_RST`

```sql
CREATE TABLE `TB_CTR_OPT_RST` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `OPT_IDX` varchar(200) NOT NULL COMMENT '펌프제어KEY',
  `ANLY_TIME` datetime NOT NULL COMMENT '분석일시',
  `PRDCT_TIME` datetime NOT NULL COMMENT '예측일시',
  `PRDCT_TIME_DIFF` int(11) NOT NULL COMMENT '예측시차',
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `PRDCT_MEAN` float NOT NULL COMMENT '예측값 평균',
  `PRDCT_STD` float NOT NULL COMMENT '예측값 표준편차',
  `TUBE_PRSR_PRDCT` float NOT NULL COMMENT '관압 예측값',
  `PWR_PRDCT` float NOT NULL COMMENT '전력량 예측값',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`OPT_IDX`,`ANLY_TIME`,`PRDCT_TIME`,`RGSTR_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='최적 펌프제어 지역결과'
```

## `TB_CTR_OPT_RST2`

```sql
CREATE TABLE `TB_CTR_OPT_RST2` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `OPT_IDX` varchar(200) DEFAULT NULL COMMENT '펌프제어KEY',
  `ANLY_TIME` datetime DEFAULT NULL COMMENT '분석일시',
  `PRDCT_TIME` datetime NOT NULL COMMENT '예측일시',
  `PRDCT_TIME_DIFF` int(11) NOT NULL COMMENT '예측시차',
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `PRDCT_MEAN` float NOT NULL COMMENT '예측값 평균',
  `PRDCT_STD` float NOT NULL COMMENT '예측값 표준편차',
  `TUBE_PRSR_PRDCT` float NOT NULL COMMENT '관압 예측값',
  `PWR_PRDCT` float NOT NULL COMMENT '전력량 예측값',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='최적 펌프제어 지역결과'
```

## `TB_CTR_PRF_PUMPMST_INF`

```sql
CREATE TABLE `TB_CTR_PRF_PUMPMST_INF` (
  `WPP_CODE` varchar(7) NOT NULL COMMENT '정수장 코드',
  `PUMP_IDX` int(11) NOT NULL COMMENT '펌프인덱스',
  `LEI_IDX` int(11) NOT NULL DEFAULT 1 COMMENT '수위 인덱스',
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `PUMP_GRP_IDX` int(11) NOT NULL COMMENT '펌프 그룹 인덱스',
  `PUMP_GRP_NM` varchar(200) DEFAULT NULL COMMENT '펌프 그룹 이름',
  `PUMP_GRP_DSC` varchar(200) DEFAULT NULL COMMENT '펌프 그룹(지역) 설명',
  `PUMP_NM` varchar(100) DEFAULT NULL COMMENT '펌프 이름',
  `PUMP_TYP` int(11) NOT NULL COMMENT '펌프타입',
  `PUMP_TYP_DSC` varchar(200) DEFAULT NULL COMMENT '펌프타입 설명',
  `PUMP_CTR_TYP` char(1) NOT NULL DEFAULT '1' COMMENT '펌프 제어 타입',
  `TNK_GRP_IDX` int(11) DEFAULT NULL COMMENT '탱크 그룹 인덱스',
  `PRI_S_TAG` varchar(30) DEFAULT NULL COMMENT '흡입압력태그',
  `PRI_D_TAG` varchar(30) DEFAULT NULL COMMENT '토출압력태그',
  `PRI_T_TAG` varchar(30) NOT NULL COMMENT '전체압력태그',
  `CTI_TAG` varchar(30) DEFAULT NULL COMMENT '주파수태그',
  `SPI_TAG` varchar(30) DEFAULT NULL COMMENT '주파수태그',
  `FRI_TAG` varchar(30) NOT NULL COMMENT '유량태그',
  `FRQ_TAG` varchar(30) DEFAULT NULL COMMENT '유출유량 적산 태그',
  `TEI_TAG` varchar(30) NOT NULL COMMENT '수온태그',
  `PWI_TAG` varchar(30) NOT NULL COMMENT '전력순시태그',
  `PWQ_TAG` varchar(30) DEFAULT NULL COMMENT '적산 태그',
  `PMB_TAG` varchar(30) NOT NULL COMMENT '펌프작동여부태그',
  `PMB_FLT_TAG` varchar(30) DEFAULT NULL COMMENT '펌프작동실패여부태그',
  `LEI_TAG` varchar(30) DEFAULT NULL COMMENT '수위 태그',
  `VVB_D_TAG` varchar(30) DEFAULT NULL COMMENT '토출밸브 연동',
  `VVB_D_TAG_USE_YN` char(1) DEFAULT NULL COMMENT '토출밸브 연동 사용여부',
  `EMS_MIN_WPP_TAG` varchar(30) DEFAULT NULL COMMENT '최소요구관압정수장',
  `EMS_MIN_WPJ_TAG` varchar(30) DEFAULT NULL COMMENT '최소요구관압분기점',
  `DUTY_H` float NOT NULL COMMENT '정격양정',
  `DUTY_Q` float NOT NULL COMMENT '정격유량',
  `PRRT_TYP` varchar(9) NOT NULL COMMENT '펌프우선순위 타입',
  `PRRT_RNK` int(10) NOT NULL COMMENT '펌프우선순위',
  `ANLY_RNK` int(10) NOT NULL COMMENT '분석펌프우선순위',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용 여부',
  `USER_RNK` int(10) NOT NULL COMMENT '사용자정의 펌프 우선순위',
  `PMS_USE_YN` char(1) DEFAULT '1' COMMENT '사용자 지정 펌프 사용여부',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `CTR_AUTO_TAG` varchar(30) DEFAULT NULL COMMENT 'AI 운영 자동 태그',
  `CTR_MANUAL_TAG` varchar(30) DEFAULT NULL COMMENT 'AI운영 반자동 태그',
  `CTR_AUTO_STOP_TAG` varchar(30) DEFAULT NULL COMMENT '가동중지 태그',
  `CTR_AUTO_FREQ_TAG` varchar(30) DEFAULT NULL COMMENT '주파수 제어 태그',
  `CTR_SYNC_TAG` varchar(30) DEFAULT NULL COMMENT '동기화 태그(운문)',
  PRIMARY KEY (`WPP_CODE`,`PUMP_IDX`,`PUMP_GRP`,`PUMP_GRP_IDX`,`PUMP_TYP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프 마스터(펌프특성곡선사용태그)'
```

## `TB_CTR_PUMPYN_INQUIRY`

```sql
CREATE TABLE `TB_CTR_PUMPYN_INQUIRY` (
  `OPT_IDX` varchar(200) NOT NULL COMMENT '펌프제어KEY("PRDCT_RUN_TIME"_"PRDCT_T_DIFF"_" LCTN")',
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `PUMP_IDX` int(11) NOT NULL COMMENT '펌프인덱스',
  `PUMP_TYP` int(11) DEFAULT NULL COMMENT '펌프타입(1 노말펌프, 2 인버터 펌프)',
  `PUMP_YN` char(1) DEFAULT '1' COMMENT '작동 여부',
  `FREQ` decimal(4,2) DEFAULT NULL COMMENT '주파수',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록 일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  `PRDCT_MEAN` float NOT NULL COMMENT '예측값 평균',
  `TUBE_PRSR_PRDCT` float NOT NULL COMMENT '관압 예측값',
  `PWR_PRDCT` float NOT NULL COMMENT '전력 예측값',
  `PRDCT_TIME_DIFF` int(11) NOT NULL DEFAULT 5 COMMENT '예측시차',
  `RATE_CTGRY` varchar(10) DEFAULT NULL COMMENT '전력 부하 종류',
  `FLOW_CTR` varchar(3) DEFAULT NULL COMMENT '유량 여부',
  PRIMARY KEY (`OPT_IDX`,`PUMP_GRP`,`PUMP_IDX`,`RGSTR_TIME`),
  KEY `TB_CTR_PUMPYN_RST_PUMP_GRP_IDX` (`PUMP_GRP`,`OPT_IDX`,`PUMP_IDX`) USING BTREE,
  KEY `TB_CTR_PUMPYN_INQUIRY_OPT_IDX_IDX` (`OPT_IDX`,`PUMP_IDX`,`PUMP_GRP`,`RGSTR_TIME`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='최적 펌프제어 펌프 결과'
```

## `TB_CTR_PUMPYN_RST`

```sql
CREATE TABLE `TB_CTR_PUMPYN_RST` (
  `OPT_IDX` varchar(200) NOT NULL COMMENT '펌프제어KEY',
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `PUMP_IDX` int(11) NOT NULL COMMENT '펌프인덱스',
  `PUMP_TYP` int(11) DEFAULT NULL COMMENT '펌프타입',
  `PUMP_YN` varchar(5) DEFAULT '1' COMMENT '펌프 작동 여부',
  `FREQ` decimal(4,2) DEFAULT NULL COMMENT '주파수',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `PWR_PRDCT` float DEFAULT NULL,
  `PRDCT_MEAN` float DEFAULT NULL COMMENT '예상 유량',
  `TUBE_PRSR_PRDCT` float DEFAULT NULL COMMENT '예상 관압',
  `PRDCT_TIME_DIFF` int(11) NOT NULL DEFAULT 5,
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  PRIMARY KEY (`OPT_IDX`,`PUMP_GRP`,`PUMP_IDX`,`PRDCT_TIME_DIFF`),
  KEY `TB_CTR_PUMPYN_RST_OPT_IDX_IDX` (`OPT_IDX`,`PUMP_IDX`,`PUMP_GRP`,`RGSTR_TIME`) USING BTREE,
  KEY `TB_CTR_PUMPYN_RST_PUMP_GRP_IDX` (`PUMP_GRP`) USING BTREE,
  KEY `TB_CTR_PUMPYN_RST_PUMP_IDX_IDX` (`PUMP_IDX`) USING BTREE,
  KEY `TB_CTR_PUMPYN_RST_RGSTR_TIME_IDX` (`RGSTR_TIME`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='최적 펌프제어 펌프 결과'
```

## `TB_CTR_PUMP_OPT_LOG`

```sql
CREATE TABLE `TB_CTR_PUMP_OPT_LOG` (
  `PUMP_GRP` int(11) NOT NULL DEFAULT 0 COMMENT '펌프 그룹 아이디',
  `PUMP_YN_LIST` varchar(100) DEFAULT NULL COMMENT '펌프 가동 이력',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT '확인여부'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='부분 AI 운전 이력 정보'
```

## `TB_CTR_PUMP_REQ_OPT`

```sql
CREATE TABLE `TB_CTR_PUMP_REQ_OPT` (
  `WPP_CODE` varchar(7) NOT NULL COMMENT '정수장_코드',
  `PUMP_IDX` int(11) NOT NULL COMMENT '펌프인덱스',
  `PUMP_CTR_TYP` char(1) NOT NULL DEFAULT '1' COMMENT '펌프_제어_타입',
  `REQ_TAG` varchar(45) NOT NULL COMMENT '선행조건 태그명',
  `REQ_CTR_TAG` varchar(100) NOT NULL COMMENT '선행조건 제어 시작 태그',
  `REQ_CTR_STOP_TAG` varchar(45) DEFAULT NULL COMMENT '선행조건 제어 종료 태그',
  `STD_VALUE` int(11) DEFAULT NULL COMMENT '제어 기준 값',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용_여부',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() COMMENT '업데이트_일시',
  PRIMARY KEY (`WPP_CODE`,`PUMP_IDX`,`PUMP_CTR_TYP`,`REQ_TAG`,`REQ_CTR_TAG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프 동작 선행조건'
```

## `TB_CTR_TNK_INF`

```sql
CREATE TABLE `TB_CTR_TNK_INF` (
  `SRTTN` varchar(100) NOT NULL COMMENT '분류',
  `TYPE` int(11) NOT NULL DEFAULT 1 COMMENT '분류타입',
  `FRI_TAG` varchar(50) DEFAULT NULL COMMENT '유량태그',
  `PRI_TAG` varchar(50) DEFAULT NULL COMMENT '압력태그',
  `DSTRB_Q_ID` varchar(50) DEFAULT NULL COMMENT '유량예측변수',
  `DSTRB_P_ID` varchar(50) DEFAULT NULL COMMENT '압력예측변수',
  `NODE_ID` varchar(50) DEFAULT NULL COMMENT 'NODE_ID',
  `LINK_ID` varchar(50) DEFAULT NULL COMMENT '링크ID',
  `USE_YN` tinyint(1) NOT NULL DEFAULT 1 COMMENT '엑셀사용여부',
  PRIMARY KEY (`SRTTN`),
  KEY `TB_CTR_TNK_INF_DSTRB_P_ID_IDX` (`DSTRB_P_ID`) USING BTREE,
  KEY `TB_CTR_TNK_INF_DSTRB_Q_ID_IDX` (`DSTRB_Q_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='배수지및분기태그정의'
```

## `TB_CTR_TNK_INF_1119`

```sql
CREATE TABLE `TB_CTR_TNK_INF_1119` (
  `SRTTN` varchar(100) NOT NULL COMMENT '분류',
  `TYPE` int(11) NOT NULL DEFAULT 1 COMMENT '분류타입',
  `FRI_TAG` varchar(50) DEFAULT NULL COMMENT '유량태그',
  `PRI_TAG` varchar(50) DEFAULT NULL COMMENT '압력태그',
  `DSTRB_Q_ID` varchar(50) DEFAULT NULL COMMENT '유량예측변수',
  `DSTRB_P_ID` varchar(50) DEFAULT NULL COMMENT '압력예측변수',
  `NODE_ID` varchar(50) DEFAULT NULL COMMENT 'NODE_ID',
  `LINK_ID` varchar(50) DEFAULT NULL COMMENT '링크ID',
  `USE_YN` tinyint(1) NOT NULL DEFAULT 1 COMMENT '엑셀사용여부',
  PRIMARY KEY (`SRTTN`),
  KEY `TB_CTR_TNK_INF_DSTRB_P_ID_IDX` (`DSTRB_P_ID`) USING BTREE,
  KEY `TB_CTR_TNK_INF_DSTRB_Q_ID_IDX` (`DSTRB_Q_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='배수지및분기태그정의'
```

## `TB_CTR_TNK_RST`

```sql
CREATE TABLE `TB_CTR_TNK_RST` (
  `DSTRB_ID` varchar(100) NOT NULL COMMENT '예측ID',
  `PRDCT_VALUE` float DEFAULT 0 COMMENT '예측값',
  `RGSTR_TIME` datetime NOT NULL COMMENT '등록일시',
  PRIMARY KEY (`DSTRB_ID`,`RGSTR_TIME`),
  KEY `TB_CTR_TNK_RST_RGSTR_TIME_IDX` (`RGSTR_TIME`,`DSTRB_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='배수지및분기결과'
```

## `TB_EMS_ALR`

```sql
CREATE TABLE `TB_EMS_ALR` (
  `ALR_ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '알람 ID',
  `ALR_TYP` varchar(20) NOT NULL,
  `ALR_TIME` varchar(50) NOT NULL COMMENT '일시',
  `AI_WEB` char(1) DEFAULT NULL COMMENT 'AI WEB',
  `AI_SCADA` char(1) DEFAULT NULL COMMENT 'AI SCADA',
  `EMS_WEB` char(1) DEFAULT NULL COMMENT 'EMS WEB',
  `EMS_SCADA` char(1) DEFAULT NULL COMMENT 'EMS SCADA',
  `PMS_WEB` char(1) DEFAULT NULL COMMENT 'PMS WEB',
  `PMS_SCADA` char(1) DEFAULT NULL COMMENT 'PMS SCADA',
  `MSG` varchar(2000) DEFAULT NULL COMMENT '메세지',
  `LINK` varchar(50) DEFAULT NULL COMMENT '주소',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT NULL ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부 (0:전송 대상/1:표현대상/2:확인완료)',
  PRIMARY KEY (`ALR_ID`,`ALR_TYP`,`ALR_TIME`,`RGSTR_TIME`)
) ENGINE=InnoDB AUTO_INCREMENT=16748 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='알람 발생 정보'
```

## `TB_EPA_PUMP_FLOW`

```sql
CREATE TABLE `TB_EPA_PUMP_FLOW` (
  `IDX` int(11) NOT NULL AUTO_INCREMENT COMMENT '인덱스',
  `PUMP_COMB` varchar(100) NOT NULL COMMENT '펌프조합',
  `MIN_FLOW` double NOT NULL COMMENT '최소유량',
  `MAX_FLOW` double NOT NULL COMMENT '최대유량',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '기록일시',
  PRIMARY KEY (`IDX`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='관망분석펌프설정및유량범위'
```

## `TB_EPA_SIM_RESV_FLOW`

```sql
CREATE TABLE `TB_EPA_SIM_RESV_FLOW` (
  `NODE_ID` varchar(50) NOT NULL COMMENT 'NODE아이디',
  `INFLOW_TAG` varchar(100) NOT NULL COMMENT '유입태그',
  `TNK_NM` varchar(100) NOT NULL COMMENT '배수지명',
  `FLOW_RATE` double NOT NULL DEFAULT 1000 COMMENT '유량',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '수정일시',
  `DISPLAY_ORDER` int(11) DEFAULT 0 COMMENT '순서',
  PRIMARY KEY (`NODE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='관망해석유량설정'
```

## `TB_EPA_TAG_INFO`

```sql
CREATE TABLE `TB_EPA_TAG_INFO` (
  `LOCATION_NM` varchar(100) NOT NULL COMMENT '위치명',
  `JUNCTION_ID` varchar(100) DEFAULT NULL COMMENT '정션ID',
  `PIPE_ID` varchar(100) DEFAULT NULL COMMENT '파이프ID',
  `PRI_TAG` varchar(50) DEFAULT NULL COMMENT '압력태그',
  `FRI_TAG` varchar(50) DEFAULT NULL COMMENT '유량태그',
  `DISPLAY_ORDER` int(11) DEFAULT 0 COMMENT '화면정렬인덱스',
  `IS_DISPLAY` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`LOCATION_NM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='EPA 관망 분석 태그 정보'
```

## `TB_FAC`

```sql
CREATE TABLE `TB_FAC` (
  `FAC_CODE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '설비 코드',
  `FAC_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '설비 이름',
  `DSC` varchar(50) DEFAULT NULL COMMENT '설명',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용 여부',
  `DCS` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`FAC_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='설비 정보'
```

## `TB_FAC_OLD`

```sql
CREATE TABLE `TB_FAC_OLD` (
  `FAC_CODE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '설비 코드',
  `FAC_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '설비 이름',
  `DSC` varchar(50) DEFAULT NULL COMMENT '설명',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용 여부',
  `DCS` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`FAC_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='설비 정보'
```

## `TB_FP_SI_VAL`

```sql
CREATE TABLE `TB_FP_SI_VAL` (
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `NODE_ID` varchar(100) NOT NULL COMMENT 'NODE_ID',
  `FP_VAL` float DEFAULT 0 COMMENT '유압값',
  `FP_ALG_RST_VAL` float DEFAULT NULL COMMENT '유압알고리즘결과값',
  `FLG` varchar(10) NOT NULL DEFAULT 'CUR' COMMENT '플래그',
  PRIMARY KEY (`NODE_ID`,`RGSTR_TIME`,`FLG`),
  KEY `TB_FP_SI_VAL_RGSTR_TIME_IDX` (`RGSTR_TIME`,`FLG`) USING BTREE,
  KEY `TB_FP_SI_VAL_FLG_IDX` (`FLG`,`RGSTR_TIME`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='유압값'
```

## `TB_FP_VAL`

```sql
CREATE TABLE `TB_FP_VAL` (
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `NODE_ID` varchar(100) NOT NULL COMMENT 'NODE_ID',
  `FP_VAL` float DEFAULT NULL COMMENT '유압값',
  `FP_ALG_RST_VAL` float DEFAULT NULL COMMENT '유압알고리즘결과값',
  `FLG` varchar(10) NOT NULL DEFAULT 'CUR' COMMENT '플래그',
  PRIMARY KEY (`NODE_ID`,`RGSTR_TIME`,`FLG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='유압값'
```

## `TB_FR_SI_VAL`

```sql
CREATE TABLE `TB_FR_SI_VAL` (
  `LINK_ID` varchar(100) NOT NULL COMMENT '링크ID',
  `HH_LOSS_VAL` float DEFAULT NULL COMMENT '수두손실값',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `LINK_VAL` float DEFAULT 0 COMMENT '유량값',
  `FLW_ALG_RST_VAL` float DEFAULT NULL,
  `FLG` varchar(10) NOT NULL DEFAULT 'CUR' COMMENT '플래그',
  PRIMARY KEY (`LINK_ID`,`RGSTR_TIME`,`FLG`),
  KEY `TB_FR_VAL_FLG_IDX` (`FLG`) USING BTREE,
  KEY `TB_FR_VAL_LINK_ID_IDX` (`LINK_ID`) USING BTREE,
  KEY `TB_FR_VAL_RGSTR_TIME_IDX` (`RGSTR_TIME`) USING BTREE,
  KEY `TB_FR_SI_VAL_RGSTR_TIME_IDX` (`RGSTR_TIME`,`FLG`) USING BTREE,
  KEY `TB_FR_SI_VAL_FLG_IDX` (`FLG`,`RGSTR_TIME`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='유속값'
```

## `TB_FR_VAL`

```sql
CREATE TABLE `TB_FR_VAL` (
  `LINK_ID` varchar(100) NOT NULL COMMENT '링크ID',
  `HH_LOSS_VAL` float DEFAULT NULL COMMENT '수두손실값',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `LINK_VAL` float DEFAULT NULL COMMENT '유량값',
  `FLW_ALG_RST_VAL` float DEFAULT NULL,
  `FLG` varchar(10) NOT NULL DEFAULT 'CUR' COMMENT '플래그',
  PRIMARY KEY (`LINK_ID`,`RGSTR_TIME`,`FLG`),
  KEY `TB_FR_VAL_FLG_IDX` (`FLG`) USING BTREE,
  KEY `TB_FR_VAL_LINK_ID_IDX` (`LINK_ID`) USING BTREE,
  KEY `TB_FR_VAL_RGSTR_TIME_IDX` (`RGSTR_TIME`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='유속값'
```

## `TB_GOALSETTING`

```sql
CREATE TABLE `TB_GOALSETTING` (
  `YEAR` varchar(50) NOT NULL DEFAULT '0' COMMENT '년도',
  `TYPE` varchar(10) NOT NULL DEFAULT 'mm',
  `1M` double DEFAULT NULL COMMENT '1월',
  `2M` double DEFAULT NULL COMMENT '2월',
  `3M` double DEFAULT NULL COMMENT '3월',
  `4M` double DEFAULT NULL COMMENT '4월',
  `5M` double DEFAULT NULL COMMENT '5월',
  `6M` double DEFAULT NULL COMMENT '6월',
  `7M` double DEFAULT NULL COMMENT '7월',
  `8M` double DEFAULT NULL COMMENT '8월',
  `9M` double DEFAULT NULL COMMENT '9월',
  `10M` double DEFAULT NULL COMMENT '10월',
  `11M` double DEFAULT NULL COMMENT '11월',
  `12M` double DEFAULT NULL COMMENT '12월',
  PRIMARY KEY (`YEAR`,`TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='월간 전력사용 목표량'
```

## `TB_HMI_ALR_TAG`

```sql
CREATE TABLE `TB_HMI_ALR_TAG` (
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `TIME` datetime NOT NULL COMMENT '일시',
  `VALUE` varchar(45) NOT NULL COMMENT '값',
  `ANLY_CD` varchar(20) NOT NULL COMMENT '분석 코드',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`TAG`,`TIME`,`ANLY_CD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='HMI 알람 태그'
```

## `TB_HMI_CTR_LOG`

```sql
CREATE TABLE `TB_HMI_CTR_LOG` (
  `CTR_LOG_IDX` int(11) NOT NULL AUTO_INCREMENT COMMENT '제어 로그 IDX',
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `TIME` datetime NOT NULL COMMENT '일시',
  `VALUE` text NOT NULL COMMENT '값',
  `ANLY_CD` varchar(20) NOT NULL COMMENT '분석 코드',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  `DCS` varchar(100) DEFAULT NULL COMMENT '설명',
  PRIMARY KEY (`CTR_LOG_IDX`,`TAG`,`TIME`,`ANLY_CD`,`RGSTR_TIME`)
) ENGINE=InnoDB AUTO_INCREMENT=183710 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프 실시간 자동 제어 태그 로그'
```

## `TB_HMI_CTR_TAG`

```sql
CREATE TABLE `TB_HMI_CTR_TAG` (
  `CTR_IDX` int(11) NOT NULL AUTO_INCREMENT COMMENT '제어 IDX',
  `CTR_NM` varchar(20) DEFAULT NULL COMMENT '제어 이름',
  `OPT_IDX` varchar(200) DEFAULT NULL COMMENT '분석 ID',
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `TIME` datetime NOT NULL COMMENT '일시',
  `VALUE` varchar(45) NOT NULL COMMENT '값',
  `ANLY_CD` varchar(20) NOT NULL COMMENT '분석 코드',
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  `AI_STATUS` char(1) DEFAULT NULL COMMENT 'AI 모드',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  PRIMARY KEY (`CTR_IDX`,`TAG`,`TIME`,`ANLY_CD`,`RGSTR_TIME`)
) ENGINE=InnoDB AUTO_INCREMENT=665 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='HMI 제어 태그'
```

## `TB_HMI_TRNSP_TAG`

```sql
CREATE TABLE `TB_HMI_TRNSP_TAG` (
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `TIME` datetime NOT NULL COMMENT '일시',
  `VALUE` varchar(45) NOT NULL COMMENT '값',
  `ANLY_CD` varchar(20) DEFAULT NULL COMMENT '분석 코드',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`TAG`,`TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='HMI 전송 태그'
```

## `TB_LINK_GRP`

```sql
CREATE TABLE `TB_LINK_GRP` (
  `LINK_ID` varchar(100) NOT NULL COMMENT '링크ID',
  `GRP_NM` varchar(10) NOT NULL COMMENT '그룹명',
  `FLW_TAGNAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`LINK_ID`,`GRP_NM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='링크그룹'
```

## `TB_LOG_TABLE`

```sql
CREATE TABLE `TB_LOG_TABLE` (
  `RGSTR_TIME` datetime NOT NULL COMMENT '등록일시',
  `ANLY_TIME` datetime NOT NULL COMMENT '분석일시',
  `MODEL` varchar(10) NOT NULL COMMENT '분석모델명',
  `PART` varchar(200) NOT NULL COMMENT '분석 파트명',
  `LOG_LEVEL` varchar(200) NOT NULL COMMENT '로그레벨',
  `DC_NMB` varchar(10) NOT NULL COMMENT '도커 번호',
  PRIMARY KEY (`RGSTR_TIME`,`ANLY_TIME`,`PART`,`LOG_LEVEL`,`DC_NMB`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='EMS로그테이블'
```

## `TB_MERGE`

```sql
CREATE TABLE `TB_MERGE` (
  `CUR_TS` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '현재시간',
  PRIMARY KEY (`CUR_TS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='사용여부 판단 필요'
```

## `TB_MNL_CHN_LOG`

```sql
CREATE TABLE `TB_MNL_CHN_LOG` (
  `RGSTR_TIME` datetime NOT NULL COMMENT '등록일시',
  `OPER` varchar(10) NOT NULL COMMENT '제어결과',
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `NewPumpComb` varchar(50) DEFAULT NULL COMMENT '신규조합',
  `NewPumpFreq` varchar(50) DEFAULT NULL COMMENT '신규주파수',
  `AgoPumpComb` varchar(50) DEFAULT NULL COMMENT '직전조합',
  `AgoPumpFreq` varchar(50) DEFAULT NULL COMMENT '직전주파수',
  PRIMARY KEY (`RGSTR_TIME`,`OPER`,`PUMP_GRP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='증감 및 감소 운영 결과 로그'
```

## `TB_MONTHLY_PEAK`

```sql
CREATE TABLE `TB_MONTHLY_PEAK` (
  `YM` date NOT NULL COMMENT '년월 (해당월 1일)',
  `PEAK_VALUE` double DEFAULT 0 COMMENT '해당월의 피크(최대)값',
  `UNIT` varchar(20) DEFAULT NULL COMMENT '단위',
  PRIMARY KEY (`YM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='월별 최대 피크값 요약 테이블'
```

## `TB_NODE_TAG`

```sql
CREATE TABLE `TB_NODE_TAG` (
  `NODE_ID` varchar(100) NOT NULL COMMENT 'NODE_ID',
  `FP_TAGNAME` varchar(100) DEFAULT NULL COMMENT '유압태그명',
  `FR_TAGNAME` varchar(100) DEFAULT NULL COMMENT '유속태그명',
  `DSTRB_Q_ID` varchar(100) DEFAULT NULL COMMENT '유량노드변수',
  `DSTRB_P_ID` varchar(100) DEFAULT NULL COMMENT '관압노드변수',
  PRIMARY KEY (`NODE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='노드태그'
```

## `TB_NODE_TAG_11190`

```sql
CREATE TABLE `TB_NODE_TAG_11190` (
  `NODE_ID` varchar(100) NOT NULL COMMENT 'NODE_ID',
  `FP_TAGNAME` varchar(100) DEFAULT NULL COMMENT '유압태그명',
  `FR_TAGNAME` varchar(100) DEFAULT NULL COMMENT '유속태그명',
  `DSTRB_Q_ID` varchar(100) DEFAULT NULL COMMENT '유량노드변수',
  `DSTRB_P_ID` varchar(100) DEFAULT NULL COMMENT '관압노드변수',
  PRIMARY KEY (`NODE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='노드태그'
```

## `TB_OPER_INF`

```sql
CREATE TABLE `TB_OPER_INF` (
  `OPER_IDX` varchar(50) NOT NULL DEFAULT 'user' COMMENT '운영 인덱스',
  `SSN` varchar(11) NOT NULL DEFAULT '0' COMMENT '계절',
  `C0` varchar(50) DEFAULT NULL COMMENT '0시',
  `C1` varchar(50) DEFAULT NULL COMMENT '1시',
  `C2` varchar(50) DEFAULT NULL COMMENT '2시',
  `C3` varchar(50) DEFAULT NULL COMMENT '3시',
  `C4` varchar(50) DEFAULT NULL COMMENT '4시',
  `C5` varchar(50) DEFAULT NULL COMMENT '5시',
  `C6` varchar(50) DEFAULT NULL COMMENT '6시',
  `C7` varchar(50) DEFAULT NULL COMMENT '7시',
  `C8` varchar(50) DEFAULT NULL COMMENT '8시',
  `C9` varchar(50) DEFAULT NULL COMMENT '9시',
  `C10` varchar(50) DEFAULT NULL COMMENT '10시',
  `C11` varchar(50) DEFAULT NULL COMMENT '11시',
  `C12` varchar(50) DEFAULT NULL COMMENT '12시',
  `C13` varchar(50) DEFAULT NULL COMMENT '13시',
  `C14` varchar(50) DEFAULT NULL COMMENT '14시',
  `C15` varchar(50) DEFAULT NULL COMMENT '15시',
  `C16` varchar(50) DEFAULT NULL COMMENT '16시',
  `C17` varchar(50) DEFAULT NULL COMMENT '17시',
  `C18` varchar(50) DEFAULT NULL COMMENT '18시',
  `C19` varchar(50) DEFAULT NULL COMMENT '19시',
  `C20` varchar(50) DEFAULT NULL COMMENT '20시',
  `C21` varchar(50) DEFAULT NULL COMMENT '21시',
  `C22` varchar(50) DEFAULT NULL COMMENT '22시',
  `C23` varchar(50) DEFAULT NULL COMMENT '23시',
  PRIMARY KEY (`OPER_IDX`,`SSN`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='운영 정보'
```

## `TB_PEAK_GNRTD_RST`

```sql
CREATE TABLE `TB_PEAK_GNRTD_RST` (
  `CNFRM_TIME` datetime NOT NULL COMMENT '확인 시간',
  `GNRTD_PWR` int(11) NOT NULL COMMENT '발생전력',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`CNFRM_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='발생 전력 결과'
```

## `TB_PEAK_LOG`

```sql
CREATE TABLE `TB_PEAK_LOG` (
  `TS` timestamp NULL DEFAULT NULL COMMENT '일시',
  `VALUE` float DEFAULT NULL COMMENT '값'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='전력피크 로그'
```

## `TB_PEAK_PRDCT_RST`

```sql
CREATE TABLE `TB_PEAK_PRDCT_RST` (
  `ANLY_TIME` datetime NOT NULL COMMENT '분석일시',
  `PRDCT_TIME` datetime NOT NULL COMMENT '예측일시',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`ANLY_TIME`,`PRDCT_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='피크시간대 결과'
```

## `TB_PEAK_PRTCP_INF`

```sql
CREATE TABLE `TB_PEAK_PRTCP_INF` (
  `PRTCP_TIME` datetime NOT NULL COMMENT '참여시점',
  `PRTCP_PWR` int(11) NOT NULL DEFAULT 0 COMMENT '참여전력량',
  `UPDT_TIME` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`PRTCP_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='전력수요거래 참여 결과(미사용)'
```

## `TB_PEAK_PWR_PRDCT_RST`

```sql
CREATE TABLE `TB_PEAK_PWR_PRDCT_RST` (
  `ANLY_TIME` datetime NOT NULL COMMENT '분석일시',
  `CNFRM_TIME` datetime NOT NULL COMMENT '확인 시간',
  `PRDCT_PWR` int(11) NOT NULL COMMENT '예상전력',
  `PEAK_YN` char(1) NOT NULL DEFAULT '1' COMMENT '피크발생여부',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`ANLY_TIME`,`CNFRM_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='전력 예측 결과'
```

## `TB_PEAK_RT_TAGHRR_INF`

```sql
CREATE TABLE `TB_PEAK_RT_TAGHRR_INF` (
  `DTRG_DATE` date NOT NULL COMMENT '데이터 등록 일자',
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `HRR_TAG` varchar(20) NOT NULL COMMENT '계층 태그',
  `HRR_DVSN` varchar(5) NOT NULL COMMENT '계층 구분',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용 여부',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  PRIMARY KEY (`DTRG_DATE`,`TAG`,`HRR_TAG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='태그 계층 정보'
```

## `TB_PEAK_RT_TAG_INF`

```sql
CREATE TABLE `TB_PEAK_RT_TAG_INF` (
  `DTRG_DATE` date NOT NULL COMMENT '데이터 등록 일자',
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `ALG_CD` varchar(5) NOT NULL COMMENT '알고리즘 코드',
  `ALG_DSC` varchar(30) NOT NULL COMMENT '알고리즘 설명',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용 여부',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='알고리즘 사용 태그 정보'
```

## `TB_PEAK_SCHDL_RST`

```sql
CREATE TABLE `TB_PEAK_SCHDL_RST` (
  `ANLY_TIME` datetime NOT NULL COMMENT '분석일시',
  `PWRFC_CD` varchar(10) NOT NULL COMMENT '전력생산설비 코드',
  `JOB_START_TIME` datetime NOT NULL COMMENT '작업 시작 일시',
  `PWRFC_KOR_NM` varchar(20) NOT NULL COMMENT '전력생산설비 한글명칭',
  `JOB_END_TIME` datetime DEFAULT NULL COMMENT '작업 종료 일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`ANLY_TIME`,`PWRFC_CD`,`JOB_START_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='전력생산설비 스케줄 결과'
```

## `TB_PEAK_TAG_INF`

```sql
CREATE TABLE `TB_PEAK_TAG_INF` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `DTRG_DATE` date NOT NULL DEFAULT current_timestamp() COMMENT '데이터 등록 일자',
  `PWI_TAG` varchar(30) NOT NULL COMMENT '전력순시태그',
  `PWI_UNIT_VALUE` double NOT NULL DEFAULT 1,
  `PWI_UNIT` varchar(3) DEFAULT NULL COMMENT '전력순시단위',
  `PWQ_TAG` varchar(30) NOT NULL COMMENT '적산 태그',
  `PWQ_UNIT_VALUE` double NOT NULL DEFAULT 1,
  `PWQ_UNIT` varchar(3) NOT NULL COMMENT '적산 단위',
  `CLSFC` varchar(20) DEFAULT NULL COMMENT '분류',
  `IS_ALL` varchar(5) DEFAULT '0' COMMENT '전체사용 전력 태그 구분',
  `MNTR_YN` char(1) NOT NULL COMMENT '감시여부(감시: 1, 미감시: 0)',
  `HMI_TAG_DSC` varchar(100) NOT NULL COMMENT 'HMI 태그 설명',
  `VSL_TAG_DSC` varchar(100) NOT NULL COMMENT '시각화 태그 설명',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  PRIMARY KEY (`PWI_TAG`,`PWQ_TAG`),
  KEY `TB_PEAK_TAG_INF_INS_TAG_IDX` (`PWI_TAG`,`PWI_UNIT`,`MNTR_YN`) USING BTREE,
  KEY `TB_PEAK_TAG_INF_INT_TAG_IDX` (`PWQ_TAG`,`PWQ_UNIT`,`MNTR_YN`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='피크 제어 태그 정보'
```

## `TB_PEAK_TAG_INF_GM_250725`

```sql
CREATE TABLE `TB_PEAK_TAG_INF_GM_250725` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `DTRG_DATE` date NOT NULL DEFAULT current_timestamp() COMMENT '데이터 등록 일자',
  `PWI_TAG` varchar(30) NOT NULL COMMENT '전력순시태그',
  `PWI_UNIT_VALUE` double NOT NULL DEFAULT 1,
  `PWI_UNIT` varchar(3) DEFAULT NULL COMMENT '전력순시단위',
  `PWQ_TAG` varchar(30) NOT NULL COMMENT '적산 태그',
  `PWQ_UNIT_VALUE` double NOT NULL DEFAULT 1,
  `PWQ_UNIT` varchar(3) NOT NULL COMMENT '적산 단위',
  `CLSFC` varchar(20) DEFAULT NULL COMMENT '분류',
  `IS_ALL` varchar(5) DEFAULT '0' COMMENT '전체사용 전력 태그 구분',
  `MNTR_YN` char(1) NOT NULL COMMENT '감시여부(감시: 1, 미감시: 0)',
  `HMI_TAG_DSC` varchar(100) NOT NULL COMMENT 'HMI 태그 설명',
  `VSL_TAG_DSC` varchar(100) NOT NULL COMMENT '시각화 태그 설명',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  PRIMARY KEY (`PWI_TAG`,`PWQ_TAG`),
  KEY `TB_PEAK_TAG_INF_INS_TAG_IDX` (`PWI_TAG`,`PWI_UNIT`,`MNTR_YN`) USING BTREE,
  KEY `TB_PEAK_TAG_INF_INT_TAG_IDX` (`PWQ_TAG`,`PWQ_UNIT`,`MNTR_YN`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='피크 제어 태그 정보'
```

## `TB_PEAK_TAG_INF_HP_250725`

```sql
CREATE TABLE `TB_PEAK_TAG_INF_HP_250725` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `DTRG_DATE` date NOT NULL DEFAULT current_timestamp() COMMENT '데이터 등록 일자',
  `PWI_TAG` varchar(30) NOT NULL COMMENT '전력순시태그',
  `PWI_UNIT_VALUE` double NOT NULL DEFAULT 1,
  `PWI_UNIT` varchar(3) DEFAULT NULL COMMENT '전력순시단위',
  `PWQ_TAG` varchar(30) NOT NULL COMMENT '적산 태그',
  `PWQ_UNIT_VALUE` double NOT NULL DEFAULT 1,
  `PWQ_UNIT` varchar(3) NOT NULL COMMENT '적산 단위',
  `CLSFC` varchar(20) DEFAULT NULL COMMENT '분류',
  `IS_ALL` varchar(5) DEFAULT '0' COMMENT '전체사용 전력 태그 구분',
  `MNTR_YN` char(1) NOT NULL COMMENT '감시여부(감시: 1, 미감시: 0)',
  `HMI_TAG_DSC` varchar(100) NOT NULL COMMENT 'HMI 태그 설명',
  `VSL_TAG_DSC` varchar(100) NOT NULL COMMENT '시각화 태그 설명',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  PRIMARY KEY (`PWI_TAG`,`PWQ_TAG`),
  KEY `TB_PEAK_TAG_INF_INS_TAG_IDX` (`PWI_TAG`,`PWI_UNIT`,`MNTR_YN`) USING BTREE,
  KEY `TB_PEAK_TAG_INF_INT_TAG_IDX` (`PWQ_TAG`,`PWQ_UNIT`,`MNTR_YN`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='피크 제어 태그 정보'
```

## `TB_PRF_INVRT_RST`

```sql
CREATE TABLE `TB_PRF_INVRT_RST` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `ANLY_DATE` date NOT NULL COMMENT '분석날짜',
  `EQ_TYP` char(2) NOT NULL COMMENT '수식타입',
  `FREQ` decimal(4,2) NOT NULL COMMENT '주파수',
  `PUMP_IDX` int(11) NOT NULL COMMENT '펌프인덱스',
  `PRFRM_COEFF` varchar(100) DEFAULT NULL COMMENT '펌프성능곡선계수',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`ANLY_DATE`,`EQ_TYP`,`FREQ`,`PUMP_IDX`),
  UNIQUE KEY `RGSTR_TIME` (`RGSTR_TIME`,`ANLY_DATE`,`EQ_TYP`,`FREQ`,`PUMP_IDX`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='인버터펌프성능곡선'
```

## `TB_PRF_PRFRM_RST`

```sql
CREATE TABLE `TB_PRF_PRFRM_RST` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `ANLY_DATE` date NOT NULL COMMENT '분석날짜',
  `EQ_TYP` char(2) NOT NULL COMMENT '수식타입',
  `WTR_TE` smallint(6) NOT NULL COMMENT '수온',
  `PUMP_IDX` int(11) NOT NULL COMMENT '펌프인덱스',
  `PRFRM_COEFF` varchar(100) DEFAULT NULL COMMENT '펌프성능곡선계수',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`ANLY_DATE`,`EQ_TYP`,`WTR_TE`,`PUMP_IDX`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프성능곡선'
```

## `TB_PRF_PUMPYN_RST`

```sql
CREATE TABLE `TB_PRF_PUMPYN_RST` (
  `OPT_IDX` varchar(200) NOT NULL COMMENT '펌프제어KEY',
  `PUMP_IDX` int(11) NOT NULL COMMENT '펌프인덱스',
  `PUMP_TYP` int(11) NOT NULL COMMENT '펌프타입',
  `PUMP_YN` varchar(5) NOT NULL COMMENT '펌프 작동 여부',
  `DC_NMB` varchar(10) NOT NULL COMMENT '도커 번호',
  PRIMARY KEY (`OPT_IDX`,`PUMP_IDX`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='최적 펌프제어 펌프결과'
```

## `TB_PRODUCER_DATA`

```sql
CREATE TABLE `TB_PRODUCER_DATA` (
  `ALIVE_TIME` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '분석시간',
  `PRD_ALG_TOPIC` varchar(45) DEFAULT NULL COMMENT '제품 알고리즘 토픽',
  PRIMARY KEY (`ALIVE_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='미사용'
```

## `TB_PTR_CTR_ANLY_RST`

```sql
CREATE TABLE `TB_PTR_CTR_ANLY_RST` (
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `TIME` datetime NOT NULL COMMENT '일시',
  `VALUE` varchar(45) NOT NULL COMMENT '값',
  `ANLY_CD` varchar(20) DEFAULT NULL COMMENT '분석 코드',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`TAG`,`TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='펌프 실시간 제어 분석 결과'
```

## `TB_PTR_CTR_INF`

```sql
CREATE TABLE `TB_PTR_CTR_INF` (
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  PRIMARY KEY (`TAG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='최적 펌프 운영 태그 정의'
```

## `TB_PTR_HALF_CTR_TAG`

```sql
CREATE TABLE `TB_PTR_HALF_CTR_TAG` (
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `TIME` datetime NOT NULL COMMENT '일시',
  `VALUE` varchar(45) NOT NULL COMMENT '값',
  `ANLY_CD` varchar(20) DEFAULT NULL COMMENT '분석 코드',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '업데이트 일시',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`TAG`,`TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='펌프 실시간 반자동 제어 태그'
```

## `TB_PTR_ORC_RST`

```sql
CREATE TABLE `TB_PTR_ORC_RST` (
  `TS` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '일시',
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  PRIMARY KEY (`TS`,`TAG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='펌프 성능 곡선 계수'
 PARTITION BY RANGE (unix_timestamp(`TS`))
(PARTITION `p202101` VALUES LESS THAN (1612105200) ENGINE = InnoDB,
 PARTITION `p202102` VALUES LESS THAN (1614524400) ENGINE = InnoDB,
 PARTITION `p202103` VALUES LESS THAN (1617202800) ENGINE = InnoDB,
 PARTITION `p202104` VALUES LESS THAN (1619794800) ENGINE = InnoDB,
 PARTITION `p202105` VALUES LESS THAN (1622473200) ENGINE = InnoDB,
 PARTITION `p202106` VALUES LESS THAN (1625065200) ENGINE = InnoDB,
 PARTITION `p202107` VALUES LESS THAN (1627743600) ENGINE = InnoDB,
 PARTITION `p202108` VALUES LESS THAN (1630422000) ENGINE = InnoDB,
 PARTITION `p202109` VALUES LESS THAN (1633014000) ENGINE = InnoDB,
 PARTITION `p202110` VALUES LESS THAN (1635692400) ENGINE = InnoDB,
 PARTITION `p202111` VALUES LESS THAN (1638284400) ENGINE = InnoDB,
 PARTITION `p202112` VALUES LESS THAN (1640962800) ENGINE = InnoDB,
 PARTITION `p202201` VALUES LESS THAN (1643641200) ENGINE = InnoDB,
 PARTITION `p202202` VALUES LESS THAN (1646060400) ENGINE = InnoDB,
 PARTITION `p202203` VALUES LESS THAN (1648738800) ENGINE = InnoDB,
 PARTITION `p202204` VALUES LESS THAN (1651330800) ENGINE = InnoDB,
 PARTITION `p202205` VALUES LESS THAN (1654009200) ENGINE = InnoDB,
 PARTITION `p202206` VALUES LESS THAN (1656601200) ENGINE = InnoDB,
 PARTITION `p202207` VALUES LESS THAN (1659279600) ENGINE = InnoDB,
 PARTITION `p202208` VALUES LESS THAN (1661958000) ENGINE = InnoDB,
 PARTITION `p202209` VALUES LESS THAN (1664550000) ENGINE = InnoDB,
 PARTITION `p202210` VALUES LESS THAN (1667228400) ENGINE = InnoDB,
 PARTITION `p202211` VALUES LESS THAN (1669820400) ENGINE = InnoDB,
 PARTITION `p202212` VALUES LESS THAN (1672498800) ENGINE = InnoDB,
 PARTITION `p202301` VALUES LESS THAN (1675177200) ENGINE = InnoDB,
 PARTITION `p202302` VALUES LESS THAN (1677596400) ENGINE = InnoDB,
 PARTITION `p202303` VALUES LESS THAN (1680274800) ENGINE = InnoDB,
 PARTITION `p202304` VALUES LESS THAN (1682866800) ENGINE = InnoDB,
 PARTITION `p202305` VALUES LESS THAN (1685545200) ENGINE = InnoDB,
 PARTITION `p202306` VALUES LESS THAN (1688137200) ENGINE = InnoDB,
 PARTITION `p202307` VALUES LESS THAN (1690815600) ENGINE = InnoDB,
 PARTITION `p202308` VALUES LESS THAN (1693494000) ENGINE = InnoDB,
 PARTITION `p202309` VALUES LESS THAN (1696086000) ENGINE = InnoDB,
 PARTITION `p202310` VALUES LESS THAN (1698764400) ENGINE = InnoDB,
 PARTITION `p202311` VALUES LESS THAN (1701356400) ENGINE = InnoDB,
 PARTITION `p202312` VALUES LESS THAN (1704034800) ENGINE = InnoDB,
 PARTITION `p202401` VALUES LESS THAN (1706713200) ENGINE = InnoDB,
 PARTITION `p202402` VALUES LESS THAN (1709218800) ENGINE = InnoDB,
 PARTITION `p202403` VALUES LESS THAN (1711897200) ENGINE = InnoDB,
 PARTITION `p202404` VALUES LESS THAN (1714489200) ENGINE = InnoDB,
 PARTITION `p202405` VALUES LESS THAN (1717167600) ENGINE = InnoDB,
 PARTITION `p202406` VALUES LESS THAN (1719759600) ENGINE = InnoDB,
 PARTITION `p202407` VALUES LESS THAN (1722438000) ENGINE = InnoDB,
 PARTITION `p202408` VALUES LESS THAN (1725116400) ENGINE = InnoDB,
 PARTITION `p202409` VALUES LESS THAN (1727708400) ENGINE = InnoDB,
 PARTITION `p202410` VALUES LESS THAN (1730386800) ENGINE = InnoDB,
 PARTITION `p202411` VALUES LESS THAN (1732978800) ENGINE = InnoDB,
 PARTITION `p202412` VALUES LESS THAN (1735657200) ENGINE = InnoDB,
 PARTITION `p202501` VALUES LESS THAN (1738335600) ENGINE = InnoDB,
 PARTITION `p202502` VALUES LESS THAN (1740754800) ENGINE = InnoDB,
 PARTITION `p202503` VALUES LESS THAN (1743433200) ENGINE = InnoDB,
 PARTITION `p202504` VALUES LESS THAN (1746025200) ENGINE = InnoDB,
 PARTITION `p202505` VALUES LESS THAN (1748703600) ENGINE = InnoDB,
 PARTITION `p202506` VALUES LESS THAN (1751295600) ENGINE = InnoDB,
 PARTITION `p202507` VALUES LESS THAN (1753974000) ENGINE = InnoDB,
 PARTITION `p202508` VALUES LESS THAN (1756652400) ENGINE = InnoDB,
 PARTITION `p202509` VALUES LESS THAN (1759244400) ENGINE = InnoDB,
 PARTITION `p202510` VALUES LESS THAN (1761922800) ENGINE = InnoDB,
 PARTITION `p202511` VALUES LESS THAN (1764514800) ENGINE = InnoDB,
 PARTITION `p202512` VALUES LESS THAN (1767193200) ENGINE = InnoDB,
 PARTITION `p202601` VALUES LESS THAN (1769871600) ENGINE = InnoDB,
 PARTITION `p202602` VALUES LESS THAN (1772290800) ENGINE = InnoDB,
 PARTITION `p202603` VALUES LESS THAN (1774969200) ENGINE = InnoDB,
 PARTITION `p202604` VALUES LESS THAN (1777561200) ENGINE = InnoDB,
 PARTITION `p202605` VALUES LESS THAN (1780239600) ENGINE = InnoDB,
 PARTITION `p202606` VALUES LESS THAN (1782831600) ENGINE = InnoDB,
 PARTITION `p202607` VALUES LESS THAN (1785510000) ENGINE = InnoDB,
 PARTITION `p202608` VALUES LESS THAN (1788188400) ENGINE = InnoDB,
 PARTITION `p202609` VALUES LESS THAN (1790780400) ENGINE = InnoDB,
 PARTITION `p202610` VALUES LESS THAN (1793458800) ENGINE = InnoDB,
 PARTITION `p202611` VALUES LESS THAN (1796050800) ENGINE = InnoDB,
 PARTITION `p202612` VALUES LESS THAN (1798729200) ENGINE = InnoDB,
 PARTITION `p202701` VALUES LESS THAN (1801407600) ENGINE = InnoDB,
 PARTITION `p202702` VALUES LESS THAN (1803826800) ENGINE = InnoDB,
 PARTITION `p202703` VALUES LESS THAN (1806505200) ENGINE = InnoDB,
 PARTITION `p202704` VALUES LESS THAN (1809097200) ENGINE = InnoDB,
 PARTITION `p202705` VALUES LESS THAN (1811775600) ENGINE = InnoDB,
 PARTITION `p202706` VALUES LESS THAN (1814367600) ENGINE = InnoDB,
 PARTITION `p202707` VALUES LESS THAN (1817046000) ENGINE = InnoDB,
 PARTITION `p202708` VALUES LESS THAN (1819724400) ENGINE = InnoDB,
 PARTITION `p202709` VALUES LESS THAN (1822316400) ENGINE = InnoDB,
 PARTITION `p202710` VALUES LESS THAN (1824994800) ENGINE = InnoDB,
 PARTITION `p202711` VALUES LESS THAN (1827586800) ENGINE = InnoDB,
 PARTITION `p202712` VALUES LESS THAN (1830265200) ENGINE = InnoDB,
 PARTITION `p202801` VALUES LESS THAN (1832943600) ENGINE = InnoDB,
 PARTITION `p202802` VALUES LESS THAN (1835449200) ENGINE = InnoDB,
 PARTITION `p202803` VALUES LESS THAN (1838127600) ENGINE = InnoDB,
 PARTITION `p202804` VALUES LESS THAN (1840719600) ENGINE = InnoDB,
 PARTITION `p202805` VALUES LESS THAN (1843398000) ENGINE = InnoDB,
 PARTITION `p202806` VALUES LESS THAN (1845990000) ENGINE = InnoDB,
 PARTITION `p202807` VALUES LESS THAN (1848668400) ENGINE = InnoDB,
 PARTITION `p202808` VALUES LESS THAN (1851346800) ENGINE = InnoDB,
 PARTITION `p202809` VALUES LESS THAN (1853938800) ENGINE = InnoDB,
 PARTITION `p202810` VALUES LESS THAN (1856617200) ENGINE = InnoDB,
 PARTITION `p202811` VALUES LESS THAN (1859209200) ENGINE = InnoDB,
 PARTITION `p202812` VALUES LESS THAN (1861887600) ENGINE = InnoDB,
 PARTITION `p202901` VALUES LESS THAN (1864566000) ENGINE = InnoDB,
 PARTITION `p202902` VALUES LESS THAN (1866985200) ENGINE = InnoDB,
 PARTITION `p202903` VALUES LESS THAN (1869663600) ENGINE = InnoDB,
 PARTITION `p202904` VALUES LESS THAN (1872255600) ENGINE = InnoDB,
 PARTITION `p202905` VALUES LESS THAN (1874934000) ENGINE = InnoDB,
 PARTITION `p202906` VALUES LESS THAN (1877526000) ENGINE = InnoDB,
 PARTITION `p202907` VALUES LESS THAN (1880204400) ENGINE = InnoDB,
 PARTITION `p202908` VALUES LESS THAN (1882882800) ENGINE = InnoDB,
 PARTITION `p202909` VALUES LESS THAN (1885474800) ENGINE = InnoDB,
 PARTITION `p202910` VALUES LESS THAN (1888153200) ENGINE = InnoDB,
 PARTITION `p202911` VALUES LESS THAN (1890745200) ENGINE = InnoDB,
 PARTITION `p202912` VALUES LESS THAN (1893423600) ENGINE = InnoDB,
 PARTITION `p203001` VALUES LESS THAN (1896102000) ENGINE = InnoDB,
 PARTITION `p203002` VALUES LESS THAN (1898521200) ENGINE = InnoDB,
 PARTITION `p203003` VALUES LESS THAN (1901199600) ENGINE = InnoDB,
 PARTITION `p203004` VALUES LESS THAN (1903791600) ENGINE = InnoDB,
 PARTITION `p203005` VALUES LESS THAN (1906470000) ENGINE = InnoDB,
 PARTITION `p203006` VALUES LESS THAN (1909062000) ENGINE = InnoDB,
 PARTITION `p203007` VALUES LESS THAN (1911740400) ENGINE = InnoDB,
 PARTITION `p203008` VALUES LESS THAN (1914418800) ENGINE = InnoDB,
 PARTITION `p203009` VALUES LESS THAN (1917010800) ENGINE = InnoDB,
 PARTITION `p203010` VALUES LESS THAN (1919689200) ENGINE = InnoDB,
 PARTITION `p203011` VALUES LESS THAN (1922281200) ENGINE = InnoDB,
 PARTITION `p203012` VALUES LESS THAN (1924959600) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_PTR_STRTG_INF`

```sql
CREATE TABLE `TB_PTR_STRTG_INF` (
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `VALUE` varchar(45) NOT NULL DEFAULT '1' COMMENT '값',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() COMMENT '업데이트 일시',
  `REAL_TIME_YN` int(11) NOT NULL DEFAULT 1 COMMENT '실시간 전략 사용여부',
  `SSN_ID` varchar(3) DEFAULT NULL COMMENT '계절 아이디',
  `SSN` varchar(3) DEFAULT NULL COMMENT '계절',
  PRIMARY KEY (`TAG`,`REAL_TIME_YN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='펌프 제어 전략 정보'
```

## `TB_PUMP_CAL`

```sql
CREATE TABLE `TB_PUMP_CAL` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL,
  `FC_MIN_VAL` double NOT NULL DEFAULT 0 COMMENT '유량범위최소값',
  `FC_MAX_VAL` double NOT NULL DEFAULT 0 COMMENT '유량범위최대값'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_0718`

```sql
CREATE TABLE `TB_PUMP_CAL_0718` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_20250418`

```sql
CREATE TABLE `TB_PUMP_CAL_20250418` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_20250528`

```sql
CREATE TABLE `TB_PUMP_CAL_20250528` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_250718`

```sql
CREATE TABLE `TB_PUMP_CAL_250718` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_250812`

```sql
CREATE TABLE `TB_PUMP_CAL_250812` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_260324`

```sql
CREATE TABLE `TB_PUMP_CAL_260324` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL,
  `FC_MIN_VAL` double NOT NULL DEFAULT 0 COMMENT '유량범위최소값',
  `FC_MAX_VAL` double NOT NULL DEFAULT 0 COMMENT '유량범위최대값'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_BACKUP`

```sql
CREATE TABLE `TB_PUMP_CAL_BACKUP` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) DEFAULT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  `COUNT_IDX` int(1) DEFAULT NULL,
  `USE_YN` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_CAL_OLD`

```sql
CREATE TABLE `TB_PUMP_CAL_OLD` (
  `PUMP_GRP` int(11) NOT NULL COMMENT '펌프그룹',
  `C_IDX` int(11) NOT NULL COMMENT '조합인덱스',
  `C_ORD` int(11) NOT NULL COMMENT '조합순번',
  `FC_VAL` double NOT NULL DEFAULT 0 COMMENT '유량상수',
  `P_ADD_VAL` double NOT NULL DEFAULT 0 COMMENT '압력추가',
  `CS_OP` varchar(5) DEFAULT NULL COMMENT '배율및추가연산자',
  `P_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력배율',
  `SS_OP` varchar(5) DEFAULT NULL COMMENT '배율및제곱연산자',
  `P_SQRT_MUL_VAL` double NOT NULL DEFAULT 1 COMMENT '압력제곱근배율',
  `PUMP_COMB` varchar(30) NOT NULL COMMENT '펌프조합',
  `PUMP_COUNT` double DEFAULT NULL,
  `PUMP_PRIORITY` int(1) DEFAULT NULL,
  PRIMARY KEY (`PUMP_GRP`,`C_IDX`,`C_ORD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='펌프가동조건조합식상수'
```

## `TB_PUMP_COMBINATION`

```sql
CREATE TABLE `TB_PUMP_COMBINATION` (
  `PUMP_GRP` int(1) NOT NULL COMMENT '펌프 그룹',
  `PUMP_IDX` int(1) NOT NULL COMMENT '펌프 IDX',
  `PUMP_SIZE` double NOT NULL COMMENT '펌프 용량',
  `PUMP_COUNT` double NOT NULL COMMENT '펌프 필요 대수',
  `PUMP_PRIORITY` int(1) NOT NULL COMMENT '우선순위',
  `PUMP_TYP` int(1) NOT NULL COMMENT '펌프 타입',
  `PUMP_YN` int(1) NOT NULL COMMENT '사용여부',
  PRIMARY KEY (`PUMP_GRP`,`PUMP_IDX`,`PUMP_SIZE`,`PUMP_COUNT`,`PUMP_PRIORITY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='펌프 운전 조합'
```

## `TB_PUMP_COMBINATION_INF`

```sql
CREATE TABLE `TB_PUMP_COMBINATION_INF` (
  `PUMP_GRP` int(1) NOT NULL COMMENT '펌프 그룹',
  `COMB_NAME` varchar(50) DEFAULT NULL COMMENT '조합 이름',
  `PUMP_COUNT` double NOT NULL COMMENT '조합 대수',
  `PUMP_PRIORITY` int(1) NOT NULL COMMENT '우선순위',
  `PUMP_PRIORITY_DCS` varchar(300) DEFAULT NULL COMMENT '우선순위 설명',
  `PUMP_RULES` varchar(150) DEFAULT NULL COMMENT '사용조건',
  `USE_YN` int(1) DEFAULT NULL COMMENT '사용여부',
  PRIMARY KEY (`PUMP_GRP`,`PUMP_COUNT`,`PUMP_PRIORITY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='펌프 운전조합 정의'
```

## `TB_PUMP_COMBINATION_INF_OLD`

```sql
CREATE TABLE `TB_PUMP_COMBINATION_INF_OLD` (
  `PUMP_GRP` int(1) DEFAULT NULL COMMENT '펌프 그룹',
  `COMB_NAME` varchar(50) DEFAULT NULL COMMENT '조합 이름',
  `PUMP_COUNT` double DEFAULT NULL COMMENT '조합 대수',
  `PUMP_PRIORITY` int(1) DEFAULT NULL COMMENT '우선순위',
  `PUMP_PRIORITY_DCS` varchar(300) DEFAULT NULL COMMENT '우선순위 설명',
  `PUMP_RULES` varchar(150) DEFAULT NULL COMMENT '사용조건',
  `USE_YN` int(1) DEFAULT NULL COMMENT '사용여부'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='펌프 운전조합 정의'
```

## `TB_PUMP_COMBINATION_OLD`

```sql
CREATE TABLE `TB_PUMP_COMBINATION_OLD` (
  `PUMP_GRP` int(1) NOT NULL COMMENT '펌프 그룹',
  `PUMP_IDX` int(1) NOT NULL COMMENT '펌프 IDX',
  `PUMP_SIZE` double NOT NULL COMMENT '펌프 용량',
  `PUMP_COUNT` double NOT NULL COMMENT '펌프 필요 대수',
  `PUMP_PRIORITY` int(1) NOT NULL COMMENT '우선순위',
  `PUMP_TYP` int(1) NOT NULL COMMENT '펌프 타입',
  `PUMP_YN` int(1) NOT NULL COMMENT '사용여부',
  PRIMARY KEY (`PUMP_GRP`,`PUMP_IDX`,`PUMP_SIZE`,`PUMP_COUNT`,`PUMP_PRIORITY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='펌프 운전 조합'
```

## `TB_PUMP_COMB_POWER`

```sql
CREATE TABLE `TB_PUMP_COMB_POWER` (
  `PUMP_COMB` varchar(64) NOT NULL,
  `PWR_UNIT_COST` double DEFAULT NULL,
  `ESTM_PWR` double DEFAULT NULL,
  `AVG_FLOW` double DEFAULT NULL,
  `RGSTR_DATE` datetime NOT NULL,
  PRIMARY KEY (`PUMP_COMB`,`RGSTR_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
```

## `TB_PUMP_CTR_RTM`

```sql
CREATE TABLE `TB_PUMP_CTR_RTM` (
  `RGSTR_TIME` datetime DEFAULT NULL COMMENT '등록일시',
  `RUN_MODE` varchar(20) NOT NULL COMMENT '운영 모드',
  `RUN_TIME` float DEFAULT NULL COMMENT '운영 시간(초)',
  `TRAIN_TIME` float DEFAULT NULL COMMENT '예측 동작 시간(초)',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='펌프 제어 작동 시간'
```

## `TB_RAWDATA`

```sql
CREATE TABLE `TB_RAWDATA` (
  `TS` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '일시',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값',
  `QUALITY` varchar(3) DEFAULT NULL COMMENT '품질',
  `SERVER` varchar(45) DEFAULT NULL COMMENT '서버 출처',
  PRIMARY KEY (`TS`,`TAGNAME`),
  KEY `TB_RAWDATA_TAGNAME_IDX` (`TAGNAME`,`TS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='분단위 SCADA 태그 데이터'
 PARTITION BY RANGE (unix_timestamp(`TS`))
(PARTITION `p202108` VALUES LESS THAN (1630422000) ENGINE = InnoDB,
 PARTITION `p202109` VALUES LESS THAN (1633014000) ENGINE = InnoDB,
 PARTITION `p202110` VALUES LESS THAN (1635692400) ENGINE = InnoDB,
 PARTITION `p202111` VALUES LESS THAN (1638284400) ENGINE = InnoDB,
 PARTITION `p202112` VALUES LESS THAN (1640962800) ENGINE = InnoDB,
 PARTITION `p202201` VALUES LESS THAN (1643641200) ENGINE = InnoDB,
 PARTITION `p202202` VALUES LESS THAN (1646060400) ENGINE = InnoDB,
 PARTITION `p202203` VALUES LESS THAN (1648738800) ENGINE = InnoDB,
 PARTITION `p202204` VALUES LESS THAN (1651330800) ENGINE = InnoDB,
 PARTITION `p202205` VALUES LESS THAN (1654009200) ENGINE = InnoDB,
 PARTITION `p202206` VALUES LESS THAN (1656601200) ENGINE = InnoDB,
 PARTITION `p202207` VALUES LESS THAN (1659279600) ENGINE = InnoDB,
 PARTITION `p202208` VALUES LESS THAN (1661958000) ENGINE = InnoDB,
 PARTITION `p202209` VALUES LESS THAN (1664550000) ENGINE = InnoDB,
 PARTITION `p202210` VALUES LESS THAN (1667228400) ENGINE = InnoDB,
 PARTITION `p202211` VALUES LESS THAN (1669820400) ENGINE = InnoDB,
 PARTITION `p202212` VALUES LESS THAN (1672498800) ENGINE = InnoDB,
 PARTITION `p202301` VALUES LESS THAN (1675177200) ENGINE = InnoDB,
 PARTITION `p202302` VALUES LESS THAN (1677596400) ENGINE = InnoDB,
 PARTITION `p202303` VALUES LESS THAN (1680274800) ENGINE = InnoDB,
 PARTITION `p202304` VALUES LESS THAN (1682866800) ENGINE = InnoDB,
 PARTITION `p202305` VALUES LESS THAN (1685545200) ENGINE = InnoDB,
 PARTITION `p202306` VALUES LESS THAN (1688137200) ENGINE = InnoDB,
 PARTITION `p202307` VALUES LESS THAN (1690815600) ENGINE = InnoDB,
 PARTITION `p202308` VALUES LESS THAN (1693494000) ENGINE = InnoDB,
 PARTITION `p202309` VALUES LESS THAN (1696086000) ENGINE = InnoDB,
 PARTITION `p202310` VALUES LESS THAN (1698764400) ENGINE = InnoDB,
 PARTITION `p202311` VALUES LESS THAN (1701356400) ENGINE = InnoDB,
 PARTITION `p202312` VALUES LESS THAN (1704034800) ENGINE = InnoDB,
 PARTITION `p202401` VALUES LESS THAN (1706713200) ENGINE = InnoDB,
 PARTITION `p202402` VALUES LESS THAN (1709218800) ENGINE = InnoDB,
 PARTITION `p202403` VALUES LESS THAN (1711897200) ENGINE = InnoDB,
 PARTITION `p202404` VALUES LESS THAN (1714489200) ENGINE = InnoDB,
 PARTITION `p202405` VALUES LESS THAN (1717167600) ENGINE = InnoDB,
 PARTITION `p202406` VALUES LESS THAN (1719759600) ENGINE = InnoDB,
 PARTITION `p202407` VALUES LESS THAN (1722438000) ENGINE = InnoDB,
 PARTITION `p202408` VALUES LESS THAN (1725116400) ENGINE = InnoDB,
 PARTITION `p202409` VALUES LESS THAN (1727708400) ENGINE = InnoDB,
 PARTITION `p202410` VALUES LESS THAN (1730386800) ENGINE = InnoDB,
 PARTITION `p202411` VALUES LESS THAN (1732978800) ENGINE = InnoDB,
 PARTITION `p202412` VALUES LESS THAN (1735657200) ENGINE = InnoDB,
 PARTITION `p202501` VALUES LESS THAN (1738335600) ENGINE = InnoDB,
 PARTITION `p202502` VALUES LESS THAN (1740754800) ENGINE = InnoDB,
 PARTITION `p202503` VALUES LESS THAN (1743433200) ENGINE = InnoDB,
 PARTITION `p202504` VALUES LESS THAN (1746025200) ENGINE = InnoDB,
 PARTITION `p202505` VALUES LESS THAN (1748703600) ENGINE = InnoDB,
 PARTITION `p202506` VALUES LESS THAN (1751295600) ENGINE = InnoDB,
 PARTITION `p202507` VALUES LESS THAN (1753974000) ENGINE = InnoDB,
 PARTITION `p202508` VALUES LESS THAN (1756652400) ENGINE = InnoDB,
 PARTITION `p202509` VALUES LESS THAN (1759244400) ENGINE = InnoDB,
 PARTITION `p202510` VALUES LESS THAN (1761922800) ENGINE = InnoDB,
 PARTITION `p202511` VALUES LESS THAN (1764514800) ENGINE = InnoDB,
 PARTITION `p202512` VALUES LESS THAN (1767193200) ENGINE = InnoDB,
 PARTITION `p202601` VALUES LESS THAN (1769871600) ENGINE = InnoDB,
 PARTITION `p202602` VALUES LESS THAN (1772290800) ENGINE = InnoDB,
 PARTITION `p202603` VALUES LESS THAN (1774969200) ENGINE = InnoDB,
 PARTITION `p202604` VALUES LESS THAN (1777561200) ENGINE = InnoDB,
 PARTITION `p202605` VALUES LESS THAN (1780239600) ENGINE = InnoDB,
 PARTITION `p202606` VALUES LESS THAN (1782831600) ENGINE = InnoDB,
 PARTITION `p202607` VALUES LESS THAN (1785510000) ENGINE = InnoDB,
 PARTITION `p202608` VALUES LESS THAN (1788188400) ENGINE = InnoDB,
 PARTITION `p202609` VALUES LESS THAN (1790780400) ENGINE = InnoDB,
 PARTITION `p202610` VALUES LESS THAN (1793458800) ENGINE = InnoDB,
 PARTITION `p202611` VALUES LESS THAN (1796050800) ENGINE = InnoDB,
 PARTITION `p202612` VALUES LESS THAN (1798729200) ENGINE = InnoDB,
 PARTITION `p202701` VALUES LESS THAN (1801407600) ENGINE = InnoDB,
 PARTITION `p202702` VALUES LESS THAN (1803826800) ENGINE = InnoDB,
 PARTITION `p202703` VALUES LESS THAN (1806505200) ENGINE = InnoDB,
 PARTITION `p202704` VALUES LESS THAN (1809097200) ENGINE = InnoDB,
 PARTITION `p202705` VALUES LESS THAN (1811775600) ENGINE = InnoDB,
 PARTITION `p202706` VALUES LESS THAN (1814367600) ENGINE = InnoDB,
 PARTITION `p202707` VALUES LESS THAN (1817046000) ENGINE = InnoDB,
 PARTITION `p202708` VALUES LESS THAN (1819724400) ENGINE = InnoDB,
 PARTITION `p202709` VALUES LESS THAN (1822316400) ENGINE = InnoDB,
 PARTITION `p202710` VALUES LESS THAN (1824994800) ENGINE = InnoDB,
 PARTITION `p202711` VALUES LESS THAN (1827586800) ENGINE = InnoDB,
 PARTITION `p202712` VALUES LESS THAN (1830265200) ENGINE = InnoDB,
 PARTITION `p202801` VALUES LESS THAN (1832943600) ENGINE = InnoDB,
 PARTITION `p202802` VALUES LESS THAN (1835449200) ENGINE = InnoDB,
 PARTITION `p202803` VALUES LESS THAN (1838127600) ENGINE = InnoDB,
 PARTITION `p202804` VALUES LESS THAN (1840719600) ENGINE = InnoDB,
 PARTITION `p202805` VALUES LESS THAN (1843398000) ENGINE = InnoDB,
 PARTITION `p202806` VALUES LESS THAN (1845990000) ENGINE = InnoDB,
 PARTITION `p202807` VALUES LESS THAN (1848668400) ENGINE = InnoDB,
 PARTITION `p202808` VALUES LESS THAN (1851346800) ENGINE = InnoDB,
 PARTITION `p202809` VALUES LESS THAN (1853938800) ENGINE = InnoDB,
 PARTITION `p202810` VALUES LESS THAN (1856617200) ENGINE = InnoDB,
 PARTITION `p202811` VALUES LESS THAN (1859209200) ENGINE = InnoDB,
 PARTITION `p202812` VALUES LESS THAN (1861887600) ENGINE = InnoDB,
 PARTITION `p202901` VALUES LESS THAN (1864566000) ENGINE = InnoDB,
 PARTITION `p202902` VALUES LESS THAN (1866985200) ENGINE = InnoDB,
 PARTITION `p202903` VALUES LESS THAN (1869663600) ENGINE = InnoDB,
 PARTITION `p202904` VALUES LESS THAN (1872255600) ENGINE = InnoDB,
 PARTITION `p202905` VALUES LESS THAN (1874934000) ENGINE = InnoDB,
 PARTITION `p202906` VALUES LESS THAN (1877526000) ENGINE = InnoDB,
 PARTITION `p202907` VALUES LESS THAN (1880204400) ENGINE = InnoDB,
 PARTITION `p202908` VALUES LESS THAN (1882882800) ENGINE = InnoDB,
 PARTITION `p202909` VALUES LESS THAN (1885474800) ENGINE = InnoDB,
 PARTITION `p202910` VALUES LESS THAN (1888153200) ENGINE = InnoDB,
 PARTITION `p202911` VALUES LESS THAN (1890745200) ENGINE = InnoDB,
 PARTITION `p202912` VALUES LESS THAN (1893423600) ENGINE = InnoDB,
 PARTITION `p203001` VALUES LESS THAN (1896102000) ENGINE = InnoDB,
 PARTITION `p203002` VALUES LESS THAN (1898521200) ENGINE = InnoDB,
 PARTITION `p203003` VALUES LESS THAN (1901199600) ENGINE = InnoDB,
 PARTITION `p203004` VALUES LESS THAN (1903791600) ENGINE = InnoDB,
 PARTITION `p203005` VALUES LESS THAN (1906470000) ENGINE = InnoDB,
 PARTITION `p203006` VALUES LESS THAN (1909062000) ENGINE = InnoDB,
 PARTITION `p203007` VALUES LESS THAN (1911740400) ENGINE = InnoDB,
 PARTITION `p203008` VALUES LESS THAN (1914418800) ENGINE = InnoDB,
 PARTITION `p203009` VALUES LESS THAN (1917010800) ENGINE = InnoDB,
 PARTITION `p203010` VALUES LESS THAN (1919689200) ENGINE = InnoDB,
 PARTITION `p203011` VALUES LESS THAN (1922281200) ENGINE = InnoDB,
 PARTITION `p203012` VALUES LESS THAN (1924959600) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_15MIN`

```sql
CREATE TABLE `TB_RAWDATA_15MIN` (
  `TS` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '일시',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값',
  `QUALITY` varchar(3) DEFAULT NULL COMMENT '품질',
  `SERVER` varchar(45) DEFAULT NULL COMMENT '서버 출처',
  PRIMARY KEY (`TS`,`TAGNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='15분단위 SCADA 태그 데이터'
 PARTITION BY RANGE (unix_timestamp(`TS`))
(PARTITION `p202108` VALUES LESS THAN (1630422000) ENGINE = InnoDB,
 PARTITION `p202109` VALUES LESS THAN (1633014000) ENGINE = InnoDB,
 PARTITION `p202110` VALUES LESS THAN (1635692400) ENGINE = InnoDB,
 PARTITION `p202111` VALUES LESS THAN (1638284400) ENGINE = InnoDB,
 PARTITION `p202112` VALUES LESS THAN (1640962800) ENGINE = InnoDB,
 PARTITION `p202201` VALUES LESS THAN (1643641200) ENGINE = InnoDB,
 PARTITION `p202202` VALUES LESS THAN (1646060400) ENGINE = InnoDB,
 PARTITION `p202203` VALUES LESS THAN (1648738800) ENGINE = InnoDB,
 PARTITION `p202204` VALUES LESS THAN (1651330800) ENGINE = InnoDB,
 PARTITION `p202205` VALUES LESS THAN (1654009200) ENGINE = InnoDB,
 PARTITION `p202206` VALUES LESS THAN (1656601200) ENGINE = InnoDB,
 PARTITION `p202207` VALUES LESS THAN (1659279600) ENGINE = InnoDB,
 PARTITION `p202208` VALUES LESS THAN (1661958000) ENGINE = InnoDB,
 PARTITION `p202209` VALUES LESS THAN (1664550000) ENGINE = InnoDB,
 PARTITION `p202210` VALUES LESS THAN (1667228400) ENGINE = InnoDB,
 PARTITION `p202211` VALUES LESS THAN (1669820400) ENGINE = InnoDB,
 PARTITION `p202212` VALUES LESS THAN (1672498800) ENGINE = InnoDB,
 PARTITION `p202301` VALUES LESS THAN (1675177200) ENGINE = InnoDB,
 PARTITION `p202302` VALUES LESS THAN (1677596400) ENGINE = InnoDB,
 PARTITION `p202303` VALUES LESS THAN (1680274800) ENGINE = InnoDB,
 PARTITION `p202304` VALUES LESS THAN (1682866800) ENGINE = InnoDB,
 PARTITION `p202305` VALUES LESS THAN (1685545200) ENGINE = InnoDB,
 PARTITION `p202306` VALUES LESS THAN (1688137200) ENGINE = InnoDB,
 PARTITION `p202307` VALUES LESS THAN (1690815600) ENGINE = InnoDB,
 PARTITION `p202308` VALUES LESS THAN (1693494000) ENGINE = InnoDB,
 PARTITION `p202309` VALUES LESS THAN (1696086000) ENGINE = InnoDB,
 PARTITION `p202310` VALUES LESS THAN (1698764400) ENGINE = InnoDB,
 PARTITION `p202311` VALUES LESS THAN (1701356400) ENGINE = InnoDB,
 PARTITION `p202312` VALUES LESS THAN (1704034800) ENGINE = InnoDB,
 PARTITION `p202401` VALUES LESS THAN (1706713200) ENGINE = InnoDB,
 PARTITION `p202402` VALUES LESS THAN (1709218800) ENGINE = InnoDB,
 PARTITION `p202403` VALUES LESS THAN (1711897200) ENGINE = InnoDB,
 PARTITION `p202404` VALUES LESS THAN (1714489200) ENGINE = InnoDB,
 PARTITION `p202405` VALUES LESS THAN (1717167600) ENGINE = InnoDB,
 PARTITION `p202406` VALUES LESS THAN (1719759600) ENGINE = InnoDB,
 PARTITION `p202407` VALUES LESS THAN (1722438000) ENGINE = InnoDB,
 PARTITION `p202408` VALUES LESS THAN (1725116400) ENGINE = InnoDB,
 PARTITION `p202409` VALUES LESS THAN (1727708400) ENGINE = InnoDB,
 PARTITION `p202410` VALUES LESS THAN (1730386800) ENGINE = InnoDB,
 PARTITION `p202411` VALUES LESS THAN (1732978800) ENGINE = InnoDB,
 PARTITION `p202412` VALUES LESS THAN (1735657200) ENGINE = InnoDB,
 PARTITION `p202501` VALUES LESS THAN (1738335600) ENGINE = InnoDB,
 PARTITION `p202502` VALUES LESS THAN (1740754800) ENGINE = InnoDB,
 PARTITION `p202503` VALUES LESS THAN (1743433200) ENGINE = InnoDB,
 PARTITION `p202504` VALUES LESS THAN (1746025200) ENGINE = InnoDB,
 PARTITION `p202505` VALUES LESS THAN (1748703600) ENGINE = InnoDB,
 PARTITION `p202506` VALUES LESS THAN (1751295600) ENGINE = InnoDB,
 PARTITION `p202507` VALUES LESS THAN (1753974000) ENGINE = InnoDB,
 PARTITION `p202508` VALUES LESS THAN (1756652400) ENGINE = InnoDB,
 PARTITION `p202509` VALUES LESS THAN (1759244400) ENGINE = InnoDB,
 PARTITION `p202510` VALUES LESS THAN (1761922800) ENGINE = InnoDB,
 PARTITION `p202511` VALUES LESS THAN (1764514800) ENGINE = InnoDB,
 PARTITION `p202512` VALUES LESS THAN (1767193200) ENGINE = InnoDB,
 PARTITION `p202601` VALUES LESS THAN (1769871600) ENGINE = InnoDB,
 PARTITION `p202602` VALUES LESS THAN (1772290800) ENGINE = InnoDB,
 PARTITION `p202603` VALUES LESS THAN (1774969200) ENGINE = InnoDB,
 PARTITION `p202604` VALUES LESS THAN (1777561200) ENGINE = InnoDB,
 PARTITION `p202605` VALUES LESS THAN (1780239600) ENGINE = InnoDB,
 PARTITION `p202606` VALUES LESS THAN (1782831600) ENGINE = InnoDB,
 PARTITION `p202607` VALUES LESS THAN (1785510000) ENGINE = InnoDB,
 PARTITION `p202608` VALUES LESS THAN (1788188400) ENGINE = InnoDB,
 PARTITION `p202609` VALUES LESS THAN (1790780400) ENGINE = InnoDB,
 PARTITION `p202610` VALUES LESS THAN (1793458800) ENGINE = InnoDB,
 PARTITION `p202611` VALUES LESS THAN (1796050800) ENGINE = InnoDB,
 PARTITION `p202612` VALUES LESS THAN (1798729200) ENGINE = InnoDB,
 PARTITION `p202701` VALUES LESS THAN (1801407600) ENGINE = InnoDB,
 PARTITION `p202702` VALUES LESS THAN (1803826800) ENGINE = InnoDB,
 PARTITION `p202703` VALUES LESS THAN (1806505200) ENGINE = InnoDB,
 PARTITION `p202704` VALUES LESS THAN (1809097200) ENGINE = InnoDB,
 PARTITION `p202705` VALUES LESS THAN (1811775600) ENGINE = InnoDB,
 PARTITION `p202706` VALUES LESS THAN (1814367600) ENGINE = InnoDB,
 PARTITION `p202707` VALUES LESS THAN (1817046000) ENGINE = InnoDB,
 PARTITION `p202708` VALUES LESS THAN (1819724400) ENGINE = InnoDB,
 PARTITION `p202709` VALUES LESS THAN (1822316400) ENGINE = InnoDB,
 PARTITION `p202710` VALUES LESS THAN (1824994800) ENGINE = InnoDB,
 PARTITION `p202711` VALUES LESS THAN (1827586800) ENGINE = InnoDB,
 PARTITION `p202712` VALUES LESS THAN (1830265200) ENGINE = InnoDB,
 PARTITION `p202801` VALUES LESS THAN (1832943600) ENGINE = InnoDB,
 PARTITION `p202802` VALUES LESS THAN (1835449200) ENGINE = InnoDB,
 PARTITION `p202803` VALUES LESS THAN (1838127600) ENGINE = InnoDB,
 PARTITION `p202804` VALUES LESS THAN (1840719600) ENGINE = InnoDB,
 PARTITION `p202805` VALUES LESS THAN (1843398000) ENGINE = InnoDB,
 PARTITION `p202806` VALUES LESS THAN (1845990000) ENGINE = InnoDB,
 PARTITION `p202807` VALUES LESS THAN (1848668400) ENGINE = InnoDB,
 PARTITION `p202808` VALUES LESS THAN (1851346800) ENGINE = InnoDB,
 PARTITION `p202809` VALUES LESS THAN (1853938800) ENGINE = InnoDB,
 PARTITION `p202810` VALUES LESS THAN (1856617200) ENGINE = InnoDB,
 PARTITION `p202811` VALUES LESS THAN (1859209200) ENGINE = InnoDB,
 PARTITION `p202812` VALUES LESS THAN (1861887600) ENGINE = InnoDB,
 PARTITION `p202901` VALUES LESS THAN (1864566000) ENGINE = InnoDB,
 PARTITION `p202902` VALUES LESS THAN (1866985200) ENGINE = InnoDB,
 PARTITION `p202903` VALUES LESS THAN (1869663600) ENGINE = InnoDB,
 PARTITION `p202904` VALUES LESS THAN (1872255600) ENGINE = InnoDB,
 PARTITION `p202905` VALUES LESS THAN (1874934000) ENGINE = InnoDB,
 PARTITION `p202906` VALUES LESS THAN (1877526000) ENGINE = InnoDB,
 PARTITION `p202907` VALUES LESS THAN (1880204400) ENGINE = InnoDB,
 PARTITION `p202908` VALUES LESS THAN (1882882800) ENGINE = InnoDB,
 PARTITION `p202909` VALUES LESS THAN (1885474800) ENGINE = InnoDB,
 PARTITION `p202910` VALUES LESS THAN (1888153200) ENGINE = InnoDB,
 PARTITION `p202911` VALUES LESS THAN (1890745200) ENGINE = InnoDB,
 PARTITION `p202912` VALUES LESS THAN (1893423600) ENGINE = InnoDB,
 PARTITION `p203001` VALUES LESS THAN (1896102000) ENGINE = InnoDB,
 PARTITION `p203002` VALUES LESS THAN (1898521200) ENGINE = InnoDB,
 PARTITION `p203003` VALUES LESS THAN (1901199600) ENGINE = InnoDB,
 PARTITION `p203004` VALUES LESS THAN (1903791600) ENGINE = InnoDB,
 PARTITION `p203005` VALUES LESS THAN (1906470000) ENGINE = InnoDB,
 PARTITION `p203006` VALUES LESS THAN (1909062000) ENGINE = InnoDB,
 PARTITION `p203007` VALUES LESS THAN (1911740400) ENGINE = InnoDB,
 PARTITION `p203008` VALUES LESS THAN (1914418800) ENGINE = InnoDB,
 PARTITION `p203009` VALUES LESS THAN (1917010800) ENGINE = InnoDB,
 PARTITION `p203010` VALUES LESS THAN (1919689200) ENGINE = InnoDB,
 PARTITION `p203011` VALUES LESS THAN (1922281200) ENGINE = InnoDB,
 PARTITION `p203012` VALUES LESS THAN (1924959600) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_DAY`

```sql
CREATE TABLE `TB_RAWDATA_DAY` (
  `TS` datetime NOT NULL COMMENT '일자 (해당일 00:00:00 시각)',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` double DEFAULT 0 COMMENT '값의 합계',
  PRIMARY KEY (`TS`,`TAGNAME`),
  KEY `TB_RAWDATA_DAY_TAGNAME_IDX` (`TAGNAME`,`TS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='1일 단위 SCADA 태그 합계 데이터'
 PARTITION BY RANGE (year(`TS`))
(PARTITION `p2023` VALUES LESS THAN (2024) ENGINE = InnoDB,
 PARTITION `p2024` VALUES LESS THAN (2025) ENGINE = InnoDB,
 PARTITION `p2025` VALUES LESS THAN (2026) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_DAY_INGRT`

```sql
CREATE TABLE `TB_RAWDATA_DAY_INGRT` (
  `TS` datetime NOT NULL COMMENT '일자 (해당일 00:00:00 시각)',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` double DEFAULT 0 COMMENT '값의 합계',
  PRIMARY KEY (`TS`,`TAGNAME`),
  KEY `TB_RAWDATA_DAY_TAGNAME_IDX` (`TAGNAME`,`TS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='1일 단위 SCADA 태그 합계 데이터'
 PARTITION BY RANGE (year(`TS`))
(PARTITION `p2023` VALUES LESS THAN (2024) ENGINE = InnoDB,
 PARTITION `p2024` VALUES LESS THAN (2025) ENGINE = InnoDB,
 PARTITION `p2025` VALUES LESS THAN (2026) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_HOUR`

```sql
CREATE TABLE `TB_RAWDATA_HOUR` (
  `TS` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '일시',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값',
  `QUALITY` varchar(3) DEFAULT NULL COMMENT '품질',
  `SERVER` varchar(45) DEFAULT NULL COMMENT '서버 출처',
  PRIMARY KEY (`TS`,`TAGNAME`),
  KEY `TB_RAWDATA_HOUR_TAGNAME_IDX` (`TAGNAME`,`TS`) USING BTREE,
  KEY `TB_RAWDATA_HOUR_TAGNAME_ONLY_IDX` (`TAGNAME`) USING BTREE,
  KEY `TB_RAWDATA_HOUR_TS_IDX` (`TS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='1시간 단위 SCADA 태그 데이터'
 PARTITION BY RANGE (unix_timestamp(`TS`))
(PARTITION `p202108` VALUES LESS THAN (1630422000) ENGINE = InnoDB,
 PARTITION `p202109` VALUES LESS THAN (1633014000) ENGINE = InnoDB,
 PARTITION `p202110` VALUES LESS THAN (1635692400) ENGINE = InnoDB,
 PARTITION `p202111` VALUES LESS THAN (1638284400) ENGINE = InnoDB,
 PARTITION `p202112` VALUES LESS THAN (1640962800) ENGINE = InnoDB,
 PARTITION `p202201` VALUES LESS THAN (1643641200) ENGINE = InnoDB,
 PARTITION `p202202` VALUES LESS THAN (1646060400) ENGINE = InnoDB,
 PARTITION `p202203` VALUES LESS THAN (1648738800) ENGINE = InnoDB,
 PARTITION `p202204` VALUES LESS THAN (1651330800) ENGINE = InnoDB,
 PARTITION `p202205` VALUES LESS THAN (1654009200) ENGINE = InnoDB,
 PARTITION `p202206` VALUES LESS THAN (1656601200) ENGINE = InnoDB,
 PARTITION `p202207` VALUES LESS THAN (1659279600) ENGINE = InnoDB,
 PARTITION `p202208` VALUES LESS THAN (1661958000) ENGINE = InnoDB,
 PARTITION `p202209` VALUES LESS THAN (1664550000) ENGINE = InnoDB,
 PARTITION `p202210` VALUES LESS THAN (1667228400) ENGINE = InnoDB,
 PARTITION `p202211` VALUES LESS THAN (1669820400) ENGINE = InnoDB,
 PARTITION `p202212` VALUES LESS THAN (1672498800) ENGINE = InnoDB,
 PARTITION `p202301` VALUES LESS THAN (1675177200) ENGINE = InnoDB,
 PARTITION `p202302` VALUES LESS THAN (1677596400) ENGINE = InnoDB,
 PARTITION `p202303` VALUES LESS THAN (1680274800) ENGINE = InnoDB,
 PARTITION `p202304` VALUES LESS THAN (1682866800) ENGINE = InnoDB,
 PARTITION `p202305` VALUES LESS THAN (1685545200) ENGINE = InnoDB,
 PARTITION `p202306` VALUES LESS THAN (1688137200) ENGINE = InnoDB,
 PARTITION `p202307` VALUES LESS THAN (1690815600) ENGINE = InnoDB,
 PARTITION `p202308` VALUES LESS THAN (1693494000) ENGINE = InnoDB,
 PARTITION `p202309` VALUES LESS THAN (1696086000) ENGINE = InnoDB,
 PARTITION `p202310` VALUES LESS THAN (1698764400) ENGINE = InnoDB,
 PARTITION `p202311` VALUES LESS THAN (1701356400) ENGINE = InnoDB,
 PARTITION `p202312` VALUES LESS THAN (1704034800) ENGINE = InnoDB,
 PARTITION `p202401` VALUES LESS THAN (1706713200) ENGINE = InnoDB,
 PARTITION `p202402` VALUES LESS THAN (1709218800) ENGINE = InnoDB,
 PARTITION `p202403` VALUES LESS THAN (1711897200) ENGINE = InnoDB,
 PARTITION `p202404` VALUES LESS THAN (1714489200) ENGINE = InnoDB,
 PARTITION `p202405` VALUES LESS THAN (1717167600) ENGINE = InnoDB,
 PARTITION `p202406` VALUES LESS THAN (1719759600) ENGINE = InnoDB,
 PARTITION `p202407` VALUES LESS THAN (1722438000) ENGINE = InnoDB,
 PARTITION `p202408` VALUES LESS THAN (1725116400) ENGINE = InnoDB,
 PARTITION `p202409` VALUES LESS THAN (1727708400) ENGINE = InnoDB,
 PARTITION `p202410` VALUES LESS THAN (1730386800) ENGINE = InnoDB,
 PARTITION `p202411` VALUES LESS THAN (1732978800) ENGINE = InnoDB,
 PARTITION `p202412` VALUES LESS THAN (1735657200) ENGINE = InnoDB,
 PARTITION `p202501` VALUES LESS THAN (1738335600) ENGINE = InnoDB,
 PARTITION `p202502` VALUES LESS THAN (1740754800) ENGINE = InnoDB,
 PARTITION `p202503` VALUES LESS THAN (1743433200) ENGINE = InnoDB,
 PARTITION `p202504` VALUES LESS THAN (1746025200) ENGINE = InnoDB,
 PARTITION `p202505` VALUES LESS THAN (1748703600) ENGINE = InnoDB,
 PARTITION `p202506` VALUES LESS THAN (1751295600) ENGINE = InnoDB,
 PARTITION `p202507` VALUES LESS THAN (1753974000) ENGINE = InnoDB,
 PARTITION `p202508` VALUES LESS THAN (1756652400) ENGINE = InnoDB,
 PARTITION `p202509` VALUES LESS THAN (1759244400) ENGINE = InnoDB,
 PARTITION `p202510` VALUES LESS THAN (1761922800) ENGINE = InnoDB,
 PARTITION `p202511` VALUES LESS THAN (1764514800) ENGINE = InnoDB,
 PARTITION `p202512` VALUES LESS THAN (1767193200) ENGINE = InnoDB,
 PARTITION `p202601` VALUES LESS THAN (1769871600) ENGINE = InnoDB,
 PARTITION `p202602` VALUES LESS THAN (1772290800) ENGINE = InnoDB,
 PARTITION `p202603` VALUES LESS THAN (1774969200) ENGINE = InnoDB,
 PARTITION `p202604` VALUES LESS THAN (1777561200) ENGINE = InnoDB,
 PARTITION `p202605` VALUES LESS THAN (1780239600) ENGINE = InnoDB,
 PARTITION `p202606` VALUES LESS THAN (1782831600) ENGINE = InnoDB,
 PARTITION `p202607` VALUES LESS THAN (1785510000) ENGINE = InnoDB,
 PARTITION `p202608` VALUES LESS THAN (1788188400) ENGINE = InnoDB,
 PARTITION `p202609` VALUES LESS THAN (1790780400) ENGINE = InnoDB,
 PARTITION `p202610` VALUES LESS THAN (1793458800) ENGINE = InnoDB,
 PARTITION `p202611` VALUES LESS THAN (1796050800) ENGINE = InnoDB,
 PARTITION `p202612` VALUES LESS THAN (1798729200) ENGINE = InnoDB,
 PARTITION `p202701` VALUES LESS THAN (1801407600) ENGINE = InnoDB,
 PARTITION `p202702` VALUES LESS THAN (1803826800) ENGINE = InnoDB,
 PARTITION `p202703` VALUES LESS THAN (1806505200) ENGINE = InnoDB,
 PARTITION `p202704` VALUES LESS THAN (1809097200) ENGINE = InnoDB,
 PARTITION `p202705` VALUES LESS THAN (1811775600) ENGINE = InnoDB,
 PARTITION `p202706` VALUES LESS THAN (1814367600) ENGINE = InnoDB,
 PARTITION `p202707` VALUES LESS THAN (1817046000) ENGINE = InnoDB,
 PARTITION `p202708` VALUES LESS THAN (1819724400) ENGINE = InnoDB,
 PARTITION `p202709` VALUES LESS THAN (1822316400) ENGINE = InnoDB,
 PARTITION `p202710` VALUES LESS THAN (1824994800) ENGINE = InnoDB,
 PARTITION `p202711` VALUES LESS THAN (1827586800) ENGINE = InnoDB,
 PARTITION `p202712` VALUES LESS THAN (1830265200) ENGINE = InnoDB,
 PARTITION `p202801` VALUES LESS THAN (1832943600) ENGINE = InnoDB,
 PARTITION `p202802` VALUES LESS THAN (1835449200) ENGINE = InnoDB,
 PARTITION `p202803` VALUES LESS THAN (1838127600) ENGINE = InnoDB,
 PARTITION `p202804` VALUES LESS THAN (1840719600) ENGINE = InnoDB,
 PARTITION `p202805` VALUES LESS THAN (1843398000) ENGINE = InnoDB,
 PARTITION `p202806` VALUES LESS THAN (1845990000) ENGINE = InnoDB,
 PARTITION `p202807` VALUES LESS THAN (1848668400) ENGINE = InnoDB,
 PARTITION `p202808` VALUES LESS THAN (1851346800) ENGINE = InnoDB,
 PARTITION `p202809` VALUES LESS THAN (1853938800) ENGINE = InnoDB,
 PARTITION `p202810` VALUES LESS THAN (1856617200) ENGINE = InnoDB,
 PARTITION `p202811` VALUES LESS THAN (1859209200) ENGINE = InnoDB,
 PARTITION `p202812` VALUES LESS THAN (1861887600) ENGINE = InnoDB,
 PARTITION `p202901` VALUES LESS THAN (1864566000) ENGINE = InnoDB,
 PARTITION `p202902` VALUES LESS THAN (1866985200) ENGINE = InnoDB,
 PARTITION `p202903` VALUES LESS THAN (1869663600) ENGINE = InnoDB,
 PARTITION `p202904` VALUES LESS THAN (1872255600) ENGINE = InnoDB,
 PARTITION `p202905` VALUES LESS THAN (1874934000) ENGINE = InnoDB,
 PARTITION `p202906` VALUES LESS THAN (1877526000) ENGINE = InnoDB,
 PARTITION `p202907` VALUES LESS THAN (1880204400) ENGINE = InnoDB,
 PARTITION `p202908` VALUES LESS THAN (1882882800) ENGINE = InnoDB,
 PARTITION `p202909` VALUES LESS THAN (1885474800) ENGINE = InnoDB,
 PARTITION `p202910` VALUES LESS THAN (1888153200) ENGINE = InnoDB,
 PARTITION `p202911` VALUES LESS THAN (1890745200) ENGINE = InnoDB,
 PARTITION `p202912` VALUES LESS THAN (1893423600) ENGINE = InnoDB,
 PARTITION `p203001` VALUES LESS THAN (1896102000) ENGINE = InnoDB,
 PARTITION `p203002` VALUES LESS THAN (1898521200) ENGINE = InnoDB,
 PARTITION `p203003` VALUES LESS THAN (1901199600) ENGINE = InnoDB,
 PARTITION `p203004` VALUES LESS THAN (1903791600) ENGINE = InnoDB,
 PARTITION `p203005` VALUES LESS THAN (1906470000) ENGINE = InnoDB,
 PARTITION `p203006` VALUES LESS THAN (1909062000) ENGINE = InnoDB,
 PARTITION `p203007` VALUES LESS THAN (1911740400) ENGINE = InnoDB,
 PARTITION `p203008` VALUES LESS THAN (1914418800) ENGINE = InnoDB,
 PARTITION `p203009` VALUES LESS THAN (1917010800) ENGINE = InnoDB,
 PARTITION `p203010` VALUES LESS THAN (1919689200) ENGINE = InnoDB,
 PARTITION `p203011` VALUES LESS THAN (1922281200) ENGINE = InnoDB,
 PARTITION `p203012` VALUES LESS THAN (1924959600) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_HOUR_INGRT`

```sql
CREATE TABLE `TB_RAWDATA_HOUR_INGRT` (
  `TS` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '일시',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값',
  `QUALITY` varchar(3) DEFAULT NULL COMMENT '품질',
  `SERVER` varchar(45) DEFAULT NULL COMMENT '서버 출처',
  PRIMARY KEY (`TS`,`TAGNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='1시간 단위 적산 SCADA 태그 데이터'
 PARTITION BY RANGE (unix_timestamp(`TS`))
(PARTITION `p202108` VALUES LESS THAN (1630422000) ENGINE = InnoDB,
 PARTITION `p202109` VALUES LESS THAN (1633014000) ENGINE = InnoDB,
 PARTITION `p202110` VALUES LESS THAN (1635692400) ENGINE = InnoDB,
 PARTITION `p202111` VALUES LESS THAN (1638284400) ENGINE = InnoDB,
 PARTITION `p202112` VALUES LESS THAN (1640962800) ENGINE = InnoDB,
 PARTITION `p202201` VALUES LESS THAN (1643641200) ENGINE = InnoDB,
 PARTITION `p202202` VALUES LESS THAN (1646060400) ENGINE = InnoDB,
 PARTITION `p202203` VALUES LESS THAN (1648738800) ENGINE = InnoDB,
 PARTITION `p202204` VALUES LESS THAN (1651330800) ENGINE = InnoDB,
 PARTITION `p202205` VALUES LESS THAN (1654009200) ENGINE = InnoDB,
 PARTITION `p202206` VALUES LESS THAN (1656601200) ENGINE = InnoDB,
 PARTITION `p202207` VALUES LESS THAN (1659279600) ENGINE = InnoDB,
 PARTITION `p202208` VALUES LESS THAN (1661958000) ENGINE = InnoDB,
 PARTITION `p202209` VALUES LESS THAN (1664550000) ENGINE = InnoDB,
 PARTITION `p202210` VALUES LESS THAN (1667228400) ENGINE = InnoDB,
 PARTITION `p202211` VALUES LESS THAN (1669820400) ENGINE = InnoDB,
 PARTITION `p202212` VALUES LESS THAN (1672498800) ENGINE = InnoDB,
 PARTITION `p202301` VALUES LESS THAN (1675177200) ENGINE = InnoDB,
 PARTITION `p202302` VALUES LESS THAN (1677596400) ENGINE = InnoDB,
 PARTITION `p202303` VALUES LESS THAN (1680274800) ENGINE = InnoDB,
 PARTITION `p202304` VALUES LESS THAN (1682866800) ENGINE = InnoDB,
 PARTITION `p202305` VALUES LESS THAN (1685545200) ENGINE = InnoDB,
 PARTITION `p202306` VALUES LESS THAN (1688137200) ENGINE = InnoDB,
 PARTITION `p202307` VALUES LESS THAN (1690815600) ENGINE = InnoDB,
 PARTITION `p202308` VALUES LESS THAN (1693494000) ENGINE = InnoDB,
 PARTITION `p202309` VALUES LESS THAN (1696086000) ENGINE = InnoDB,
 PARTITION `p202310` VALUES LESS THAN (1698764400) ENGINE = InnoDB,
 PARTITION `p202311` VALUES LESS THAN (1701356400) ENGINE = InnoDB,
 PARTITION `p202312` VALUES LESS THAN (1704034800) ENGINE = InnoDB,
 PARTITION `p202401` VALUES LESS THAN (1706713200) ENGINE = InnoDB,
 PARTITION `p202402` VALUES LESS THAN (1709218800) ENGINE = InnoDB,
 PARTITION `p202403` VALUES LESS THAN (1711897200) ENGINE = InnoDB,
 PARTITION `p202404` VALUES LESS THAN (1714489200) ENGINE = InnoDB,
 PARTITION `p202405` VALUES LESS THAN (1717167600) ENGINE = InnoDB,
 PARTITION `p202406` VALUES LESS THAN (1719759600) ENGINE = InnoDB,
 PARTITION `p202407` VALUES LESS THAN (1722438000) ENGINE = InnoDB,
 PARTITION `p202408` VALUES LESS THAN (1725116400) ENGINE = InnoDB,
 PARTITION `p202409` VALUES LESS THAN (1727708400) ENGINE = InnoDB,
 PARTITION `p202410` VALUES LESS THAN (1730386800) ENGINE = InnoDB,
 PARTITION `p202411` VALUES LESS THAN (1732978800) ENGINE = InnoDB,
 PARTITION `p202412` VALUES LESS THAN (1735657200) ENGINE = InnoDB,
 PARTITION `p202501` VALUES LESS THAN (1738335600) ENGINE = InnoDB,
 PARTITION `p202502` VALUES LESS THAN (1740754800) ENGINE = InnoDB,
 PARTITION `p202503` VALUES LESS THAN (1743433200) ENGINE = InnoDB,
 PARTITION `p202504` VALUES LESS THAN (1746025200) ENGINE = InnoDB,
 PARTITION `p202505` VALUES LESS THAN (1748703600) ENGINE = InnoDB,
 PARTITION `p202506` VALUES LESS THAN (1751295600) ENGINE = InnoDB,
 PARTITION `p202507` VALUES LESS THAN (1753974000) ENGINE = InnoDB,
 PARTITION `p202508` VALUES LESS THAN (1756652400) ENGINE = InnoDB,
 PARTITION `p202509` VALUES LESS THAN (1759244400) ENGINE = InnoDB,
 PARTITION `p202510` VALUES LESS THAN (1761922800) ENGINE = InnoDB,
 PARTITION `p202511` VALUES LESS THAN (1764514800) ENGINE = InnoDB,
 PARTITION `p202512` VALUES LESS THAN (1767193200) ENGINE = InnoDB,
 PARTITION `p202601` VALUES LESS THAN (1769871600) ENGINE = InnoDB,
 PARTITION `p202602` VALUES LESS THAN (1772290800) ENGINE = InnoDB,
 PARTITION `p202603` VALUES LESS THAN (1774969200) ENGINE = InnoDB,
 PARTITION `p202604` VALUES LESS THAN (1777561200) ENGINE = InnoDB,
 PARTITION `p202605` VALUES LESS THAN (1780239600) ENGINE = InnoDB,
 PARTITION `p202606` VALUES LESS THAN (1782831600) ENGINE = InnoDB,
 PARTITION `p202607` VALUES LESS THAN (1785510000) ENGINE = InnoDB,
 PARTITION `p202608` VALUES LESS THAN (1788188400) ENGINE = InnoDB,
 PARTITION `p202609` VALUES LESS THAN (1790780400) ENGINE = InnoDB,
 PARTITION `p202610` VALUES LESS THAN (1793458800) ENGINE = InnoDB,
 PARTITION `p202611` VALUES LESS THAN (1796050800) ENGINE = InnoDB,
 PARTITION `p202612` VALUES LESS THAN (1798729200) ENGINE = InnoDB,
 PARTITION `p202701` VALUES LESS THAN (1801407600) ENGINE = InnoDB,
 PARTITION `p202702` VALUES LESS THAN (1803826800) ENGINE = InnoDB,
 PARTITION `p202703` VALUES LESS THAN (1806505200) ENGINE = InnoDB,
 PARTITION `p202704` VALUES LESS THAN (1809097200) ENGINE = InnoDB,
 PARTITION `p202705` VALUES LESS THAN (1811775600) ENGINE = InnoDB,
 PARTITION `p202706` VALUES LESS THAN (1814367600) ENGINE = InnoDB,
 PARTITION `p202707` VALUES LESS THAN (1817046000) ENGINE = InnoDB,
 PARTITION `p202708` VALUES LESS THAN (1819724400) ENGINE = InnoDB,
 PARTITION `p202709` VALUES LESS THAN (1822316400) ENGINE = InnoDB,
 PARTITION `p202710` VALUES LESS THAN (1824994800) ENGINE = InnoDB,
 PARTITION `p202711` VALUES LESS THAN (1827586800) ENGINE = InnoDB,
 PARTITION `p202712` VALUES LESS THAN (1830265200) ENGINE = InnoDB,
 PARTITION `p202801` VALUES LESS THAN (1832943600) ENGINE = InnoDB,
 PARTITION `p202802` VALUES LESS THAN (1835449200) ENGINE = InnoDB,
 PARTITION `p202803` VALUES LESS THAN (1838127600) ENGINE = InnoDB,
 PARTITION `p202804` VALUES LESS THAN (1840719600) ENGINE = InnoDB,
 PARTITION `p202805` VALUES LESS THAN (1843398000) ENGINE = InnoDB,
 PARTITION `p202806` VALUES LESS THAN (1845990000) ENGINE = InnoDB,
 PARTITION `p202807` VALUES LESS THAN (1848668400) ENGINE = InnoDB,
 PARTITION `p202808` VALUES LESS THAN (1851346800) ENGINE = InnoDB,
 PARTITION `p202809` VALUES LESS THAN (1853938800) ENGINE = InnoDB,
 PARTITION `p202810` VALUES LESS THAN (1856617200) ENGINE = InnoDB,
 PARTITION `p202811` VALUES LESS THAN (1859209200) ENGINE = InnoDB,
 PARTITION `p202812` VALUES LESS THAN (1861887600) ENGINE = InnoDB,
 PARTITION `p202901` VALUES LESS THAN (1864566000) ENGINE = InnoDB,
 PARTITION `p202902` VALUES LESS THAN (1866985200) ENGINE = InnoDB,
 PARTITION `p202903` VALUES LESS THAN (1869663600) ENGINE = InnoDB,
 PARTITION `p202904` VALUES LESS THAN (1872255600) ENGINE = InnoDB,
 PARTITION `p202905` VALUES LESS THAN (1874934000) ENGINE = InnoDB,
 PARTITION `p202906` VALUES LESS THAN (1877526000) ENGINE = InnoDB,
 PARTITION `p202907` VALUES LESS THAN (1880204400) ENGINE = InnoDB,
 PARTITION `p202908` VALUES LESS THAN (1882882800) ENGINE = InnoDB,
 PARTITION `p202909` VALUES LESS THAN (1885474800) ENGINE = InnoDB,
 PARTITION `p202910` VALUES LESS THAN (1888153200) ENGINE = InnoDB,
 PARTITION `p202911` VALUES LESS THAN (1890745200) ENGINE = InnoDB,
 PARTITION `p202912` VALUES LESS THAN (1893423600) ENGINE = InnoDB,
 PARTITION `p203001` VALUES LESS THAN (1896102000) ENGINE = InnoDB,
 PARTITION `p203002` VALUES LESS THAN (1898521200) ENGINE = InnoDB,
 PARTITION `p203003` VALUES LESS THAN (1901199600) ENGINE = InnoDB,
 PARTITION `p203004` VALUES LESS THAN (1903791600) ENGINE = InnoDB,
 PARTITION `p203005` VALUES LESS THAN (1906470000) ENGINE = InnoDB,
 PARTITION `p203006` VALUES LESS THAN (1909062000) ENGINE = InnoDB,
 PARTITION `p203007` VALUES LESS THAN (1911740400) ENGINE = InnoDB,
 PARTITION `p203008` VALUES LESS THAN (1914418800) ENGINE = InnoDB,
 PARTITION `p203009` VALUES LESS THAN (1917010800) ENGINE = InnoDB,
 PARTITION `p203010` VALUES LESS THAN (1919689200) ENGINE = InnoDB,
 PARTITION `p203011` VALUES LESS THAN (1922281200) ENGINE = InnoDB,
 PARTITION `p203012` VALUES LESS THAN (1924959600) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_MONTH`

```sql
CREATE TABLE `TB_RAWDATA_MONTH` (
  `TS` datetime NOT NULL COMMENT '년월 (해당월 1일 00:00:00 시각)',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` double DEFAULT 0 COMMENT '값의 합계',
  PRIMARY KEY (`TS`,`TAGNAME`),
  KEY `TB_RAWDATA_MONTH_TAGNAME_IDX` (`TAGNAME`,`TS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='1개월 단위 SCADA 태그 합계 데이터'
 PARTITION BY RANGE (year(`TS`))
(PARTITION `p2023` VALUES LESS THAN (2024) ENGINE = InnoDB,
 PARTITION `p2024` VALUES LESS THAN (2025) ENGINE = InnoDB,
 PARTITION `p2025` VALUES LESS THAN (2026) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_MONTH_INGRT`

```sql
CREATE TABLE `TB_RAWDATA_MONTH_INGRT` (
  `TS` datetime NOT NULL COMMENT '년월 (해당월 1일 00:00:00 시각)',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` double DEFAULT 0 COMMENT '값의 합계',
  PRIMARY KEY (`TS`,`TAGNAME`),
  KEY `TB_RAWDATA_MONTH_TAGNAME_IDX` (`TAGNAME`,`TS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='1개월 단위 SCADA 태그 합계 데이터'
 PARTITION BY RANGE (year(`TS`))
(PARTITION `p2023` VALUES LESS THAN (2024) ENGINE = InnoDB,
 PARTITION `p2024` VALUES LESS THAN (2025) ENGINE = InnoDB,
 PARTITION `p2025` VALUES LESS THAN (2026) ENGINE = InnoDB,
 PARTITION `p_future` VALUES LESS THAN MAXVALUE ENGINE = InnoDB)
```

## `TB_RAWDATA_PMB_HOUR`

```sql
CREATE TABLE `TB_RAWDATA_PMB_HOUR` (
  `TS` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '일시',
  `TAGNAME` varchar(45) NOT NULL COMMENT '태그 이름',
  `VALUE` varchar(45) DEFAULT NULL COMMENT '값 (0 또는 1)',
  PRIMARY KEY (`TS`,`TAGNAME`),
  KEY `idx_tagname_ts` (`TAGNAME`,`TS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='펌프 가동상태(PMB) 태그 전용 테이블'
```

## `TB_RST_SAVINGS_TARGET`

```sql
CREATE TABLE `TB_RST_SAVINGS_TARGET` (
  `DATE` varchar(50) NOT NULL COMMENT '날짜',
  `TYPE` varchar(50) DEFAULT NULL COMMENT '타입',
  `SAVINGCOST` varchar(50) DEFAULT NULL COMMENT '절감 비용',
  `SAVINGKWH` varchar(50) DEFAULT NULL COMMENT '전력절감량',
  `SAVINGCO2` varchar(50) DEFAULT NULL COMMENT '탄소절감량',
  `SAVINGUNIT` varchar(50) DEFAULT NULL COMMENT '현재원단위',
  `NOW_GOAL` varchar(100) DEFAULT NULL COMMENT '목표(테스트)',
  `NOW_PWR` varchar(100) DEFAULT NULL COMMENT '전력량(테스트)',
  `NOW_FRQ` varchar(100) DEFAULT NULL COMMENT '유량(테스트)',
  PRIMARY KEY (`DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='전력 절감 결과'
```

## `TB_RT_JOB_INF`

```sql
CREATE TABLE `TB_RT_JOB_INF` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `DTRG_DATE` date NOT NULL COMMENT '데이터 등록 일자',
  `TAG` varchar(45) NOT NULL COMMENT '태그',
  `JOB_CD` varchar(5) NOT NULL COMMENT '작업 코드',
  `JOB_PRP` varchar(100) NOT NULL COMMENT '작업 목적',
  `JOB_START_TIME` datetime NOT NULL COMMENT '작업 시작 일시',
  `JOB_END_TIME` datetime NOT NULL COMMENT '작업 종료 일시',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용 여부',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT current_timestamp() COMMENT '업데이트 일시',
  PRIMARY KEY (`DTRG_DATE`,`TAG`,`JOB_CD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='작업정보'
```

## `TB_RT_MSTR_INF`

```sql
CREATE TABLE `TB_RT_MSTR_INF` (
  `RATE_IDX` int(11) NOT NULL COMMENT '요금제 인덱스',
  `LARGE_CTGRY` varchar(10) DEFAULT NULL COMMENT '대분류',
  `MIDDLE_CTGRY` varchar(3) DEFAULT NULL COMMENT '중분류',
  `SMALL_CTGRY` varchar(5) DEFAULT NULL COMMENT '소분류',
  `VLTG_DVSN` varchar(5) DEFAULT NULL COMMENT '전압 구분',
  `RATE_CD` varchar(4) DEFAULT NULL COMMENT '요금제 코드',
  `DTRG_DATE` date DEFAULT NULL COMMENT '데이터 등록 일자',
  `APLCT_POINT` date DEFAULT NULL COMMENT '적용 시점',
  `USE_YN` char(1) DEFAULT '1' COMMENT '사용 여부',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  PRIMARY KEY (`RATE_IDX`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='요금제 코드 정보'
```

## `TB_RT_POWER_RST`

```sql
CREATE TABLE `TB_RT_POWER_RST` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `ANLY_DATE` date NOT NULL COMMENT '분석날짜',
  `RST_TYP` char(1) NOT NULL DEFAULT '1' COMMENT '결과 종류',
  `DATA_BS_YMNTH` char(6) NOT NULL COMMENT '데이터 기준 년월',
  `PWR` int(11) NOT NULL COMMENT '전력량',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`ANLY_DATE`,`RST_TYP`,`DATA_BS_YMNTH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='요금적용전력결과'
```

## `TB_RT_RATE_INF`

```sql
CREATE TABLE `TB_RT_RATE_INF` (
  `MNTH` varchar(3) NOT NULL COMMENT '월',
  `STN_TM` char(2) NOT NULL COMMENT '기준 일시',
  `RATE_IDX` int(11) NOT NULL COMMENT '요금제 인덱스',
  `SSN` varchar(3) NOT NULL COMMENT '계절',
  `TIMEZONE` char(1) NOT NULL COMMENT '시간대',
  `BASE_RATE` int(11) NOT NULL COMMENT '기본요금제',
  `ELCTR_RATE` float NOT NULL COMMENT '전기사용요금제',
  PRIMARY KEY (`MNTH`,`STN_TM`,`RATE_IDX`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='요금제 정보'
```

## `TB_RT_RATE_RST`

```sql
CREATE TABLE `TB_RT_RATE_RST` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `ANLY_DATE` date NOT NULL COMMENT '분석날짜',
  `DATA_BS_YMNTH` char(6) NOT NULL COMMENT '데이터 기준 년월',
  `RATE_IDX` int(11) NOT NULL COMMENT '요금제 인덱스',
  `TNMNTH_RATE_YN` char(1) DEFAULT '1' COMMENT '익월 최적요금제 여부',
  `DATA_MSN_PRCNT` float NOT NULL COMMENT '데이터 누락율 (%)',
  `TOT_PWR` int(11) NOT NULL COMMENT '전체 전력량',
  `TOT_FEE` int(11) NOT NULL COMMENT '전체 요금',
  `BASE_FEE` int(11) NOT NULL COMMENT '기본 요금',
  `ETC_FEE` int(11) NOT NULL COMMENT '기타 요금',
  `L_PWR` int(11) NOT NULL COMMENT '경부하 전력량',
  `M_PWR` int(11) NOT NULL COMMENT '중간부하 전력량',
  `H_PWR` int(11) NOT NULL COMMENT '최대부하 전력량',
  `L_ELCTR_FEE` int(11) NOT NULL COMMENT '경부하 전력요금',
  `M_ELCTR_FEE` int(11) NOT NULL COMMENT '중간부하 전력요금',
  `H_ELCTR_FEE` int(11) NOT NULL COMMENT '최대부하 전력요금',
  `DC_NMB` varchar(10) DEFAULT NULL COMMENT '도커 번호',
  `RGSTR_TIME` datetime DEFAULT current_timestamp() COMMENT '등록일시',
  `OPT_RATE_YN` int(11) DEFAULT NULL COMMENT '최적요금제 사용 여부',
  `FLAG` char(1) DEFAULT '0' COMMENT 'kafka producer 전송 여부',
  PRIMARY KEY (`ANLY_DATE`,`DATA_BS_YMNTH`,`RATE_IDX`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='최적요금제결과'
```

## `TB_TAGINFO`

```sql
CREATE TABLE `TB_TAGINFO` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `TAGNAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '태그 이름',
  `ZONE_CODE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '시설 코드',
  `FAC_CODE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '설비 코드',
  `USE_YN` char(1) NOT NULL DEFAULT '1' COMMENT '사용 여부',
  PRIMARY KEY (`TAGNAME`,`ZONE_CODE`,`FAC_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='정수장 시설 및 설비 태그 정의'
```

## `TB_TAG_UNIT_INFO`

```sql
CREATE TABLE `TB_TAG_UNIT_INFO` (
  `TAG_TYP` varchar(100) DEFAULT NULL COMMENT '태그 타입',
  `TAG_NAME` varchar(50) DEFAULT NULL COMMENT '태그 이름',
  `TAG_DSC` varchar(100) DEFAULT NULL COMMENT '태그 설명',
  `TAG_UNIT` varchar(100) DEFAULT NULL COMMENT '태그 단위',
  `TAG_UNIT_VALUE` varchar(100) DEFAULT NULL COMMENT '태그 단위 값',
  `TAG_DCS` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='태그 단위 정의'
```

## `TB_TNK_GRP_INF`

```sql
CREATE TABLE `TB_TNK_GRP_INF` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `TNK_GRP_IDX` int(11) NOT NULL COMMENT '탱크 그룹 인덱스',
  `TNK_IDX` int(11) NOT NULL COMMENT '탱크 인덱스',
  `VLV_IDX` int(11) NOT NULL COMMENT '밸브 인덱스',
  `IN_FLW_IDX` int(11) NOT NULL DEFAULT 1 COMMENT '유입 인덱스',
  `OUT_FLW_IDX` int(11) NOT NULL DEFAULT 1 COMMENT '유출 인덱스',
  `TNK_TYP` int(1) DEFAULT NULL COMMENT '탱크 타입(1: 배수지, 2: 정수지)',
  `TNK_GRP_NM` varchar(200) DEFAULT NULL COMMENT '탱크 그룹 인덱스',
  `TNK_NM` varchar(100) DEFAULT NULL COMMENT '탱크 이름',
  `PUMP_GRP` int(11) DEFAULT NULL COMMENT '펌프그룹',
  `PUMP_GRP_NM` varchar(200) DEFAULT NULL COMMENT '펌프 그룹 이름',
  `IN_FC_TAG` varchar(30) DEFAULT NULL COMMENT '유입밸브 닫힘 태그',
  `OUT_FC_TAG` varchar(30) DEFAULT NULL COMMENT '유출밸브 닫힘 태그',
  `IN_FO_TAG` varchar(30) DEFAULT NULL COMMENT '유입밸브 열림 태그',
  `OUT_FO_TAG` varchar(30) DEFAULT NULL COMMENT '유출밸브 열림 태그',
  `IN_POI_TAG` varchar(30) DEFAULT NULL COMMENT '유입밸브 개도율 태그',
  `OUT_POI_TAG` varchar(30) DEFAULT NULL COMMENT '유출밸브 개도율 태그',
  `LEI_TAG` varchar(30) DEFAULT NULL COMMENT '수위 태그',
  `IN_FLW_TAG` varchar(30) DEFAULT NULL COMMENT '유입 유량 태그',
  `OUT_FLW_TAG` varchar(30) DEFAULT NULL COMMENT '유출 유량 태그',
  `DMD_PRI` float DEFAULT NULL COMMENT '최소요구관압',
  `LWL_LIM` float DEFAULT NULL COMMENT '최저 수위 제한',
  `HWL_LIM` float DEFAULT NULL COMMENT '최고 수위 제한',
  `MIN_LOAD_LWL` float DEFAULT NULL COMMENT '최소 부하 최저 수위',
  `MID_LOAD_LWL` float DEFAULT NULL COMMENT '중간 부하 최저 수위',
  `MAX_LOAD_LWL` float DEFAULT NULL COMMENT '최대 부하 최저 수위',
  `VLM` float DEFAULT NULL COMMENT '부피',
  `LWL` float DEFAULT NULL COMMENT '최저수위',
  `HWL` float DEFAULT NULL COMMENT '최고수위',
  `BASE_AREA` varchar(50) DEFAULT NULL COMMENT '기준 지역',
  `USE_YN` char(1) DEFAULT NULL COMMENT '사용 여부',
  `RGSTR_TIME` datetime DEFAULT NULL COMMENT '등록일시',
  `UPDT_TIME` datetime DEFAULT NULL COMMENT '업데이트 일시',
  PRIMARY KEY (`TNK_GRP_IDX`,`TNK_IDX`,`VLV_IDX`,`IN_FLW_IDX`,`OUT_FLW_IDX`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='배수지 그룹 정보'
```

## `TB_TOT_ALG`

```sql
CREATE TABLE `TB_TOT_ALG` (
  `RGSTR_TIME` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일시',
  `HH_LOSS_VAL_TOT` float DEFAULT NULL COMMENT '수두손실값합계',
  `FLW_VAL` float DEFAULT NULL COMMENT '유량값',
  `FP_VAL` float DEFAULT NULL COMMENT '유압값',
  `FP_ALG_RST_VAL` float DEFAULT NULL COMMENT '유압알고리즘결과값',
  `FLG` varchar(10) NOT NULL DEFAULT 'CUR' COMMENT '플래그',
  PRIMARY KEY (`RGSTR_TIME`,`FLG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='통합알고리즘'
```

## `TB_TOT_GRP`

```sql
CREATE TABLE `TB_TOT_GRP` (
  `TOT_GRP` varchar(11) NOT NULL COMMENT '펌프 수두 그룹',
  `GRP_KEY` varchar(11) NOT NULL COMMENT '그룹 키워드',
  `DCS` varchar(100) DEFAULT NULL COMMENT '설명',
  PRIMARY KEY (`TOT_GRP`,`GRP_KEY`),
  KEY `TB_TOT_GRP_TOT_GRP_IDX` (`TOT_GRP`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='통합그룹'
```

## `TB_WPP_TAG_CODE`

```sql
CREATE TABLE `TB_WPP_TAG_CODE` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `FUNC_TYP` varchar(100) DEFAULT NULL COMMENT '기능 구분',
  `DISPLAY_ID` varchar(100) DEFAULT NULL COMMENT '화면 값 아이디',
  `DISPLAY_NM` varchar(100) DEFAULT NULL COMMENT '화면 값 이름',
  `TAG_GRP` varchar(5) DEFAULT NULL COMMENT '태그 그룹',
  `TAG` varchar(45) DEFAULT NULL COMMENT '태그',
  `TAG_KOR_NM` varchar(100) DEFAULT NULL COMMENT '태그 한글명',
  `TAG_UNIT` varchar(100) DEFAULT NULL COMMENT '태그 단위',
  `TAG_DSC` varchar(100) DEFAULT NULL COMMENT '태그 설명',
  `DEFAULT_VALUE` varchar(100) DEFAULT NULL COMMENT '정의 전 임의값',
  `TAG_DCS` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='데이터 태그 정의'
```

## `TB_WPP_TAG_INF`

```sql
CREATE TABLE `TB_WPP_TAG_INF` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `TAG_GRP` varchar(5) DEFAULT NULL COMMENT '태그 그룹',
  `TAG` varchar(45) DEFAULT NULL COMMENT '태그',
  `USE_YN` varchar(1) DEFAULT '1' COMMENT '사용 여부'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Kafka Consumer 사용 태그 정의'
```

## `TB_ZONE`

```sql
CREATE TABLE `TB_ZONE` (
  `WPP_CODE` varchar(7) DEFAULT NULL COMMENT '정수장 코드',
  `ZONE_IDX` int(11) DEFAULT NULL COMMENT '시설 인덱스',
  `ZONE_CODE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '시설 코드',
  `ZONE_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '시설 이름',
  `DSC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '설명',
  `USE_YN` varchar(1) DEFAULT '1' COMMENT '사용 여부',
  `DCS` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ZONE_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='시설 정보'
```
