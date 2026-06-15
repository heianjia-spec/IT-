# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目：IT 资产管理系统

Vue 3 + Django REST Framework 前后端分离架构的企业 IT 资产全生命周期管理系统。

### 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3 (`<script setup>` SFC), Vite, Element Plus (中文), Pinia, Vue Router, ECharts, Axios, xlsx, qrcode |
| 后端 | Django + Django REST Framework, SimpleJWT, django-mptt, django-filter, django-cors-headers, openpyxl |
| 数据库 | SQLite（开发），可按需切换 MySQL/PostgreSQL |

---

## 项目结构

```
it资产管理系统/
├── frontend/                # Vue 3 SPA 前端
│   ├── src/
│   │   ├── api/             # Axios 接口封装（auth, assets, baseData, dashboard, alerts, users）
│   │   ├── components/
│   │   │   ├── layout/      # AppLayout.vue（侧边栏+顶栏布局壳）
│   │   │   └── assets/      # LabelDialog.vue（标签打印对话框）
│   │   ├── router/          # Vue Router 路由定义 + 导航守卫
│   │   ├── store/           # Pinia store（user.js）
│   │   ├── utils/           # constants.js
│   │   └── views/           # 业务页面（按模块分目录）
│   │       ├── auth/        # 登录页
│   │       ├── dashboard/   # 仪表盘
│   │       ├── assets/      # 资产列表、详情、表单
│   │       ├── baseData/    # 分类、部门、位置、供应商
│   │       ├── alerts/      # 告警规则、日志、邮件配置、模板
│   │       └── settings/    # 用户管理
│   └── vite.config.js       # 含 API 代理配置（/api → 127.0.0.1:9000）
│
├── backend/                 # Django + DRF 后端
│   ├── config/              # Django 项目配置
│   │   ├── settings/
│   │   │   ├── base.py      # 基础设置（DRF/JWT/CORS/分页/过滤）
│   │   │   └── dev.py       # 开发环境覆盖（DEBUG=True, CORS_ALLOW_ALL）
│   │   └── urls.py          # 根路由
│   ├── apps/
│   │   ├── core/            # 共享基础设施
│   │   │   ├── pagination.py    # StandardPagination（默认50条/页）
│   │   │   └── permissions.py   # IsAdmin, IsAdminOrAssetManager, IsAdminOrManagerOrUser
│   │   ├── accounts/        # 用户认证与账号管理
│   │   │   ├── models.py    # User（AbstractUser），角色: admin/asset_manager/user/viewer
│   │   │   ├── serializers.py  # LoginSerializer, UserSerializer, ChangePasswordSerializer
│   │   │   ├── views.py     # LoginView (JWT), MeView, ChangePasswordView, UserViewSet
│   │   │   └── urls.py      # auth/login, auth/refresh, auth/me, auth/users, auth/change-password
│   │   ├── base_data/       # 基础字典（AssetCategory, Department, Location, Supplier）
│   │   │   ├── models.py    # MPTT 树形结构（分类和部门）
│   │   │   └── views.py     # CRUD ViewSet，list 时仅返回根节点
│   │   ├── assets/          # 资产核心 CRUD + 导入导出
│   │   │   ├── models.py    # Asset（统一模型），AssetStatusChange, OperationLog
│   │   │   ├── views.py     # AssetViewSet（含批量删除、导入导出、状态历史、二维码）
│   │   │   ├── serializers.py
│   │   │   ├── filters.py   # AssetFilter（多条件筛选 + 分类级联查询 + 全文搜索）
│   │   │   ├── import_export.py  # Excel 导入导出逻辑（openpyxl）
│   │   │   └── qrcode_utils.py   # 资产二维码生成
│   │   ├── dashboard/       # 仪表盘统计（API 就绪，模型待填充）
│   │   └── alerts/          # 告警规则、告警日志、邮件配置、邮件模板
│   │       └── models.py    # AlertRule, AlertLog, EmailConfig, EmailTemplate（支持变量模板渲染）
│   └── manage.py
│
├── venv/                    # Python 虚拟环境
├── 资产管理系统需求说明书.md  # 项目需求文档
├── 管理端UI规范.md           # Element 风格 UI 规范
├── PRD设计规范.md            # PRD 编写规范
└── 通用组件说明文档规范.md    # 通用组件文档规范
```

---

## 常用命令

### 后端

```bash
# 激活虚拟环境
source venv/Scripts/activate

# 开发服务器（默认 127.0.0.1:9000）
cd backend
python manage.py runserver 0.0.0.0:9000

# 数据库迁移
python manage.py makemigrations && python manage.py migrate

# 初始化种子数据（分类、部门、位置、供应商 + 演示资产）
python manage.py init_data

# 创建超级用户
python manage.py createsuperuser
```

### 前端

```bash
cd frontend
npm run dev        # 开发服务器（默认 localhost:5173，API 代理到 9000）
npm run build      # 生产构建 → dist/
npm run preview    # 预览生产构建
```

### 默认管理员

通过 `createsuperuser` 创建，或使用 `init_data` 后创建。

---

## 架构关键信息

### API 路由

| 前缀 | App | 说明 |
|------|-----|------|
| `/api/auth/` | accounts | 登录、刷新 Token、用户信息、用户 CRUD |
| `/api/assets/` | assets | 资产 CRUD、批量删除、导入导出、状态历史、二维码 |
| `/api/assets/operation-logs/` | assets | 操作日志（只读） |
| `/api/` | base_data | 分类/部门/位置/供应商 CRUD |
| `/api/dashboard/` | dashboard | 仪表盘统计 |
| `/api/` | alerts | 告警规则/日志/邮件配置/模板 |

### 认证

- JWT 认证（SimpleJWT），Access Token 12h，Refresh Token 7d
- 登录接口 `/api/auth/login/` 返回 `access` + `refresh` + `user`
- 前端自动将 Token 存入 localStorage，请求时通过 Axios 拦截器自动携带
- 路由守卫 `router.beforeEach` 检查 Token，未登录跳转 `/login`

### 权限模型（4 角色）

| 角色 | 代码 | 权限 |
|------|------|------|
| 管理员 | `admin` | 全部操作 |
| 资产管理员 | `asset_manager` | 资产/基础数据的增删改 |
| 普通用户 | `user` | 查看 + 资产增删改 |
| 只读用户 | `viewer` | 仅查看 |

权限类位于 `backend/apps/core/permissions.py`：
- `IsAdmin` — 仅管理员可写
- `IsAdminOrAssetManager` — 管理员和资产管理员可写，其他人可读
- `IsAdminOrManagerOrUser` — viewer 只读，其余可写

### Asset 模型设计（统一模型）

采用**单一 Asset 表**存储所有资产类型，通过 `asset_type` 区分：

| 类型 | 枚举值 | 特定字段 |
|------|--------|---------|
| 硬件（服务器/PC） | `server`, `pc` | CPU, 内存, 硬盘, OS, OOB地址, 网卡 |
| 打印机 | `printer` | 打印机类型, 色彩, 双面, 连接方式, 硒鼓型号 |
| 网络设备 | `network_device`, `switch` | 网络类型, 端口类型, PoE, 堆叠, 冗余电源 |
| 软件 | `software` | 软件类型, 版本, 授权类型, 许可证号, 许可到期 |
| 耗材 | `consumable` | 耗材类型, 单位, 当前库存, 最低库存预警, 适用设备 |

关键特性：
- 保存时自动从分类树推导 `asset_type`（`_derive_asset_type()`）
- 保修截止日期过期自动标记 `warranty_status='expired'`
- 资产编号自动生成（格式：`IT-YYYYMMDD-XXXX`）
- 分类筛选支持级联（选父分类自动包含子分类下的资产）
- 状态变更自动记录到 `AssetStatusChange`

### 前端页面路由

```
/login                          → LoginView
/ (AppLayout)                   → 重定向到 /dashboard
  /dashboard                    → DashboardView
  /assets                       → AssetListView
  /assets/add                   → AssetFormView
  /assets/:id                   → AssetDetailView
  /assets/:id/edit              → AssetFormView
  /basic-data/categories        → CategoryView
  /basic-data/departments       → DepartmentView
  /basic-data/locations         → LocationView
  /basic-data/suppliers         → SupplierView
  /notifications/rules          → AlertRuleView
  /notifications/logs           → AlertLogView
  /notifications/email-config   → EmailConfigView
  /notifications/email-template → EmailTemplateView
  /settings/users               → UserManagement
  /settings/operation-logs      → OperationLogView
```

### 默认分页

- 后端 DRF 全局分页：`StandardPagination`，默认 `page_size=50`，最大 200
- 前端表格默认每页 50 条（遵循管理端 UI 规范）

---

## 核心模式与约定

### 后端

1. **配置分离**：`config/settings/base.py` + `dev.py`，生产环境需新增 `prod.py`。`__init__.py` 当前导入 `dev.py`
2. **Apps 路径**：本地 app 在 `apps/` 目录，`sys.path` 已注入，可直接 `import accounts` 而非 `import apps.accounts`
3. **视图**：统一使用 DRF `ModelViewSet` + `@action` 装饰器扩展自定义端点
4. **搜索与过滤**：全局 `DjangoFilterBackend` + `SearchFilter` + `OrderingFilter`，在每个 ViewSet 上按需配置
5. **树形结构**：`AssetCategory` 和 `Department` 使用 `django-mptt`，list 接口只返回根节点（`parent__isnull=True`）
6. **审计日志**：资产的新增/编辑/删除/导入/导出自动记录到 `OperationLog`，记录 IP 地址
7. **序列化器**：列表与详情使用不同序列化器（`AssetListSerializer` vs `AssetSerializer`），优化查询性能

### 前端

1. **SFC 语法**：所有组件使用 `<script setup>` 语法
2. **API 层**：`src/api/index.js` 封装了 Axios 实例，自动注入 `Bearer Token`，401 时自动清除登录态
3. **Element Plus**：全局注册中文 locale，所有图标全局注册（`@element-plus/icons-vue`）
4. **状态管理**：用户信息存储在 `store/user.js`（Pinia）
5. **通用 CRUD 页面**：`views/baseData/CrudPage.vue` 是一个可复用的 CRUD 页面组件，供分类/部门/位置/供应商等基础数据模块使用
6. **查询交互**：所有列表页遵循 `管理端UI规范.md`——点击"查询"按钮才执行查询，不实时过滤

### 前后端对接

- Vite 开发时通过 `proxy` 配置将 `/api` 请求代理到 `http://127.0.0.1:9000`
- 生产环境可使用 Nginx 反向代理，或将前端构建产物放入 Django static 目录
- 二维码中嵌入了前端 URL（`FRONTEND_BASE_URL` 配置项），指向 `localhost:5173`

---

## 待完成事项

- [ ] `requirements.txt` —— 后端尚未有 requirements.txt，需根据 `INSTALLED_APPS` 和 import 语句生成
- [ ] Dashboard 模块 —— 路由已配置但 views 和 models 实现不完整
- [ ] Celery 异步任务 —— 告警模块定义了规则和邮件模板，但缺少异步发送逻辑
- [ ] 生产环境配置 —— 需要 `config/settings/prod.py`，关闭 DEBUG，配置 ALLOWED_HOSTS
- [ ] 单元测试 —— 各 app 的 `tests.py` 均为空

---

## 参考文档

- [资产管理系统需求说明书.md](资产管理系统需求说明书.md)
- [管理端UI规范.md](管理端UI规范.md) — Element 风格 UI 布局、列表页、详情页、选择交互规范
- [PRD设计规范.md](PRD设计规范.md) — PRD 编写标准和模板
- [通用组件说明文档规范.md](通用组件说明文档规范.md) — 通用组件的文档编写规范

## 语言偏好

- **与用户对话使用简体中文**
- 代码、标识符使用英文，向用户解释功能时用中文
