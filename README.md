# Casares

Run a Flask server with routes as decorations. Specially tailored for Morel AI tools.

![Casares](/images/casares.jpg)


## Installation

First, ensure you have Conda installed, then create and activate a new environment:


## Environment
```
conda env create -f environment.yml
conda activate casares-env
```

## Example

```python
from casares.server import casares_get, run_server

@casares_get
def hello():
    return "Hello World!"

if __name__ == "__main__":
    run_server()
```

it starts a server on port 3000 (by default). Go to `localhost:3000/hello` and you should see `Hello World!` as a message

- Combine two images


```bash
curl -X POST localhost:3000/combine_images -F "image1=@/path/to/image1.png" -F "image2=@/path/to/image2.png" --output "/path/to/output.jpg"
```