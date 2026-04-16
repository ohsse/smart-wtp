package com.hscmt.simulation.group.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QGroupBase is a Querydsl query type for GroupBase
 */
@Generated("com.querydsl.codegen.DefaultSupertypeSerializer")
public class QGroupBase extends EntityPathBase<GroupBase> {

    private static final long serialVersionUID = -790310080L;

    public static final QGroupBase groupBase = new QGroupBase("groupBase");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final StringPath grpDesc = createString("grpDesc");

    public final StringPath grpId = createString("grpId");

    public final StringPath grpNm = createString("grpNm");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final NumberPath<Integer> sortOrd = createNumber("sortOrd", Integer.class);

    public final StringPath upGrpId = createString("upGrpId");

    public QGroupBase(String variable) {
        super(GroupBase.class, forVariable(variable));
    }

    public QGroupBase(Path<? extends GroupBase> path) {
        super(path.getType(), path.getMetadata());
    }

    public QGroupBase(PathMetadata metadata) {
        super(GroupBase.class, metadata);
    }

}

