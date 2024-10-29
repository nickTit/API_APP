from database.models import *

db.bind(provider='sqlite', filename='/home/redmi/Python_test_tasks/API_APP/database/database.sqlite', create_db=True)

db.generate_mapping(create_tables=True)