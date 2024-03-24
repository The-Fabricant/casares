from casares.server import casares_get, run_server

@casares_get
def hello():
    return "Hello World!"

if __name__ == "__main__":
    run_server()
