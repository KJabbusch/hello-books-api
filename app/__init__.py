from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    # importing hello_word_bp into module so we can use it in following line
    from .routes import hello_world_bp, books_bp
    # app's predefined function to register Blueprint
    app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)
    # we can follow this pattern & duplicate this code to create/register more
    return app
