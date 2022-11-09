from website import create_app
from flask import Flask
from flask_cors import CORS
app = create_app()
CORS(app,resources=r'/*',vary_header=False,supports_credentials=True)
if __name__ == '__main__':
    app.run(debug=False,port=9494,host="0.0.0.0")
