from flask import Flask, request, send_file
import argparse
import functools
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello from the server!"

def casares_get(f):
    """
    Decorator to define a Flask route for POST requests
    using the function name as the endpoint.
    """
    endpoint = f"/{f.__name__}"  # Route based on the function name

    @app.route(endpoint, methods=['GET'])  # Define route with Flask
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    
    return wrapper

def casares_post(f):
    """
    Decorator to define a Flask route for POST requests
    using the function name as the endpoint.
    """
    endpoint = f"/{f.__name__}"  # Route based on the function name

    @app.route(endpoint, methods=['POST'])  # Define route with Flask
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    
    return wrapper

def casares_post_images(func):
    """
    A decorator that processes POST requests with 1 to N images,
    calls the decorated function with those images as a list, and returns the result as an image response.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        images = []

        # Loop through all files in the POST request
        for image_key in request.files:
            image = Image.open(request.files[image_key].stream)
            images.append(image)

        # Ensure there's at least one image
        if not images:
            return "No images provided", 400

        # Call the decorated function with the list of images
        result_image = func(images)

        # Prepare and send the result image as a response
        img_io = BytesIO()
        result_image.save(img_io, 'JPEG', quality=80)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    # Register the wrapper function as a Flask route
    endpoint = f"/{func.__name__}"
    app.route(endpoint, methods=['POST'])(wrapper)
    
    return wrapper


def run_server(port=3000):
    """Function to run the Flask server."""
    app.run(debug=True, host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Run the Flask server.")
    parser.add_argument('--port', '-p', type=int, default=3000, help="Port number to run the Flask server on. Default is 3000.")
    args = parser.parse_args()

    # Start the Flask app on the specified port
    run_server(port=args.port)
