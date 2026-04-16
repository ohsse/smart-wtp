package com.hscmt.waternet.tag.domain.key;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QRwisDataKey is a Querydsl query type for RwisDataKey
 */
@Generated("com.querydsl.codegen.DefaultEmbeddableSerializer")
public class QRwisDataKey extends BeanPath<RwisDataKey> {

    private static final long serialVersionUID = -910535891L;

    public static final QRwisDataKey rwisDataKey = new QRwisDataKey("rwisDataKey");

    public final StringPath logTime = createString("logTime");

    public final NumberPath<Long> tagsn = createNumber("tagsn", Long.class);

    public QRwisDataKey(String variable) {
        super(RwisDataKey.class, forVariable(variable));
    }

    public QRwisDataKey(Path<? extends RwisDataKey> path) {
        super(path.getType(), path.getMetadata());
    }

    public QRwisDataKey(PathMetadata metadata) {
        super(RwisDataKey.class, metadata);
    }

}

