package com.hscmt.simulation.program.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QProgramExecHist is a Querydsl query type for ProgramExecHist
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QProgramExecHist extends EntityPathBase<ProgramExecHist> {

    private static final long serialVersionUID = -1276652830L;

    public static final QProgramExecHist programExecHist = new QProgramExecHist("programExecHist");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final StringPath errText = createString("errText");

    public final DateTimePath<java.time.LocalDateTime> execEndDttm = createDateTime("execEndDttm", java.time.LocalDateTime.class);

    public final DateTimePath<java.time.LocalDateTime> execStrtDttm = createDateTime("execStrtDttm", java.time.LocalDateTime.class);

    public final EnumPath<com.hscmt.common.enumeration.ExecStat> execSttsCd = createEnum("execSttsCd", com.hscmt.common.enumeration.ExecStat.class);

    public final EnumPath<com.hscmt.common.enumeration.ExecutionType> execTypeCd = createEnum("execTypeCd", com.hscmt.common.enumeration.ExecutionType.class);

    public final StringPath histId = createString("histId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final StringPath pgmId = createString("pgmId");

    public final StringPath procsId = createString("procsId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final NumberPath<Long> rsltBytes = createNumber("rsltBytes", Long.class);

    public final StringPath rsltDirId = createString("rsltDirId");

    public QProgramExecHist(String variable) {
        super(ProgramExecHist.class, forVariable(variable));
    }

    public QProgramExecHist(Path<? extends ProgramExecHist> path) {
        super(path.getType(), path.getMetadata());
    }

    public QProgramExecHist(PathMetadata metadata) {
        super(ProgramExecHist.class, metadata);
    }

}

