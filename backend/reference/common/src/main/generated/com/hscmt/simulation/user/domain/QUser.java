package com.hscmt.simulation.user.domain;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QUser is a Querydsl query type for User
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QUser extends EntityPathBase<User> {

    private static final long serialVersionUID = -1265129475L;

    public static final QUser user = new QUser("user");

    public final com.hscmt.common.domain.QBaseEntity _super = new com.hscmt.common.domain.QBaseEntity(this);

    public final EnumPath<com.hscmt.common.enumeration.AuthCd> authCd = createEnum("authCd", com.hscmt.common.enumeration.AuthCd.class);

    //inherited
    public final DateTimePath<java.time.LocalDateTime> mdfDttm = _super.mdfDttm;

    //inherited
    public final StringPath mdfId = _super.mdfId;

    public final StringPath rftkVal = createString("rftkVal");

    //inherited
    public final DateTimePath<java.time.LocalDateTime> rgstDttm = _super.rgstDttm;

    //inherited
    public final StringPath rgstId = _super.rgstId;

    public final StringPath saltKey = createString("saltKey");

    public final StringPath userEmail = createString("userEmail");

    public final StringPath userId = createString("userId");

    public final StringPath userMblno = createString("userMblno");

    public final StringPath userNm = createString("userNm");

    public final StringPath userPwd = createString("userPwd");

    public final StringPath userTelno = createString("userTelno");

    public QUser(String variable) {
        super(User.class, forVariable(variable));
    }

    public QUser(Path<? extends User> path) {
        super(path.getType(), path.getMetadata());
    }

    public QUser(PathMetadata metadata) {
        super(User.class, metadata);
    }

}

