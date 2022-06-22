from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel # Pydantic is used to make schemas
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    #it's doing all the kind of validations we need (Pydantic)
    title: str
    content: str
    published: bool = True  #default value
    rating: Optional[int] = None #Optional Value

#Storing data in a memory that's an array for now 
my_posts = [{
    "title": "title of post 1", "content": "content of post 1", "id": 1
},
{
    "title": "Cookies", "content": "content of post 2", "id": 2
}
]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#@app.get -> Method , ("/") -> path

@app.get("/")
async def root():
    return {"message": "Welcome to fast API"}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

# Without using schemas
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):   #Payload 
    # print(payLoad)
    # return {
    #     "message": "successfully created post",
    #     "new_post": f"title {payLoad['title']} content: {payload['content']}"
    # }

#By using Schemas
@app.post("/createposts", status_code = status.HTTP_201_CREATED)   #201 is used as it's a default status code for creation
def create_posts(new_post: Post):  
    print(new_post)
    print(new_post.title)
    print(new_post.dict())
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

#getting the latest post 
@app.get("/posts/latest")
def get_latest_post():
    latest = my_posts[len(my_posts)-1]
    return {
        "detail": latest
    }

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = find_posts(id)
    print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND  #For diplaying the status code 404
        # return {"message" : f"Post with {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with {id} was not found") #Using FastAPI we get this in one line 
    return{"post_detail" : post}


#tile strr, content str

# We need a schema for proper validation 


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT) #204 is the status code for no data back
def delete_post(id : int):
    #deleting post
    #find index in the array and pop
    index = find_index_post(id)
    if index == None:
        return HTTPException(status_code=404, detail=f"post with {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
    if index == None:
        return HTTPException(status_code=404, detail=f"post with {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{
        "message": "Updated post",
        "data": post_dict
    }
