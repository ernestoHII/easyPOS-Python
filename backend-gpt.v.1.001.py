from backend_imports import *
from initialization import *

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


                
if __name__ == "__main__":
    config = Config(app=app, host="localhost", port=8000)
    server = Server(config)
    server.run()
