import oracledb
from config import ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN, POOL_MIN, POOL_MAX, POOL_INC

#crear un pool de conexiones
_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(
            user =  ORACLE_USER,
            password = ORACLE_PASSWORD,
            dsn =  ORACLE_DSN,
            min = POOL_MIN,
            max = POOL_MAX,
            increment = POOL_INC,
            encoding = 'UTF-8'
        )
    return _pool

#crud basico para la tabla pacientes .
 def list_pacientes():
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ID, NOMBRE, APELLIDO, EDAD, TELEFONO, CORREO FROM PACIENTES ORDER BY ID")
            cols = [d[0].lower() for d in cur.description]
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
            return rows

def get_paciente(p_id):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ID, NOMBRE, APELLIDO, EDAD, TELEFONO, CORREO FROM PACIENTES WHERE ID = :id", [p_id])
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0].lower() for d in cur.description]
            return dict(zip(cols, row))
        
def create_paciente(data):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO PACIENTES (NOMBRE, APELLIDO, EDAD, TELEFONO, CORREO) VALUES (:1, :2, :3, :4, :5)",
                        (data.get('nombre'), data.get('apellido'), data.get('edad'),
                         data.get('telefono'), data.get('correo'))
            )
        conn.commit()
            
def update_paciente(p_id, data):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE PACIENTES SET NOMBRE=:1, APELLIDO=:2, EDAD=:3, TELEFONO=:4,CORREO=:5 WHERE ID=:6",
                (data.get('nombre'), data.get('apellido'), data.get('edad'),
                 data.get('telefono'), data.get('correo'), p_id)
            )
        conn.commit()

def delete_paciente(p_id):
    pool = get_pool()
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM PACIENTES WHERE ID= :id", [p_id])
        conn.commit()