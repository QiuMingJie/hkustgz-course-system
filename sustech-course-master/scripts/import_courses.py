#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
from datetime import datetime

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入Flask应用和模型
from app import app, db
from app.models.course import Course, CourseTerm, CourseRate
from app.models.user import Teacher

def get_or_create_teacher(name):
    """获取或创建教师"""
    teacher = Teacher.query.filter_by(name=name.strip()).first()
    if not teacher:
        teacher = Teacher(name=name.strip())
        db.session.add(teacher)
        db.session.commit()
    return teacher

def import_courses(csv_file):
    """导入课程到数据库"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # 处理教师（可能有多个，用分号分隔）
                teachers = []
                teacher_names = set()  # 使用集合去重
                for teacher_name in row['teachers'].split(';'):
                    if teacher_name.strip() and teacher_name.strip() not in teacher_names:
                        teacher_names.add(teacher_name.strip())
                        teacher = get_or_create_teacher(teacher_name)
                        teachers.append(teacher)
                
                # 检查课程是否已存在
                course = Course.query.filter_by(course_code=row['course_code']).first()
                if not course:
                    course = Course()
                    course._course_rate = CourseRate()
                
                # 更新课程基本信息
                course.course_code = row['course_code']
                course.name = row['name']
                course.teachers = teachers  # 设置教师关联
                course.introduction = row['description']
                course.homepage = row['homepage']
                course.last_edit_time = datetime.now()
                course.course_material_code = row['courseries']
                
                if not course.id:
                    db.session.add(course)
                    db.session.commit()
                
                # 创建或更新学期信息
                term = row['term']
                course_term = CourseTerm.query.filter_by(course_id=course.id, term=term).first()
                if not course_term:
                    course_term = CourseTerm(course_id=course.id, term=term)
                
                # 更新学期详细信息
                course_term.courseries = row['courseries']
                course_term.course_major = row['course_major']
                course_term.course_type = row['course_type']
                course_term.course_level = row['course_level']
                course_term.teaching_type = row['teaching_type']
                course_term.grading_type = row['grading_type']
                course_term.credit = float(row['credit'])
                course_term.hours = int(row['hours'])
                course_term.hours_per_week = int(row['hours_per_week'])
                course_term.campus = row['campus']
                course_term.start_week = int(row['start_week'])
                course_term.end_week = int(row['end_week'])
                course_term.teaching_material = row['teaching_material']
                course_term.reference_material = row['reference_material']
                course_term.student_requirements = row['student_requirements']
                course_term.description = row['description']
                course_term.description_eng = row['description_eng']
                
                if not course_term.id:
                    db.session.add(course_term)
                
                db.session.commit()
                print(f"成功导入/更新课程: {course.course_code} ({term})")
                
            except Exception as e:
                print(f"导入课程 {row.get('course_code', 'unknown')} 时出错: {str(e)}")
                db.session.rollback()
                continue

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python import_courses.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"错误: 文件 {csv_file} 不存在")
        sys.exit(1)
    
    print("开始导入课程...")
    with app.app_context():
        import_courses(csv_file)
    print("导入完成!")

if __name__ == '__main__':
    main() 