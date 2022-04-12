from gevent.pywsgi import WSGIServer
from dme_p1_server import app

http_server = WSGIServer(("localhost", 5002), app)
http_server.serve_forever()