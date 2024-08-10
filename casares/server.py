import inspect
from flask import Flask, request, send_file
import argparse
import functools
from PIL import Image
from io import BytesIO
import trimesh # for 3d assets

app = Flask(__name__)


@app.route("/") # the only function not decored by casares itself!
def hello_world():
    return "Hello from a Casares server!"

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

def casares_post(input_types, output_type):
    """
    A generic decorator that processes POST requests with different types of inputs
    and returns an image as a response.
    
    Parameters:
    - input_types: Expected input types (list of 'text', 'image', 'obj')
    - output_type: Expected output type ('image')
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            inputs = {}

            if 'text' in input_types:
                # Process text input
                text = request.form.get('text', '')
                if text:
                    inputs['text'] = text

            if 'image' in input_types:
                # Process multiple images
                images = []
                for image_key in request.files:
                    if request.files[image_key].mimetype.startswith('image/'):
                        image = Image.open(request.files[image_key].stream)
                        images.append(image)

                if images:
                    inputs['images'] = images

            if 'obj' in input_types:
                # Process single OBJ file
                if 'file' in request.files and request.files['file'].mimetype == 'application/octet-stream':
                    obj_file = request.files['file']
                    try:
                        obj_mesh = trimesh.load(obj_file, file_type='obj')
                        inputs['obj'] = obj_mesh
                    except Exception as e:
                        return f"Failed to process OBJ file: {str(e)}", 400

            if not inputs:
                return "No valid inputs provided", 400

            # Call the decorated function with the collected inputs
            result_image = func(**inputs)

            if output_type == 'image':
                # Prepare and send the result image as a response
                img_io = BytesIO()
                result_image.save(img_io, 'PNG')
                img_io.seek(0)
                return send_file(img_io, mimetype='image/png')
            else:
                return "Unsupported output type", 400

        # Register the wrapper function as a Flask route
        endpoint = f"/{func.__name__}"
        app.route(endpoint, methods=['POST'])(wrapper)

        return wrapper
    return decorator


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
