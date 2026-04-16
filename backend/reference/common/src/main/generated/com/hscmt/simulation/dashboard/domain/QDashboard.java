package com.hscmt.simulation.dashboard.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QDashboard is a Querydsl query type for Dashboard
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QDashboard extends EntityPathBase<Dashboard> {

    private static final long serialVersionUID = 831160047L;

    public static final QDashboard dashboard = new QDashboard("dashboard");

    public final com.hscmt.common.domain.QBaseEntity _super = new com.hscmt.common.domain.QBaseEntity(this);

    public final StringPath dsbdDesc = createString("dsbdDesc");

    public final StringPath dsbdId = createString("dsbdId");

    public final StringPath dsbdNm = createString("dsbdNm");

    public final StringPath grpId = createString("grpId");

    public final ListPath<com.hscmt.simulation.dashboard.dto.DsbdVisItemDto, SimplePath<com.hscmt.simulation.dashboard.dto.DsbdVisItemDto>> items = this.<com.hscmt.simulation.dashboard.dto.DsbdVisItemDto, SimplePath<com.hscmt.simulation.dashboard.dto.DsbdVisItemDto>>createList("items", com.hscmt.simulation.dashboard.dto.DsbdVisItemDto.class, SimplePath.class, PathInits.DIRECT2);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final NumberPath<Integer> resHglnVal = createNumber("resHglnVal", Integer.class);

    public final NumberPath<Integer> resWidthVal = createNumber("resWidthVal", Integer.class);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final NumberPath<Integer> sortOrd = createNumber("sortOrd", Integer.class);

    public QDashboard(String variable) {
        super(Dashboard.class, forVariable(variable));
    }

    public QDashboard(Path<? extends Dashboard> path) {
        super(path.getType(), path.getMetadata());
    }

    public QDashboard(PathMetadata metadata) {
        super(Dashboard.class, metadata);
    }

}

