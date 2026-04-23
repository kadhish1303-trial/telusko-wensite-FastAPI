from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Product
from database import session, engine
import database_model
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)


#the below line will create tables on its own 
database_model.Base.metadata.create_all(bind = engine )
    #metadatawill all the info about the talbe, columns, data types etc

@app.get("/")
def greeet():
    #print("Welcome to backend") ---> this will print the message on terminal so we use "return"
    return "Welcome to backend"

products = [
    Product(id = 1,name = "Phone", description = "budget phone", price = 99, quantity = 10),
    Product(id = 2,name ="Laptop", description =  "budge Laptop", price = 999, quantity = 10),
    Product(id = 3,name ="Table", description =  "budge table", price = 10, quantity = 100),
    Product(id = 4,name ="Pen", description =  "budge pen", price = 9, quantity = 10),
    Product(id = 5,name ="iphone", description =  "budge phone", price = 999, quantity = 10)
]

def get_db():
    db = session() # crearing th db
    try:
        yield db        #waiting for others to use it 
    finally:
        db.close()      #then closing the db


def init_db():
    db = Session()
    print("--- DATABASE SYNC STARTING ---")
    count = db.query(database_model.Product).count
    if count == 0:

        for product in products:
            # This will print every time it tries to add something
            print(f"Syncing: {product.name}") 
            db.add(database_model.Product(**product.model_dump()))
            #**product.model_dump() 
                    #--> model_dump() - will give you dictonary
                    #--> ** - will unpack the dictonary into key value pair
    
    db.commit()
    print("--- DATABASE SYNC COMPLETE ---")
    db.close()

init_db()


#If a person adds wrong info foe ex Budget = -1000 which wrong since it in negative for this we have to do DATA VALIDATION 
#So for that data validation we will add a library in model.py i.e. "pydantic" 
@app.get("/products")   #get request to fetch all the products
def get_all_products(db : Session = Depends(get_db)):
    #rather than manually writing the products we can also fetch the products from database but for that we have to add a library "sqlalchemy" in our project
    #db connection 
    #query to fetch all the data from database
    #db = session()
    #db.query()
    db_products = db.query(database_model.Product).all()
    return db_products

#searching a product using the id
@app.get("/product/{id}")
def get_product_by_id(id : int, db : Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()         
    if(db_product):
            return db_product
        
    return "Product not found"

#adding new product
@app.post("/products")
def add_product(product : Product, db : Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

#updating a product  
@app.put("/products")
def update_product(id : int, product : Product, db : Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "No product Found"   
    

#in this funct we are deleting a product using id
@app.delete("/products")
def delete_product(id : int, db : Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "Product not found"