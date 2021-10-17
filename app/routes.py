from flask import Blueprint

# first arg is used to identify this Blueprint from Flask server logs
# second arg usually always name 
hello_word_bp = Blueprint("hello_world", __name__)

# responsibility of an endpoint:
    # match the HTTP verb & request URL of an HTTP request
    # form an HTTP response to send back to client

@hello_world_bp.route("/hello_world", methods=["GET"])
def say_hello_world():
    my_response_body = "Hello, world!"
    return my_response_body

