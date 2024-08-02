from fastapi import FastAPI

app=FastAPI()

@app.get('/hello')
async def root():
    return{"message":"Hello World"}

@app.get('/')
async def sunil():
    return{"message":"Hello Welocome to fastapi tutorial"}