from objectpath import Tree
import os

inputData = {
    "info": "2020-09-30"
    # "kinderen" : {
    #     "geboortedatum": "2019-01-01"
    # }
}

BRP = os.path.join(PROJECT_PATH, 'tests', 'fixtures', 'data', 'brp.json')

treedata = Tree(inputData)

rule = 'dateTime($.brp.kinderen.geboortedatum) + timeDelta(18, 0, 0, 0, 0, 0) > dateTime($.info)'
print("WAT IS DIT", treedata.execute(rule))