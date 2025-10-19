from flask import Flask, request, jsonify
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/controlCamera/', methods=['GET'])
def control_camera():
    IDRobot = request.args.get('IDRobot')
    action = request.args.get('action')
    if not IDRobot or not action:
        return jsonify({'error': 'Missing IDRobot or action'}), 400

    socketio.emit('camera_action', {'action': action}, room=IDRobot)
    return jsonify({'message': f'Action "{action}" sent to IDRobot "{IDRobot}"'}), 200

@socketio.on('join')
def on_join(data):
    IDRobot = data.get('room')
    if IDRobot:
        join_room(IDRobot)
        print(f"joined IDRobot: {IDRobot}")

if __name__ == '__main__':
    socketio.run(app, debug=True)
    print('start')