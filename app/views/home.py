            user = User(
                username=form['username'].data,
                email=form['email'].data,
                password=form['password'].data
            )
            # 根据邮箱后缀判断用户身份
            email_suffix = user.email.split('@')[-1]
            if email_suffix == 'connect.hkust-gz.edu.cn':
                user.identity = 'Student'
            elif email_suffix == 'hkust-gz.edu.cn':
                user.identity = 'Teacher'
            else:
                user.identity = 'Student'  # 默认设置为学生
            db.session.add(user)
            db.session.commit()
            send_confirm_mail(user.email) 