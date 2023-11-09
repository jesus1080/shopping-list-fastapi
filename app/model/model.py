from pydantic import BaseModel, Field, EmailStr
from datetime import date

class ProductSchema(BaseModel):
    name: str = Field(default=None)
    price: float = Field(default=None)
    date_creation: date = Field(default=None)
    id_provider: int = Field(default=None)
    class Config:
        json_schema_extra = {
            "producto" : {
                "name" : "papas",
                "price" : 3500,
                "date_creation" : "2008-09-15"
            }
        }

class ProductUpdate(BaseModel):
    name: str = Field(default=None)
    price: float = Field(default=None)
    class Config:
        json_schema_extra = {
            "producto" : {
                "name" : "papas",
                "price" : 3500,
            }
        }

class UserSchema(BaseModel):
    fullname : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        json_the_schema = {
            "user_fake" : {
                "fullname" : "Simon",
                "email" : "simon@email.com",
                "password": "123"
            }
        }

class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        json_the_schema = {
            "user_fake" : {
                "email" : "simon@email.com",
                "password": "123"
            }
        }

class ProductListSchema(BaseModel):
    name : str = Field(default=None)
    id_user : int = Field(default=None)
    class Config:
        json_the_schema = {
            "list_product" : {
                "name" : "Simon",
                "id_user" : 1,
            }
        }

class ProductToList(BaseModel):
    id_product : int = Field()
    id_list : int = Field()
    

class ProviderSchema(BaseModel):
    name : str = Field(default=None)
    date_creation: date = Field(default=None)