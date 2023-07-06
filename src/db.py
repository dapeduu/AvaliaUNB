import psycopg

class Database():
    def __init__(self) -> None:
        "Inicializa conexão com o banco"
        self.db = psycopg.connect(
                host='localhost',
                port='5432',
                dbname='avalia_unb',
                user='postgres',
                password='postgres'
            )

    def __del__(self) -> None:
        "Encerra conexão quando a variável sair do escopo"
        self.db.close()

    def execute_query(self, query: str):
        "Executa query que não retorna um registro"
        self.db.execute(query)
        self.db.commit()

    def execute_multiple_queries(self, queries: list[str]):
        "Executa múltiplas queries"
        for query in queries:
            self.db.execute(query)
        self.db.commit()

    def execute_fetchone_query(self, query: str):
        "Executa query que retorna apenas um registro"
        result = self.db.execute(query).fetchone()
        self.db.commit()
        return result

    def execute_fetchall_query(self, query: str):
        "Executa query que retorna múltiplos registros"
        result = self.db.execute(query).fetchall()
        self.db.commit()
        return result

