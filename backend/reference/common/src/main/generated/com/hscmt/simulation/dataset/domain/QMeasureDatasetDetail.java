package com.hscmt.simulation.dataset.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QMeasureDatasetDetail is a Querydsl query type for MeasureDatasetDetail
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QMeasureDatasetDetail extends EntityPathBase<MeasureDatasetDetail> {

    private static final long serialVersionUID = -363973612L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QMeasureDatasetDetail measureDatasetDetail = new QMeasureDatasetDetail("measureDatasetDetail");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final QDataset dataset;

    public final StringPath dsItmId = createString("dsItmId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final NumberPath<Integer> sortOrd = createNumber("sortOrd", Integer.class);

    public final StringPath tagSn = createString("tagSn");

    public QMeasureDatasetDetail(String variable) {
        this(MeasureDatasetDetail.class, forVariable(variable), INITS);
    }

    public QMeasureDatasetDetail(Path<? extends MeasureDatasetDetail> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QMeasureDatasetDetail(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QMeasureDatasetDetail(PathMetadata metadata, PathInits inits) {
        this(MeasureDatasetDetail.class, metadata, inits);
    }

    public QMeasureDatasetDetail(Class<? extends MeasureDatasetDetail> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.dataset = inits.isInitialized("dataset") ? new QDataset(forProperty("dataset")) : null;
    }

}

