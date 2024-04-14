from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import numpy as np 
from fastapi import HTTPException,status,Response

app=FastAPI()


class DataValidatorForPost(BaseModel):
    num1:int=0
    num2:int=0
    title:str="sum"
    result:bool=True
    return_type:Optional[int]=4
    id:int


post_db=[{"num1":1,"num2":2,"title":"average","result":1.5,"return_type":4,"id":1},
         {"num1":1,"num2":2,"title":"sum","result":3,"return_type":4,"id":2},
         {"num1":1,"num2":2,"title":"subtract","result":-1,"return_type":4,"id":3}]

@app.get("/")
def route():
    return "Welcome Back NooB!!!"

@app.get("/posts/GetPosts")
def route():
    return post_db

@app.get("/posts/Send")
def post_api():
    return {"Request Sent":"OK!!"} 


@app.post("/posts/CreatePost")
def create_post(payload:dict=Body(...),num=3):
    print(payload)

    return {"Post Message": "Post Request Activated -"}

@app.post("/posts/CreatePostWithValidator")
def CreatePostWithValidator(payload:DataValidatorForPost):
    dct=payload.model_dump(mode='dict')
    id=np.random.randint(4,1000)
    dct["id"]=id
    post_db.append(dct)
    return post_db


@app.get("/posts/GetPostsWithID/{id}")
def GetPostsWithID(id:int):

    for i in range(len(post_db)):
        if(post_db[i]["id"]==id):
            return post_db[i]
    
    return "Post Not Found"


@app.get("/posts/GetLatestPost")
def GetLatestPost():

    return post_db[-1]

@app.delete("/posts/DeletePost/{id}")
def DeletePost(id:int):
    
    for i in range(len(post_db)):
        if(post_db[i]["id"]==id):
            post_db.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id-{id} not found")


@app.put("/posts/UpdatePost")
def UpdatePost(post_detail:DataValidatorForPost):

    
    payload=post_detail.model_dump(mode='dict')
    print(payload)
    for i in range(len(post_db)):
        if(post_db[i]["id"]==payload["id"]):
            post_db[i]=payload
            return {"Message":f"Update for post with id-{post_detail.id} is done"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details=f"Your request for post id-{post_detail.id} not found in the DB")
    