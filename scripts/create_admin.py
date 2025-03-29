#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入Flask应用
from app import app, db
from app.models.user import User

def create_admin():
    """创建管理员账号"""
    with app.app_context():
        # 检查是否已存在管理员账号
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("管理员账号已存在")
            return
        
        # 创建新管理员账号
        admin = User(
            username='admin',
            email='jruan189@connect.hkust-gz.edu.cn',
            password='admin'
        )
        admin.role = 'Admin'
        admin.identity = 'Teacher'
        admin.active = True
        admin.confirmed_at = datetime.utcnow()
        admin.last_login_time = datetime.utcnow()
        admin.last_edit_time = datetime.utcnow()
        
        db.session.add(admin)
        db.session.commit()
        print("管理员账号创建成功！")
        print("用户名：admin")
        print("邮箱：jruan189@connect.hkust-gz.edu.cn")
        print("密码：admin")

if __name__ == '__main__':
    create_admin() 