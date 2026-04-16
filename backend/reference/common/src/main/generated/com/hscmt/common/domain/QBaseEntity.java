package com.hscmt.common.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QBaseEntity is a Querydsl query type for BaseEntity
 */
@Generated("com.querydsl.codegen.DefaultSupertypeSerializer")
public class QBaseEntity extends EntityPathBase<BaseEntity> {

    private static final long serialVersionUID = -2070305513L;

    public static final QBaseEntity baseEntity = new QBaseEntity("baseEntity");

    public final DateTimePath<java.time.LocalDateTime> mdfDttm = createDateTime("mdfDttm", java.time.LocalDateTime.class);

    public final StringPath mdfId = createString("mdfId");

    public final DateTimePath<java.time.LocalDateTime> rgstDttm = createDateTime("rgstDttm", java.time.LocalDateTime.class);

    public final StringPath rgstId = createString("rgstId");

    public QBaseEntity(String variable) {
        super(BaseEntity.class, forVariable(variable));
    }

    public QBaseEntity(Path<? extends BaseEntity> path) {
        super(path.getType(), path.getMetadata());
    }

    public QBaseEntity(PathMetadata metadata) {
        super(BaseEntity.class, metadata);
    }

}

