import calendar
from sqlite3 import complete_statement
class commandsHandler:

    @staticmethod
    def getCommands(bot:object, financeCursor:object, stackCursor:object) -> dict:
        return {
            "/помощь" : {
            "function" : bot.help, 
            "arguments_check": lambda list: True if not len(list) else False, 
            "text_to_print": "",
            "bot_function" : bot.send_message
            },            
            "/склад" : {
            "function" : stackCursor.revealDatabaseString, 
            "arguments_check": lambda list: True if (len(list)==1 and int(list[0]) <= stackCursor.MAX_STRING_LINES and int(list[0])>0) or len(list) == 0  else False, 
            "text_to_print": "ID\tName\tRemaining\tCost\tRevenue\tProfit\tProfit procent\tCost of 1\n{}",
            "bot_function" : bot.send_message
            },
            "/финансы" : {
            "function" : financeCursor.revealDatabaseString, 
            "arguments_check": lambda list: True if (len(list)==1 and int(list[0]) <= financeCursor.MAX_STRING_LINES and int(list[0])>0) or len(list) == 0 else False, 
            "text_to_print": "ID\tName\tPlan\tReal_profit\n{}",
            "bot_function" : bot.send_message
            },
            "/склад_поиск": {
            "function" : stackCursor.searchProductInfo, 
            "arguments_check": lambda list: True if len(list)> 0 and set([argument.split("=")[0] for argument in list if argument]).issubset(set(stackCursor.fields)) else False, 
            "text_to_print": "",
            "bot_function" : bot.send_message
            },
            "/спт" : {
            "function" : stackCursor.getMostProfitableProduct, 
            "arguments_check": lambda list: True if not len(list) else False,  
            "text_to_print": "Most profitable product:\nID\tName\tRemaining:\tProfit\n{}",
            "bot_function" : bot.send_message
            },
            "/ов" : {
            "function" : stackCursor.getCompleteRevenue, 
            "arguments_check": lambda list: True if not len(list) else False,  
            "text_to_print": "Complete revenue is:\n{} ₽",
            "bot_function" : bot.send_message
            },
            "/оп" : {
            "function" : stackCursor.getCompleteProfit, 
            "arguments_check": lambda list: True if not len(list) else False,  
            "text_to_print": "Complete profit is:\n{} ₽",
            "bot_function" : bot.send_message
            },
            "/тву" : {
            "function" : stackCursor.deleteProduct, 
            "arguments_check": lambda list: True if len(list)==1 else False,  
            "text_to_print": "Product is deleted",
            "bot_function" : bot.send_message
            },
            "/твиз" : {
            "function" : stackCursor.setRowInfo, 
            "arguments_check": lambda list: True if len(list)==3 and int(list[0]) > 0 and int(list[0]) <= stackCursor.rowsCount else False,  
            "text_to_print": "Product info changed:\n",
            "bot_function" : bot.send_message
            },
            "/твд" : {
            "function" : stackCursor.addNewProduct, 
            "arguments_check": lambda list: True if len(list)>=3 and len(list)<=7 else False,  
            "text_to_print": "New product added",
            "bot_function" : bot.send_message
            },
            "/п" : {
            "function" : financeCursor.getCurrentMonthProfit, 
            "arguments_check": lambda list: True if not len(list) else False,  
            "text_to_print": "Profit from current month:\n{} ₽",
            "bot_function" : bot.send_message
            },
            "/пм" : {
            "function" : financeCursor.getMonthProfit, 
            "arguments_check": lambda list: True if len(list)==1 and list[0] in calendar.month_name else False,  
            "text_to_print": "Profit from this month:\n{} ₽",
            "bot_function" : bot.send_message
            },
            "/планм" : {
            "function" : financeCursor.getCurrentMonthPlan, 
            "arguments_check": lambda list: True if not len(list) else False,  
            "text_to_print": "Plan for current month:\n{} ₽",
            "bot_function" : bot.send_message
            },
            "/план" : {
            "function" : financeCursor.getMonthPlan, 
            "arguments_check": lambda list: True if len(list) == 1 and list[0] in calendar.month_name else False,  
            "text_to_print": "Plan on this month:\n{} ₽",
            "bot_function" : bot.send_message
            },
            "/иплан" : {
            "function" : financeCursor.setPlanForMonth, 
            "arguments_check": lambda list: True if len(list) == 2 and list[0] in calendar.month_name and int(list[1]) >=0 else False,  
            "text_to_print": "Changed plan for this month",
            "bot_function" : bot.send_message
            },
            "/excel" : {
            "function" : bot.sendExcelFile, 
            "arguments_check": lambda list: True if len(list) == 1 and list[0] in bot.table_names else False,  
            "text_to_print": "",
            "bot_function" : bot.send_document
            },
            "/продал" : {
            "function" : bot.productSold, 
            "arguments_check": lambda list: True if len(list)==2 and (int(list[0])>=0 and int(list[0])<=stackCursor.rowsCount) and int(list[1])>0 else False,  
            "text_to_print": "",
            "bot_function" : bot.send_message
            }
        }