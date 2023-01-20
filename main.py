from fastapi import FastAPI
from fastapi.requests import Request
from models import UserData, getData, delData

app = FastAPI()

retJson = {
    'name': None,
    'surname': None,
    'patronymic_': None,
    'phone_number': None,
    'email_': None,
    'country': None,
    'country_code': None,
}

@app.post("/save_user_data")
async def saveUserData(request: Request):
    sender = UserData(await request.json())
    er = sender.examination()
    if er is not None:
        return er
    res = sender.addData()
    return res

@app.post("/get_user_data")
async def getUserData(request: Request):
    returnUserData = retJson
    sender = UserData(await request.json())
    res = getData(request.json()['phone_number'])
    if res is None:
        return 'Данного номер нет в базе'
    for i, key in enumerate(returnUserData.keys()):
        returnUserData[key] = res[i]
    return returnUserData

@app.post("/delete_user_data")
async def delUserData(request: Request):
    res = delData(request.json()['phone_number'])   
    if res is None:
        return 'Данного номер нет в базе'
    return res
