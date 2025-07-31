from flask import Flask, render_template

def init_routes(app):
    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/listlocations")
    def list_locations():
        return render_template('listlocation.html')