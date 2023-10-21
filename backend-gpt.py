from backend_imports import *
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
load_dotenv()
drivers = pyodbc.drivers()
print(drivers)
# Example: Choose the first available driver (not always the best choice)
drivers = drivers[2]
# Check if there are any drivers available
if not drivers:
    raise RuntimeError("No ODBC drivers are available on this system.")
# Get database credentials from environment variables
db_server = os.getenv("DB_SERVER")
db_database = os.getenv("DB_DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
connection_string = f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_database}?driver={drivers}"
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
    
# ORM models
class MstUnit(Base):
    __tablename__ = 'MstUnit'
    Id = Column(Integer, primary_key=True)
    Unit = Column(String)

class MstSupplier(Base):
    __tablename__ = 'MstSupplier'
    Id = Column(Integer, primary_key=True)
    Supplier = Column(String)

class MstItem(Base):
    __tablename__ = 'MstItem'
    Id = Column(Integer, primary_key=True)
    ItemCode = Column(String)
    Barcode = Column(String)
    ItemDescription = Column(String)
    UnitId = Column(Integer, ForeignKey('MstUnit.Id'))
    Unit = relationship('MstUnit')
    Category = Column(String)
    DefaultSupplierId = Column(Integer, ForeignKey('MstSupplier.Id'))
    Supplier = relationship('MstSupplier')
    Price = Column(Integer)
    OnhandQuantity = Column(Integer)
    IsInventory = Column(Boolean)
    IsLocked = Column(Boolean)
    
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



    def model_dump(self, **kwargs):
        return super().model_dump(**kwargs)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print("Exception occurred!")   # Add this line
    pyperclip.copy(tb)
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred! Traceback copied to clipboard."}
    )
    
# Column Names:
# 0. Id, 1. ItemCode, 2. BarCode, 3. ItemDescription, 4. Alias, 5. GenericName, 6. Category, 
# 7. SalesAccountId, 8. AssetAccountId, 9. CostAccountId, 10. InTaxId, 11. OutTaxId, 
# 12. UnitId, 13. DefaultSupplierId, 14. Cost, 15. MarkUp, 16. Price, 17. ImagePath, 
# 18. ReorderQuantity, 19. OnhandQuantity, 20. IsInventory, 21. ExpiryDate, 22. LotNumber, 
# 23. Remarks, 24. EntryUserId, 25. EntryDateTime, 26. UpdateUserId, 27. UpdateDateTime, 
# 28. IsLocked, 29. DefaultKitchenReport, 30. IsPackage, 31. cValue, 32. ChildItemId, 
# 33. IsMonitored, 34. IsStickerPrinted

@app.get("/table-data3/{table_name}")
def get_table_data(table_name: str, column_indices: str = Query(default="", alias="column_indices"), skip: int = 0, limit: int = 10):
    # Split the column_indices string into a list of integers
    indices = [int(index) for index in column_indices.split(",") if index.isdigit()]

    # Select desired columns using provided indices
    if table_name == 'MstItem':
        all_columns = [column for column in MstItem.__table__.columns]
        desired_columns = [all_columns[i] for i in indices if i < len(all_columns)]
    else:
        raise HTTPException(status_code=400, detail="Unknown table name")

    # Construct and execute the query
    session = SessionLocal()
    query = session.query(*desired_columns)
    
    # Add the ORDER BY clause (ordering by the first column in this example)
    query = query.order_by(desired_columns[0]).offset(skip).limit(limit)
    
    rows = query.all()
    
    # Convert rows to a list of dicts for the response
    result_data = [dict(zip([col.name for col in desired_columns], row)) for row in rows]
    
    return {
        "data": result_data
    }
        
# @app.get("/table-data2/{table_name}")
# def get_table_data2(table_name: str, column_indices: List[int] = Query(None), skip: int = 0, limit: int = 10):
#     try:
#         table = get_table(table_name)
#         all_headers = [column.name for column in table.columns]

#         # If specific column indices are provided, filter headers.
#         if column_indices:
#             headers = [all_headers[i] for i in column_indices if 0 <= i < len(all_headers)]
#         else:
#             headers = all_headers

#         # Construct the initial query
#         session = SessionLocal()
#         query = session.query(*[getattr(table.c, header) for header in headers])
#         query = query.order_by(table.columns[0])  # ordering by the first column, adjust as needed
        
#         # Fetch the total count only once
#         total_count = session.query(table).count()

#         # Apply the pagination
#         query = query.offset(skip).limit(limit)

#         # Fetch data
#         data = [list(row) for row in query.all()]

#         # Check if there are more records after the current page
#         has_more = total_count > skip + limit

#         return {
#             "headers": headers,
#             "data": data,
#             "has_more": has_more,
#             "total_count": total_count
#         }

    # except ValueError as ve:
    #     raise HTTPException(status_code=400, detail=str(ve))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# @app.get("/table-data/{table_name}")
# def get_table_data(table_name: str, column_indices: List[int] = Query(None), skip: int = 0, limit: int = 10):
#     try:
#         table = get_table(table_name)
#         all_headers = [column.name for column in table.columns]

#         # If specific column indices are provided, filter headers.
#         if column_indices:
#             headers = [all_headers[i] for i in column_indices if 0 <= i < len(all_headers)]
#         else:
#             headers = all_headers
#         # Construct the initial query
#         session = SessionLocal()
#         columns_to_select = [getattr(table.c, header) for header in headers]
        
#         # Add window function to compute total count
#         total = over(func.count()).label('total_count')
#         columns_to_select.append(total)
        
#         query = session.query(*columns_to_select)
#         query = query.order_by(table.columns[0])  # ordering by the first column, adjust as needed
        
#         # Apply the pagination
#         query = query.offset(skip).limit(limit)

#         # Fetch data
#         result = query.all()
#         data = [list(row[:-1]) for row in result]  # Exclude the last column which is 'total_count'
#         total_count = result[0][-1] if result else 0  # Get the 'total_count' from the last column of the first row

#         # Check if there are more records after the current page
#         has_more = total_count > skip + limit

#         return {
#             "headers": headers,
#             "data": data,
#             "has_more": has_more,
#             "total_count": total_count
#         }

#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        




if __name__ == "__main__":
    config = Config(app=app, host="localhost", port=8000)
    server = Server(config)
    server.run()
