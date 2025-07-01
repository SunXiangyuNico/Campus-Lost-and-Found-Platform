# **校园失物招领平台 API **





## **A. 基础与约定**





### **A.1 API 版本与基础路径**



- **基础路径 (Base URL):** `/api/v1`
- 所有 API 路径都以此为前缀，以支持未来版本迭代。



### **A.2 认证方式**



对于需要登录才能访问的接口，需要在 HTTP 请求头 (Header) 中加入 `Authorization` 字段。

- **格式:** `Authorization: Bearer <YOUR_JWT_TOKEN>`
- `Token` 在用户登录成功后由 `/api/v1/auth/login` 接口返回。



### **A.3 通用数据模型**



- 所有核心数据模型 (如 User, Item) 均包含以下两个字段：
  - `createdAt` (Date): 资源创建时间。
  - `updatedAt` (Date): 资源最后更新时间。



### **A.4 通用响应状态码**



- `200 OK`: 请求成功。
- `201 Created`: 资源创建成功。
- `400 Bad Request`: 请求语法或参数无效。
- `401 Unauthorized`: 未认证或 Token 无效/过期。
- `403 Forbidden`: 已认证，但无权执行该操作。
- `404 Not Found`: 请求的资源不存在。
- `422 Unprocessable Entity`: 请求内容语义错误 (如违反验证规则)。
- `500 Internal Server Error`: 服务器内部错误。

------



## **1. 认证 (Authentication)**





### **1.1 用户注册**



- **功能:** 创建新用户账户。

- **路径与方法:** `POST /api/v1/auth/register`

- **请求体 (Request Body):**

  JSON

  ```
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```

- **验证规则:**

  - `username`: 必填，2-20个字符。
  - `email`: 必填，必须是合法的邮箱格式。
  - `password`: 必填，至少8个字符。

- **成功响应 (201 Created):** `{ "message": "用户注册成功" }`



### **1.2 用户登录**



- **功能:** 用户登录以获取认证 Token。

- **路径与方法:** `POST /api/v1/auth/login`

- **请求体:**

  JSON

  ```
  {
    "email": "string",
    "password": "string"
  }
  ```

- **成功响应 (200 OK):** `{ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }`

------



## **2. 密码管理 (Password Management)**





### **2.1 请求重置密码**



- **功能:** 用户忘记密码时，输入邮箱申请重置邮件。
- **路径与方法:** `POST /api/v1/auth/forgot-password`
- **请求体:** `{ "email": "user@example.com" }`
- **成功响应 (200 OK):** `{ "message": "如果邮箱存在，重置链接已发送" }`



### **2.2 执行密码重置**



- **功能:** 用户通过邮件中的链接，提交新的密码。

- **路径与方法:** `POST /api/v1/auth/reset-password`

- **请求体:**

  JSON

  ```
  {
    "resetToken": "string",
    "newPassword": "string"
  }
  ```

- **成功响应 (200 OK):** `{ "message": "密码重置成功" }`

------



## **3. 物品 (Items)**





### **3.1 发布新物品**



- **功能:** 发布一个新的失物或拾物信息。

- **认证:** 需要

- **路径与方法:** `POST /api/v1/items`

- **请求体:**

  JSON

  ```
  {
    "title": "string",
    "description": "string",
    "type": "string",         // 'lost' 或 'found'
    "category": "string",     // 如 '电子产品', '证件' 等
    "locationText": "string",
    "eventDate": "date",      // 'YYYY-MM-DD'
    "imageUrl": "string",     // 可选, 先通过 /upload/image 获取
    "coordinates": {          // 可选, 地图选点
      "lat": "number",
      "lng": "number"
    }
  }
  ```

- **验证规则:**

  - `title`: 必填，1-50个字符。
  - `description`: 必填，1-1000个字符。

- **成功响应 (201 Created):** 返回新创建的物品对象。



### **3.2 获取物品列表 (信息墙)**



- **功能:** 分页、筛选、排序获取物品列表。

- **认证:** 不需要

- **路径与方法:** `GET /api/v1/items`

- **查询参数:**

  - `page` (number, 可选, 默认1): 页码。
  - `limit` (number, 可选, 默认10): 每页数量。
  - `type` (string, 可选, 'lost' 或 'found'): 按类型筛选。
  - `category` (string, 可选): 按分类筛选。
  - `sortBy` (string, 可选, 默认 `createdAt`): 排序字段 (`createdAt` 或 `eventDate`)。
  - `direction` (string, 可选, 默认 `desc`): 排序方向 (`asc` 或 `desc`)。

- **成功响应 (200 OK):**

  JSON

  ```
  {
    "totalPages": "number",
    "currentPage": "number",
    "items": [ /* 物品对象数组 */ ]
  }
  ```



### **3.3 搜索物品**



- **功能:** 根据关键词、分类、日期等进行模糊搜索。
- **认证:** 不需要
- **路径与方法:** `GET /api/v1/items/search`
- **查询参数:**
  - `q` (string, 可选): 关键词。
  - `category` (string, 可选): 分类。
  - `startDate` (date, 可选, 'YYYY-MM-DD'): 起始日期。
  - `endDate` (date, 可选, 'YYYY-MM-DD'): 结束日期。
- **成功响应 (200 OK):** 格式同 `3.2 获取物品列表`。



### **3.4 获取单个物品详情**



- **功能:** 查看某一个物品的完整信息。
- **认证:** 不需要
- **路径与方法:** `GET /api/v1/items/:id`
- **成功响应 (200 OK):** 返回单个完整的物品对象，包含发布者信息。



### **3.5 更新物品信息**



- **功能:** 编辑自己发布的物品信息。
- **认证:** 需要 (且为物品发布者)
- **路径与方法:** `PUT /api/v1/items/:id`
- **请求体:** 格式同 `3.1 发布新物品`。
- **成功响应 (200 OK):** 返回更新后的物品对象。



### **3.6 删除物品信息**



- **功能:** 删除自己发布的物品。
- **认证:** 需要 (且为物品发布者)
- **路径与方法:** `DELETE /api/v1/items/:id`
- **成功响应 (200 OK):** `{ "message": "物品删除成功" }`



### **3.7 更新物品状态 (标记为已找回)**



- **功能:** 将物品的状态更新为“已找回”。
- **认证:** 需要 (且为物品发布者)
- **路径与方法:** `PATCH /api/v1/items/:id/status`
- **请求体:** `{ "status": "reclaimed" }`
- **成功响应 (200 OK):** `{ "message": "物品状态更新成功" }`



### **3.8 查看物品的智能匹配结果**



- **功能:** 查看某个“失物”的所有潜在匹配“拾物”项。
- **认证:** 需要 (且为物品发布者)
- **路径与方法:** `GET /api/v1/items/:id/matches`
- **成功响应 (200 OK):** 返回一个匹配到的物品对象数组。

------



## **4. 用户 (Users)**





### **4.1 获取当前用户信息 (个人中心)**



- **功能:** 获取当前登录用户的个人资料。
- **认证:** 需要
- **路径与方法:** `GET /api/v1/users/me`
- **成功响应 (200 OK):** 返回当前用户的对象 (不含密码)。



### **4.2 获取当前用户发布的物品列表**



- **功能:** 在个人中心查看自己发布过的所有物品。
- **认证:** 需要
- **路径与方法:** `GET /api/v1/users/me/items`
- **成功响应 (200 OK):** 格式同 `3.2 获取物品列表`。

------



## **5. 文件上传 (File Upload)**





### **5.1 上传图片**



- **功能:** 上传一张图片，服务器返回图片的URL。
- **认证:** 需要
- **路径与方法:** `POST /api/v1/upload/image`
- **请求头:** `Content-Type: multipart/form-data`
- **请求体:** 表单中包含一个名为 `image` 的文件字段。
- **成功响应 (200 OK):** `{ "imageUrl": "https://..." }`

------



## **6. 消息/私信 (Messages)**





### **6.1 发送私信**



- **功能:** 就某个物品向其发布者发送私信。

- **认证:** 需要

- **路径与方法:** `POST /api/v1/messages`

- **请求体:**

  JSON

  ```
  {
    "recipientId": "string",
    "itemId": "string",
    "content": "string"
  }
  ```

- **成功响应 (201 Created):** `{ "message": "消息发送成功" }`



### **6.2 获取对话列表**



- **功能:** 获取当前用户的所有对话（按联系人分组）。

- **认证:** 需要

- **路径与方法:** `GET /api/v1/messages/conversations`

- **成功响应 (200 OK):**

  JSON

  ```
  [
    {
      "withUser": { "id": "...", "username": "..." },
      "lastMessage": "string",
      "timestamp": "date"
    }
  ]
  ```



### **6.3 获取与某用户的具体对话内容**



- **功能:** 获取与特定用户之间的所有历史消息。

- **认证:** 需要

- **路径与方法:** `GET /api/v1/messages/:userId`

- **成功响应 (200 OK):**

  JSON

  ```
  [
    { "sender": "me | them", "content": "string", "timestamp": "date" }
  ]
  ```

------



## **7. 通知系统 (Notification System)**





### **7.1 获取通知列表**



- **功能:** 获取当前用户的所有通知（新私信、智能匹配提醒）。

- **认证:** 需要

- **路径与方法:** `GET /api/v1/notifications`

- **成功响应 (200 OK):**

  JSON

  ```
  [
    {
      "id": "string",
      "type": "string", // 'new_message' 或 'new_match'
      "content": "string",
      "link": "string", // 点击后跳转的前端路由
      "isRead": "boolean",
      "createdAt": "date"
    }
  ]
  ```



### **7.2 将通知标记为已读**



- **功能:** 将单条通知标记为已读。
- **认证:** 需要
- **路径与方法:** `PATCH /api/v1/notifications/:id`
- **请求体:** `{ "isRead": true }`
- **成功响应 (200 OK):** `{ "message": "操作成功" }`

------



## **8. 地图 (Map)**





### **8.1 获取地图视野内的物品**



- **功能:** 高效获取在指定地图视野内的所有物品标记点。

- **认证:** 不需要

- **路径与方法:** `GET /api/v1/map/items`

- **查询参数:**

  - `ne_lat`, `ne_lng`: 地图东北角坐标。
  - `sw_lat`, `sw_lng`: 地图西南角坐标。

- **成功响应 (200 OK):**

  JSON

  ```
  [
    {
      "id": "string",
      "title": "string",
      "type": "string", // 'lost' 或 'found'
      "coordinates": { "lat": "number", "lng": "number" }
    }
  ]
  ```