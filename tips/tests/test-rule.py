from objectpath import Tree
from unittest import TestCase


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
for geboortedatum in inputData:
    print(geboortedatum)

print("WAT IS DIT", treedata.execute(rule))


# def test_rule(inputData):
