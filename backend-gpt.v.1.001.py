from backend_imports import *
from initialization import *

# Define SQLAlchemy model for MstTax
class MstTax(Base):
    __tablename__ = 'MstTax'

    id = Column(Integer, primary_key=True, index=True)
    Code = Column(String, index=True)
class ItemCodeResponse(BaseModel):
    ItemCode: str
class DynamicItemCreate(BaseModel):
    data: dict

class MstItemCategory(Base):
    __tablename__ = 'MstItemCategory'

    id = Column(Integer, primary_key=True, index=True)
    Category = Column(String, index=True)
class MstItem(Base):
    __tablename__ = 'MstItem'
    
    ItemCode = Column(String, primary_key=True)
    Barcode = Column(String)
    ItemDescription = Column(String)
    UnitId = Column(Integer, ForeignKey('MstUnit.Id'))
    Category = Column(String)
    DefaultSupplierId = Column(Integer, ForeignKey('MstSupplier.Id'))
    Price = Column(Integer)
    OnhandQuantity = Column(Integer)
    IsInventory = Column(Boolean)
    IsLocked = Column(Boolean)
    Alias = Column(String, primary_key=True)
    GenericName = Column(String(255))
    SalesAccountId = Column(Integer)
    AssetAccountId = Column(Integer)
    CostAccountId = Column(Integer)
    InTaxId = Column(Integer)
    OutTaxId = Column(Integer)
    Cost = Column(Numeric(18, 5))
    MarkUp = Column(Numeric(18, 5))
    ImagePath = Column(String(255))
    ReorderQuantity = Column(Numeric(18, 5))
    ExpiryDate = Column(DateTime)
    LotNumber = Column(String(50))
    Remarks = Column(String(255))
    EntryUserId = Column(Integer)
        
    unit = relationship("MstUnit")
    supplier = relationship("MstSupplier")

class MstUnit(Base):
    __tablename__ = 'MstUnit'
    
    Id = Column(Integer, primary_key=True)
    Unit = Column(String)

class MstSupplier(Base):
    __tablename__ = 'MstSupplier'
    
    Id = Column(Integer, primary_key=True)
    Supplier = Column(String)

def row2dict(row):
    """Convert a SQLAlchemy row to a dictionary."""
    return {col.name: getattr(row, col.name) for col in row.__table__.columns}

@app.get("/items/")
def get_all_items():
    session = SessionLocal()
    try:
        items = session.query(MstItem).all()

        # Convert items to a list of dictionaries
        items_list = [row2dict(item) for item in items]

        return {"items": items_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

# Define a FastAPI endpoint to fetch and update the ItemCode
@app.get("/update_item_detail/", response_model=ItemCodeResponse)
async def update_item_code():
    try:
        # Get the last ItemCode using SQLAlchemy
        session = SessionLocal()
        last_item = (
            session.query(MstItem)
            .order_by(MstItem.ItemCode.desc())
            .first()
        )

        if last_item:
            new_item_code = last_item.ItemCode - 2
            formatted_item_code = str(new_item_code).zfill(10)
        else:
            formatted_item_code = "0000000001"

        # Update the ItemCode in the database (optional)
        # You can uncomment and modify this part if you want to update the database.

        # new_item = MstItem(ItemCode=new_item_code)
        # session.add(new_item)
        # session.commit()

        return {"ItemCode": formatted_item_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        session.close()

# Define a FastAPI endpoint to display the ItemCode (optional)
@app.get("/display_item_code/")
async def display_item_code():
    try:
        # Get the last ItemCode using SQLAlchemy
        session = SessionLocal()
        last_item = (
            session.query(MstItem)
            .order_by(MstItem.ItemCode.desc())
            .first()
        )

        if last_item:
            formatted_item_code = str(last_item.ItemCode).zfill(10)
        else:
            formatted_item_code = "0000000001"

        return {"ItemCode": formatted_item_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        session.close()
                
# Define a FastAPI endpoint to populate comboBoxChildItem
@app.get("/populate_combo_box_child_item/")
async def populate_combo_box_child_item():
    try:
        # Get the data from the MstItem table using SQLAlchemy
        session = SessionLocal()
        items = session.query(MstItem.ItemDescription).all()
        item_aliases = [item[0] for item in items]  # Extract the Alias values
        print(item_aliases)
        return {"items": item_aliases}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        session.close()
        
# Define a function to fetch category data
def get_categories():
    session = SessionLocal()
    categories = session.query(MstItemCategory.Category).all()
    session.close()
    return categories

# Create a FastAPI endpoint to fetch categories
@app.get("/categories/")
async def fetch_categories():
    categories = get_categories()
    return {"categories": [category[0] for category in categories]}
    
@app.post("/items/", response_model=dict)
async def create_item(item: DynamicItemCreate):
    data = item.data
    db_item = MstItem(**data)
    session = SessionLocal()
    try:
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item.__dict__
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Define a function to fetch category data
def get_unit():
    session = SessionLocal()
    categories = session.query(MstUnit.Unit).all()
    session.close()
    return categories

# Create a FastAPI endpoint to fetch categories
@app.get("/units/")
async def fetch_units():
    categories = get_unit()
    return {"units": [category[0] for category in categories]}
            
def get_vat():
    session = SessionLocal()
    vat = session.query(MstTax.Code).all()
    session.close()
    return vat

@app.get("/vat/")
async def fetch_vat_codes():
    vat = get_vat()
    vat_codes = [item.Code for item in vat]
    return {"vat": vat_codes}

# Create an endpoint to fetch supplier data
@app.get("/suppliers/")
async def fetch_suppliers():
    session = SessionLocal()
    try:
        suppliers = session.query(MstSupplier.Supplier).all()
        return {"suppliers": [supplier[0] for supplier in suppliers]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
        
if __name__ == "__main__":
    config = Config(app=app, host="localhost", port=8000)
    server = Server(config)
    server.run()
