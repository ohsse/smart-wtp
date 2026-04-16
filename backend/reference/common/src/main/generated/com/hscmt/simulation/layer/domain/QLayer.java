package com.hscmt.simulation.layer.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QLayer is a Querydsl query type for Layer
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QLayer extends EntityPathBase<Layer> {

    private static final long serialVersionUID = -1431569137L;

    public static final QLayer layer = new QLayer("layer");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    public final EnumPath<com.hscmt.common.enumeration.CrsyType> crsyTypeCd = createEnum("crsyTypeCd", com.hscmt.common.enumeration.CrsyType.class);

    public final StringPath grpId = createString("grpId");

    public final EnumPath<com.hscmt.common.enumeration.YesOrNo> initDspyYn = createEnum("initDspyYn", com.hscmt.common.enumeration.YesOrNo.class);

    public final StringPath layerDesc = createString("layerDesc");

    public final EnumPath<com.hscmt.common.enumeration.FeatureType> layerFtype = createEnum("layerFtype", com.hscmt.common.enumeration.FeatureType.class);

    public final StringPath layerId = createString("layerId");

    public final StringPath layerNm = createString("layerNm");

    public final ListPath<com.hscmt.simulation.layer.dto.LayerStyleInfo, SimplePath<com.hscmt.simulation.layer.dto.LayerStyleInfo>> layerStyles = this.<com.hscmt.simulation.layer.dto.LayerStyleInfo, SimplePath<com.hscmt.simulation.layer.dto.LayerStyleInfo>>createList("layerStyles", com.hscmt.simulation.layer.dto.LayerStyleInfo.class, SimplePath.class, PathInits.DIRECT2);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final ListPath<String, StringPath> properties = this.<String, StringPath>createList("properties", String.class, StringPath.class, PathInits.DIRECT2);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final NumberPath<Integer> sortOrd = createNumber("sortOrd", Integer.class);

    public final EnumPath<com.hscmt.common.enumeration.YesOrNo> useAbleYn = createEnum("useAbleYn", com.hscmt.common.enumeration.YesOrNo.class);

    public QLayer(String variable) {
        super(Layer.class, forVariable(variable));
    }

    public QLayer(Path<? extends Layer> path) {
        super(path.getType(), path.getMetadata());
    }

    public QLayer(PathMetadata metadata) {
        super(Layer.class, metadata);
    }

}

