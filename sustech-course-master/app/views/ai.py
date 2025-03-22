from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from datetime import datetime

bp = Blueprint('ai', __name__)

@bp.route('/chat')
@login_required
def chat():
    """AI聊天页面"""
    return render_template('ai_chat.html')

@bp.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    """处理AI聊天请求"""
    data = request.get_json()
    message = data.get('message')
    chat_id = data.get('chatId')
    
    # TODO: 这里需要调用实际的AI API
    # 目前返回模拟响应
    response = {
        'message': f"这是对'{message}'的模拟回复。在实际实现中，这里应该调用AI API获取真实响应。"
    }
    
    # 保存消息到数据库
    with db.session.begin():
        db.session.execute(
            "INSERT INTO chat_messages (chat_id, user_id, content, type, created_at) VALUES (%s, %s, %s, %s, %s)",
            [chat_id, current_user.id, message, 'user', datetime.now()]
        )
        db.session.execute(
            "INSERT INTO chat_messages (chat_id, user_id, content, type, created_at) VALUES (%s, %s, %s, %s, %s)",
            [chat_id, current_user.id, response['message'], 'ai', datetime.now()]
        )
    
    return jsonify(response)

@bp.route('/api/chat/history', methods=['GET'])
@login_required
def get_chat_history():
    """获取用户的聊天历史"""
    chats = db.session.execute(
        "SELECT id, title, created_at FROM chat_conversations WHERE user_id = %s ORDER BY updated_at DESC",
        [current_user.id]
    ).fetchall()
    
    return jsonify([{
        'id': chat.id,
        'title': chat.title,
        'created_at': chat.created_at.isoformat()
    } for chat in chats])

@bp.route('/api/chat/history', methods=['POST'])
@login_required
def save_chat_history():
    """保存新的聊天会话"""
    data = request.get_json()
    chat_id = data.get('id')
    title = data.get('title', '新会话')
    
    with db.session.begin():
        db.session.execute(
            "INSERT INTO chat_conversations (id, user_id, title) VALUES (%s, %s, %s)",
            [chat_id, current_user.id, title]
        )
    
    return jsonify({'status': 'success'})

@bp.route('/api/chat/rename/<chat_id>', methods=['POST'])
@login_required
def rename_chat(chat_id):
    """重命名聊天会话"""
    data = request.get_json()
    new_title = data.get('title')
    
    if not new_title:
        return jsonify({'error': '标题不能为空'}), 400
    
    with db.session.begin():
        result = db.session.execute(
            "UPDATE chat_conversations SET title = %s WHERE id = %s AND user_id = %s",
            [new_title, chat_id, current_user.id]
        )
        if result.rowcount == 0:
            return jsonify({'error': '未找到会话或无权限修改'}), 404
    
    return jsonify({'status': 'success'})

@bp.route('/api/chat/messages/<chat_id>', methods=['GET'])
@login_required
def get_chat_messages(chat_id):
    """获取特定会话的聊天记录"""
    # 首先验证用户是否有权限访问该会话
    chat = db.session.execute(
        "SELECT id FROM chat_conversations WHERE id = %s AND user_id = %s",
        [chat_id, current_user.id]
    ).fetchone()
    
    if not chat:
        return jsonify({'error': '未找到会话或无权限访问'}), 404
    
    messages = db.session.execute(
        "SELECT content, type, created_at FROM chat_messages WHERE chat_id = %s ORDER BY created_at",
        [chat_id]
    ).fetchall()
    
    return jsonify([{
        'content': msg.content,
        'type': msg.type,
        'created_at': msg.created_at.isoformat()
    } for msg in messages]) 