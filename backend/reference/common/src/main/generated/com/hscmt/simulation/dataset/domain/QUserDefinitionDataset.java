package com.hscmt.simulation.dataset.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QUserDefinitionDataset is a Querydsl query type for UserDefinitionDataset
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QUserDefinitionDataset extends EntityPathBase<UserDefinitionDataset> {

    private static final long serialVersionUID = -1713290671L;

    public static final QUserDefinitionDataset userDefinitionDataset = new QUserDefinitionDataset("userDefinitionDataset");

    public final QDataset _super = new QDataset(this);

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

    public QUserDefinitionDataset(String variable) {
        super(UserDefinitionDataset.class, forVariable(variable));
    }

    public QUserDefinitionDataset(Path<? extends UserDefinitionDataset> path) {
        super(path.getType(), path.getMetadata());
    }

    public QUserDefinitionDataset(PathMetadata metadata) {
        super(UserDefinitionDataset.class, metadata);
    }

}

