package com.hscmt.simulation.program.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QProgramVisualization is a Querydsl query type for ProgramVisualization
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QProgramVisualization extends EntityPathBase<ProgramVisualization> {

    private static final long serialVersionUID = -437813515L;

    public static final QProgramVisualization programVisualization = new QProgramVisualization("programVisualization");

    public final com.hscmt.common.domain.QDomainEventEntity _super = new com.hscmt.common.domain.QDomainEventEntity(this);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final StringPath pgmId = createString("pgmId");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final StringPath visId = createString("visId");

    public final StringPath visNm = createString("visNm");

    public final SimplePath<com.hscmt.simulation.program.dto.vis.VisSetupItem> visSetupText = createSimple("visSetupText", com.hscmt.simulation.program.dto.vis.VisSetupItem.class);

    public final EnumPath<com.hscmt.common.enumeration.VisTypeCd> visTypeCd = createEnum("visTypeCd", com.hscmt.common.enumeration.VisTypeCd.class);

    public QProgramVisualization(String variable) {
        super(ProgramVisualization.class, forVariable(variable));
    }

    public QProgramVisualization(Path<? extends ProgramVisualization> path) {
        super(path.getType(), path.getMetadata());
    }

    public QProgramVisualization(PathMetadata metadata) {
        super(ProgramVisualization.class, metadata);
    }

}

