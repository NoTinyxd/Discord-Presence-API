import threading
import bot #the file bot.py contain all discord bot related code
import api #while the file api.py contain all request and api related code 

if __name__=='__main__':
 api.setup()
 bot_thread=threading.Thread(target=bot.run)
 api_thread=threading.Thread(target=api.run)
 bot_thread.start()
 api_thread.start()
 bot_thread.join()
 api_thread.join()
#it took me 1 hour and 30 minutes something xd