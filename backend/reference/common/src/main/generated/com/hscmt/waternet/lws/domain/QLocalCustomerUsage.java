package com.hscmt.waternet.lws.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QLocalCustomerUsage is a Querydsl query type for LocalCustomerUsage
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QLocalCustomerUsage extends EntityPathBase<LocalCustomerUsage> {

    private static final long serialVersionUID = 1075451664L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QLocalCustomerUsage localCustomerUsage = new QLocalCustomerUsage("localCustomerUsage");

    public final com.hscmt.waternet.lws.domain.key.QLocalCustomerUsageKey key;

    public final StringPath oriStym = createString("oriStym");

    public final NumberPath<Double> wsstvol = createNumber("wsstvol", Double.class);

    public final NumberPath<Double> wsusevol = createNumber("wsusevol", Double.class);

    public QLocalCustomerUsage(String variable) {
        this(LocalCustomerUsage.class, forVariable(variable), INITS);
    }

    public QLocalCustomerUsage(Path<? extends LocalCustomerUsage> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QLocalCustomerUsage(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QLocalCustomerUsage(PathMetadata metadata, PathInits inits) {
        this(LocalCustomerUsage.class, metadata, inits);
    }

    public QLocalCustomerUsage(Class<? extends LocalCustomerUsage> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.key = inits.isInitialized("key") ? new com.hscmt.waternet.lws.domain.key.QLocalCustomerUsageKey(forProperty("key")) : null;
    }

}

