package com.hscmt.waternet.wro.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QWideCustomerUsage is a Querydsl query type for WideCustomerUsage
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QWideCustomerUsage extends EntityPathBase<WideCustomerUsage> {

    private static final long serialVersionUID = -620288564L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QWideCustomerUsage wideCustomerUsage = new QWideCustomerUsage("wideCustomerUsage");

    public final com.hscmt.waternet.common.QBaseEntity _super = new com.hscmt.waternet.common.QBaseEntity(this);

    public final StringPath cntrctStatEndDe = createString("cntrctStatEndDe");

    public final StringPath cntrctStatStrtDe = createString("cntrctStatStrtDe");

    public final StringPath cstmrNm = createString("cstmrNm");

    public final StringPath cstmrNo = createString("cstmrNo");

    //inherited
    public final StringPath distrCd = _super.distrCd;

    //inherited
    public final StringPath distrNm = _super.distrNm;

    public final com.hscmt.waternet.wro.domain.key.QWideUsageCustomerKey key;

    //inherited
    public final StringPath mgcCd = _super.mgcCd;

    //inherited
    public final StringPath mgcNm = _super.mgcNm;

    public final NumberPath<Double> mtUsgqty = createNumber("mtUsgqty", Double.class);

    public final StringPath oriCntrctStatEndDe = createString("oriCntrctStatEndDe");

    public final StringPath oriCntrctStatStrtDe = createString("oriCntrctStatStrtDe");

    public QWideCustomerUsage(String variable) {
        this(WideCustomerUsage.class, forVariable(variable), INITS);
    }

    public QWideCustomerUsage(Path<? extends WideCustomerUsage> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QWideCustomerUsage(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QWideCustomerUsage(PathMetadata metadata, PathInits inits) {
        this(WideCustomerUsage.class, metadata, inits);
    }

    public QWideCustomerUsage(Class<? extends WideCustomerUsage> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.key = inits.isInitialized("key") ? new com.hscmt.waternet.wro.domain.key.QWideUsageCustomerKey(forProperty("key")) : null;
    }

}

