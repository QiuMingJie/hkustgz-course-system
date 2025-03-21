#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入Flask应用
from app import app, db

# 基础URL
BASE_URL = "https://w5.hkust-gz.edu.cn"

def get_all_subjects():
    """获取所有学科列表"""
    url = urljoin(BASE_URL, "/wcq/cgi-bin/2430/")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有学科链接
        subject_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and 'subject/' in href:
                full_url = urljoin(BASE_URL, href)
                subject_links.append(full_url)
                print(f"找到学科链接: {full_url}")
        
        return list(set(subject_links))  # 去重
    except Exception as e:
        print(f"获取学科列表时出错: {str(e)}")
        return []

def get_courses_from_subject(url):
    """从学科页面获取所有课程信息"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        courses = []
        current_course = {}
        
        # 遍历所有课程块
        for course_div in soup.find_all('div', class_='course'):
            try:
                # 获取课程代码和名称
                header = course_div.find('h2')
                if not header:
                    continue
                    
                title_text = header.text.strip()
                code_name = title_text.split(' - ', 1)
                if len(code_name) != 2:
                    continue
                
                course_code, name_with_units = code_name
                # 提取学分
                credit = "3"  # 默认值
                if '(' in name_with_units and ')' in name_with_units:
                    name = name_with_units.split('(')[0].strip()
                    credit_part = name_with_units[name_with_units.find('(')+1:name_with_units.find(')')]
                    if 'unit' in credit_part.lower():
                        credit = credit_part.split()[0].strip()
                else:
                    name = name_with_units.strip()
                
                current_course = {
                    'course_code': course_code.strip(),
                    'name': name,
                    'credit': credit
                }
                
                # 获取课程描述
                desc_div = course_div.find('div', class_='courseinfo')
                if desc_div:
                    current_course['description'] = desc_div.text.strip()
                
                # 获取教师信息
                instructors = []
                instructor_links = course_div.find_all('a', href=lambda x: x and 'instructor' in x)
                for instructor in instructor_links:
                    instructors.append(instructor.text.strip())
                current_course['teachers'] = ';'.join(instructors)
                
                # 获取课程时间信息
                sections = course_div.find_all('tr')
                for section in sections:
                    cols = section.find_all(['th', 'td'])
                    if len(cols) >= 2:
                        header = cols[0].text.strip().lower()
                        value = cols[1].text.strip()
                        
                        if header == 'vector':
                            try:
                                vector = value.strip('[]')
                                if ':' in vector:
                                    hours = vector.split(':')[0].split('-')
                                    if len(hours) >= 3:
                                        total_hours = sum(int(h or 0) for h in hours)
                                        current_course['hours'] = str(total_hours)
                                        current_course['hours_per_week'] = str(total_hours)
                            except Exception as e:
                                print(f"解析课时信息出错 '{value}': {str(e)}")
                
                # 补充默认信息
                current_course.update({
                    'term': "2024-1",  # 当前学期
                    'courseries': current_course['course_code'][:4],  # 课程系列
                    'course_major': current_course['course_code'][:4],  # 使用课程代码前缀作为主修
                    'course_type': current_course['course_code'][:4],  # 使用课程代码前缀作为课程类型
                    'course_level': "Undergraduate" if len(current_course['course_code']) > 4 and current_course['course_code'][4] in '123' else "Graduate",  # 根据课程号判断
                    'teaching_type': "Regular",  # 默认值
                    'grading_type': "Letter Grade",  # 默认值
                    'campus': "GZ",  # 默认值
                    'start_week': "1",  # 默认值
                    'end_week': "13",  # 默认值
                    'description_eng': "",  # 英文描述
                    'teaching_material': "",  # 教材
                    'reference_material': "",  # 参考书
                    'student_requirements': "",  # 学生要求
                    'homepage': url,  # 课程主页
                })
                
                # 确保所有必需字段都存在
                if 'hours' not in current_course:
                    current_course['hours'] = "39"  # 默认学时
                if 'hours_per_week' not in current_course:
                    current_course['hours_per_week'] = "3"  # 默认周学时
                if 'description' not in current_course:
                    current_course['description'] = ""  # 空描述
                
                courses.append(current_course.copy())
                print(f"成功解析课程: {current_course['course_code']} - {current_course['name']}")
                
            except Exception as e:
                print(f"解析课程时出错: {str(e)}")
                continue
        
        return courses
    except Exception as e:
        print(f"从 {url} 获取课程信息时出错: {str(e)}")
        return []

def save_to_csv(courses, output_file):
    """保存课程信息到CSV文件"""
    if not courses:
        print("没有课程需要保存")
        return
    
    fieldnames = [
        'course_code', 'name', 'courseries', 'term', 'course_major', 
        'course_type', 'course_level', 'teaching_type', 'grading_type',
        'credit', 'hours', 'hours_per_week', 'campus', 'start_week',
        'end_week', 'teachers', 'description', 'description_eng',
        'teaching_material', 'reference_material', 'student_requirements',
        'homepage'
    ]
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for course in courses:
            writer.writerow(course)
    print(f"成功保存 {len(courses)} 门课程到 {output_file}")

def import_courses(csv_file):
    """导入课程到数据库"""
    from app.models.course import Course, CourseTerm, CourseRate
    from app.models.user import Teacher
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 处理教师（可能有多个，用分号分隔）
            teachers = []
            for teacher_name in row['teachers'].split(';'):
                if teacher_name.strip():
                    teacher = Teacher.query.filter_by(name=teacher_name.strip()).first()
                    if not teacher:
                        teacher = Teacher(name=teacher_name.strip())
                        db.session.add(teacher)
                        db.session.commit()
                    teachers.append(teacher)
            
            # 检查课程是否已存在
            course = Course.query.filter_by(course_code=row['course_code']).first()
            if not course:
                course = Course()
                course._course_rate = CourseRate()
            
            # 更新课程基本信息
            course.course_code = row['course_code']
            course.name = row['name']
            course.teachers = teachers
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
            course_term.description = row['description']
            course_term.description_eng = row['description_eng']
            course_term.teaching_material = row['teaching_material']
            course_term.reference_material = row['reference_material']
            course_term.student_requirements = row['student_requirements']
            
            if not course_term.id:
                db.session.add(course_term)
            
            try:
                db.session.commit()
                print(f"Successfully imported/updated course: {course.course_code} for term {term}")
            except Exception as e:
                db.session.rollback()
                print(f"Error importing course {course.course_code}: {str(e)}")

def main():
    """主函数"""
    print("开始爬取课程信息...")
    
    # 获取所有学科链接
    subject_links = get_all_subjects()
    if not subject_links:
        print("未找到任何学科链接")
        return
    
    print(f"找到 {len(subject_links)} 个学科")
    
    # 获取所有课程信息
    all_courses = []
    for url in subject_links:
        print(f"\n正在处理学科: {url}")
        courses = get_courses_from_subject(url)
        all_courses.extend(courses)
        time.sleep(1)  # 添加延迟，避免请求过于频繁
    
    # 保存到CSV文件
    output_file = os.path.join('data', 'courses_2024_spring.csv')
    save_to_csv(all_courses, output_file)
    
    print("\n爬取完成!")
    print(f"总共爬取了 {len(all_courses)} 门课程")
    print(f"数据已保存到: {output_file}")

    # 导入到数据库
    print("开始导入课程到数据库...")
    import_courses(output_file)
    print("导入完成！")

if __name__ == '__main__':
    with app.app_context():
        main() 