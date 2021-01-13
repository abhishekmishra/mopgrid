import os
import json

def sample_grid():
    gpath = os.path.join(os.getcwd(), "..", "test", "data", "sample0.json")
    with open(gpath, "r") as f:
        gstr = f.read()
        g = json.loads(gstr)
    return g


if __name__ == "__main__":
    g = sample_grid()
    print(g["metadata"])