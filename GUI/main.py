DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables in the database (only for this demonstration)
Base.metadata.create_all(bind=engine)

# Create a new user using SQLAlchemy
db = SessionLocal()
new_user = User(username="alice", age=25)
db.add(new_user)
db.commit()
db.refresh(new_user)

# Convert the SQLAlchemy object to a Pydantic object
user_out = UserOut.from_orm(new_user)
print(user_out.json())  # {"id": 1, "username": "alice", "age": 25}
