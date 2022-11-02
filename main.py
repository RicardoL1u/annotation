from website import create_app
from flask import Flask
from flask_cors import CORS
app = create_app()
CORS(app,resources=r'/*',vary_header=False,supports_credentials=True)
if __name__ == '__main__':
    app.run(debug=True,port=9522,host="0.0.0.0")
