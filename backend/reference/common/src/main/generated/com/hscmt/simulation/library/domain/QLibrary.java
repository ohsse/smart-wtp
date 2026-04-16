package com.hscmt.simulation.library.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QLibrary is a Querydsl query type for Library
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QLibrary extends EntityPathBase<Library> {

    private static final long serialVersionUID = 288087439L;

    public static final QLibrary library = new QLibrary("library");

    public final com.hscmt.common.domain.QBaseEntity _super = new com.hscmt.common.domain.QBaseEntity(this);

    public final StringPath lbrId = createString("lbrId");

    public final StringPath lbrNm = createString("lbrNm");

    public final StringPath lbrVrsn = createString("lbrVrsn");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final StringPath ortxFileNm = createString("ortxFileNm");

    public final StringPath pyVrsn = createString("pyVrsn");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public QLibrary(String variable) {
        super(Library.class, forVariable(variable));
    }

    public QLibrary(Path<? extends Library> path) {
        super(path.getType(), path.getMetadata());
    }

    public QLibrary(PathMetadata metadata) {
        super(Library.class, metadata);
    }

}

