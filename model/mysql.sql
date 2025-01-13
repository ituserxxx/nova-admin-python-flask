
CREATE TABLE users
(
    id         INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID', -- ID字段，自动递增
    userName   VARCHAR(100) NOT NULL COMMENT '用户名',
    age        INT          default NULL COMMENT '年龄',
    email      VARCHAR(100) default NULL COMMENT '电子邮件',
    gender     INT          DEFAULT 0 COMMENT '性别（0 未知，1 男，2 女）',
    tel        VARCHAR(20)  default NULL COMMENT '联系电话',
    roleId     INT          default 0 COMMENT '角色id',
    status     TINYINT(1)   DEFAULT 1 COMMENT '状态（1 启用，0 禁用）',
    remark     TEXT         default NUL COMMENT '备注',
    createTime DATETIME     NOT NULL COMMENT '创建时间',          -- 创建时间
    creatorId  INT NOT NULL COMMENT '创建人id',           -- 创建人
    updateTime DATETIME     default NULL COMMENT '更新时间'       -- 更新时间
) COMMENT='用户信息表';


CREATE TABLE roles
(
    id         INT AUTO_INCREMENT PRIMARY KEY COMMENT '角色ID', -- 角色ID
    createBy   VARCHAR(100) NOT NULL COMMENT '创建人',           -- 创建人
    createTime DATETIME     NOT NULL COMMENT '创建时间',          -- 创建时间
    updateBy   VARCHAR(100) default NULL COMMENT '更新人',       -- 更新人
    updateTime DATETIME     default NULL COMMENT '更新时间',      -- 更新时间
    `status`   TINYINT(1) default 1 COMMENT '状态（1 启用，0 禁用）',  -- 状态（1 启用，0 禁用）
    roleName   VARCHAR(100) NOT NULL COMMENT '角色名称',          -- 角色名称
    roleCode   VARCHAR(50)  NOT NULL COMMENT '角色编码',          -- 角色编码
    roleDesc   TEXT COMMENT '角色描述'                            -- 角色描述
) COMMENT='角色信息表'; -- 表注释


CREATE TABLE menus
(
    id         INT AUTO_INCREMENT PRIMARY KEY COMMENT '菜单ID',           -- 菜单ID
    createBy   VARCHAR(100) NOT NULL COMMENT '创建人',                     -- 创建人
    createTime DATETIME     NOT NULL COMMENT '创建时间',                    -- 创建时间
    updateBy   VARCHAR(100)          DEFAULT '' COMMENT '更新人',          -- 更新人
    updateTime DATETIME              DEFAULT NULL COMMENT '更新时间',       -- 更新时间
    status     TINYINT(1) DEFAULT 1 COMMENT '状态（1 启用，0 禁用）',            -- 状态（1 启用，0 禁用）
    parentId   INT          NOT NULL DEFAULT 0 COMMENT '父级菜单ID',        -- 父级菜单ID
    menuType   TINYINT(1) NOT NULL COMMENT '菜单类型（1：功能，2：菜单）',           -- 菜单类型（1：功能，2：菜单）
    menuName   VARCHAR(255) NOT NULL COMMENT '菜单名称',                    -- 菜单名称
    routeName  VARCHAR(100) NOT NULL COMMENT '路由名称',                    -- 路由名称
    routePath  VARCHAR(255) NOT NULL COMMENT '路由路径',                    -- 路由路径
    component  VARCHAR(255) NOT NULL COMMENT '组件名称',                    -- 组件名称
    `order`    INT          NOT NULL DEFAULT 0 COMMENT '菜单顺序',          -- 菜单顺序
    i18nKey    VARCHAR(255)          DEFAULT NULL COMMENT '国际化键',       -- 国际化键
    icon       VARCHAR(255)          DEFAULT NULL COMMENT '图标',         -- 图标
    iconType   TINYINT(1) NOT NULL DEFAULT 1 COMMENT '图标类型（1：默认，2：自定义）' -- 图标类型（1：默认，2：自定义）
) COMMENT='菜单信息表'; -- 表注释

CREATE TABLE rela_user_role
(
    id       INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID', -- ID字段，自动递增
    userId   INT         NOT NULL COMMENT '用户ID',           -- 用户ID
    roleId   INT         NOT NULL COMMENT '角色ID',           -- 角色ID
    roleCode VARCHAR(50) NOT NULL COMMENT '角色编码',           -- 角色编码
) COMMENT='关系表-用户角色表'; -- 表注释


CREATE TABLE rela_role_menu
(
    id     INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID', -- ID字段，自动递增
    roleId INT NOT NULL COMMENT '角色ID',                   -- 角色ID
    menuId INT NOT NULL COMMENT '菜单ID',                   -- 菜单ID
) COMMENT='关系表-角色菜单表'; -- 表注释