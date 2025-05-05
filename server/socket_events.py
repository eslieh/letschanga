from flask import current_app, request
from flask_socketio import SocketIO

socketio = SocketIO()


@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')
    if user_id:
        with current_app.app_context():
            cache = current_app.cache
            cache.set(f"user_sid:{user_id}", request.sid, timeout=0)
            print(f"[+] User {user_id} connected with SID {request.sid}")
        socketio.emit('connected', {'message': f'Connected as {user_id}'})
