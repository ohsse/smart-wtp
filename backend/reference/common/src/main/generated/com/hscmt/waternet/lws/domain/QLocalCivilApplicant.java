package com.hscmt.waternet.lws.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QLocalCivilApplicant is a Querydsl query type for LocalCivilApplicant
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QLocalCivilApplicant extends EntityPathBase<LocalCivilApplicant> {

    private static final long serialVersionUID = 557460802L;

    public static final QLocalCivilApplicant localCivilApplicant = new QLocalCivilApplicant("localCivilApplicant");

    public final com.hscmt.waternet.common.QBaseEntity _super = new com.hscmt.waternet.common.QBaseEntity(this);

    public final StringPath caappldt = createString("caappldt");

    public final StringPath calrgcd = createString("calrgcd");

    public final StringPath calrgnm = createString("calrgnm");

    public final StringPath camidcd = createString("camidcd");

    public final StringPath camidnm = createString("camidnm");

    public final StringPath cano = createString("cano");

    public final StringPath caprcsrslt = createString("caprcsrslt");

    //inherited
    public final StringPath distrCd = _super.distrCd;

    //inherited
    public final StringPath distrNm = _super.distrNm;

    //inherited
    public final StringPath mgcCd = _super.mgcCd;

    //inherited
    public final StringPath mgcNm = _super.mgcNm;

    public final StringPath prcsdt = createString("prcsdt");

    public final StringPath supdt = createString("supdt");

    public QLocalCivilApplicant(String variable) {
        super(LocalCivilApplicant.class, forVariable(variable));
    }

    public QLocalCivilApplicant(Path<? extends LocalCivilApplicant> path) {
        super(path.getType(), path.getMetadata());
    }

    public QLocalCivilApplicant(PathMetadata metadata) {
        super(LocalCivilApplicant.class, metadata);
    }

}

