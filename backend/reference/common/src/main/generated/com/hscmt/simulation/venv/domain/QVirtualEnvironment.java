package com.hscmt.simulation.venv.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QVirtualEnvironment is a Querydsl query type for VirtualEnvironment
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QVirtualEnvironment extends EntityPathBase<VirtualEnvironment> {

    private static final long serialVersionUID = 1756931238L;

    public static final QVirtualEnvironment virtualEnvironment = new QVirtualEnvironment("virtualEnvironment");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final StringPath pyVrsn = createString("pyVrsn");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final EnumPath<com.hscmt.common.enumeration.YesOrNo> useAbleYn = createEnum("useAbleYn", com.hscmt.common.enumeration.YesOrNo.class);

    public final StringPath venvDesc = createString("venvDesc");

    public final StringPath venvId = createString("venvId");

    public final StringPath venvNm = createString("venvNm");

    public QVirtualEnvironment(String variable) {
        super(VirtualEnvironment.class, forVariable(variable));
    }

    public QVirtualEnvironment(Path<? extends VirtualEnvironment> path) {
        super(path.getType(), path.getMetadata());
    }

    public QVirtualEnvironment(PathMetadata metadata) {
        super(VirtualEnvironment.class, metadata);
    }

}

