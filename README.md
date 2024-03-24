# Casares

Run a Flask server with routes as decorations. Specially tailored for Morel AI tools.  
It abstracts all the mechanism of creating routes typical of Flask, the only thing needed is to add a decorator that transforms the function in a route

![Casares](/images/casares.jpg)

[Wonder who is Casares?](https://en.wikipedia.org/wiki/Adolfo_Bioy_Casares)


## Installation

You can install as `pip` package:

```bash
git clone https://github.com/The-Fabricant/casares
cd casares
pip install -e .
```



## Conda Environment
```
conda env create -f environment.yml
conda activate casares-env
```

## Examples

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

- Combine two images by sending a POST request

```python
@casares_post_images
def combine_images(images):

    image1, image2 = images
    """
    Combine two images into one and return the result.
    """
    # An example image processing operation: merge images side by side
    total_width = image1.width + image2.width
    max_height = max(image1.height, image2.height)
    new_image = Image.new('RGB', (total_width, max_height))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1.width, 0))
    return new_image
```

then you can call the API with:

```bash
curl -X POST localhost:3000/combine_images -F "image1=@/path/to/image1.png" -F "image2=@/path/to/image2.png" --output "/path/to/output.jpg"
```