from fastapi import FastAPI
from model import Product
from database import Session, engine
import database_model

app = FastAPI()
#the below line will create tables on its own 
database_model.Base.metadata.create_all(bind = engine )

@app.get("/")
def greeet():
    #print("Welcome to backend") ---> this will print the message on terminal so we use "return"
    return "Welcome to backend"

products = [
    Product(id = 1,name = "Phone", description = "budget phone", price = 99, quantity = 10),
    Product(id =2,name ="Laptop", description =  "budge Laptop", price = 999, quantity = 10),
    Product(id =3,name ="Table", description =  "budge table", price = 10, quantity = 100),
    Product(id =4,name ="Pen", description =  "budge pen", price = 9, quantity = 10)
]

#def init_db():





#If a person adds wrong info foe ex Budget = -1000 which wrong since it in negative for this we have to do DATA VALIDATION 
#So for that data validation we will add a library in model.py i.e. "pydantic" 
@app.get("/products")   #get request to fetch all the products
def get_all_products():
    #rather than manually writing the products we can also fetch the products from database but for that we have to add a library "sqlalchemy" in our project
    #db connection 
    #query to fetch all the data from database
    db = Session()
    db.query()
    return products

#in this funt we are trying to search the product using the id
@app.get("/product/{id}")
def get_product_by_id(id : int):
    for product in products:        #this will iterate through the list "products" and checks the id that is being menstioned is there in that list or not 
        if(product.id == id):
            return product
        
    return "Product not found"

#in this funct we are adding a new product
@app.post("/product")
def add_product(product : Product):
    products.append(product)
    return product

#in this funct we are updating a product which already there 
@app.put("/product")
def update_product(id : int, product : Product):
    for i in range(len(products)):
         if(products[i].id == id):
             products[i] = product
             return "Product Added Succesfully" 
    return "No product Found"

#in this funct we are deleting a product using id
@app.delete("/product")
def delete_product(id : int):
    for product in products:
        if(product.id == id):
            products.remove(id)
            return "Product Deleted Successfuly"
    return "Product not found"