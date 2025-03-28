from flask import Blueprint,render_template,abort,redirect,url_for,request,abort,jsonify
from flask_security import current_user,login_required
from app.models import Course, Review, ReviewHistory
from app.forms import ReviewForm
from app.utils import sanitize, editor_parse_at
from flask_babel import gettext as _
from .course import course
import markdown
from datetime import datetime

review = Blueprint('review',__name__)


def record_review_history(review, operation, commit=True):
    history = ReviewHistory()
    history.difficulty = review.difficulty
    history.homework = review.homework
    history.grading = review.grading
    history.gain = review.gain
    history.rate = review.rate
    history.content = review.content
    history.author_id = review.author_id
    history.course_id = review.course_id
    history.term = review.term
    history.publish_time = review.publish_time
    history.update_time = review.update_time
    history.is_anonymous = review.is_anonymous
    history.only_visible_to_student = review.only_visible_to_student
    history.is_hidden = review.is_hidden
    history.is_blocked = review.is_blocked

    history.review_id = review.id
    history.operation = operation
    if current_user and current_user.is_authenticated:
        history.operation_user_id = current_user.id

    if commit:
        history.add()
    return history


@course.route('/<int:course_id>/review/',methods=['GET','POST'])
@login_required
def new_review(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404)
    user = current_user
    review = Review.query.with_for_update().filter_by(course=course, author=user).first()
    old_review = None
    if not review:
        is_new = True
        review = Review()
        review.course = course
        review.author = user
    else:
        is_new = False
        old_review = Review()
        old_review.content = review.content
        old_review.difficulty = review.difficulty
        old_review.homework = review.homework
        old_review.grading = review.grading
        old_review.gain = review.gain
        old_review.rate = review.rate

    message = ''
    form = ReviewForm(formdata=request.form, obj=review)
    polls = [
        {'name': 'difficulty', 'display': '课程难度', 'options': ['简单', '中等', '困难']},
        {'name': 'homework', 'display': '作业多少', 'options': ['不多', '中等', '超多']},
        {'name': 'grading', 'display': '给分好坏', 'options': ['超好', '一般', '杀手']},
        {'name': 'gain', 'display': '收获多少', 'options': ['很多', '一般', '没有']},
    ]

    if request.method == 'POST':
        print("接收到的表单数据:", request.form)  # 调试信息
        
        # 手动转换数值类型字段
        try:
            if request.form.get('difficulty'):
                form.difficulty.data = int(request.form.get('difficulty'))
            if request.form.get('homework'):
                form.homework.data = int(request.form.get('homework'))
            if request.form.get('grading'):
                form.grading.data = int(request.form.get('grading'))
            if request.form.get('gain'):
                form.gain.data = int(request.form.get('gain'))
            if request.form.get('rate'):
                form.rate.data = int(request.form.get('rate'))
            if request.form.get('term'):
                form.term.data = request.form.get('term')
        except ValueError as e:
            print("数值转换错误:", str(e))  # 调试信息
            if request.form.get('is_ajax'):
                return jsonify({
                    'ok': False,
                    'message': '数值字段格式错误'
                })
            message = '提交失败，请确保所有评分项填写正确！'
            return render_template('new-review.html', form=form, course=course, review=review, polls=polls, message=message, is_new=is_new, title='写点评')
        
        if not form.validate():
            print("表单验证错误:", form.errors)  # 调试信息
            if request.form.get('is_ajax'):
                return jsonify({
                    'ok': False,
                    'message': '表单验证失败：' + '; '.join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
                })
            message = '提交失败，请检查所有必填项！'
            return render_template('new-review.html', form=form, course=course, review=review, polls=polls, message=message, is_new=is_new, title='写点评')
            
        try:
            # check validity of term
            if str(form.term.data) not in course.term_ids:
                raise ValueError('无效的学期选择')

            form.populate_obj(review)
            review.content, mentioned_users = editor_parse_at(review.content)
            review.content = sanitize(review.content)

            if review.is_hidden or review.is_blocked:
                users_to_notify = []
                mentioned_users = []
            else:
                users_to_notify = course.followers
                if not review.is_anonymous:
                    users_to_notify = set(users_to_notify + current_user.followers)

            if is_new:
                review.add()
                for user in users_to_notify:
                    if user != current_user:
                        user.notify('review', review, ref_display_class='Course')
                for user in mentioned_users:
                    user.notify('mention', review)
                record_review_history(review, 'create')
            else:
                if old_review.content == review.content and old_review.difficulty == review.difficulty and old_review.homework == review.homework and old_review.grading == review.grading and old_review.gain == review.gain and old_review.rate == review.rate:
                    pass
                else:
                    review.update_time = datetime.utcnow()
                    review.course.update_rate()
                    for user in users_to_notify:
                        if user != current_user:
                            user.notify('update-review', review, ref_display_class='Course')
                    for user in mentioned_users:
                        user.notify('mention', review)
                record_review_history(review, 'update')

            next_url = url_for('course.view_course', course_id=course_id, _external=True) + '#review-' + str(review.id)
            if request.form.get('is_ajax'):
                return jsonify({'ok': True, 'next_url': next_url})
            return redirect(next_url)
            
        except Exception as e:
            print("处理评论时出错:", str(e))  # 调试信息
            if request.form.get('is_ajax'):
                return jsonify({'ok': False, 'message': str(e)})
            message = f'提交失败：{str(e)}'
            return render_template('new-review.html', form=form, course=course, review=review, polls=polls, message=message, is_new=is_new, title='写点评')

    if request.form.get('is_ajax'):
        return jsonify({'ok': False, 'message': '无效的请求'})
    return render_template('new-review.html', form=form, course=course, review=review, polls=polls, message=message, is_new=is_new, title='写点评')


@review.route('/delete/',methods=['POST'])
@login_required
def delete_review():
    review_id = request.form.get('id',type=int)
    if not review_id:
        message = _('You must specify a id.')
        return jsonify(ok=ok,message=message)
    review = Review.query.with_for_update().get(review_id)
    ok = False
    message = _('Something wrong happend.')
    if not review:
        message = _('Can\'t find the review.')
        return jsonify(ok=ok,message=message)
    #check if the user is the author
    if review.author != current_user and not current_user.is_admin:
        message = _('You have no right to do this.')
        return jsonify(ok=ok,message=message)

    record_review_history(review, 'delete')
    review.delete()
    ok = True
    message = _('The review has been deleted.')
    return jsonify(ok=ok,message=message)

@review.route('/comments/', methods=['GET'])
def show_comments():
    review_id = request.args.get('review_id', type=int)
    if not review_id:
        abort(404)
    review = Review.query.get(review_id)
    if not review:
        abort(404)
    return render_template('review-comments.html', review=review, user=current_user)
