from fastapi import FastAPI
from fastapi.requests import Request
from models import UserData, interactionData
import uvicorn
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

@app.get("/")
def read_root():
    return {"UserData"}

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
    IData = interactionData(await request.json())
    res = await IData.getData()
    if res is None:
        return 'Данного номер нет в базе'
    for i, key in enumerate(returnUserData.keys()):
        returnUserData[key] = res[i]
    return returnUserData

@app.post("/delete_user_data")
async def delUserData(request: Request):
    IData = interactionData(await request.json())   
    res = await IData.delData()
    if res is None:
        return 'Данного номер нет в базе'
    return res
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

