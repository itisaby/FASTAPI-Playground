from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel # Pydantic is used to make schemas
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    #it's doing all the kind of validations we need (Pydantic)
    title: str
    content: str
    published: bool = True  #default value
    rating: Optional[int] = None #Optional Value

#@app.get -> Method , ("/") -> path

@app.get("/")
async def root():
    return {"message": "Welcome to fast API"}

@app.get("/posts")
def get_posts():
    return {"data" : "This is your posts"}

# Without using schemas
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):   #Payload 
    # print(payLoad)
    # return {
    #     "message": "successfully created post",
    #     "new_post": f"title {payLoad['title']} content: {payload['content']}"
    # }

#By using Schemas
@app.post("/createposts")
def create_posts(new_post: Post):  
    print(new_post)
    print(new_post.title)
    print(new_post.dict())
    return {"data" : "new post"}


#tile strr, content str

# We need a schema for proper validation 