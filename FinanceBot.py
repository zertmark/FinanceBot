import asyncio, os, telebot
import time
from telebot.types import InputFile
from telebot.async_telebot import AsyncTeleBot
from src.Stack import Stack
from src.Finance import Finance
from src.commands import commandsHandler
from src.ExcelWriter import excelWriter

class MessageHandler:
    def __init__(self, bot, stackCursor:Stack, financeCursor:Finance) -> None:
        self.bot = bot
        self.stackCursor:Stack = stackCursor
        self.financeCursor:Finance = financeCursor
        self.messageCount:int = 0
        self.messageChunk:int = 20
        self.messageSenderTask:asyncio.Task = None

    def extractArguments(self, command:str) -> list:
        return command.split()[1:]

    def areValidArguments(self, command, args:list) -> bool:
        if self.bot.commands[command]["arguments_check"](args) and self.stackCursor.fieldsAreNotSQLCommands(args):
            return all(args)
        
        return False

    async def sendMessages(self):
        while self.bot.replies_queue:
            for chat_id in list(self.bot.replies_queue.keys()):
                for reply in list(self.bot.replies_queue[chat_id]):
                    await reply["command"](chat_id, reply["reply_message"])
                    await asyncio.sleep(1)
                    self.bot.replies_queue[chat_id].remove(reply)

                if not len(self.bot.replies_queue[chat_id]):
                    del self.bot.replies_queue[chat_id]

    async def handleMessage(self, message:telebot.types.Message) -> None:
        command:str = message.text.split()[0].lower()
        reply_message:str = "Invalid command\nEnter /помощь to look at the commands"
        if command not in self.bot.commands.keys(): 
            await self.bot.send_message(message.chat.id, reply_message)
            return
     
        arguments = self.extractArguments(message.text)    
        reply_message = "Error: invalid arguments"
        if self.areValidArguments(command, arguments):
            reply_message = self.bot.commands[command]["function"](*arguments)
            if self.bot.commands[command]["text_to_print"]:
                reply_message = self.bot.commands[command]["text_to_print"].format(reply_message)
        
        if message.chat.id not in self.bot.replies_queue.keys():
            self.bot.replies_queue[message.chat.id] = []
        
        self.bot.replies_queue[message.chat.id].append({"command":self.bot.commands[command]["bot_function"], "reply_message":reply_message})
        
        if not self.messageSenderTask or self.messageSenderTask.done():
            self.messageSenderTask = asyncio.create_task(self.sendMessages())
            await self.messageSenderTask

        #await self.bot.commands[command]["bot_function"](message.chat.id, reply_message)
        #if self.messageCount % self.messageChunk ==0:
            #self.messageCount = 0 

class Bot(AsyncTeleBot):
    def __init__(self, token: str, stackCursor:Stack, financeCursor:Finance) -> None:
        self.token:str = token
        self.stackCursor:Stack = stackCursor
        self.financeCursor:Finance = financeCursor
        self.helpMessage:str = self.getHelpMessage()
        self.replies_queue:dict = {}
        super().__init__(self.token)
        self.messageHandler:MessageHandler = MessageHandler(self, self.stackCursor, self.financeCursor)
        self.commands:dict = commandsHandler.getCommands(self, self.financeCursor, self.stackCursor)
        self.table_names:dict = {
            "STACK" : self.stackCursor,
            "FINANCE" : self.financeCursor
        }


    def setMessageHandler(self) -> None:
        self.add_message_handler(Bot._build_handler_dict(self.messageHandler.handleMessage))

    def isSalesNumberIncorrect(self, remaining:int = 0, sales_number:int = 0) -> bool:
        return True if not remaining and not remaining < sales_number else False

    def sendExcelFile(self, table_name:str) -> None:
        if table_name in self.table_names.keys():
            self.excelWriter:excelWriter = excelWriter(f"{self.table_names[table_name].dataBaseTableName}.xlsx")
            self.excelWriter.generateExcelFile(self.table_names[table_name])
            return InputFile(self.excelWriter.getFilePath())

    def getHelpMessage(self) -> str:
        with open("help.txt", "r", encoding="UTF-8") as file:
            return " ".join(file.readlines())

    def help(self) -> str:
        return self.helpMessage

    def productSold(self, id:int, sales_number:int) -> str:
        name, remaining, cost_1 = self.stackCursor.executeReadCommand(f"SELECT name, remaining, cost_1 FROM {self.stackCursor.dataBaseTableName} WHERE product_id = ?;", (id,)).fetchall()[0]
        month_id, current_month_revenue = self.financeCursor.getMonthProfitID(self.financeCursor.getCurrentMonth())
        if self.isSalesNumberIncorrect(remaining, sales_number):
            return 

        self.stackCursor.setRowInfo(id, "remaining", int(remaining)-int(sales_number))
        self.financeCursor.setRowInfo(month_id, "real_profit", current_month_revenue + (cost_1 * int(sales_number)))
        return f"Sold!\nName\tRemaining\n{name}\t{int(remaining)-int(sales_number)}"

class Main:
    def __init__(self, token:str) -> None:
        
        self.stackCursor:Stack = Stack(os.path.join(f"{os.path.dirname(os.path.abspath(__file__))}\\databases", "stack.db"))
        self.financeCursor:Finance = Finance(os.path.join(f"{os.path.dirname(os.path.abspath(__file__))}\\databases", "finance.db"))
        self.excelWriter:excelWriter = excelWriter("")
        self.bot:Bot = Bot(token, self.stackCursor, self.financeCursor) 
        self.bot.setMessageHandler()

    def Run(self) -> None:
        asyncio.run(self.bot.polling(non_stop=False, allowed_updates=["message"], interval=3, timeout=20))
    
if __name__ == "__main__":
    main = Main(token="5766970401:AAG-FASqyH8mQqQ9V6Wwuex0MeJBq3fkwBI")
    main.Run()