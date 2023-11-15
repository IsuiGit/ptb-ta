#------SCRIPT START-#
#----IMPORT SECTION-#
import logging
import httplib2
import apiclient.discovery
from frames import SimpleDataFrame
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
#-------------------#
#-DIR NAME IN CONFIG#
#--------------FILE-#
DIR_NAME = 'GOOGLE'
#-------------------#
#-----TABOT SECTION-#
class Bot:
    def __init__(self, config):
        try:
            self.api = config['BOTSETTINGS']['bot_api']
            self.credentials = config[DIR_NAME]['credentials']
            self.spreadsheetId = config[DIR_NAME]['spreadsheetId']
            self.sheetName = config[DIR_NAME]['sheetName']
            self.range = config[DIR_NAME]['range']
            self.trusts = config['BOTSETTINGS']['trusts'].split('/')
            self.service = self.__table_connect__()
            self.log = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        except Exception as e:
            print('__exception__in: __init__() completed with an error\n', repr(e))

    def __table_connect__(self):
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials, ['https://www.googleapis.com/auth/spreadsheets'])
            httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
            service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
            print('Bot connected to Google API')
            return service
        except Exception as e:
            print('__exception__in: __table_connect__() completed with an error\n', repr(e))
            return None

    def __get_info__(self):
        if self.service != None and self.spreadsheetId:
            try:
                results = self.service.spreadsheets().values().batchGet(spreadsheetId = self.spreadsheetId, ranges = [f'{self.sheetName}!{self.range}'], valueRenderOption = 'FORMATTED_VALUE', dateTimeRenderOption = 'FORMATTED_STRING').execute()
                sheet_values = results['valueRanges'][0]['values']
                return sheet_values[0], sheet_values[1:]
            except Exception as e:
                print('__exception__in: __get_info__() completed with an error\n', repr(e))

    def __print_sheets__(self):
        if self.service != None and self.spreadsheetId:
            try:
                spreadsheets = self.service.spreadsheets().get(spreadsheetId = self.spreadsheetId).execute()
                sheetList = spreadsheets.get('sheets')
                for sheet in sheetList:
                    print(sheet['properties']['sheetId'], sheet['properties']['title'])
            except Exception as e:
                print('__exception__in: __print_sheets__() completed with an error\n', repr(e))

    def __section_data_to_frame__(self):
        try:
            return SimpleDataFrame(self.__get_info__()).__section_dataframe_output__()
        except Exception as e:
            print('__exception__in: __section_data_to_frame__() completed with an error\n', repr(e))

    async def __start__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[InlineKeyboardButton("Экзамены", callback_data='exams')],]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот Академии ТОР СПб Удельная!", reply_markup=reply_markup)

    async def __exams__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.__section_data_to_frame__())

    async def __button__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == 'exams':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.__section_data_to_frame__())
        else:
            pass

    def __run__(self):
        application = ApplicationBuilder().token(self.api).build()
        application.add_handler(CommandHandler('start', self.__start__, filters=filters.Chat(username=self.trusts)))
        application.add_handler(CallbackQueryHandler(self.__button__))
        application.run_polling()
#-------------------#
#--------SCRIPT END-#
