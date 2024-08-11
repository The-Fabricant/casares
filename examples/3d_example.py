from casares.server import casares_post, run_server
from PIL import Image

@casares_post("obj", "text")
def obj_vertices(obj):
    """
    asset is a trimesh object, this function returns a text response with the vertices of the object
    """

    print(obj.vertices)
    print(obj.faces)

    try:
        # Convert the list of vertices to a string
        vertices_string = "\n".join([f"{vertex[0]} {vertex[1]} {vertex[2]}" for vertex in obj.vertices])
        return vertices_string

    except Exception as e:
        print(f"Error occurred during rendering: {e}")
        return None


if __name__ == "__main__":
    run_server()