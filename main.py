#------SCRIPT START-#
#----IMPORT SECTION-#
import configparser
from tabot import Bot
import asyncio
#-------------------#

#-----CONFIG LOADER-#
def load_config():
    try:
        config = configparser.ConfigParser()
        config.read('main.ini', encoding="utf-8")
        return config
    except OSError:
        print('Configuration file not found!')
#-------------------#
#-------MAIN SECTION-#
if __name__ == '__main__':
    bot = Bot(load_config()).__run__()
#-------------------#
#--------SCRIPT END-#
