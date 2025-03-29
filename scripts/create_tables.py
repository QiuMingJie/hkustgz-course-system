from app import app, db

with app.app_context():
    db.create_all()
    print("所有数据库表已创建！") 