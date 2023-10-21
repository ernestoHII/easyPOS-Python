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
# drivers = pyodbc.drivers()
# print(drivers)
# # Example: Choose the first available driver (not always the best choice)
# drivers = drivers[2]
# # Check if there are any drivers available
# if not drivers:
#     raise RuntimeError("No ODBC drivers are available on this system.")
# Get database credentials from environment variables
db_server = os.getenv("DB_SERVER")
db_database = os.getenv("DB_DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
# connection_string = f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_database}?driver={drivers}"
connection_string = f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_database}?driver=SQL Server"
# engine = create_engine(connection_string)
# Debugging
engine = create_engine(connection_string, echo=True)
#This resolves issues with bulk inserts or operations:
connection = engine.raw_connection()
connection.cursor().fast_executemany = True
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()  # This is the missing line