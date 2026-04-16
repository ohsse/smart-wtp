package com.hscmt.simulation.group.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QDatasetGroup is a Querydsl query type for DatasetGroup
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QDatasetGroup extends EntityPathBase<DatasetGroup> {

    private static final long serialVersionUID = -73768553L;

    public static final QDatasetGroup datasetGroup = new QDatasetGroup("datasetGroup");

    public final QGroupBase _super = new QGroupBase(this);

    //inherited
    public final StringPath grpDesc = _super.grpDesc;

    //inherited
    public final StringPath grpId = _super.grpId;

    //inherited
    public final StringPath grpNm = _super.grpNm;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    //inherited
    public final NumberPath<Integer> sortOrd = _super.sortOrd;

    //inherited
    public final StringPath upGrpId = _super.upGrpId;

    public QDatasetGroup(String variable) {
        super(DatasetGroup.class, forVariable(variable));
    }

    public QDatasetGroup(Path<? extends DatasetGroup> path) {
        super(path.getType(), path.getMetadata());
    }

    public QDatasetGroup(PathMetadata metadata) {
        super(DatasetGroup.class, metadata);
    }

}

