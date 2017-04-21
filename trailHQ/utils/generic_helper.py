


def combineDicts(results):
    combined = []
    TF_to_combine = []
    MP_to_combine = []
    TA_to_combine = []
    TFURL_to_combine =[]
    MPID_to_combine = []
    TAID_to_combine = []

    id = None
    dups = False
    startingCountForDuplicate = 0
    for rowNum in range(0, len(results)-1):

        if dups :

            # if this is true were going to add the list
            if results[rowNum]["key"] == id:
                if results[rowNum]["TrailForks"] != None:
                    TF_to_combine.append(results[rowNum]["TrailForks"])
                    TFURL_to_combine.append(results[rowNum]["TFURL"])
                if results[rowNum]["MtbProject"] !=None:
                    MP_to_combine.append(results[rowNum]["MtbProject"])
                    MPID_to_combine.append(results[rowNum]["MPID"])
                if results[rowNum]["TFArea"] != None:
                    TA_to_combine.append(results[rowNum]["TFArea"])
                    TAID_to_combine.append(results[rowNum]["TFAID"])

                # clear that row from the list or at least don't add it do combine


            # this means that we've switched numbers so we reset and look for the next ones
            else:
                results[startingCountForDuplicate]["TrailForks"] =  TF_to_combine
                results[startingCountForDuplicate]["MtbProject"] = MP_to_combine
                results[startingCountForDuplicate]["TFArea"] = TA_to_combine
                results[startingCountForDuplicate]["TFURL"] = TFURL_to_combine
                results[startingCountForDuplicate]["MPID"] = MPID_to_combine
                results[startingCountForDuplicate]["TFAID"] = TAID_to_combine
                combined.append(results[startingCountForDuplicate])

                # we've appended last duplicates now time to see if trail is duplicated

                # clear the lists
                TF_to_combine = []
                MP_to_combine = []
                TA_to_combine = []
                TFURL_to_combine =[]
                MPID_to_combine = []
                TAID_to_combine =[]

                # next trail is also duplicated so we set everything to it
                if results[rowNum]["duplicates"] == True:
                    id = results[rowNum]["key"]
                    startingCountForDuplicate = rowNum
                    dups = True
                    TF_to_combine.append(results[rowNum]["TrailForks"])
                    MP_to_combine.append(results[rowNum]["MtbProject"])
                    TA_to_combine.append(results[rowNum]["TFArea"])
                    TFURL_to_combine.append(results[rowNum]["TFURL"])
                    MPID_to_combine.append(results[rowNum]["MPID"])
                    TAID_to_combine.append(results[rowNum]["TFAID"])

                # next trail only has a single result
                else:
                    startingCountForDuplicate = 0
                    dups = False
                    combined.append((results[rowNum]))

         # we just found that the this is the first trail in the set to have duplicates
        elif results[rowNum]["duplicates"] == True:
            id = results[rowNum]["key"]
            dups = True
            startingCountForDuplicate = rowNum
            TF_to_combine.append(results[rowNum]["TrailForks"])
            MP_to_combine.append(results[rowNum]["MtbProject"])
            TA_to_combine.append(results[rowNum]["TFArea"])
            TFURL_to_combine.append(results[rowNum]["TFURL"])
            MPID_to_combine.append(results[rowNum]["MPID"])
            TAID_to_combine.append(results[rowNum]["TFAID"])
        else:
            combined.append(results[rowNum])

    return combined