from chat import app, db, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)


