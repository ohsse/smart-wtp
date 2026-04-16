package com.hscmt.waternet.wro.domain.key;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QWideUsageCustomerKey is a Querydsl query type for WideUsageCustomerKey
 */
@Generated("com.querydsl.codegen.DefaultEmbeddableSerializer")
public class QWideUsageCustomerKey extends BeanPath<WideUsageCustomerKey> {

    private static final long serialVersionUID = 768698726L;

    public static final QWideUsageCustomerKey wideUsageCustomerKey = new QWideUsageCustomerKey("wideUsageCustomerKey");

    public final StringPath fcltyMrnrNo = createString("fcltyMrnrNo");

    public final StringPath mrnrNo = createString("mrnrNo");

    public final StringPath useYm = createString("useYm");

    public QWideUsageCustomerKey(String variable) {
        super(WideUsageCustomerKey.class, forVariable(variable));
    }

    public QWideUsageCustomerKey(Path<? extends WideUsageCustomerKey> path) {
        super(path.getType(), path.getMetadata());
    }

    public QWideUsageCustomerKey(PathMetadata metadata) {
        super(WideUsageCustomerKey.class, metadata);
    }

}

