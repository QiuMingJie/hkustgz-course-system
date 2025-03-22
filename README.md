# HKUST-GZ 课程评价系统

港科广课程评价系统是一个为香港科技大学（广州）学生提供的课程信息和评价平台。学生可以在这里查看课程信息、分享课程体验、获取AI辅导等功能。本系统提供了类似RateMyProfessors的界面风格，让用户可以快速了解课程评价情况。

## 功能特点

- 课程信息浏览和搜索（按课程名称、教师、类别等）
- 课程评价和评分系统（课程难度、作业多少、给分好坏、收获大小）
- 教师信息查看和评价
- 用户认证（仅限港科广邮箱）
- AI智能助手（基于大语言模型的辅导功能）
- 响应式设计，支持移动端访问
- 分段式进度条的可视化课程评价

## 环境配置

### 系统要求

- Python 3.8+
- SQLite（开发环境）或 MySQL 5.7+（生产环境）
- 虚拟环境（推荐使用venv或conda）

### 安装步骤

1. 克隆项目并进入目录
```bash
git clone https://github.com/yourusername/hkustgz-course.git
cd hkustgz-course
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

4. 配置环境变量（可选）
如果需要更改默认配置，可以编辑 `app/config/default.py`

5. 初始化数据库
```bash
# 在项目根目录执行
python -c "from app import db; db.create_all()"
# 或使用初始化脚本创建带有测试数据的数据库
python init_db.py
```

6. 创建管理员账户
```bash
python scripts/create_admin.py
```

7. 运行开发服务器
```bash
python run.py -d
```

访问 http://127.0.0.1:2021 即可看到网站。

## 数据爬取与导入

系统可以从香港科技大学（广州）的课程系统自动爬取课程数据。遵循以下步骤：

1. 运行爬虫脚本爬取课程数据到CSV文件
```bash
python scripts/crawl_courses.py
```
这将从学校官网爬取课程信息并保存到 `data/courses_YYYY-MM-DD.csv` 文件中。

2. 导入爬取的课程数据到系统
```bash
python scripts/import_courses.py data/courses_YYYY-MM-DD.csv
```

爬虫会自动处理以下信息：
- 课程基本信息（课程名称、代码、学分等）
- 教师信息
- 课程描述
- 学期信息
- 课程类别

## 生产环境部署

### 使用Gunicorn和Nginx部署

1. 安装Gunicorn
```bash
pip install gunicorn
```

2. 创建Gunicorn服务配置文件（示例：/etc/systemd/system/hkustgz-course.service）
```
[Unit]
Description=HKUSTGZ Course Evaluation Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/hkustgz-course
ExecStart=/path/to/hkustgz-course/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 run:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

3. 配置Nginx（示例：/etc/nginx/sites-available/hkustgz-course）
```
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/hkustgz-course/app/static;
    }
}
```

4. 启动服务
```bash
sudo systemctl start hkustgz-course
sudo systemctl enable hkustgz-course
sudo systemctl restart nginx
```

### 使用Docker部署（可选）

1. 在项目根目录创建Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 2021

CMD ["python", "run.py"]
```

2. 构建并运行Docker容器
```bash
docker build -t hkustgz-course .
docker run -d -p 2021:2021 hkustgz-course
```

## 项目结构

```
hkustgz-course/
├── app/                    # 应用主目录
│   ├── models/            # 数据模型定义
│   │   ├── course.py      # 课程相关模型
│   │   ├── user.py        # 用户相关模型
│   │   ├── review.py      # 评价相关模型
│   │   └── ...
│   ├── views/             # 视图函数（路由和控制器）
│   │   ├── home.py        # 主页和通用视图
│   │   ├── course.py      # 课程相关视图
│   │   ├── review.py      # 评价相关视图
│   │   ├── ai.py          # AI助手相关视图
│   │   └── ...
│   ├── templates/         # HTML模板
│   ├── static/            # 静态文件（CSS、JS、图片等）
│   │   ├── css/           # 样式表
│   │   ├── js/            # JavaScript文件
│   │   └── image/         # 图片资源
│   ├── utils.py           # 工具函数
│   └── __init__.py        # 应用初始化
├── scripts/               # 实用脚本
│   ├── crawl_courses.py   # 爬取课程数据
│   ├── import_courses.py  # 导入课程数据
│   ├── create_admin.py    # 创建管理员账户
│   └── ...
├── data/                  # 数据文件（CSV等）
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试文件
├── init_db.py             # 数据库初始化脚本
├── run.py                 # 应用启动脚本
└── requirements.txt       # 依赖包列表
```

## 数据库架构

系统主要数据模型包括：

1. **User** - 用户信息
   - 普通用户（学生）
   - 管理员
   - 教师

2. **Course** - 课程基本信息
   - 名称、代码、描述等
   - 与教师的多对多关系

3. **CourseTerm** - 课程学期信息
   - 学分、课时、学期等

4. **CourseRate** - 课程评分汇总
   - 平均分、难度、作业量等

5. **Review** - 用户评价
   - 内容、评分、难度评价等

6. **Teacher** - 教师信息
   - 姓名、所属院系等

## 社区规范与贡献指南

### 行为准则

1. **尊重与包容** - 尊重所有用户和贡献者，不得发表歧视、侮辱或攻击性言论。
2. **诚实与客观** - 提供诚实、客观的课程评价，避免情绪化或不公平的评价。
3. **保护隐私** - 不得分享他人个人信息或未经授权的课程资料。
4. **学术诚信** - 不得使用平台协助作弊或违反学术诚信原则。

### 评价指南

1. **内容相关性** - 评价应与课程内容、教学质量和学习体验相关。
2. **具体详细** - 提供具体细节和实例，避免过于笼统的评价。
3. **建设性意见** - 即使是负面评价也应提供建设性的反馈。
4. **适当语言** - 使用得体的语言表达观点，避免粗俗或过激言论。

### 贡献代码

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/YourFeature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/YourFeature`)
5. 提交 Pull Request

### 报告问题

如发现系统问题，请通过GitHub Issues提交，包含以下信息：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（浏览器、操作系统等）
- 屏幕截图（如适用）

## 维护与更新

### 定期维护

1. 课程数据更新
```bash
python scripts/crawl_courses.py
python scripts/import_courses.py data/latest_courses.csv
```

2. 数据库备份
```bash
# SQLite
sqlite3 app/app.db .dump > backup_$(date +%Y%m%d).sql

# MySQL
mysqldump -u username -p database_name > backup_$(date +%Y%m%d).sql
```

3. 系统更新
```bash
git pull
pip install -r requirements.txt
flask db upgrade
systemctl restart hkustgz-course  # 如果使用systemd
```

## 联系与支持

如有问题或建议，请通过以下方式联系我们：
- GitHub Issues
- 邮件：jruan189@connect.hkust-gz.edu.cn

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解更多详情。
