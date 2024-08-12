import inspect
from flask import Flask, Response, request, send_file
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
    and returns an image, OBJ, GLB, or text as a response.
    
    Parameters:
    - input_types: Expected input types (list of 'text', 'image', 'obj', 'glb')
    - output_type: Expected output type ('image', 'jpg', 'png', 'obj', 'glb', 'text')
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

            if 'image' in input_types or 'jpg' in input_types or 'png' in input_types:
                # Process multiple images
                images = []
                for image_key in request.files:
                    if request.files[image_key].mimetype.startswith('image/'):
                        image = Image.open(request.files[image_key].stream)
                        images.append(image)

                if images:
                    # If only one image is expected, pass it directly
                    if len(images) == 1:
                        inputs['png'] = images[0]
                    else:
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

            if 'glb' in input_types:
                # Process single GLB file
                if 'file' in request.files and request.files['file'].mimetype == 'model/gltf-binary':
                    glb_file = request.files['file']
                    try:
                        glb_mesh = trimesh.load(glb_file, file_type='glb')
                        inputs['glb'] = glb_mesh
                    except Exception as e:
                        return f"Failed to process GLB file: {str(e)}", 400

            if not inputs:
                return "No valid inputs provided", 400

            # Extract query parameters and pass them as extra arguments
            for key, value in request.args.items():
                if key not in inputs:
                    try:
                        # Attempt to convert to float, otherwise keep as string
                        inputs[key] = float(value)
                    except ValueError:
                        inputs[key] = value

            # Call the decorated function with the collected inputs
            result = func(**inputs)

            if output_type in ['image', 'jpg', 'png']:
                # Prepare and send the result image as a response
                img_io = BytesIO()
                image_format = 'PNG' if output_type == 'image' else output_type.upper()
                result.save(img_io, format=image_format)
                img_io.seek(0)
                mimetype = f'image/{output_type.lower()}'
                return send_file(img_io, mimetype=mimetype)

            elif output_type == 'obj':
                # Return OBJ file
                obj_io = BytesIO()
                result.export(file_obj=obj_io, file_type='obj')
                obj_io.seek(0)
                return send_file(obj_io, mimetype='application/octet-stream', as_attachment=True, download_name='output.obj')

            elif output_type == 'glb':
                # Return GLB file
                glb_io = BytesIO()
                result.export(glb_io, file_type='glb')
                glb_io.seek(0)
                return send_file(glb_io, mimetype='model/gltf-binary', as_attachment=True, download_name='output.glb')

            elif output_type == 'text':
                # Return plain text response
                return Response(result, mimetype='text/plain')

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
