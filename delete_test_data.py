from app import app, db
from app.models import Course, Teacher, Review, CourseRate

def delete_test_data():
    with app.app_context():
        # 删除评价
        review = Review.query.filter_by(id=1).first()
        if review:
            print(f"删除评价 #{review.id}")
            db.session.delete(review)

        # 删除课程
        course = Course.query.filter_by(id=1).first()
        if course:
            print(f"删除课程: {course.name}")
            # 删除课程评分
            course_rate = CourseRate.query.filter_by(id=course.id).first()
            if course_rate:
                print("删除课程评分")
                db.session.delete(course_rate)
            db.session.delete(course)

        # 删除教师
        teacher = Teacher.query.filter_by(id=1).first()
        if teacher:
            print(f"删除教师: {teacher.name}")
            db.session.delete(teacher)

        # 提交更改
        db.session.commit()
        print("所有测试数据已删除")

if __name__ == '__main__':
    delete_test_data() 