from flask import Flask, request
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from datetime import timedelta
from functools import wraps

app = Flask(__name__)

app.config['APP_DEBUG']= True

################################
# JWT
################################
app.config['JWT_SECRET_KEY'] = 'Ak4ch4nt0b0ku'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'claims' : identity,
        'identifier' : 'ALTABATCH3'
    }

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        verify_jwt_in_request()
        role = get_jwt_identity()
        if role == 'internal':
            return fn(*args, **kwargs)
        else:
            return {'status':'Forbidden', 'message' : 'internal only'},403
    return wrapper
####################
# Database
#############
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://resita:alta123@localhost:3306/rest_training' # //user:password@host/nama_database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

#########################################
# Middlewares
#########################################
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'method' : request.method,
            'code' : response.status,
            'uri':request.full_path,
            'request': requestData, 
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    
    return response

#########################################
# import blueprints
#########################################
from blueprints.anime import bp_anime
app.register_blueprint(bp_anime,url_prefix='/anime')
db.create_all()