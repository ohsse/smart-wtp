package com.hscmt.simulation.dataset.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QMeasureList is a Querydsl query type for MeasureList
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QMeasureList extends EntityPathBase<MeasureList> {

    private static final long serialVersionUID = 1412722451L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QMeasureList measureList = new QMeasureList("measureList");

    public final com.hscmt.common.domain.QBaseEntity _super = new com.hscmt.common.domain.QBaseEntity(this);

    public final com.hscmt.simulation.dataset.key.QMeasureListKey id;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final NumberPath<java.math.BigDecimal> msrmVal = createNumber("msrmVal", java.math.BigDecimal.class);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public QMeasureList(String variable) {
        this(MeasureList.class, forVariable(variable), INITS);
    }

    public QMeasureList(Path<? extends MeasureList> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QMeasureList(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QMeasureList(PathMetadata metadata, PathInits inits) {
        this(MeasureList.class, metadata, inits);
    }

    public QMeasureList(Class<? extends MeasureList> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.id = inits.isInitialized("id") ? new com.hscmt.simulation.dataset.key.QMeasureListKey(forProperty("id")) : null;
    }

}

