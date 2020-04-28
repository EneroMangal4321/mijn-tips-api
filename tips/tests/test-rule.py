from objectpath import Tree
from unittest import TestCase
import json

def test_rule():
    inputData = {
        "info": "2020-09-30",
        "kinderen": [
            {
                "geboortedatum": "1995-01-01"
            },
            {
                "geboortedatum": "2005-01-01"
            }
        ]
    }
    rule = 'dateTime($.kinderen.geboortedatum[1]) + timeDelta(18, 0, 0, 0, 0, 0) > dateTime($.info)'
    treedata = Tree(inputData)
    print("WAT IS DIT", treedata.execute(rule))
    som = 'dateTime($.kinderen.geboortedatum[1]) + timeDelta(18, 0, 0, 0, 0, 0)'
    print(treedata.execute(som))
    return inputData

def test_loop(inputData):
    jsonData = json.loads(inputData)
    print("HSHSH", jsonData)

if __name__ == "__main__":
    test_rule()
    test_loop(inputData)
    print("OK")