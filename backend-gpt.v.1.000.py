from backend_imports import *
from initialization import app, engine, SessionLocal, Base, metadata, db, cipher_suite

class Item(Base):
    __tablename__ = "MstItem"  # Specify the table name here
    id = Column(Integer, primary_key=True, index=True)
    ItemCode = Column(String)
    Barcode = Column(String)
    ItemDescription = Column(String)
    DefaultSupplierId = Column(Integer)
    Category = Column(String)
    Cost = Column(Float)
    Price = Column(Float)
    OnhandQuantity = Column(Float)
    IsInventory = Column(Boolean)
    IsLocked = Column(Boolean)

class ItemCreate(BaseModel):
    ItemCode: str
    Barcode: str
    ItemDescription: str
    DefaultSupplierId: int
    Category: str
    Cost: float
    Price: float
    OnhandQuantity: float
    IsInventory: bool
    IsLocked: bool

@app.get("/table-data/{table_name}")
def get_table_data(table_name: str, column_indices: List[int] = Query(None), skip: int = 0, limit: int = 10):
    try:
        table = get_table(table_name)
        all_headers = [column.name for column in table.columns]

        # If specific column indices are provided, filter headers.
        if column_indices:
            headers = [all_headers[i] for i in column_indices if 0 <= i < len(all_headers)]
        else:
            headers = all_headers

        # Construct the initial query
        session = SessionLocal()
        columns_to_select = [getattr(table.c, header) for header in headers]
        
        # Add window function to compute total count
        total = over(func.count()).label('total_count')
        columns_to_select.append(total)
        
        query = session.query(*columns_to_select)
        query = query.order_by(table.columns[0])  # ordering by the first column, adjust as needed
        
        # Apply the pagination
        query = query.offset(skip).limit(limit)

        # Fetch data
        result = query.all()
        data = [list(row[:-1]) for row in result]  # Exclude the last column which is 'total_count'
        total_count = result[0][-1] if result else 0  # Get the 'total_count' from the last column of the first row

        # Check if there are more records after the current page
        has_more = total_count > skip + limit

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
