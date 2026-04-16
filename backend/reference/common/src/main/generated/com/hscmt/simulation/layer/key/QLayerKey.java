package com.hscmt.simulation.layer.key;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QLayerKey is a Querydsl query type for LayerKey
 */
@Generated("com.querydsl.codegen.DefaultEmbeddableSerializer")
public class QLayerKey extends BeanPath<LayerKey> {

    private static final long serialVersionUID = 110587813L;

    public static final QLayerKey layerKey = new QLayerKey("layerKey");

    public final NumberPath<Long> fid = createNumber("fid", Long.class);

    public final EnumPath<com.hscmt.common.enumeration.FeatureType> ftype = createEnum("ftype", com.hscmt.common.enumeration.FeatureType.class);

    public final StringPath layerId = createString("layerId");

    public QLayerKey(String variable) {
        super(LayerKey.class, forVariable(variable));
    }

    public QLayerKey(Path<? extends LayerKey> path) {
        super(path.getType(), path.getMetadata());
    }

    public QLayerKey(PathMetadata metadata) {
        super(LayerKey.class, metadata);
    }

}

