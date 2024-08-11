# Casares

Run a Flask server with routes as decorations. Specially tailored for Morel AI tools.  
It abstracts all the mechanism of creating routes typical of Flask, the only thing needed is to add a decorator that transforms the function in a route

![Casares](/images/casares.jpg)

[Wonder who is Casares?](https://en.wikipedia.org/wiki/Adolfo_Bioy_Casares)

### Example

```python
from casares.server import casares_post, run_server

@casares_post("obj", "text")
def obj_to_txt(obj,scale=1.0,translate_y=0.0):
    """
    asset is a trimesh object, this function returns a text response with the vertices of the object
    """

    print(scale)
    print(translate_y)

    try:
        # Convert the list of vertices to a string
        output_txt = str(scale) + "\n" + str(translate_y) + "\n"
        vertices_string = "\n".join([f"{vertex[0]} {vertex[1]} {vertex[2]}" for vertex in obj.vertices])
        return output_txt+ vertices_string

    except Exception as e:
        print(f"Error occurred during rendering: {e}")
        return None

if __name__ == "__main__":
    run_server()
```

that it can be called by:
```bash
 curl -X POST "localhost:3000/obj_to_txt?scale=2.0&translate_y=2.0" -F "file=@/path/to/mesh.obj" --output "/path/to/output.txt"
```


## Installation

You can install as `pip` package:

```bash
git clone https://github.com/The-Fabricant/casares
cd casares
pip install -e .
```

## Change Log

### v0.4
- additional arguments can be added to the decorated function and called as parameters from the query

### v0.3
- now `png`, `jpg`, `obj`, `glb`, `text` accepted as input or output



## Conda Environment
```bash
conda env create -f environment.yml
conda activate casares-env
```


Designed a more generic decorator, that accepts an arbitrary number of images, text of 3d obj assets and returns an image



### Example

```python
@casares_post("obj", "text")
def obj_to_txt(obj):
    """
    asset is a trimesh object, this function just returns a cyan flat image
    """
    output_txt = "Hello World"

    try:
        # DO SOMETHING WITH YOUR OBJ
        # output_txt = func(obj)

        return output_txt

    except Exception as e:
        print(f"Error occurred during rendering: {e}")
        return None
```
 that can be called by:  
```bash
 curl -X POST localhost:3000/obj_to_txt -F "file=@/path/to/mesh.obj" --output "/path/to/output.txt"
```

### Example
```python
@casares_post("obj", "image")
def obj_to_image(obj):
    """
    asset is a trimesh object, this function just returns a cyan flat image
    """
    image_size = (800, 800)

    print(obj.vertices)
    print(obj.faces)

    try:
        # Create a blank image just for testing
        image = Image.new('RGB', image_size, color='cyan')

        return image

    except Exception as e:
        print(f"Error occurred during rendering: {e}")
        return None
```


then you call the API with:
```bash
curl -X POST "localhost:3000/frontal_view?scale=30.0&translate_y=10.0" -F "file=@/path/to/mesh.obj" --output "/path/to/output.png"
```

## Other Examples

- a simple GET request

```python
from casares.server import casares_get, run_server

@casares_get
def hello():
    return "Hello World!"

if __name__ == "__main__":
    run_server()
```

it starts a server on port 3000 (by default). Go to `localhost:3000/hello` and you should see `Hello World!` as a message

