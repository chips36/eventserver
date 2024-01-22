from waitress import serve
from EventServer.wsgi import application

if __name__ == '__main__':
    serve(application, host='192.168.0.150', port='8002')
