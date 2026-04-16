package com.hscmt.waternet.tag.domain.child;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QRwisMinuteData is a Querydsl query type for RwisMinuteData
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QRwisMinuteData extends EntityPathBase<RwisMinuteData> {

    private static final long serialVersionUID = -1067845335L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QRwisMinuteData rwisMinuteData = new QRwisMinuteData("rwisMinuteData");

    public final com.hscmt.waternet.tag.domain.QRwisData _super;

    // inherited
    public final com.hscmt.waternet.tag.domain.key.QRwisDataKey id;

    //inherited
    public final NumberPath<java.math.BigDecimal> val;

    public QRwisMinuteData(String variable) {
        this(RwisMinuteData.class, forVariable(variable), INITS);
    }

    public QRwisMinuteData(Path<? extends RwisMinuteData> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QRwisMinuteData(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QRwisMinuteData(PathMetadata metadata, PathInits inits) {
        this(RwisMinuteData.class, metadata, inits);
    }

    public QRwisMinuteData(Class<? extends RwisMinuteData> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this._super = new com.hscmt.waternet.tag.domain.QRwisData(type, metadata, inits);
        this.id = _super.id;
        this.val = _super.val;
    }

}

