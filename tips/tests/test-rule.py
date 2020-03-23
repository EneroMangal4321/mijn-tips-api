from objectpath import Tree

inputData = {
    "geboortedatum": "2000-01-01",
    "datumInToekomst": "2018-01-01",
}


treedata = Tree(inputData)

rule = 'dateTime($.datumInToekomst) - timeDelta(18, 0, 0, 0, 0, 0) > dateTime($.geboortedatum)'
print(treedata.execute(rule))