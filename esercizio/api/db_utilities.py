import psycopg2 as pg


class Connection():
    conn_params : any
    def __init__(self, host, port, dbname,user, password):
        self.conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
        }
        self.conn = None
    
    def connection_creator(self):
        if self.conn is None or self.conn.closed:
            self.conn = pg.connect(**self.conn_params)

    def connection_destructor(self):
        if self.conn and not self.conn.closed:
            self.conn.close()

    def query_executor(self, sql: str, params = None):
        self.connection_creator()
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
        self.conn.commit()

    def query_executor2(self, sql: str, params=None):
        self.connection_creator()
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            status = cur.statusmessage
        self.conn.commit()
        return status
    
    def fetch_query(self, sql, params = None):
        self.connection_creator()
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
        
    def insert_executor(self, sql, params):
        self.connection_creator()
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                id_creato = cur.fetchone()[0]
            self.conn.commit()
            return id_creato
        except Exception as e:
            print(e)
            return None
        finally:
            self.connection_destructor()
        
    
    def __del__(self):
        self.connection_destructor()