package com.hscmt.simulation.dataset.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QPipeNetworkDataset is a Querydsl query type for PipeNetworkDataset
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QPipeNetworkDataset extends EntityPathBase<PipeNetworkDataset> {

    private static final long serialVersionUID = -1484132383L;

    public static final QPipeNetworkDataset pipeNetworkDataset = new QPipeNetworkDataset("pipeNetworkDataset");

    public final QDataset _super = new QDataset(this);

    public final EnumPath<com.hscmt.common.enumeration.CrsyType> crsyTypeCd = createEnum("crsyTypeCd", com.hscmt.common.enumeration.CrsyType.class);

    //inherited
    public final StringPath dsDesc = _super.dsDesc;

    //inherited
    public final StringPath dsId = _super.dsId;

    //inherited
    public final StringPath dsNm = _super.dsNm;

    //inherited
    public final EnumPath<com.hscmt.common.enumeration.FileExtension> fileXtns = _super.fileXtns;

    //inherited
    public final StringPath grpId = _super.grpId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    //inherited
    public final NumberPath<Integer> sortOrd = _super.sortOrd;

    public QPipeNetworkDataset(String variable) {
        super(PipeNetworkDataset.class, forVariable(variable));
    }

    public QPipeNetworkDataset(Path<? extends PipeNetworkDataset> path) {
        super(path.getType(), path.getMetadata());
    }

    public QPipeNetworkDataset(PathMetadata metadata) {
        super(PipeNetworkDataset.class, metadata);
    }

}

