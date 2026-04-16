package com.hscmt.simulation.group.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QLayerGroup is a Querydsl query type for LayerGroup
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QLayerGroup extends EntityPathBase<LayerGroup> {

    private static final long serialVersionUID = -54965154L;

    public static final QLayerGroup layerGroup = new QLayerGroup("layerGroup");

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

    public QLayerGroup(String variable) {
        super(LayerGroup.class, forVariable(variable));
    }

    public QLayerGroup(Path<? extends LayerGroup> path) {
        super(path.getType(), path.getMetadata());
    }

    public QLayerGroup(PathMetadata metadata) {
        super(LayerGroup.class, metadata);
    }

}

