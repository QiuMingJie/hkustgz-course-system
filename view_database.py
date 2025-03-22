from app import app, db
from app.models import Course, Teacher, Review, CourseRate, User, Student

def view_database():
    with app.app_context():
        print('\n=== 课程列表 ===')
        courses = Course.query.all()
        for course in courses:
            print(f'ID: {course.id}')
            print(f'名称: {course.name}')
            print(f'教师: {", ".join([t.name for t in course.teachers])}')
            print('---')

        print('\n=== 教师列表 ===')
        teachers = Teacher.query.all()
        for teacher in teachers:
            print(f'ID: {teacher.id}')
            print(f'姓名: {teacher.name}')
            print('---')

        print('\n=== 用户列表 ===')
        users = User.query.all()
        for user in users:
            print(f'ID: {user.id}')
            print(f'用户名: {user.username}')
            print(f'邮箱: {user.email}')
            print('---')

        print('\n=== 评价列表 ===')
        reviews = Review.query.all()
        for review in reviews:
            print(f'ID: {review.id}')
            print(f'课程ID: {review.course_id}')
            print(f'作者ID: {review.author_id}')
            print(f'内容: {review.content[:100]}...' if len(review.content) > 100 else f'内容: {review.content}')
            print('---')

if __name__ == '__main__':
    view_database() 