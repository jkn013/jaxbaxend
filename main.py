from fastapi import FastAPI
key = "placeholder"
app = FastAPI()
@app.get("/read")
def read_root():
    return {"key": key}
@app.get("/add")
def add(q: str):
    global key
    key = q
    return {"received": q}
