from django.db import connection
from trailHQ.models import SingletracksTrail, Matches, TFid, TFStateArea, MtbProjStateId, MtbProjTrailId, TFState, MtbProjTr, TFTrail,TFArea


# this file is for making raw queries against the db

queryList= {

    "AreaResults": "select match.duplicates, st.key,st.length as length, st.name as SingleTracks, tfi.name as TrailForks, mtb.name as MtbProject, tfa.riding_area as TFArea from trailHQ_matches match join trailHQ_singletrackstrail st on match.SingleTracksId_id =  st.key left join trailHQ_tfid tfi on match.TfTrailId_id = tfi.Tid left join trailHQ_mtbprojtrailid mtb on match.MTrailId_id = mtb.mtrailId	left join trailHQ_tfstatearea tfa on match.TfAreaId_id = tfa.riding_area where (select key from trailHQ_singletrackstrail where city = %s and state = %s)",
    'area': "select * from trailHQ_tfstatearea  tfa join trailHQ_tfstate  tfs on tfa.stateId_id = tfs.Sid where tfa.riding_area LIKE %s AND tfs.state_name = %s",
    'trail': "select * from trailHQ_tfid tf join trailHQ_tfstatearea tfa on tf.areaId_id = tfa.Aid join trailHQ_tfstate tfs on tfa.stateId_id = tfs.Sid where tf.name LIKE %s and tfs.state_name = %s",
    'mtrail': "select * from trailHQ_mtbprojtrailid mtt	join trailHQ_mtbprojstateid mts on mtt.stateId_id = mts.state_id where mtt.name LIKE %s and  mts.state_name = %s;",
    'singtrail': "Select tfi.Tid as Tid, tfi.url as TFI_URL, st.key as key, st.length as length, mtt.mtrailId as Mid, tfa.Aid as Aid, match.duplicates as duplicates from trailHQ_matches match 	left join trailHQ_tfid tfi on tfi.Tid = match.TfTrailId_id	left join trailHQ_singletrackstrail st on st.key = match.SingleTracksId_id	left join trailHQ_mtbprojtrailid mtt on match.MTrailId_id = mtt.mtrailId	left join trailHQ_tfstatearea tfa on match.TfAreaId_id = tfa.Aid where st.key = %s",
    'detail':   "select s.name, s.difficulty, s.description, s.length, s.rating, s.url, tft.description as TFTDesc, tfi.name as TFName, tft.difficulty as TFTDiff, tft.lastReport as TFTRepor, tft.length as TFTLength, tft.climb as TFTClimb, tft.descent as TFTDescent, tft.area as TFTArea, tft.trailType as TFTType, tfa.regionDesc as TFADesc, tfa.regionDiff as TFADiff, tfa.localTrailGroup as TFAGroup, tfa.length as TFALen, tfa.vertical as TFAVert, tfa.numTrails as TFANum, mpt.description as MDesc, mpi.name as MName, mpt.orgs as MORgs, mpt.length as MLen, mpt.ascent as MAscent, mpt.descent as MDescent, mpt.highElev as MHelev, mpt.lowElev as MLelev, mpt.avgGrade as MAGr, mpt.maxGrade as MMGr from trailHQ_matches m left join trailHQ_singletrackstrail s on s.key = m.SingleTracksId_id left join trailHQ_tftrail tft on tft.id_id = m.TfTrailId_id left join trailHQ_tfarea tfa on tfa.id = m.TfAreaId_id left join trailHQ_mtbprojtr mpt on mpt.id_id = m.MTrailId_id left join trailHQ_tfid tfi on tfi.Tid = tft.id_id left join trailHQ_tfstatearea tfai on tfai.Aid = tfa.id left join trailHQ_mtbprojtrailid mpi on mpi.mtrailId = mpt.id_id where s.key = %s",
    'STsing': "select s.name, s.difficulty, s.description, s.length, s.rating, s.url, s.latitude, s.longitude from trailHQ_matches m left join trailHQ_singletrackstrail s on s.key = m.singleTracksId_id where m.singleTracksId_id = %s",
    'TFsing': "select tft.description as TFTDesc, tfi.name as TFName, tft.difficulty as TFTDiff, tft.lastReport as TFTRepor, tft.length as TFTLength, tft.climb as TFTClimb, tft.descent as TFTDescent, tft.area as TFTArea, tft.trailType as TFTType, tfi.url as URL from trailHQ_matches m join trailHQ_tftrail tft on tft.Tid_id = m.TfTrailId_id join trailHQ_tfid tfi on tfi.Tid = tft.Tid_id where m.singleTracksId_id = %s",
    'TFAsing': "select tfa.regionDesc as TFADesc, tfa.regionDiff as TFADiff, tfa.localTrailGroup as TFAGroup, tfa.length as TFALen, tfa.vertical as TFAVert, tfa.numTrails as TFANum, tfai.riding_area as Riding_Area, tfa.url as url from trailHQ_matches m join trailHQ_tfarea tfa on tfa.Aid_id = m.TfAreaId_id join trailHQ_tfstatearea tfai on tfai.Aid = tfa.Aid_id where m.singleTracksId_id = %s",
    'MBsing': "select mpt.description as MDesc, mpi.name as MName, mpt.orgs as MORgs, mpt.length as MLen, mpt.ascent as MAscent, mpt.descent as MDescent, mpt.highElev as MHelev, mpt.lowElev as MLelev, mpt.avgGrade as MAGr, mpt.maxGrade as MMGr, mpt.url as url from trailHQ_matches m join trailHQ_mtbprojtr mpt on mpt.Mid_id = m.MTrailId_id join trailHQ_mtbprojtrailid mpi on mpi.mtrailId = mpt.Mid_id where m.singleTracksId_id = %s",
}



'''
select s.name, s.difficulty, s.description, s.length, s.rating, s.url, tft.description as TFTDesc, tfi.name as TFName, tft.difficulty as TFTDiff, tft.lastReport as TFTRepor, tft.length as TFTLength, tft.climb as TFTClimb, tft.descent as TFTDescent, tft.area as TFTArea, tft.trailType as TFTType, tfa.regionDesc as TFADesc, tfa.regionDiff as TFADiff, tfa.localTrailGroup as TFAGroup, tfa.length as TFALen, tfa.vertical as TFAVert, tfa.numTrails as TFANum, mpt.description as MDesc, mpi.name as MName, mpt.orgs as MORgs, mpt.length as MLen, mpt.ascent as MAscent, mpt.descent as MDescent, mpt.highElev as MHelev, mpt.lowElev as MLelev, mpt.avgGrade as MAGr, mpt.maxGrade as MMGr from trailHQ_matches m
	left join trailHQ_singletrackstrail s on s.key = m.SingleTracksId_id
	left join trailHQ_tftrail tft on tft.id_id = m.TfTrailId_id
	left join trailHQ_tfarea tfa on tfa.id = m.TfAreaId_id
	left join trailHQ_mtbprojtr mpt on mpt.id_id = m.MTrailId_id
	left join trailHQ_tfid tfi on tfi.Tid = tft.id_id
	left join trailHQ_tfstatearea tfai on tfai.Aid = tfa.id
	left join trailHQ_mtbprojtrailid mpi on mpi.mtrailId = mpt.id_id
	where s.key = 2
'''
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


def get_or_none(classmodel, pk, id):
    try:
        kw = {id:pk}
        result = classmodel.objects.get(**kw)
        return result
    except classmodel.DoesNotExist:
        return None