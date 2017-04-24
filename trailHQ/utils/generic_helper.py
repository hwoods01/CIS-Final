
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







'''    id = None
    dups = False
    print(len(keyList))
    startingCountForDuplicate = 0
    for rowNum in range(0, len(results)):
        for i in range(0, len(keyList) ):
            if dups :

                # if this is true were going to add the list
                if results[rowNum]["key"] == id:
                    if results[rowNum][keyList[i]] != None:
                        combineLists[i].append(results[rowNum][keyList[i]])
                        combineLists[i].append(results[rowNum][idList[i]])


                    # clear that row from the list or at least don't add it do combine


                # this means that we've switched numbers so we reset and look for the next ones
                else:
                    if combineLists[i] == [ None ]:
                        combineLists[i] = None
                        idCombine[i] = None

                    results[startingCountForDuplicate][keyList[i]] =  combineLists[i]

                    results[startingCountForDuplicate][idList[i]] = idCombine[i]

                    combined.append(results[startingCountForDuplicate])

                    # we've appended last duplicates now time to see if trail is duplicated

                    # clear the lists
                    combineLists[i] =[]
                    idCombine[i]=[]

                    # next trail is also duplicated so we set everything to it
                    if results[rowNum]["duplicates"] == True:
                        id = results[rowNum]["key"]
                        startingCountForDuplicate = rowNum
                        dups = True

                        combineLists[i].append(results[rowNum][keyList[i]])
                        idCombine[i].append(results[rowNum][idList[i]])


                    # next trail only has a single result
                    else:
                        startingCountForDuplicate = 0
                        dups = False
                        if results[rowNum][keyList[i]] != None:
                            combined.append((results[rowNum]))

             # we just found that the this is the first trail in the set to have duplicates
            elif results[rowNum]["duplicates"] == True:
                id = results[rowNum]["key"]
                dups = True
                startingCountForDuplicate = rowNum
                if results.append(results[rowNum][keyList[i]]) != None:
                    combineLists[i].append(results[rowNum][keyList[i]])

                    idCombine[i].append(results[rowNum][idList[i]])

            else:
                if results[rowNum][keyList[i]] == None :
                    results[rowNum][keyList[i]] = None
                    results[rowNum][idList[i]] = None

        combined.append(results[rowNum])

    return combined '''