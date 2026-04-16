package com.hscmt.simulation.dataset.key;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QMeasureListKey is a Querydsl query type for MeasureListKey
 */
@Generated("com.querydsl.codegen.DefaultEmbeddableSerializer")
public class QMeasureListKey extends BeanPath<MeasureListKey> {

    private static final long serialVersionUID = -1399437453L;

    public static final QMeasureListKey measureListKey = new QMeasureListKey("measureListKey");

    public final DateTimePath<java.time.LocalDateTime> msrmDttm = createDateTime("msrmDttm", java.time.LocalDateTime.class);

    public final StringPath tagSn = createString("tagSn");

    public QMeasureListKey(String variable) {
        super(MeasureListKey.class, forVariable(variable));
    }

    public QMeasureListKey(Path<? extends MeasureListKey> path) {
        super(path.getType(), path.getMetadata());
    }

    public QMeasureListKey(PathMetadata metadata) {
        super(MeasureListKey.class, metadata);
    }

}

