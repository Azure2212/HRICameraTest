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

@app.route('/TourchScreenAction/', methods=['POST'])
def TourchScreenAction():
    data = request.get_json()  # Get JSON payload
    if not data:
        return jsonify({'error': 'Missing JSON payload'}), 400

    IDRobot = data.get('IDRobot')
    Move2Page = data.get('Move2Page')
    action = data.get('action')
    value = data.get('value')

    if not IDRobot or not action:
        return jsonify({'error': 'Missing IDRobot or action'}), 400

    # Emit the socket event
    socketio.emit('TourchScreenAction', 
                  {'Move2Page': Move2Page, 'action': action, 'value': value}, 
                  room=IDRobot)

    return jsonify({'message': f'Action: "{action}", value: "{value}", Move2Page:"{Move2Page}"  sent to IDRobot "{IDRobot}"'}), 200

@socketio.on('join')
def on_join(data):
    IDRobot = data.get('room')
    if IDRobot:
        join_room(IDRobot)
        print(f"joined IDRobot: {IDRobot}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    print('start')
    
    #http://192.168.0.17:5000/controlCamera?IDRobot=100&action=stop
    #https://hricameratest.onrender.com/controlCamera/?IDRobot=100&action=stop