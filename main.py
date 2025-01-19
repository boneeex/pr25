import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import asyncio
from queries.companyquery import AsyncORM

asyncio.run(AsyncORM.insert_company())