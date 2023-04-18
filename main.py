"""
tutorial 1 introduction
from fastapi import FastAPI #class that provides functionality

app=FastAPI() #referenced by uvicorn

#use paths to separate concerns
#operations:post(create), get(read), put(update), delete(delete)
#@(decorator) announces that we do an above operation
@app.get("/") #https://example.com/items/foo, / se refera la ce e dupa example.com care e adresa IP
async def root(): #function that executes when this decorator is called
    # async, python can go and do something instead of waiting a await function
    return {"message": "Hello World"} #uvicorn running on -unde merge-
    #you can return any python object
#swagger ui cu /docs in coada adresei web
#sau /redoc in coada, dar alt ui
#/openapi.json pentru response schema, pe baza lui, se creaza UI-urile
"""
###
"""
tutorial 2 path parameters
from fastapi import FastAPI

app=FastAPI()
"""
"""
#foo replaces whatever is between {} whenever it appears
@app.get("/items/{item_id}") #example URL:http://127.0.0.1:8000/items/foo
async def read_item(item_id: int): #and we can have types, error if item_id is not an int here
    return {item_id: item_id}
#open with /docs (only http://dns name/docs) to try, you can do /redoc for another ui tool
"""
"""
@app.get("/users/me")   #this path need to be declared first because we do some unique operation with "me", but the other get can match with it
async def read_user_me():
    return {"user_id":"the current user"}
@app.get("/users/{user_id}")    #the first crud operation, python mathches, thats the one that it executes
async def read_user(user_id: str):
    return {"user_id": user_id}
"""
"""
@app.get("/users")          #the first one will not latch the second get to match anything
async def read_users():
    return ["Rick", "Morty"]
@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]
"""
"""
from enum import Enum

class ModelName(str, Enum): #declare an enum in python
    alexnet="alexnet"
    resnet="resnet"
    lenet="lenet"

#exercise with the docs
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): #the type is the enum, also a path parameter
    if model_name is ModelName.alexnet: #this is how you check if is in the enum, by invoking the enum class member
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet": #other way of checking by getting the value because is a string
        #instead of "lenet", could be ModelName.lenet.value
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
#every returned statement is converted into a string before being given back to the client
#path parameters can contain paths like /files/{file_path} with /files/home/johndoe/myfile.txt

#openAPI specification doesnt support the path op, but starlette (class inheritted by fastapi) does with /files/{file_path:path}
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
#You could need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).
#In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home
"""
###
"""
tutorial 3 - query parameters
from fastapi import FastAPI

app = FastAPI()
"""
"""
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10): #query parameters, trebuie dati prin url astfel:
    #http: // 127.0.0.1: 8000 / items /?skip = 0 & limit = 10 #pt ca le-am declarat pe ambele int-uri, vor fi validate si cu acele conditii
    #pentru ca skip and limit have values 0 and 10 in the function declaration, tjeir called defaults if we dont specify them in the url
    #http://127.0.0.1:8000/items/?skip=20 face overriding la valoarea de default a lui skip
    return fake_items_db[skip : skip + limit]
"""
"""
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None): #None, deci acum q este optional sa aiba o valoare in functie
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
"""
"""
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
#acum http://127.0.0.1:8000/items/foo?short= 1 sau True sau true sau on sau yes sau orice variatie de upper lower case letters, va pune short pe True
"""
"""
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
#putem avea si query si path parameters
"""
"""
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
#needy acum e require, altfel ne da eroare (n-are default-ul pe None)
#asta ar trebui sa mearga: http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
"""
"""
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
#avem query parameters required, optional si cu valori de default
"""
###
"""
Tutorial 4-Request body
#request body is the body similar that what we get from the api (response body), but we give it to the api from the clint with other
#operations besides get
#for request body, we will use pydantic library
"""
"""
from fastapi import FastAPI
from pydantic import BaseModel #class to make other objects for schema for request body


class Item(BaseModel):  #schema class that inherits from the dedicated calss
    name: str                       #required
    description: str | None = None  #optional
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item): #query parameter
    return item
#url work for get operations #for post, we need to go to swagger ui
"""
"""
both good in swagger ui
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
{
    "name": "Foo",
    "price": 45.2
}
"""
#pydantic objects enjoys auto-completition
"""
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
#access directly of item attributes, seen above
"""
"""
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
#You can declare path parameters and request body at the same time.

#FastAPI will recognize that the function parameters that match path parameters should be taken from the path, and that function parameters that are declared to be Pydantic models should be taken from the request body.
"""
"""
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
#You can also declare body, path and query parameters, all at the same time.

#FastAPI will recognize each of them and take the data from the correct place.
"""
###
"""
#chapter Query Parameters and String Validations (i dont think i did this in the lab)
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(q: str | None = None): #q has the type: Union[str, None] (or str | None in Python 3.10)
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
"""
###
"""
same for chapter: Path Parameters and Numeric Validations
"""
###
"""
# capitol 5 - Body - Multiple Parameters
# skip Mix Path, Query and body parameters sub-chapter
In the previous example, the path operations would expect a JSON body with the attributes of an Item, like:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
In this case, FastAPI will notice that there are more than one body parameters in the function (two parameters that are Pydantic models).

So, it will then use the parameter names as keys (field names) in the body, and expect a body like:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
Notice that even though the item was declared the same way as before, it is now expected to be inside of the body with a key item.
FastAPI will do the automatic conversion from the request, so that the parameter item receives it's specific content and the same for user.

It will perform the validation of the compound data, and will document it like that for the OpenAPI schema and automatic docs.

skip the other sub-chapters because I never did them in the first lab
"""

















