from fastapi import FastAPI, HTTPException, Request, Query, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from typing import List, Optional
from sqlalchemy.orm import sessionmaker, declarative_base
from uvicorn import Config, Server
import traceback, subprocess, pyperclip, firebase_admin, os
from firebase_admin import credentials, firestore
from sqlalchemy import MetaData, Table
from cryptography.fernet import Fernet
from pydantic import BaseModel

import logging

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate("hii-pos-330e9-firebase-adminsdk-jjeto-43862bd4d4.json")
firebase_admin.initialize_app(cred)

# Generate a key. Store this key securely. Do not lose it.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Initialize Firestore client
db = firestore.client()

# Initialize FastAPI
app = FastAPI()

# # MSSQL Connection Information
mssql_server = "DESKTOP-JDQGAO5"
mssql_database = "easypos"
mssql_username = "sa"
mssql_password = "easyfis"
# mssql_driver = "SQL Server"
mssql_driver = "ODBC Driver 17 for SQL Server"
connection_string = f"mssql+pyodbc://{mssql_username}:{mssql_password}@{mssql_server}/{mssql_database}?driver={mssql_driver}"

# engine = create_engine(connection_string)
# Debugging
engine = create_engine(connection_string, echo=True)

#This resolves issues with bulk inserts or operations:
connection = engine.raw_connection()
connection.cursor().fast_executemany = True

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()  # This is the missing line

def encrypt_message(message: str) -> bytes:
    """Encrypts a message."""
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes) -> str:
    """Decrypts an encrypted message."""
    return cipher_suite.decrypt(encrypted_message).decode()  

SECURITY_CODE_PLAIN = "my_secure_code_123"
SECURITY_CODE_ENCRYPTED = encrypt_message(SECURITY_CODE_PLAIN)

class ColumnInfo(BaseModel):
    column_name: str
    column_type: str
    encrypted_security_code: bytes

class SomeModel(BaseModel):
    name: str
    age: int
    is_active: bool = True
    
@app.post("/add-column/{table_name}")
def add_column_to_table(table_name: str, column_info: ColumnInfo):
    # Decrypt security code
    decrypted_code = decrypt_message(column_info.encrypted_security_code)

    # Check security code
    if decrypted_code != SECURITY_CODE_PLAIN:
        raise HTTPException(status_code=403, detail="Invalid security code.")

def verify_security_code(security_code: str):
    if security_code != SECURITY_CODE_PLAIN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return security_code

@app.post("/some_endpoint/")
def some_endpoint(data: SomeModel, security_code: str = Depends(verify_security_code)):
    # your regular logic here
    pass

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

# Create the 'items' table if it doesn't exist
Base.metadata.create_all(bind=engine)

class ItemModel(BaseModel):
    title: str
    description: str
    price: float

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

class ProductModel(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

@app.post("/create-item/")
def create_item(item: ItemModel):
    try:
        db_item = Item(title=item.title, description=item.description, price=item.price)
        db_session = SessionLocal()
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)
        db_session.close()

        firestore_item_ref = db.collection("items").document(str(db_item.id))
        firestore_item_ref.set(item.model_dump())

        return {"message": "Item created successfully"}

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/items/")
def read_items():
    db_session = SessionLocal()
    items = db_session.query(Item).all()
    db_session.close()
    return items


@app.post("/create-product/")
def create_product(product: ProductModel):
    try:
        db_product = Product(name=product.name, price=product.price)
        db_session = SessionLocal()
        db_session.add(db_product)
        db_session.commit()
        db_session.refresh(db_product)
        db_session.close()

        firestore_product_ref = db.collection("products").document(str(db_product.id))
        firestore_product_ref.set(product.model_dump())

        return {"message": "Product created successfully"}

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/products/")
def read_products():
    db_session = SessionLocal()
    products = db_session.query(Product).all()
    db_session.close()
    return products

@app.get("/products-firestore/")
def read_products_firestore():
    products = db.collection("products").stream()
    return [product.to_dict() for product in products]

@app.get("/items-firestore/")
def read_items_firestore():
    items = db.collection("items").stream()
    return [item.to_dict() for item in items]

@app.get("/table-data/{table_name}")
def get_table_data(table_name: str, search: Optional[str] = None, column_indices: List[int] = Query(None), skip: int = 0, limit: int = 10):
    try:
        table = get_table(table_name)
        all_headers = [column.name for column in table.columns]

        # If specific column indices are provided, filter headers.
        headers = all_headers
        if column_indices:
            headers = [all_headers[i] for i in column_indices if 0 <= i < len(all_headers)]

        # Construct the initial query
        session = SessionLocal()
        query = session.query(*[getattr(table.c, header) for header in headers])

        # Apply the search filter if provided
        if search:
            search_filter = getattr(table.c, 'ItemDescription').ilike(f"%{search}%")  # Case-insensitive search
            query = query.filter(search_filter)

        # Apply the pagination
        query = query.offset(skip).limit(limit)

        # Fetch data
        data = [list(row) for row in query.all()]

        # Check if there are more records after the current page
        has_more = session.query(table).count() > skip + limit
        total_count = session.query(table).count()
        return {
            "headers": headers,
            "data": data,
            "has_more": has_more,
            "total_count": total_count
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    pyperclip.copy(tb)
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred! Traceback copied to clipboard."}
    )

def get_table(table_name: str):
    """Fetch the SQLAlchemy table object based on table name."""
    try:
        # Reflect tables from the database
        metadata.reflect(bind=engine)
        
        if table_name not in metadata.tables:
            raise ValueError(f"Table '{table_name}' not found in the database.")
        
        return metadata.tables[table_name]
    except Exception as e:
        raise ValueError(f"Error fetching table '{table_name}': {str(e)}")  

if __name__ == "__main__":
    config = Config(app=app, host="localhost", port=8000)
    server = Server(config)
    server.run()
