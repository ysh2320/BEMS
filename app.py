from flask import Flask
from routes import *
from flask_session import Session
from flask_cors import CORS

app= Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(routes)

app.config['SESSION_TYPE'] = 'fileSystem'
 
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

Session(app)


if __name__ == '__main__':
    
    app.run(debug = True)
