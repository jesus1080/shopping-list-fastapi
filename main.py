import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException, status
from app.model.model import ProductSchema, UserSchema, UserLoginSchema, ProductUpdate, ProductListSchema, ProductToList, ProviderSchema
from typing import Annotated
from app.model import model_db
from app.auth.jwt_handler import signJWT, decodeJWTT
from app.auth.jwt_bearer import jwtBearer
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
model_db.Base.metadata.create_all(bind=engine)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependeny = Annotated[Session, Depends(get_db)]



#------Product-------------------------------------------------------------------------------
# Get Products
@app.get("/products", status_code=status.HTTP_200_OK, tags=["products"])
async def get_products(db : db_dependeny):
    products = db.query(model_db.Product).all()
    return products

# Get single product
@app.get("/products/{id}", status_code=status.HTTP_200_OK, tags=["products"])
async def get_one_product(id : int, db : db_dependeny):
    product = db.query(model_db.Product).filter(model_db.Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not foun, perro no esta!")
    return product

# Create new product
@app.post("/products", dependencies=[Depends(jwtBearer())], tags=["products"])
async def add_product(product : ProductSchema, db : db_dependeny):
    db_product = model_db.Product(**product.model_dump())
    db.add(db_product)
    db.commit()

# Delete product 
@app.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["products"])
def delete_product(product_id: int, db: db_dependeny):
    product = db.query(model_db.Product).filter(model_db.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto not found! Periito")
    db.delete(product)
    db.commit()

# Update product 
@app.put("/products/{id}", tags=["products"])
def update_product(id : int, product_data: ProductUpdate, db : db_dependeny):
    product = db.query(model_db.Product).filter(model_db.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto not found! Periito")
    
    product.name = product_data.name
    product.price = product_data.price
    db.commit()
    db.refresh(product)

#-----User-----------------------------------------------------------------------
# User Signup { Create a new user}
@app.post("/user/signup", status_code=status.HTTP_200_OK,tags=["user"])
async def user_create(user : UserSchema, db : db_dependeny):
    db_user = model_db.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return signJWT(user.email)

@app.post("/user/login", tags=["user"])
def user_login(data: UserLoginSchema, db : db_dependeny):
    user = db.query(model_db.User).filter(model_db.User.email == data.email and model_db.User.password == data.password)
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid login details")
    return signJWT(data.email)

# user auth
@app.post("/user/yo/")
async def user_current(token : str, db : db_dependeny):
    token_decode = decodeJWTT(token)
    if token_decode:
        user = db.query(model_db.User).filter(model_db.User.email == token_decode["userID"]).first()
        return user.id
    else:
        return {'error' : 'token na valido perroo'}


#-----Provedor----------------------------------------------------------------------
# Create provider
@app.post("/provider", dependencies=[Depends(jwtBearer())], tags=["providers"])
async def add_provider(provider : ProviderSchema, db : db_dependeny):
    db_provider = model_db.Provider(**provider.model_dump())
    db.add(db_provider)
    db.commit()

# Get providers
@app.get("/provider", status_code=status.HTTP_200_OK, tags=["providers"])
async def get_providers(db : db_dependeny):
    providers = db.query(model_db.Provider).all()
    return providers

#-----BuyList------------------------------------------------------------ 

# Create list_products
@app.post("/list/", status_code=status.HTTP_200_OK, tags=["list-products"])
async def list_create(list : ProductListSchema, db : db_dependeny):
    db_list = model_db.ProductList(**list.model_dump())
    db.add(db_list)
    db.commit()

# Get list
@app.get("/lists/", status_code=status.HTTP_200_OK, tags=["list-products"])
async def get_lists(db : db_dependeny):
    lists = db.query(model_db.ProductList).all()
    return lists

# Add Product to list

@app.post("/producttolist/", tags=["list-products"])
def add_product_tolist(data: ProductToList, db : db_dependeny):
    list = db.query(model_db.ProductList).filter(model_db.ProductList.id == data.id_list).first()
    product = db.query(model_db.Product).filter(model_db.Product.id == data.id_product).first()
    
    if list is None or product is None:
        raise HTTPException(status_code=404, detail="Invalid login details")
    
    product.product_list_id = data.id_list
    
    db.commit()
    db.refresh(product)

# Delete Product to list
@app.post("/producttolist/delet/", tags=["list-products"])
def delet_product_tolist(data: ProductToList, db : db_dependeny):
    list = db.query(model_db.ProductList).filter(model_db.ProductList.id == data.id_list).first()
    product = db.query(model_db.Product).filter(model_db.Product.id == data.id_product).first()
    
    if list is None or product is None:
        raise HTTPException(status_code=404, detail="Invalid login details")
    
    product.product_list_id = 0
    
    db.commit()
    db.refresh(product)