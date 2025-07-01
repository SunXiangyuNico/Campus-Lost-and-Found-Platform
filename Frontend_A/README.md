# Frontend_A - Campus Lost and Found Platform

## 项目简介

Frontend_A 是失物招领平台的前端项目，基于 Vue 3、Vite 和 Element Plus，提供用户注册、登录、个人中心、物品信息展示与管理等功能。

## 技术栈
- **Vue 3**：渐进式 JavaScript 框架
- **Vite**：极速前端构建工具
- **Element Plus**：UI 组件库
- **Vue Router 4**：路由管理
- **Pinia**：状态管理
- **Axios**：HTTP 客户端

## 目录结构
```
Frontend_A/
├── index.html              # 入口 HTML
├── package.json            # 项目依赖与脚本
├── vite.config.js          # Vite 配置
├── src/
│   ├── api/                # API 请求封装
│   ├── components/         # 公共组件（Navbar、ItemCard、Uploader 等）
│   ├── views/              # 页面视图（Home、Login、Register、UserProfile 等）
│   ├── router/             # 路由配置
│   ├── store/              # Pinia 状态管理
│   ├── App.vue             # 根组件
│   └── main.js             # 应用入口
```

## 主要功能
- 用户注册、登录、登出
- 个人信息管理
- 物品信息的发布、浏览、搜索
- 图片上传
- 路由与权限控制
- 响应式 UI 设计

## 快速开始
### 环境要求
- Node.js >= 16.0.0
- npm >= 8.0.0

### 安装依赖
```bash
npm install
```

### 启动开发环境
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

## 重要目录与文件说明
- `src/api/`：封装所有与后端交互的 API 方法
- `src/components/`：复用型 UI 组件（如 Navbar、Uploader、ItemCard 等）
- `src/views/`：页面级组件（如首页、登录、注册、个人中心等）
- `src/router/`：路由定义与守卫
- `src/store/`：用户状态管理（Pinia）
- `vite.config.js`：开发服务器代理配置，API 请求自动转发到后端

## API 约定
- 用户相关：`/api/auth/*`
- 物品相关：`/api/items/*`
- 详见 `src/api/` 目录下实现

## 许可证
MIT License 