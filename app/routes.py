from flask import Blueprint, jsonify

# first arg is used to identify this Blueprint from Flask server logs
# second arg usually always name 
hello_world_bp = Blueprint("hello_world", __name__)
books_bp = Blueprint("books", __name__, url_prefix="/books")

# responsibility of an endpoint:
    # match the HTTP verb & request URL of an HTTP request
    # form an HTTP response to send back to client

@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    my_response_body = "Hello, world!"
    return my_response_body

@hello_world_bp.route("/hello/JSON", methods=["GET"])
def say_hello_json():
    return {
        "name": "Kristel Jabbusch",
        "message": "Hello!",
        "hobbies": ["kpop", "anime", "binge-snacking", "programming"]
    }

@hello_world_bp.route("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Kristel Jabbusch",
        "message": "Hello!",
        "hobbies": ["kpop", "anime", "binge-snacking", "programming"]
    }
    new_hobby = ["volleyball"]
    response_body["hobbies"] += new_hobby
    return response_body

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Honk If You Bonk", "A honky novel set in the bonkiest world."),
    Book(2, "Hork If You Bork", "A horky novel set in the borkiest world."),
    Book(3, "Hort If You Bort", "A horty novel set in the bortiest world.")
    ]

@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book_id = int(book_id)
    for book in books:
        if book.id == book_id:
            return {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
            



