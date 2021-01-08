from dashapp.server import server
from dashapp.dashapp import app

if __name__ == "__main__":
    server.run(debug=True, threaded=True, port=5000)
