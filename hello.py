from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal ,engine
from models import Base , User
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os


Base.metadata.create_all(bind=engine)




class Usercreate(BaseModel):
    name:Optional[str] =None
    email:Optional[str] =None
    age:Optional[int]   =None
    address:Optional[str] =None



app=FastAPI()

@app.get("/")
def home():
    return{"message:":"Hi"}

# create for databse access
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
#function post for create a rows in datbase
@app.post("/create_user")
def create(Usertable:Usercreate,db:Session=Depends(get_db)):
    new_user=User(
        name = Usertable.name,
        email = Usertable.email,
        age= Usertable.age,
        address=Usertable.address,
        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message":"add value in user table successfully created succesfully"}

# function for update all the instance of row all row update(uddate dawwod row)
@app.put("/update_user/{user_id}")
def update_user(user_id: int, user: Usercreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User nahi mila!")
    
    existing_user.name    = user.name
    existing_user.email   = user.email
    existing_user.age     = user.age
    existing_user.address = user.address
    
    db.commit()
    db.refresh(existing_user)
    return {"message": "User successfully updated!"}
#function for update some value of row(chnage ali district to tehsil)
@app.patch("/patch_user/{user_id}")
def patch_user(user_id: int, user: Usercreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User nahi mila!")
    
    if user.name    is not None: existing_user.name    = user.name
    if user.email   is not None: existing_user.email   = user.email
    if user.age     is not None: existing_user.age     = user.age
    if user.address is not None: existing_user.address = user.address
    
    db.commit()
    db.refresh(existing_user)
    return {"message": "User partially updated!"}

#function for delete row (delete saad)
@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User nahi mila!")
    
    db.delete(existing_user)
    db.commit()
    return {"message": "User successfully deleted!"}