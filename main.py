
from fastapi import FastAPI, Request,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pydantic import BaseModel
app=FastAPI()
app.mount("/static",StaticFiles(directory='static'),name='static')
templates=Jinja2Templates(directory='templates')
conn=MongoClient('mongodb://localhost:27017/')
class Note(BaseModel):
    notes:str

@app.get("/",response_class=HTMLResponse)
async def sayhelloworld(request: Request):
    
    return templates.TemplateResponse('a.html',{'request':request})
# @app.get("/getnotes")
# async def getnotes(request: Request):
#     mydata = conn['Notes']['Notes'].find({})
#     newdata=[]
#     for i,doc in enumerate(mydata):
#         if doc:
#             doc["_id"] = str(doc["_id"])
#         print(doc)
#         newdata.append({
#             f"id{i+1}":doc["_id"],
#             "notes":doc["notes"]
#         })
#     return newdata
@app.get("/getnotes",response_class=HTMLResponse)
async def getdata(request:Request):
    newdata=[]
    fetchdata=conn.Notes.Notes.find({})
    for i in fetchdata:
        if i:
            i["_id"]=str(i["_id"])
        newdata.append({
            "id":i["_id"],
            "notes":i["notes"]
        })
    print(newdata)
    return templates.TemplateResponse('a.html',{"request":request,"data":newdata})

# the [post]  service is note working
@app.post("/addnotes",response_class=HTMLResponse)
async def addnote(request: Request):
    forms=await request.form()
    forms_dict=dict(forms)
    conn.Notes.Notes.insert_one(forms_dict)
    
    return templates.TemplateResponse('a.html',{"request":request,"message": "The data has been added."})

# @app.get("/item/{item_id}")
# def readitem(item_id:int,q:str|None=None):
#     return {"item_id": item_id, "q": f"{'please add some string' if q is None else q}"}

