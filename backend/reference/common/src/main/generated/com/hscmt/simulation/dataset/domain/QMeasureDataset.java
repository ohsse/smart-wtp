package com.hscmt.simulation.dataset.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QMeasureDataset is a Querydsl query type for MeasureDataset
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QMeasureDataset extends EntityPathBase<MeasureDataset> {

    private static final long serialVersionUID = 1291347427L;

    public static final QMeasureDataset measureDataset = new QMeasureDataset("measureDataset");

    public final QDataset _super = new QDataset(this);

    public final ListPath<MeasureDatasetDetail, QMeasureDatasetDetail> detailItems = this.<MeasureDatasetDetail, QMeasureDatasetDetail>createList("detailItems", MeasureDatasetDetail.class, QMeasureDatasetDetail.class, PathInits.DIRECT2);

    //inherited
    public final StringPath dsDesc = _super.dsDesc;

    //inherited
    public final StringPath dsId = _super.dsId;

    //inherited
    public final StringPath dsNm = _super.dsNm;

    public final DateTimePath<java.time.LocalDateTime> endDttm = createDateTime("endDttm", java.time.LocalDateTime.class);

    //inherited
    public final EnumPath<com.hscmt.common.enumeration.FileExtension> fileXtns = _super.fileXtns;

    //inherited
    public final StringPath grpId = _super.grpId;

    public final NumberPath<Integer> inqyTerm = createNumber("inqyTerm", Integer.class);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final EnumPath<com.hscmt.common.enumeration.YesOrNo> rltmYn = createEnum("rltmYn", com.hscmt.common.enumeration.YesOrNo.class);

    //inherited
    public final NumberPath<Integer> sortOrd = _super.sortOrd;

    public final DateTimePath<java.time.LocalDateTime> strtDttm = createDateTime("strtDttm", java.time.LocalDateTime.class);

    public final EnumPath<com.hscmt.common.enumeration.CycleCd> termTypeCd = createEnum("termTypeCd", com.hscmt.common.enumeration.CycleCd.class);

    public QMeasureDataset(String variable) {
        super(MeasureDataset.class, forVariable(variable));
    }

    public QMeasureDataset(Path<? extends MeasureDataset> path) {
        super(path.getType(), path.getMetadata());
    }

    public QMeasureDataset(PathMetadata metadata) {
        super(MeasureDataset.class, metadata);
    }

}

