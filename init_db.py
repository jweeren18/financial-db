from db import engine
from models import Base

if __name__ == '__main__':
    print('Creating database tables...')
    Base.metadata.create_all(bind=engine)
    print('Done. Database created at data.db')
