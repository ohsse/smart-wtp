package com.hscmt.simulation.dataset.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QWaternetTag is a Querydsl query type for WaternetTag
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QWaternetTag extends EntityPathBase<WaternetTag> {

    private static final long serialVersionUID = 21837963L;

    public static final QWaternetTag waternetTag = new QWaternetTag("waternetTag");

    public final com.hscmt.common.domain.QBaseEntity _super = new com.hscmt.common.domain.QBaseEntity(this);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final StringPath tagDesc = createString("tagDesc");

    public final StringPath tagSeCd = createString("tagSeCd");

    public final StringPath tagSn = createString("tagSn");

    public final EnumPath<com.hscmt.common.enumeration.YesOrNo> useYn = createEnum("useYn", com.hscmt.common.enumeration.YesOrNo.class);

    public QWaternetTag(String variable) {
        super(WaternetTag.class, forVariable(variable));
    }

    public QWaternetTag(Path<? extends WaternetTag> path) {
        super(path.getType(), path.getMetadata());
    }

    public QWaternetTag(PathMetadata metadata) {
        super(WaternetTag.class, metadata);
    }

}

