from fastapi import FastAPI,Query,Path,Body,Cookie,Header,status,Form,File,UploadFile,HTTPException,Request
from fastapi.responses import JSONResponse,PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarlettHTTPException
from enum import Enum
from typing import Optional,Literal,Union
from pydantic import BaseModel,Field,HttpUrl,EmailStr      
from datetime import datetime, time, timedelta
from uuid import UUID

app = FastAPI()

'''
@app.get('/hello')
async def root():
    return {"message": "Hello World"}


@app.get('/')
async def sunil():
    return {"message": "Hello Welocome to fastapi tutorial"}


# ----------------------
# path parameter

# @app.get("/item{Item}")
# def path_fun(Item):
#     var_name={"path_variable":Item}
#     return(var_name)


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}

    if food_name.value == "fruits":
        return {"food_name": food_name, "message": "you are healthy but still like sweet"}

    return {"food_name": food_name, "message": "you like dairy you are unhealthy"}


fake_items_db = [{"item_name": "foo"}, {"item_name": "bar"}, {"item_name": "baz"}]


# @app.get("/items")
# async def list_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


# if we want to make some query parameters optional

# @app.get("/items/{item-id}")
# async def get_item(item_id : str, q:str |None=None):
#     if q:
#         return {"item_id":item_id,"q":q}
#     return {"item_id":item_id}

@app.get("/items/{item_id}")
async def get_item(item_id: str, sample_query_param: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "sample_query_param": sample_query_param}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus justo."
            }
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
        user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus justo."
            }
        )
    return item


# requestbody
# ------------------------------------------------------------------------------

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items")
# async def read_items (q: str | None=Query(None,min_length=2,max_length=10,regex="^fixedquery$")):

# if want set default query        defaultquery
# async def read_items(q: str=Query("fixedquery", min_length=2,max_length=10,)): 


# if we want optional parameter we should give like this below
#                           optional parameter        
# async def read_items(q: str |None = Query(None)):     

# there is no default value but it has to be something means we should write like below(... denotes there is no default but it has to be something)
# async def read_items(q: str = Query(...,min_length=2,max_length=10)):   


# if route (localhost 8000/items?q=a&q=b&q=c&q=d) this gives q=d.if we want to allow multiple values/options do like below list[str]
# and below Query(["foo","bar"]) denotes default query
# async def read_items(q: list[str]=Query(["foo","bar"])):                                         


async def read_items (q: str | None=Query(
    None,
    min_length=2,
    max_length=10,
    title="sample query string",
    description="this is a sample query string",
    alias="item_query",
    )):
    results = {"items": [{"items_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_hidden")
async def hidden_query_route(
    hidden_query: str |None = Query(None,include_in_schema=False)
):
    if hidden_query:
        return{"hidden_query":hidden_query}
    return{"hidden_query":"not found"}


@app.get("/items_validation/{item_id}")
async def read_items_validation(
   *,
   item_id: int =Path(...,title="the id of the item to get",ge=10,le=100),
   q:str,
):
    results = {"item_id":item_id}
    if q:
        results.update({"q":q})
    return results    

'''

# part7--body multiple parameter
'''
class Item(BaseModel):
    name: str
    description: str |None = None
    price: float
    tax: float |None = None

class User(BaseModel):
    username: str
    full_name: str| None = None

class Importance(BaseModel):
    importance: int    


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(...,title="the id of the item to get",ge=0,le=150),
    q: str | None = None,
    item: Item  ,
    user: User,
    importance: int = Body(...)
):
    results = {"item_id":item_id}
    if q:
        results.update({"q":q})
    if item:
        results.update({"item":item}) 
    if  user:
        results.update({"user":user})  
    if importance:
        results.update({"importance":importance})       
    return results    
'''



''' Body-Fields'''

'''
class  Item(BaseModel):
    name: str
    description: str | None = Field(
        None,title="the description of the item",max_length=300
    )
    price: float=Field(...,gt=0, description="the price must be grater than zero.")
    tax: float |None = None

@app.put("/items/{item_id}")
async def update_item(item_id:int ,item:Item = Body(...,embed=True)):
    results={"item_id":item_id,"item":item}
    return results  

'''

# Body-Nested Models
'''
class Image(BaseModel):
    url:HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None =None
    price:float
    tax: float |None = None
    tags: set[str] = set()
    # tags: list[int] = []
    image:list[Image] |None = None

class Offer(BaseModel):
    name: str
    description: str |None = None
    price:float
    items: list[Item]        # model inside the model 

@app.put("/items/{item_id}")
async def update_item(item_id:int,item:Item):
    results = {"item_id":item_id,"item":item}
    return results

@app.post("/offers")
async def create_offer(offer:Offer= Body(...,embed = True)):
    return offer

@app.post("/images/multiple")
async def create_multiple_images(images:list[Image]):
    return images
@app.post("/blah")
async def create_some_blahs(blahs:dict[int, float]):
    return blahs

 '''

 # declare request example data :3 ways we can declare example data
'''
class Item(BaseModel):
    name:str = Field(...,example="foo")
    description:str |None=Field(None, example="a very nice item")               #second way
    price:float = Field(...,example=16.25)
    tax: float |None=Field(None,example = 1.62)
  '''
# class Item(BaseModel):
#     name:str 
#     description:str |None=None
#     price:float 
#     tax: float 

    # class Config:
    #     json_schema_extra={
    #          "example":{                                    #first way
    #             "name":"foo",
    #             "description":"A very nice item",
    #             "price":16.6,
    #             "tax":1.67,
    #         }
    #     }
'''
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id:int, item:Item = Body(
    openapi_examples={  
        "normal":{  
            "summary":"A normal example",
            "description":"A **normal** item works correctly.",
            "value":{
                "name":"foo",
                "description":"A very nice item",
                "price":36.25,
                "tax":1.62,
            },                                                                    #third way
            
        },
        "Converted":{
            "summary":"An example with converted data",
            "description":"FastAPI can convert price `strings` to actual `numbers` automatically",
            "value":{"name":"Bar","price":35.4,}
        },
        "invalid":{
            "summary":"Invalid data is rejected with an error",
            "value":{"name":"Baz","price":"thirty five point four", }
        },
    },
),
):
    results={"item_id":item_id,"item":item}
    return results       
    '''

# extra data types
'''
@app.put("/items/{item_id}")
async def read_items(
    item_id:UUID,
    start_date: datetime |None=Body(None),
    end_date: datetime | None=Body(None),
    repeat_at: time |None = Body(None),
    process_after: timedelta |None = Body(None),

):
    start_process = start_date + process_after
    duration = end_date -start_process
    return{
         "item_id": item_id,
         "start_date":start_date,
         "end_date":end_date,
         "repeat_at": repeat_at,
         "process_after": process_after,
         "start_process":start_process,
         "duration":duration,
    }

'''
#cookie and header parameters
'''
@app.get("/items")
async def read_items(
   cookie_id: str |None= Cookie(None),
   accept_encoding: str |None= Header(None),
   sec_ch_ua: str |None =Header(None),
   user_agent:str |None = Header(None),
   x_token: list[str] |None = Header(None),
):
    return{
        "cookie_id":cookie_id,
        "accept_encoding": accept_encoding,
        "sec_ch_ua":sec_ch_ua,
        "user_agent": user_agent,
        "x_token":x_token,
    }

'''

# Response model
# we need to install  package pip install pydantic[email] for cdemailstr
'''
class Item(BaseModel):
    name: str
    description: str |None = None
    price: float
    tax: float = 10.5
    tags:list[str]=[]

@app.post("/items/",response_model=Item)
async def create_item(item:Item):
    return item

class UserBase(BaseModel):
    username: str
    email:EmailStr
    full_name:str |None = None

class UserIN(UserBase):
    password:str

class UserOut(UserBase):
    pass        
    
@app.post("/users/",response_model=UserOut)
async def create_user(user:UserIN):
    return user

'''

'''
class Item(BaseModel):
    name: str
    description: str |None = None
    price: float
    tax: float = 10.5
    tags:list[str]=[]

items = {
    "foo":{"name":"Foo","price":50.2},
    "bar":{"name":"Bar","description":"the bar tenders","price":62,"tax":20.2},
    "baz":{"name":"Baz","description":None,"price":50.2,"tax":10.5,"tags":[]},
}   

@app.get("/items/{item_id}",response_model=Item,response_model_exclude_unset=True)
async def read_item(item_id: Literal["foo","bar","baz"]):
    return items[item_id]

@app.get(
    "items/{item_id}/name",
    response_model=Item,
    response_model_include={"name","description"}    
         )
async def read_item_name(item_id:Literal['foo','bar','baz']):
    return items[item_id]

@app.get("/items/{item_id}/public",response_model=Item,response_model_exclude={"tax"})
async def read_items_public_data(item_id:Literal['foo','bar','baz']):
    return items[item_id]

'''    
# part 14 - Extra models
'''
class UserBase(BaseModel):
    username:str
    email: EmailStr
    full_name:str |None = None 

class UserIn(UserBase):
    password: str
   

class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
    
   

def fake_password_hasher(raw_password:str):
    return f"supersecret{raw_password}" 

def fake_save_user(User_in:UserIn):
    hashed_password= fake_password_hasher(User_in.password)
    user_in_db = UserInDB(**User_in.dict(),hashed_password=hashed_password)
    print("User 'saved'.")
    return user_in_db

@app.post("/user/",response_model=UserOut)
async def create_user(user_in:UserIn):
    user_saved=fake_save_user(user_in)
    return user_saved       


class BaseItem(BaseModel):
    description: str
    type:str

class CarItem(BaseItem):
    type:str="car"

class PlaneItem(BaseItem):
    type:str="plane" 
    size:int

items={
    "item1":{"description":"all my friends drive a low rider","type":"car"},
    "item2":{
        "description":"music is my aeroplane,its my aeroplane",
        "type":"plane",
        "size":5,
    }
}   

@app.get("/items/{item_id}",response_model=Union[PlaneItem, CarItem])
async def read_item(item_id:Literal["item1","item2"]):
    return items[item_id]


class ListItem(BaseModel):
    name: str
    description: str

list_items=[
    {"name":"foo","description":"there comes my hero"},
    {"name":"red","description":"its my aeroplane"},

]
@app.get("/list_items/",response_model=list[ListItem])
async def read_items():
    return items

@app.get("/arbitrary", response_model=dict[str,float])
async def get_arbitrary():
    return{"foo":1,"bar":"2"}

'''

# Response status code
# @app .post("/items/",status_code=201)  #by default status code is 200
# async def create_item(name:str):
#     return{"name":name}

# @app.delete("/items/{pk}",status_code=204) #status code 204 means no content if there is a content also it wont dispaly
# async def delete_item(pk: str):
#     print("pk",pk)

# @app.get("/items/",status_code=401)
# async def read_items_redirect():
#     return{"helloo":"world"}    


 
# @app .post("/items/",status_code=status.HTTP_201_CREATED)  
# async def create_item(name:str):
#     return{"name":name}

# @app.delete("/items/{pk}",status_code=status.HTTP_204_NO_CONTENT) 
# async def delete_item(pk: str):
#     print("pk",pk)

# @app.get("/items/",status_code=status.HTTP_302_FOUND)
# async def read_items_redirect():
#     return{"helloo":"world"}    
 

# Part 16-Form fields:
# (we need to install pip install python-multipart)


# @app.post("/login/")
# async def login(username:str = Form(...),password: str = Form(...)):
#     print("password",password)
#     return{"usernmae":username}

# @app.post("/login-json/")
# async def login_json(username: str = Body(...),password:str = Body(...)):
#     print("password",password)
#     return{"username:username"}
 

#  PART 17 REQUEST FILES

# @app.post("/files/")
# async def create_field(
#     files:list[bytes]= File(...,description="A file read as bytes")

# ):
#     return {"file_size":[len(file) for file in files]}

# @app.post("/uploadfile/")
# async def create_upload_file(
#     files: list[UploadFile]=File(..., description="a file read as upload file")
# ):
#     return{"filename":[file.filename for file in files]}

# part 18 (request)
# request forms and files
'''
@app.post("/files/")
async def create_file(
file:bytes =File(...),
fileb:UploadFile = File(...),
token: str = Form(...),
hello: str = Body(...),
):
    return{
        "file_size":len(file),
        "token":token,
        "fileb_content_type": fileb.content_type,
        "hello":hello,
    }

   ''' 

# Part 18 Handling Errors


# items={"foo":"The foo wrestlers"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404,detail="Item not found",headers={"x-Error":"there goes my error"}) #using httpexception we can rise custom error
#     return{"item":items[item_id]}

# we need to import request from fastapi and from fastapi.responses import HTML_Response

# class UnicornException(Exception):
#     def __init__(self,name:str):
#         self.name=name

# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request:Request,exc:UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message":f"Oops! {exc.name} did something.there goes a rainbow..."}
#      )

# @app.get("/unicorns/{name}")
# async def read_unicorns(name:str):
#     if name == "yolo":
#         raise UnicornException(name=name) 
#     return {"unicorn_name":name}       


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request,exc):    #  THIS GIVES DETAIL ERROR MESSEGE
#     return PlainTextResponse(str(exc),status_code=400)

# @app.exception_handler(StarlettHTTPException)
# async def http_exception_handler(request,exc):
#     return PlainTextResponse(str(exc.detail),status_code=exc.status_code)

# @app.get("/validation_items/{item_id}")
# async def read_validation_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418,detail="Nope! i dont like 3")
#     return {"item_id":item_id}


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request:Request,exc:RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail":exc.errors(),"blahblah":exc.body})
#     )

# class Item(BaseModel):
#     title: str
#     size:int

# @app.post("/items/")
# async def create_item(item:Item):
#     return item    

'''

@app.exception_handler(StarlettHTTPException)
async def custom_http_exception_handler(request,exc):
    print(f"OMG! AN HTTP error!:{repr(exc)}")
    return await http_exception_handler(request,exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request,exc):
    print(f"OMG! the client sent invalid data!:{exc}")
    return await request_validation_exception_handler(request,exc)

@app.get("/blah_items/{item_id}")
async def read_items(item_id:int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! i dont like 3")
    return{"item_id":item_id}

'''

# Path operation ocnfiguration

# class Item(BaseModel):
#     name: str
#     description: str| None = None
#     price: float
#     tax: float |None = None 
#     tags: set[str]= set()

# class Tags(Enum):
#     items="items"
#     users="users"    

# @app.post("/items/",
#         response_model=Item,
#         status_code=status.HTTP_201_CREATED,
#         tags=[Tags.items],
#         summary="Create an Item-type item",
#         # description="Create an item with all the information:"
#         # "name; description; price; tax; and a set of "
#         # "unique tags",
#         response_description="The created item",
#         )
# async def create_item(item:Item):
#     """
#     Create an item with all the information:

#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax** : if the item doesnt have tax,tou can omit this
#     - **tags**: a set of unique tag strings for this item

#     """
#     return item

# @app.get("/items/",tags=[Tags.items])
# async def read_items():
#     return [{"name":"Foo","price":42}]

# @app.get("/users",tags=[Tags.users])
# async def read_users():
#     return[{"username":"phoebebuffy"}] 

# @app.get("/elements/",tags=[Tags.items],deprecated=True)   #depricated means it no longer anactive use but we can use
# async def read_elements():
#     return[{"item_id":"foo"}]

# Part-21 Json compatible Encoder and Body -Updates
# first thing is handling data and converting into json format
'''
fake_db={}

class Item(BaseModel):
    title:str
    timestamp :datetime
    description: str | None= None

@app.put("/items/{id}")
async  def update_item(id:str,item:Item):
    fake_db[id]=item
    print(fake_db)
    return "success"    

'''

class Item(BaseModel):
    name:str |None = None
    description: str |None = None
    price: float |None =None
    tax: float =10.5
    tags: list[str]=[]


items={
    "foo":{"name":"Foo","price":50.2},
    "bar":{"name":"Bar","description":"the bar tenders","price":62,"tax":20.2},
    "baz":{"name":"Baz","description":None,"price":50.2,"tax":10.5,"tags":[]},

}    

@app.get("/items/{item_id}",response_model=Item)
async def read_item(item_id:str):
    return items.get(item_id)

@app.put("/items/{item_id}",response_model=Item)
async def update_item(item_id:str,item:Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id]=update_item_encoded
    return update_item_encoded

@app.patch("/items/{item_id}",response_model=Item)
def patch_item(item_id: str, item: Item):
    stored_item_data= items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Item(**stored_item_data)
    else:
        stored_item_model = Item()
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id]= jsonable_encoder(updated_item)
    return updated_item    
