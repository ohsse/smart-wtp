package com.hscmt.simulation.program.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QProgram is a Querydsl query type for Program
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QProgram extends EntityPathBase<Program> {

    private static final long serialVersionUID = -1933446545L;

    public static final QProgram program = new QProgram("program");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final StringPath fnlExecId = createString("fnlExecId");

    public final StringPath fnlPdirId = createString("fnlPdirId");

    public final StringPath grpId = createString("grpId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final ListPath<com.hscmt.simulation.program.dto.ProgramArgDto, SimplePath<com.hscmt.simulation.program.dto.ProgramArgDto>> pgmArgs = this.<com.hscmt.simulation.program.dto.ProgramArgDto, SimplePath<com.hscmt.simulation.program.dto.ProgramArgDto>>createList("pgmArgs", com.hscmt.simulation.program.dto.ProgramArgDto.class, SimplePath.class, PathInits.DIRECT2);

    public final StringPath pgmDesc = createString("pgmDesc");

    public final StringPath pgmId = createString("pgmId");

    public final StringPath pgmNm = createString("pgmNm");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final EnumPath<com.hscmt.common.enumeration.YesOrNo> rltmYn = createEnum("rltmYn", com.hscmt.common.enumeration.YesOrNo.class);

    public final EnumPath<com.hscmt.common.enumeration.CycleCd> rpttIntvTypeCd = createEnum("rpttIntvTypeCd", com.hscmt.common.enumeration.CycleCd.class);

    public final NumberPath<Integer> rpttIntvVal = createNumber("rpttIntvVal", Integer.class);

    public final NumberPath<Integer> sortOrd = createNumber("sortOrd", Integer.class);

    public final DateTimePath<java.time.LocalDateTime> strtExecDttm = createDateTime("strtExecDttm", java.time.LocalDateTime.class);

    public final StringPath venvId = createString("venvId");

    public QProgram(String variable) {
        super(Program.class, forVariable(variable));
    }

    public QProgram(Path<? extends Program> path) {
        super(path.getType(), path.getMetadata());
    }

    public QProgram(PathMetadata metadata) {
        super(Program.class, metadata);
    }

}

