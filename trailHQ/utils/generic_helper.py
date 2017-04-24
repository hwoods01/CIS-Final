
keyList = ["TrailForks", "MtbProject", "TFArea"]

combineLists = [ [],[],[] ]
idCombine = [ [], [], [] ]

def combineDicts(results):
    combined = []

    starting_rowNum = 0
    dups = False
    id = 0
    for rowNum in range(0, len(results)):

        if dups:

            # not done adding to the list
            if results[rowNum]["key"] == id:
                for i in range(0,3):
                   if checkDuplicate(keyList[i], results, rowNum):
                       results[starting_rowNum][keyList[i]].append(results[rowNum][keyList[i]])


            # we are done with that trail duplicates
            else:
                combined.append(results[starting_rowNum])

                if results[rowNum]["duplicates"] == True:
                    starting_rowNum = rowNum
                    id = results[rowNum]["key"]

                    for i in range(0,3):
                        if checkDuplicate(keyList[i], results, rowNum):
                            smallList = []
                            smallList.append(results[starting_rowNum][keyList[i]])
                            results[starting_rowNum][keyList[i]] = smallList



                else:
                    dups = False
                    combined.append(results[rowNum])


        elif results[rowNum]["duplicates"] == True:
            starting_rowNum = rowNum
            dups = True
            id = results[rowNum]["key"]
            for i in range(0,3):
                if checkDuplicate(keyList[i], results, rowNum):
                    smallList =[]
                    smallList.append(results[starting_rowNum][keyList[i]])
                    results[starting_rowNum][keyList[i]]= smallList

        else:
            combined.append(results[rowNum])
    return combined






def checkDuplicate(key, results, num ):

    value = results[num][key]
    if value == None:
        return False
    else:
        return True
