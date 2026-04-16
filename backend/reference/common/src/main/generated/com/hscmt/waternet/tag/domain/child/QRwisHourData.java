package com.hscmt.waternet.tag.domain.child;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QRwisHourData is a Querydsl query type for RwisHourData
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QRwisHourData extends EntityPathBase<RwisHourData> {

    private static final long serialVersionUID = 1337898937L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QRwisHourData rwisHourData = new QRwisHourData("rwisHourData");

    public final com.hscmt.waternet.tag.domain.QRwisData _super;

    // inherited
    public final com.hscmt.waternet.tag.domain.key.QRwisDataKey id;

    //inherited
    public final NumberPath<java.math.BigDecimal> val;

    public QRwisHourData(String variable) {
        this(RwisHourData.class, forVariable(variable), INITS);
    }

    public QRwisHourData(Path<? extends RwisHourData> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QRwisHourData(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QRwisHourData(PathMetadata metadata, PathInits inits) {
        this(RwisHourData.class, metadata, inits);
    }

    public QRwisHourData(Class<? extends RwisHourData> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this._super = new com.hscmt.waternet.tag.domain.QRwisData(type, metadata, inits);
        this.id = _super.id;
        this.val = _super.val;
    }

}

