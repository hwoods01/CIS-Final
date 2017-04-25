from django.db import connection
from trailHQ.models import SingletracksTrail, Matches, TFid, TFStateArea, MtbProjStateId, MtbProjTrailId, TFState


# this file is for making raw queries against the db

queryList= {

    "AreaResults": "select tfi.url as TFURL, tfa.area_id as TFAID, mtb.MTrailId as MPID, match.duplicates, st.key, st.name as SingleTracks, tfi.name as TrailForks, mtb.name as MtbProject, tfa.riding_area as TFArea from trailHQ_matches match join trailHQ_singletrackstrail st on match.SingleTracksId_id =  st.key left join trailHQ_tfid tfi on match.TfTrailId_id = tfi.Tid left join trailHQ_mtbprojtrailid mtb on match.MTrailId_id = mtb.mtrailId	left join trailHQ_tfstatearea tfa on match.TfAreaId_id = tfa.riding_area where (select key from trailHQ_singletrackstrail where city = %s and state = %s)",
    'area': "select * from trailHQ_tfstatearea  tfa join trailHQ_tfstate  tfs on tfa.stateId_id = tfs.Sid where tfa.riding_area LIKE %s AND tfs.state_name = %s",
    'trail': "select * from trailHQ_tfid tf join trailHQ_tfstatearea tfa on tf.areaId_id = tfa.Aid join trailHQ_tfstate tfs on tfa.stateId_id = tfs.Sid where tf.name LIKE %s and tfs.state_name = %s",
    'mtrail': "select * from trailHQ_mtbprojtrailid mtt	join trailHQ_mtbprojstateid mts on mtt.stateId_id = mts.state_id where mtt.name LIKE %s and  mts.state_name = %s;",
    'singtrail': "select tfi.Tid as TID, st.key as KEY, mtt.mtrailId as MID, tfa.Aid as AID from trailHQ_matches match 	left join trailHQ_tfid tfi on tfi.Tid = match.TfTrailId_id	left join trailHQ_singletrackstrail st on st.key = match.SingleTracksId_id	left join trailHQ_mtbprojtrailid mtt on match.MTrailId_id = mtt.mtrailId	left join trailHQ_tfstatearea tfa on match.TfAreaId_id = tfa.Aid where st.key = %s"
}

# returns the results as a dictionary so you can grab by column name
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns,row))
        for row in cursor.fetchall()
    ]


def makeQuery(queryType, params):

    with connection.cursor() as cursor:
        query = queryList[queryType]
        cursor.execute(query, params)
        results = dictfetchall(cursor)
    return results


def get_or_none(classmodel, pk):
    try:
        return classmodel.objects.get(pk)
    except classmodel.DoesNotExists:
        return None