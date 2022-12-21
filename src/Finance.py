import sqlite3
from .Database import SQLBase
import os, calendar, random
import datetime
class Finance(SQLBase):
    def __init__(self, database_path: str = "", table_name: str = 'FINANCE', primary_key_column: str = "month_id") -> None:
        self.fields:list = ["month_id", "name", "plan", "real_profit"] 
        super().__init__(database_path, table_name, primary_key_column, self.fields)

    def getPlanForYear(self) -> int:
        return self.getFieldsSum("plan")
    
    def getCurrentMonth(self) -> str:
        return calendar.month_name[datetime.datetime.now().month]

    def getMonthProfitID(self, name_of_month :str = "") -> tuple:
        return self.executeReadCommand(f"SELECT month_id, real_profit FROM {self.dataBaseTableName} WHERE name = ?;", (name_of_month , )).fetchall()[0]
    
    def getMonthProfit(self, name_of_month:str = "") -> tuple:
        if name_of_month in calendar.month_name:
            return self.executeReadCommand(f"SELECT real_profit FROM {self.dataBaseTableName} WHERE name = ?;", (name_of_month, )).fetchone()[0]

    def getCurrentMonthPlan(self) -> int:
        return self.executeReadCommand(f"SELECT plan FROM {self.dataBaseTableName} WHERE name = ?;", (self.getCurrentMonth(),)).fetchone()[0]

    def getMonthPlan(self, name_of_month:str) -> int:
        if name_of_month in calendar.month_name:
            return self.executeReadCommand(f"SELECT plan FROM {self.dataBaseTableName} WHERE name = ?;", (name_of_month, )).fetchone()[0]

    def getCurrentMonthProfit(self) -> int:
        return self.getMonthProfit(self.getCurrentMonth())

    def setPlanForMonth(self, name_of_month:str = "", new_plan_value:int = 0) -> None:
        self.executeWriteCommand(f"UPDATE {self.dataBaseTableName} SET plan = ? WHERE name = ?;", (new_plan_value, name_of_month,))

    def setProfitForMonth(self, name_of_month:str, new_value:int = 0) -> None:
        self.setRowInfo(id, name_of_month, int(new_value))

if __name__ == "__main__":
    finance = Finance(os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance.db"))
    finance.executeWriteCommand("DROP TABLE FINANCE;")
    #stack.deleteProduct(10)
    finance.executeWriteCommand("""CREATE TABLE IF NOT EXISTS FINANCE(
    month_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL,
    plan INTEGER NOT NULL,
    real_profit INTEGER NOT NULL);
    """)
    names = ["Haski","Premium", "HQD"]
    for i in range(1,13):
        finance.executeWriteCommand("INSERT INTO FINANCE (name, plan, real_profit) VALUES (?,?,?);", (calendar.month_name[i],random.randint(1,10000), 0))
        #stack.executeWriteCommand("INSERT INTO STACK (product_id, name, remaining, cost, revenue, profit, profit_procent, cost_1) VALUES  (7, 'Haski', 10, 100, 1000, 1000, 1.0, 350);")
        #stack.executeWriteCommand("INSERT INTO STACK (name, remaining, cost, revenue, profit, profit_procent, cost_1) VALUES  (?, ?, ?, ?, ?, ?, ?);", (random.choice(names), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), round(random.random(), 2), random.randint(350,1000)))

    
    #stack.executeCommand("INSERT INTO STACK (name) VALUES ('JOHN');")
    #print(stack.revealStackString(stack.RowsCount))
    print(finance.revealDatabaseString(3))
    finance.close()

