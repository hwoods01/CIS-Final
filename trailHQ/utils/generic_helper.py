

'''
def combineDicts(results):
    combined = []
    dicts_to_combine = []
    id = None
    dups = False
    for rowNum in range(0, len(results)-1):
        if dups :
            if results[rowNum]["key"] == id:


        elif results[rowNum]["duplicates"] == True:
            id = results[rowNum]["key"]
            dups = True
            dicts_to_combine.append(results[rowNum])

        else:
            combined.append(results[rowNum])'''