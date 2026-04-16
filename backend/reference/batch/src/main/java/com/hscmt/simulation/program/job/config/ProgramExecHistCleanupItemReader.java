package com.hscmt.simulation.program.job.config;

import com.hscmt.simulation.program.dto.ProgramExecHistDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.configuration.annotation.StepScope;
import org.springframework.batch.item.*;
import org.springframework.batch.item.database.JdbcCursorItemReader;
import org.springframework.batch.item.database.builder.JdbcCursorItemReaderBuilder;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;

@StepScope
@Component
@RequiredArgsConstructor
@Slf4j
public class ProgramExecHistCleanupItemReader implements ItemStreamReader<ProgramExecHistDto> {
    @Value("#{stepExecutionContext['targetList']}")
    private List<String> targetList;
    @Value("#{jobParameters['startDttm']}")
    private LocalDateTime startDttm;
    @Value("#{jobParameters['endDttm']}")
    private LocalDateTime endDttm;
    @Qualifier("simulationDataSource")
    private final DataSource dataSource;

    private int currentPgmIndex = - 1;

    private JdbcCursorItemReader<ProgramExecHistDto> delegate;

    @Override
    public void open(ExecutionContext executionContext) throws ItemStreamException {
        if (targetList == null || targetList.isEmpty()) return;

        this.currentPgmIndex = 0;
        initDelegateForCurrentPgm();
    }

    private void initDelegateForCurrentPgm() {
        closeCurrentDelegate();

        if (currentPgmIndex < 0 || currentPgmIndex >= targetList.size()) {
            delegate = null;
            return;
        }

        String pgmId = targetList.get(currentPgmIndex);
        String sql =
                "SELECT pgm_id, rslt_dir_id, hist_id " +
                        "FROM pgm_exec_h " +
                        "WHERE pgm_id = ? " +
                        "  AND exec_strt_dttm >= ? " +
                        "  AND exec_strt_dttm <= ? ";

        log.info("[ProgramExecHistItemReader] init delegate. pgmId={}, start={}, end={}",
                pgmId, startDttm, endDttm);

        this.delegate = new JdbcCursorItemReaderBuilder<ProgramExecHistDto>()
                .name("programExecHistReader_" + pgmId)
                .dataSource(dataSource)
                .sql(sql)
                .fetchSize(1000)
                .preparedStatementSetter(ps -> {
                    ps.setString(1, pgmId);
                    ps.setTimestamp(2, Timestamp.valueOf(startDttm));
                    ps.setTimestamp(3, Timestamp.valueOf(endDttm));
                })
                .rowMapper((rs, rowNum) -> {
                    ProgramExecHistDto dto = new ProgramExecHistDto();
                    dto.setPgmId(rs.getString("pgm_id"));
                    dto.setRsltDirId(rs.getString("rslt_dir_id"));
                    dto.setHistId(rs.getString("hist_id"));
                    return dto;
                })
                .build();

        // delegate 자체도 open 필요
        this.delegate.open(new ExecutionContext());
    }

    private void closeCurrentDelegate() {
        if (this.delegate != null) {
            try {
                this.delegate.close();
            } catch (Exception e) {
                log.warn("Error closing delegate reader", e);
            }
        }
    }

    @Override
    public ProgramExecHistDto read() throws Exception {
        // 더 이상 처리할 pgmId가 없으면 끝
        if (delegate == null) {
            return null;
        }

        while (true) {
            ProgramExecHistDto item = delegate.read();
            if (item != null) {
                // ✅ 항상 "한 레코드(= 한 pgmId의 한 이력)"씩 반환
                return item;
            }

            // 현재 pgmId의 데이터가 끝났으면 다음 pgmId로 넘어감
            currentPgmIndex++;
            if (currentPgmIndex >= targetList.size()) {
                // 모든 pgmId 처리 완료 → 전체 read 끝
                closeCurrentDelegate();
                delegate = null;
                return null;
            }

            // 다음 pgmId용 delegate 새로 생성
            initDelegateForCurrentPgm();
            // 그리고 다시 while 한 바퀴 돌면서 read() 계속
        }
    }


    @Override
    public void update(ExecutionContext executionContext) throws ItemStreamException {
        // 재시작(restart) 고려하려면 currentPgmIndex 등을 저장해야 하지만
        // 일단 기본 구현에서는 생략해도 됨.
        if (delegate != null) {
            delegate.update(executionContext);
        }
    }


    @Override
    public void close() throws ItemStreamException {
        closeCurrentDelegate();
    }
}
