from dashapp.server import server
from dashapp.dashapp import app

if __name__ == '__main__':
    server.run(threaded=True, port=5000)