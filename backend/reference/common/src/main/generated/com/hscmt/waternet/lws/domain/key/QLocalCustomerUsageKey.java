package com.hscmt.waternet.lws.domain.key;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QLocalCustomerUsageKey is a Querydsl query type for LocalCustomerUsageKey
 */
@Generated("com.querydsl.codegen.DefaultEmbeddableSerializer")
public class QLocalCustomerUsageKey extends BeanPath<LocalCustomerUsageKey> {

    private static final long serialVersionUID = -524298528L;

    public static final QLocalCustomerUsageKey localCustomerUsageKey = new QLocalCustomerUsageKey("localCustomerUsageKey");

    public final StringPath dmno = createString("dmno");

    public final StringPath stym = createString("stym");

    public QLocalCustomerUsageKey(String variable) {
        super(LocalCustomerUsageKey.class, forVariable(variable));
    }

    public QLocalCustomerUsageKey(Path<? extends LocalCustomerUsageKey> path) {
        super(path.getType(), path.getMetadata());
    }

    public QLocalCustomerUsageKey(PathMetadata metadata) {
        super(LocalCustomerUsageKey.class, metadata);
    }

}

