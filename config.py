import os
from dotenv import load_dotenv
load_dotenv()

ORACLE_USER = os.getenv('ORACLE_USER', 'system')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', 'Tapiero123')

# DSN formato : host:port/service_name -> ejemplo: 127.0.0.1:1521/orcl
ORACLE_DSN = "localhost:1521/orcl"

#opciones de pool
POOL_MIN = int(os.getenv('POOL_MIN', '1'))
POOL_MAX = int(os.getenv('POOL_MAX', '4'))
POOL_INC = int(os.getenv('POOL_INC', '1'))
