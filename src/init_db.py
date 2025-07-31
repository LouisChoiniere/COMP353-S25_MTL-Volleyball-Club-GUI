from flask_sqlalchemy import SQLAlchemy

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:toor@172.16.16.241:3306/mvc"
    app.config["SECRET_KEY"] = "MY_SECRET"
    
    db = SQLAlchemy()
    db.init_app(app)

    return db