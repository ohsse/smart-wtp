package com.hscmt.simulation.program.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QProgramResult is a Querydsl query type for ProgramResult
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QProgramResult extends EntityPathBase<ProgramResult> {

    private static final long serialVersionUID = 1569380204L;

    public static final QProgramResult programResult = new QProgramResult("programResult");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final EnumPath<com.hscmt.common.enumeration.FileExtension> fileXtns = createEnum("fileXtns", com.hscmt.common.enumeration.FileExtension.class);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final StringPath pgmId = createString("pgmId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final StringPath rsltId = createString("rsltId");

    public final StringPath rsltNm = createString("rsltNm");

    public QProgramResult(String variable) {
        super(ProgramResult.class, forVariable(variable));
    }

    public QProgramResult(Path<? extends ProgramResult> path) {
        super(path.getType(), path.getMetadata());
    }

    public QProgramResult(PathMetadata metadata) {
        super(ProgramResult.class, metadata);
    }

}

