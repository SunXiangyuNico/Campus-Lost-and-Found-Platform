# 校园失物招领平台

一个基于Vue 3 + Element Plus的现代化校园失物招领平台前端应用。

## 功能特性

### 🏠 首页
- **搜索功能**: 支持按物品名称、地点等模糊搜索
- **帖子列表**: 左侧显示所有帖子，支持失物/招领标签区分
- **帖子详情**: 右侧显示选中帖子的详细信息
- **发帖功能**: 支持发布失物或招领信息
- **评论系统**: 支持对帖子进行评论
- **认领功能**: 支持认领失物或联系失主

### 👤 用户系统
- **注册功能**: 支持学号注册，包含昵称、头像、联系方式、学院信息
- **登录功能**: 支持学号密码登录，记住登录状态
- **个人中心**: 查看个人信息，管理历史认领和发布的帖子

### 📱 响应式设计
- 支持桌面端和移动端
- 现代化的UI设计
- 良好的用户体验

## 技术栈

- **前端框架**: Vue 3 (Composition API)
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **路由管理**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios
- **图标**: Element Plus Icons

## 项目结构

```
src/
├── api/                 # API接口
│   ├── auth.js         # 认证相关API
│   └── posts.js        # 帖子相关API
├── components/         # 组件
│   ├── Navbar.vue      # 导航栏
│   ├── PostCard.vue    # 帖子卡片
│   ├── PostDetail.vue  # 帖子详情
│   └── PublishDialog.vue # 发帖对话框
├── stores/             # 状态管理
│   ├── user.js         # 用户状态
│   └── posts.js        # 帖子状态
├── views/              # 页面
│   ├── Home.vue        # 首页
│   ├── Login.vue       # 登录页
│   ├── Register.vue    # 注册页
│   └── Profile.vue     # 个人中心
├── router/             # 路由配置
│   └── index.js
├── App.vue             # 根组件
└── main.js             # 入口文件
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 功能说明

### 用户注册
- 学号：8-12位数字，作为唯一用户名
- 昵称：1-20个字符
- 头像：支持jpg/png格式，最大2MB
- 联系方式：电话或邮箱（可选）
- 学院：学院/系别信息（可选）

### 发帖功能
- 类型选择：失物/招领
- 标题：2-50个字符
- 地点：必填项
- 描述：10-500个字符
- 图片：支持1-5张，每张最大2MB

### 帖子管理
- 查看帖子详情
- 发表评论
- 认领失物/联系失主
- 关闭/删除自己的帖子

## API接口

项目配置的API基础URL为 `http://localhost:8080/api`，需要配合后端服务使用。

### 主要接口
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/profile` - 获取用户信息
- `GET /api/posts` - 获取帖子列表
- `POST /api/posts` - 创建帖子
- `GET /api/posts/:id` - 获取帖子详情
- `POST /api/posts/:id/claim` - 认领帖子
- `POST /api/posts/:id/comments` - 添加评论

## 开发说明

### 环境要求
- Node.js >= 16
- npm >= 8

### 开发规范
- 使用Vue 3 Composition API
- 组件命名采用PascalCase
- 文件命名采用kebab-case
- 使用Element Plus组件库
- 状态管理使用Pinia

### 代码风格
- 使用ESLint进行代码检查
- 使用Prettier进行代码格式化
- 遵循Vue 3官方风格指南

## 部署

### 构建
```bash
npm run build
```

### 部署到服务器
将 `dist` 目录下的文件部署到Web服务器即可。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License 