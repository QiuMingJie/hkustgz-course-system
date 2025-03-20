# HKUST-GZ 课程评价系统

港科广课程评价系统是一个为香港科技大学（广州）学生提供的课程信息和评价平台。学生可以在这里查看课程信息、分享课程体验、获取AI辅导等功能。

## 功能特点

- 课程信息浏览和搜索
- 课程评价和评分系统
- 教师信息查看
- 用户认证（仅限港科广邮箱）
- AI智能助手（新功能）
- 响应式设计，支持移动端访问
- 暗色模式支持

## 环境配置

### 系统要求

- Python 3.8+
- MySQL 5.7+
- Redis (可选，用于缓存)

### 安装步骤

1. 克隆项目并进入目录
```bash
git clone [repository_url]
cd sustech-course-master
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp config/default.py config/development.py
```
编辑 `config/development.py`，设置以下配置：
- 数据库连接信息
- 邮件服务器配置
- AI API密钥（如果使用AI功能）
- 其他必要的配置项

5. 初始化数据库
```bash
flask db upgrade
```

6. 运行开发服务器
```bash
python run.py -d
```

访问 http://127.0.0.1:2021 即可看到网站。

## 项目结构

```
sustech-course-master/
├── app/                    # 应用主目录
│   ├── models/            # 数据模型
│   ├── views/             # 视图函数
│   ├── templates/         # 模板文件
│   ├── static/            # 静态文件
│   └── utils/             # 工具函数
├── config/                # 配置文件
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试文件
└── run.py                 # 启动脚本
```

## 待开发功能

### 1. AI助手功能完善
- [ ] 接入实际的AI API（如OpenAI、文心一言等）
- [ ] 实现聊天历史的数据库存储
- [ ] 添加更多AI功能（课程推荐、学习计划生成等）
- [ ] 优化AI响应的性能和稳定性

### 2. 用户体验优化
- [ ] 实现用户个性化设置
- [ ] 添加课程收藏功能
- [ ] 优化移动端适配
- [ ] 改进搜索功能（支持模糊搜索和高级筛选）

### 3. 社区功能增强
- [ ] 添加用户间私信功能
- [ ] 实现课程讨论区
- [ ] 添加课程资料共享功能
- [ ] 建立教师-学生互动平台

### 4. 系统性能优化
- [ ] 实现缓存机制
- [ ] 优化数据库查询
- [ ] 添加异步任务处理
- [ ] 实现分布式部署支持

### 5. 安全性增强
- [ ] 实现更完善的权限管理
- [ ] 添加操作日志记录
- [ ] 实现敏感信息加密
- [ ] 添加防爬虫措施

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 注意事项

- 确保所有代码更改都经过测试
- 遵循项目的代码风格指南
- 保护用户隐私和数据安全
- 遵守开源协议

## 技术支持

如有问题或建议，请通过以下方式联系我们：
- 提交 Issue
- 发送邮件至：[Jruan189@connect.hkust-gz.edu.cn]
- 访问我们的帮助文档：[docs_url]

## 许可证

本项目采用 [许可证类型] 许可证 - 查看 [LICENSE](LICENSE) 文件了解更多详情。
