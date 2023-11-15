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
#-----TABOT SECTION-#
class Bot:
    def __init__(self, config):
        try:
            self.api = config['BOTSETTINGS']['bot_api']
            self.credentials = config['GOOGLE']['credentials']
            self.spreadsheetId = config['GOOGLE']['spreadsheetId']
            self.sheetName = self.__sheets_to_dict__(config['GOOGLE']['sheetName'].split(';'))
            self.range = config['GOOGLE']['range']
            self.trusts = config['BOTSETTINGS']['trusts'].split(';')
            self.service = self.__table_connect__()
            self.log = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        except Exception as e:
            print('__exception__in: __init__() completed with an error\n', repr(e))

    def __sheets_to_dict__(self, x):
        resp = {}
        for i in x:
            resp[i.split('=')[0]]=i.split('=')[1]
        return resp

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

    def __get_info__(self, name):
        if self.service != None and self.spreadsheetId:
            try:
                results = self.service.spreadsheets().values().batchGet(spreadsheetId = self.spreadsheetId, ranges = [f'{name}!{self.range}'], valueRenderOption = 'FORMATTED_VALUE', dateTimeRenderOption = 'FORMATTED_STRING').execute()
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

    def __section_data_to_frame__(self, name):
        try:
            return SimpleDataFrame(self.__get_info__(name)).__section_dataframe_output__()
        except Exception as e:
            print('__exception__in: __section_data_to_frame__() completed with an error\n', repr(e))

    def __square_data_to_frame__(self, name):
        try:
            return SimpleDataFrame(self.__get_info__(name)).__square_dataframe_output__()
        except Exception as e:
            print('__exception__in: __square_data_to_frame__() completed with an error\n', repr(e))

    async def __start__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton("Экзамены", callback_data='exams'),
            ],
            [
                InlineKeyboardButton("Отработки (Список)", callback_data='wo_sec'),
                InlineKeyboardButton("Отработки (Таблица)", callback_data='wo_sq'),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот Академии ТОР СПб Удельная!", reply_markup=reply_markup)

    async def __button__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == 'exams':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.__section_data_to_frame__(self.sheetName['exams']))
        elif query.data == 'wo_sec':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.__section_data_to_frame__(self.sheetName['wo']))
        elif query.data == 'wo_sq':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.__square_data_to_frame__(self.sheetName['wo']), parse_mode=constants.ParseMode.MARKDOWN_V2)
        else:
            pass

    def __run__(self):
        application = ApplicationBuilder().token(self.api).build()
        application.add_handler(CommandHandler('start', self.__start__, filters=filters.Chat(username=self.trusts)))
        application.add_handler(CallbackQueryHandler(self.__button__))
        application.run_polling()
#-------------------#
#--------SCRIPT END-#
