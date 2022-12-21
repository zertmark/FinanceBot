import os
from xlsxwriter import Workbook
class excelWriter(Workbook):
    def __init__(self, filename="", options=None) -> None:
        self.filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        super().__init__(self.filePath, options)
        self.workSheet = self.add_worksheet()

    def writeColumnNames(self, dataBaseCursor) -> None:
        column_counter:int = 0
        for column_name in dataBaseCursor.fields:
            self.workSheet.write(0, column_counter, column_name.capitalize())
            column_counter+=1

    def generateExcelFile(self, dataBaseCursor) -> None:
        self.writeColumnNames(dataBaseCursor)
        for row_count, row in enumerate(dataBaseCursor.executeReadCommand(f"SELECT * FROM {dataBaseCursor.dataBaseTableName};").fetchall()):
            for column_count, column in enumerate(row):
                self.workSheet.write(row_count+1, column_count, column)
        
        self.close()

    def getFilePath(self) -> str:
        return self.filePath

        