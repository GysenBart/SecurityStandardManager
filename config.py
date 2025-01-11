import os

basedir = os.path.abspath(os.path.dirname(__file__))

repo_folder = os.path.join(basedir, "SCF_files")

repo_url = "https://github.com/securecontrolsframework/securecontrolsframework.git"

debug_enabled = True
host = "0.0.0.0"
port = 8080
folder_static = "app/static"

prod_name = "Security Standard Manager"
database_name = "SSM"
database_user = "postgres"
database_pwd = "postgres"
database_host = "postgres"
database_port = 5432

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'postgresql://'+str(database_user) +':'+str(database_pwd)+'@'+str(database_host)+':'+str(database_port)+'/' + str(database_name)
    FLASK_ADMIN_SWATCH = "darkly"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir,"tempdownloads")
    SECRET_KEY = "testkey"
    SCEDULER_API_ENABLED = True
    
