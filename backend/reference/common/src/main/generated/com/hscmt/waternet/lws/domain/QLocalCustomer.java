package com.hscmt.waternet.lws.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QLocalCustomer is a Querydsl query type for LocalCustomer
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QLocalCustomer extends EntityPathBase<LocalCustomer> {

    private static final long serialVersionUID = 2106554641L;

    public static final QLocalCustomer localCustomer = new QLocalCustomer("localCustomer");

    public final com.hscmt.waternet.common.QBaseEntity _super = new com.hscmt.waternet.common.QBaseEntity(this);

    //inherited
    public final StringPath distrCd = _super.distrCd;

    //inherited
    public final StringPath distrNm = _super.distrNm;

    public final StringPath dmaddr = createString("dmaddr");

    public final StringPath dmnm = createString("dmnm");

    public final StringPath dmno = createString("dmno");

    public final StringPath lfcltyNm = createString("lfcltyNm");

    public final StringPath mfcltyNm = createString("mfcltyNm");

    //inherited
    public final StringPath mgcCd = _super.mgcCd;

    //inherited
    public final StringPath mgcNm = _super.mgcNm;

    public final StringPath sfcltyNm = createString("sfcltyNm");

    public final StringPath sgccd = createString("sgccd");

    public QLocalCustomer(String variable) {
        super(LocalCustomer.class, forVariable(variable));
    }

    public QLocalCustomer(Path<? extends LocalCustomer> path) {
        super(path.getType(), path.getMetadata());
    }

    public QLocalCustomer(PathMetadata metadata) {
        super(LocalCustomer.class, metadata);
    }

}

