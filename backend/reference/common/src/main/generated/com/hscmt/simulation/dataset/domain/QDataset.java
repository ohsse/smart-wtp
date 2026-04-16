package com.hscmt.simulation.dataset.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QDataset is a Querydsl query type for Dataset
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QDataset extends EntityPathBase<Dataset> {

    private static final long serialVersionUID = -1221800977L;

    public static final QDataset dataset = new QDataset("dataset");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final StringPath dsDesc = createString("dsDesc");

    public final StringPath dsId = createString("dsId");

    public final StringPath dsNm = createString("dsNm");

    public final EnumPath<com.hscmt.common.enumeration.FileExtension> fileXtns = createEnum("fileXtns", com.hscmt.common.enumeration.FileExtension.class);

    public final StringPath grpId = createString("grpId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final NumberPath<Integer> sortOrd = createNumber("sortOrd", Integer.class);

    public QDataset(String variable) {
        super(Dataset.class, forVariable(variable));
    }

    public QDataset(Path<? extends Dataset> path) {
        super(path.getType(), path.getMetadata());
    }

    public QDataset(PathMetadata metadata) {
        super(Dataset.class, metadata);
    }

}

