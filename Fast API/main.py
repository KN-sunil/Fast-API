from fastapi import FastAPI,Query,Path,Body
from enum import Enum
from typing import Optional
from pydantic import BaseModel

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