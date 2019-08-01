from flask import Flask, request
from flask_restful import Api 
import sys, logging
from logging.handlers import RotatingFileHandler

####################################
# Import Blueprints
####################################
from blueprints import app, manager

api = Api(app, catch_all_404s=True)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'db':
            manager.run()
    except Exception as ex:
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/error.log'), maxBytes=10000, backupCount=5)
        log_handler.setLevel(logging.ERROR)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)

    app.run(debug=True, host='0.0.0.0', port=8383)