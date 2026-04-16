package com.hscmt.waternet.tag.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QIfTag is a Querydsl query type for IfTag
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QIfTag extends EntityPathBase<IfTag> {

    private static final long serialVersionUID = -763946029L;

    public static final QIfTag ifTag = new QIfTag("ifTag");

    public final StringPath tagAlias = createString("tagAlias");

    public final StringPath tagDesc = createString("tagDesc");

    public final StringPath tagSeCd = createString("tagSeCd");

    public final StringPath tagSn = createString("tagSn");

    public final EnumPath<com.hscmt.common.enumeration.YesOrNo> useYn = createEnum("useYn", com.hscmt.common.enumeration.YesOrNo.class);

    public QIfTag(String variable) {
        super(IfTag.class, forVariable(variable));
    }

    public QIfTag(Path<? extends IfTag> path) {
        super(path.getType(), path.getMetadata());
    }

    public QIfTag(PathMetadata metadata) {
        super(IfTag.class, metadata);
    }

}

