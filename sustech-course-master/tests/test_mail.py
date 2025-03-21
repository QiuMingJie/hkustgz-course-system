import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_mail import Mail, Message
from app import app
from app.utils import mail

def test_mail():
    with app.app_context():
        try:
            msg = Message('测试邮件 - HKUST-GZ Course Evaluation System',
                        recipients=['Aurorra1123@outlook.com'])
            msg.body = '这是一封测试邮件，用于验证邮件服务器配置是否正确。'
            mail.send(msg)
            print('邮件发送成功！')
        except Exception as e:
            print(f'邮件发送失败: {str(e)}')

if __name__ == '__main__':
    test_mail() 