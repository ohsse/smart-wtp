package com.hscmt.simulation.program.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QProgramInputFile is a Querydsl query type for ProgramInputFile
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QProgramInputFile extends EntityPathBase<ProgramInputFile> {

    private static final long serialVersionUID = 1917863607L;

    public static final QProgramInputFile programInputFile = new QProgramInputFile("programInputFile");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final StringPath inputFileId = createString("inputFileId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final StringPath pgmId = createString("pgmId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final StringPath trgtId = createString("trgtId");

    public final EnumPath<com.hscmt.common.enumeration.InputFileType> trgtType = createEnum("trgtType", com.hscmt.common.enumeration.InputFileType.class);

    public QProgramInputFile(String variable) {
        super(ProgramInputFile.class, forVariable(variable));
    }

    public QProgramInputFile(Path<? extends ProgramInputFile> path) {
        super(path.getType(), path.getMetadata());
    }

    public QProgramInputFile(PathMetadata metadata) {
        super(ProgramInputFile.class, metadata);
    }

}

