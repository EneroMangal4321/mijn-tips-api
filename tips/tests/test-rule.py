from objectpath import Tree


inputData = {
    "info": "2020-09-30",
    "kinderen": [
        {
            "geboortedatum": "1995-01-01"
        },
        {
            "geboortedatum": "1999-01-01"
        }
    ]
}
rule = 'dateTime($.kinderen.geboortedatum) + timeDelta(18, 0, 0, 0, 0, 0) > dateTime($.info)'
treedata = Tree(inputData)
for geboortedatum in inputData:
    print(geboortedatum)

print("WAT IS DIT", treedata.execute(rule))




