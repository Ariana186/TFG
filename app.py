from flask import Flask
from views import setup_routes
#from waitress import serve

app = Flask(__name__)


setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
    #serve(app, host='0.0.0.0', port=8000)


