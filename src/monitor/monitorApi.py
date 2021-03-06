# encoding:utf-8
# 外部文件引入
import src.crabapple as crab

# list monitor
def getMonitors(req):
    userId=crab.checkToken(req)
    if userId==-1:
        return crab.responseMsg(0, "Your identity is not identified!")
    sql = "SELECT * FROM monitor"
    try:
        values = req.get_json()
        sql += (" WHERE"+crab.getByConditions(values))
    except:
        sql = sql
    try:
        res = monitorPojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get monitor information failure!")


def monitorPojo(data):
    pojoModel = ['monitor_id','device_id', 'identification', 'value', 'create_time']
    return crab.toList(pojoModel, data)