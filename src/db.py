import psycopg
from psycopg.rows import dict_row
from datetime import datetime

class Database:
    def __init__(self) -> None:
        "Inicializa conexão com o banco"
        self.db = psycopg.connect(
                host='localhost',
                port='5432',
                dbname='avalia_unb',
                user='postgres',
                password='postgres',
                row_factory=dict_row
            )

        print('Conexão iniciada! ', self.__current_time_formated())

    def __del__(self) -> None:
        "Encerra conexão quando a classe sair do escopo"
        self.db.close()
        print('Conexão encerrada! ', self.__current_time_formated())

    def execute_query(self, query: str, params=None):
        "Executa query que não retorna um registro"
        self.db.execute(query, params)
        self.db.commit()

    def execute_multiple_queries(self, queries: list[str]):
        "Executa múltiplas queries que não retornam registros"
        for query in queries:
            self.db.execute(query)
        self.db.commit()

    def execute_fetchone_query(self, query: str, params=None):
        "Executa query que retorna apenas um registro"
        result = self.db.execute(query, params).fetchone()
        self.db.commit()
        return result

    def execute_fetchall_query(self, query: str, params=None):
        "Executa query que retorna múltiplos registros"
        result = self.db.execute(query, params).fetchall()
        self.db.commit()
        return result

    def __current_time_formated(self):
        return datetime.now().strftime("%H:%M:%S.%f")