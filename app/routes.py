from flask import redirect, url_for


def init_routes(app):
    
    @app.route('/')
    def initial():
        return redirect(url_for('login'))