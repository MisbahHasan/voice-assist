import getpass
import os
from langchain_fireworks import ChatFireworks
import os
from flask import Flask, render_template,send_file
from flask_socketio import SocketIO, emit
from langchain_fireworks import ChatFireworks
import os


# Set the environment variable for authentication (use your service account key path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/content/drive/MyDrive/GCP/gen-lang-client-0748896060-f1c61cb77bf6.json'
os.environ["FIREWORKS_API_KEY"] = "D1AfcywKsqg7xj1vy0cX5fRucxrulLJ2LIUNexVS0quOnWqY"
model = ChatFireworks(model="accounts/fireworks/models/mixtral-8x7b-instruct")



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")



@app.route('/')
def index():
    return send_file('src/index.html')

@socketio.on('user_audio')
def handle_audio(data):
    user_text = data.get('text')
    session_id = data.get('sessionId')


    if user_text:
        try:
            response = model.invoke(user_text).content
            print('Generated response:', response)
        except Exception as e:
            response = f"Error generating response: {str(e)}"
    else:
        response = "Sorry, I didn't catch that."

    # Send response along with the session ID
    emit('bot_response', {'response': response, 'sessionId': session_id}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app,allow_unsafe_werkzeug=True)
