from objectpath import Tree

inputData = {
    "info": "2020-09-30",
    "kinderen" : {
        "geboortedatum": "2019-01-01"
    }
}


treedata = Tree(inputData)

rule = 'dateTime($.kinderen.geboortedatum) + timeDelta(18, 0, 0, 0, 0, 0) > dateTime($.info)'
print(treedata.execute(rule))