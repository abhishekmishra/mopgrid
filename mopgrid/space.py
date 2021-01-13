import os
import json


if __name__ == "__main__":
    gpath = os.path.join(os.getcwd(), "test", "data", "sample0.json")
    with open(gpath, "r") as f:
        gstr = f.read()
        g = json.loads(gstr)
        print(g["metadata"])