package com.hscmt.simulation.layer.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QLayerList is a Querydsl query type for LayerList
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QLayerList extends EntityPathBase<LayerList> {

    private static final long serialVersionUID = 1264386637L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QLayerList layerList = new QLayerList("layerList");

    public final com.hscmt.common.domain.QBaseEntity _super = new com.hscmt.common.domain.QBaseEntity(this);

    public final StringPath colorStr = createString("colorStr");

    public final ComparablePath<org.locationtech.jts.geom.Geometry> gmtrVal = createComparable("gmtrVal", org.locationtech.jts.geom.Geometry.class);

    public final com.hscmt.simulation.layer.key.QLayerKey id;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final MapPath<String, Object, SimplePath<Object>> property = this.<String, Object, SimplePath<Object>>createMap("property", String.class, Object.class, SimplePath.class);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public QLayerList(String variable) {
        this(LayerList.class, forVariable(variable), INITS);
    }

    public QLayerList(Path<? extends LayerList> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QLayerList(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QLayerList(PathMetadata metadata, PathInits inits) {
        this(LayerList.class, metadata, inits);
    }

    public QLayerList(Class<? extends LayerList> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.id = inits.isInitialized("id") ? new com.hscmt.simulation.layer.key.QLayerKey(forProperty("id")) : null;
    }

}

