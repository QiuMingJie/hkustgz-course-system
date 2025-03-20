from app import app, db
from app.models import *
from datetime import datetime

with app.app_context():
    # 清空数据库
    db.drop_all()
    db.create_all()

    # 创建测试用户
    test_user = User(username='test_user', email='test@test.com', password='test123')
    db.session.add(test_user)

    # 创建测试部门
    test_dept = Dept(name='计算机科学与工程系', code='20070')
    db.session.add(test_dept)

    # 创建测试教师
    test_teacher = Teacher(name='张三', dept=test_dept)
    db.session.add(test_teacher)

    # 创建测试课程
    test_course = Course(name='Python编程', _dept=test_dept)
    test_course.teachers.append(test_teacher)
    db.session.add(test_course)

    # 创建课程评分
    test_course_rate = CourseRate(course=test_course)
    db.session.add(test_course_rate)

    # 创建课程学期
    test_course_term = CourseTerm(
        course=test_course,
        term='20231',  # 2023年第1学期
        courseries='CS101',
        credit=3.0,
        hours=48,
        description='Python编程入门课程',
        teaching_material='Python编程：从入门到实践',
        reference_material='Python Cookbook'
    )
    db.session.add(test_course_term)

    # 创建课程班级
    test_course_class = CourseClass(
        course=test_course,
        term='20231',
        cno='CS101-01'
    )
    db.session.add(test_course_class)

    # 提交以获取ID
    db.session.commit()

    # 创建测试评论
    test_review = Review()
    test_review.course = test_course
    test_review.author = test_user
    test_review.term = '20231'
    test_review.content = '这是一个测试点评'
    test_review.rate = 9
    test_review.difficulty = 2
    test_review.homework = 2
    test_review.grading = 2
    test_review.gain = 3
    test_review.is_anonymous = False
    test_review.publish_time = datetime.utcnow()
    test_review.add()

    print("数据库表和测试数据创建成功！") 