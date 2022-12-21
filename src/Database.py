import sqlite3, os, asyncio
from .ExcelWriter import excelWriter

class SQLBase(sqlite3.Connection):

    def __init__(self, database_path:str = "", table_name:str = 'STACK', primary_key_column:str = "product_id", fields:list = []) -> None:
        if self.checkDatabasesPath(database_path):
            super().__init__(database_path,5.0,0,"DEFERRED",True,sqlite3.Connection, 100, False)
            self.databasePath:str = database_path
            self.dataBaseTableName:str = table_name if not sqlite3.complete_statement(table_name) else ""
            self.primaryKey:str = primary_key_column                
            self.Cursor:sqlite3.Cursor = self.newCursor()
            self.__rowsCount:int = 0    
            self.fields:list = fields
            self.MAX_STRING_LINES:int = 100

    @property
    def rowsCount(self) -> int:
        try:
            self.__rowsCount  = len(list(self.executeReadCommand(f"SELECT {self.primaryKey} FROM {self.dataBaseTableName};").fetchall()))
        except:
            pass

        return self.__rowsCount
    
    def fieldsAreNotSQLCommands(self, fields:list) -> bool:
        for field in fields:
            if sqlite3.complete_statement(field):
                return False

        return True

    def getFieldsAverageSum(self, field) -> float:
        sumFromTable:float = 0.0
        if not sqlite3.complete_statement(field):
            for row in self.executeReadCommand(f"SELECT {field} FROM {self.dataBaseTableName};").fetchall():
                sumFromTable+=row[0]
                
        return round(sumFromTable/self.rowsCount, 2)

    def getFieldsSum(self, field) -> float:
        sumFromTable:float = 0.0
        if not sqlite3.complete_statement(field):
            for row in self.executeReadCommand(f"SELECT {field} FROM {self.dataBaseTableName};").fetchall():
                sumFromTable+=row[0]
        
        return sumFromTable

    def revealDatabaseFields(self, *fields) -> sqlite3.Cursor:    
        return self.executeReadCommand(f"SELECT {','.join(list(fields))} FROM {self.dataBaseTableName};")

    def revealDatabaseString(self, len_of_list:int = 100) -> str:
        if int(len_of_list)  > self.MAX_STRING_LINES:
            return ""

        outputString:str = ""
        for row in self.revealDatabaseFields(*self.fields).fetchmany(int(len_of_list)):
            for column in row:
                outputString+= f"{column} "
            outputString+="\n"

        return outputString
    
    def rowExists(self, field:str, field_data) -> bool:
        return True if self.executeReadCommand(f"SELECT EXISTS(SELECT 1 FROM {self.dataBaseTableName} WHERE {field}=?);", (field_data,)).fetchone()[0] else False 

    def checkDatabasesPath(self, path:str = "") -> bool:
        return os.path.exists(path)
        
    def newCursor(self) -> sqlite3.Cursor:
        return self.cursor()

    def executeReadCommand(self, command, *args) -> object:
        if sqlite3.complete_statement(command):
            return self.Cursor.execute(command, *args)

    def executeWriteCommand(self, command, *args) -> None:
        if sqlite3.complete_statement(command):
            self.Cursor.execute(command ,*args)
            self.commit()
    
    def setRowInfo(self, id:int, field:str, new_info) -> None:
        self.executeWriteCommand(f"UPDATE {self.dataBaseTableName} SET {field} = ? WHERE {self.primaryKey} = ?;", (new_info,id))

if __name__ == "__main__":
    database = SQLBase(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.db"))
    #database.executeWriteCommand("DROP TABLE STACK;")
    database.executeWriteCommand("""CREATE TABLE IF NOT EXISTS STACK(
    product_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL,
    remaining INTEGER NOT NULL,
    cost INTEGER NOT NULL,
    revenue INTEGER NOT NULL,
    profit INTEGER NOT NULL,
    profit_procent REAL NOT NULL,
    cost_1  INTEGER NOT NULL);
    """)
    database.executeWriteCommand("INSERT INTO STACK (name, remaining, cost, revenue, profit, profit_procent, cost_1) VALUES  ('Haski', 10, 100, 1000, 1000, 1.0, 350);")
    #database.executedWriteCommand("INSERT INTO STACK (name) VALUES ('Bob');")
    #database.executedWriteCommand("INSERT INTO STACK (name) VALUES ('JOHN');")
    print(database.rowsCount)
    database.close()
    #database.executeCommand("DROP TABLE TEST")
