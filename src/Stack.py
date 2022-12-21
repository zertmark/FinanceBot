import sqlite3
from .Database import SQLBase
import os, random
class Stack(SQLBase): 
    def __init__(self, database_path: str = "stack.db") -> None:
        self.fields:list =  ["product_id", "name", "remaining", "cost", "revenue", "profit", "profit_procent", "cost_1"]
        super().__init__(database_path, "STACK", "product_id", self.fields)

    def getCompleteProfit(self) -> float:
        return self.getCompleteRevenue()-self.getCompleteCost()       
    
    def getCompleteProfitProcent(self) -> float:
        return round(self.getCompleteRevenue()/self.getCompleteCost(), 2)

    def getCompleteCost(self) -> float:
        return self.getFieldsSum("cost")

    def getCompleteRevenue(self) -> float:
        return self.getFieldsSum("revenue")

    def getAverageCostOne(self) -> float:
        return self.getFieldsAverageSum("cost_1")

    def getMostProfitableProduct(self) -> str:
        MostProfitableProduct:tuple = self.executeReadCommand(f"SELECT product_id, name, remaining, max(profit_procent) FROM {self.dataBaseTableName};").fetchone()    
        return "\t".join(str(field) for field in MostProfitableProduct) if MostProfitableProduct else None

    def addNewDataToRow(self, row,  remaining, cost, revenue, profit, profit_procent, cost_1) -> tuple:
        for key, newFieldData in enumerate([remaining,cost,revenue,profit]):
            row[key+2] = row[key+2]+int(newFieldData)

        row[5]=profit_procent if profit_procent else round(row[4]/row[3],2)
        row[6]=cost_1
        return row

    def addNewProduct(self, name:str, remaining:int, cost:int, revenue:int = 0, profit:int = 0, profit_procent:float = 0.0, cost_1:int = 0) -> None:
        if not self.rowExists("name", name):
            self.executeWriteCommand(f"INSERT INTO {self.dataBaseTableName} (name, remaining, cost, revenue, profit, profit_procent, cost_1) VALUES  (?, ?, ?, ?, ?, ?, ?);",(name, int(remaining), int(cost), int(profit), int(revenue), float(profit_procent), int(cost_1)))
            return

        row:tuple = self.addNewDataToRow(list(self.executeReadCommand(f"SELECT product_id, name, remaining, cost, revenue, profit, profit_procent, cost_1 FROM {self.dataBaseTableName} WHERE name = ?;", (name,)).fetchone()),remaining, cost, revenue, profit, profit_procent, cost_1)
        for key, field in enumerate(["remaining", "cost", "revenue", "profit", "profit_procent", "cost_1"]):
            self.setRowInfo(row[0], field, row[key+2])

    def getProductIDString(self, name) -> tuple:
        return self.executeReadCommand(f"SELECT product_id, name FROM TABLE {self.dataBaseTableName} WHERE name = ?;", (name,))
    
    def searchProductInfo(self, *args) -> tuple:
        args:list = [argument.split("=") for argument in args if argument]
        outputString:str = "Didn't find anything"
        results:list = self.executeReadCommand(f"SELECT {', '.join([field for field in self.fields])} FROM {self.dataBaseTableName} WHERE {' AND '.join([f'{argument[0]} = ?' for argument in args])};", tuple([argument[1] for argument in args])).fetchall()
        if results:
            outputString="ID\tName\tRemaining\tCost\tRevenue\tProfit\tProfit_procent\tCost_1\n"
            for row in results:
                outputString+=f"{' '.join(str(column) for column in row)}\n"

        return outputString
    
    def getProductInfo(self, id:int, field:str) -> tuple:
        if not sqlite3.complete_statement(field):
            return self.executeReadCommand(f"SELECT product_id, name, {field} FROM {self.dataBaseTableName} WHERE product_id = ?;", (int(id),)).fetchone()

    def deleteProduct(self, id:int) -> None:
        self.executeWriteCommand(f"DELETE FROM {self.dataBaseTableName} WHERE product_id = ?;", (id,))

if __name__ == "__main__":
    stack = Stack(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.db"))
    #stack.executeWriteCommand("DROP TABLE STACK;")
    stack.executeWriteCommand("""CREATE TABLE IF NOT EXISTS STACK(
    product_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL,
    remaining INTEGER NOT NULL,
    cost INTEGER NOT NULL,
    revenue INTEGER,
    profit INTEGER,
    profit_procent REAL,
    cost_1  INTEGER);
    """)
    names = ["Haski","Premium", "HQD"]
    for i in range(0,5):
        stack.executeWriteCommand("INSERT INTO STACK (name, remaining, cost, revenue, profit, profit_procent, cost_1) VALUES  (?, ?, ?, ?, ?, ?, ?);", (random.choice(names), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), round(random.random(), 2), random.randint(350,1000)))

    print(stack.revealDatabaseString(3))
    print(stack.getCompleteProfit())
    print(stack.getMostProfitableProduct(), end="")
    stack.close()
