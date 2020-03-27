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

for geboortedatum in "kinderen":
    

treedata = Tree(inputData)

rule = 'for geboortedatum in kinderen dateTime($.kinderen.geboortedatum) + timeDelta(18, 0, 0, 0, 0, 0) > dateTime($.info)'
print("WAT IS DIT", treedata.execute(rule))