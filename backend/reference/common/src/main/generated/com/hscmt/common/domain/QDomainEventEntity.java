package com.hscmt.common.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QDomainEventEntity is a Querydsl query type for DomainEventEntity
 */
@Generated("com.querydsl.codegen.DefaultSupertypeSerializer")
public class QDomainEventEntity extends EntityPathBase<DomainEventEntity> {

    private static final long serialVersionUID = -2098131114L;

    public static final QDomainEventEntity domainEventEntity = new QDomainEventEntity("domainEventEntity");

    public final QBaseEntity _super = new QBaseEntity(this);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public QDomainEventEntity(String variable) {
        super(DomainEventEntity.class, forVariable(variable));
    }

    public QDomainEventEntity(Path<? extends DomainEventEntity> path) {
        super(path.getType(), path.getMetadata());
    }

    public QDomainEventEntity(PathMetadata metadata) {
        super(DomainEventEntity.class, metadata);
    }

}

