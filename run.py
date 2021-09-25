from app import app
from werkzeug.serving import run_simple
from time import sleep

if __name__ == '__main__':
    run_simple('localhost', 8090, app, use_reloader=False, use_debugger=True, use_evalex=True, threaded=True)
    while True:
        sleep(1)
