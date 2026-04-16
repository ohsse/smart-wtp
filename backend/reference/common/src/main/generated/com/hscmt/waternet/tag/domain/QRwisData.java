package com.hscmt.waternet.tag.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QRwisData is a Querydsl query type for RwisData
 */
@Generated("com.querydsl.codegen.DefaultSupertypeSerializer")
public class QRwisData extends EntityPathBase<RwisData> {

    private static final long serialVersionUID = 1640525859L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QRwisData rwisData = new QRwisData("rwisData");

    public final com.hscmt.waternet.tag.domain.key.QRwisDataKey id;

    public final NumberPath<java.math.BigDecimal> val = createNumber("val", java.math.BigDecimal.class);

    public QRwisData(String variable) {
        this(RwisData.class, forVariable(variable), INITS);
    }

    public QRwisData(Path<? extends RwisData> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QRwisData(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QRwisData(PathMetadata metadata, PathInits inits) {
        this(RwisData.class, metadata, inits);
    }

    public QRwisData(Class<? extends RwisData> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.id = inits.isInitialized("id") ? new com.hscmt.waternet.tag.domain.key.QRwisDataKey(forProperty("id")) : null;
    }

}

