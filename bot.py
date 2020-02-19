import telebot
import time

import config
import amb

from telebot import types

def check_users_loaded(msg_id):
    if (config.users_loaded == 0):
        config.users_loaded = 1
        try:
            f = open("content/members.txt"+str(msg_id), "r") 
        except IOError:
            f = open("content/members.txt"+str(msg_id), "x") 
            f.close()
            f = open("content/members.txt"+str(msg_id), "r") 
        spltd = f.read()
        spltd = spltd.split()
        config.USERS = list(spltd)
        f.close()
        config.startup('Users loaded, Array: '+str(config.USERS))

bot = telebot.TeleBot(config.TOKEN) 

@bot.message_handler(commands=['start'])
def welcome(message):
    amb.log('/start executed, Executor: '+message.from_user.first_name)

    sti = open('content/start.webp', 'rb')
    bot.send_message(message.chat.id, 
        'Бот сделан членом клуба хейтеров питона - @depozzyx-ом, по просьбе клуба хейтеров питона и членов XVIII Съезда КПСС. Все комманды высвечиваются при нажатие на "/" ')
    bot.send_sticker(message.chat.id, sti)

#@bot.message_handler(commands=['TEST'])
#def execute(message):
#    amb.log('/TEST executed, Executor: '+message.from_user.first_name)

@bot.message_handler(commands=['myid'])
def execute(message):
    amb.log('/myid executed, Executor: '+message.from_user.first_name)

    bot.send_message(message.chat.id, 'Your id is '+str(message.from_user.id))

@bot.message_handler(commands=['info'])
def execute(message):
    amb.log('/info executed, Executor: '+message.from_user.first_name)

    sti = open('content/info.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Бот сделан членом клуба хейтеров питона - @depozzyx-ом, по просьбе клуба хейтеров питона и членов XVIII Съезда КПСС ')

@bot.message_handler(commands=['list'])
def execute(message):
    amb.log('/list executed, Executor: '+message.from_user.first_name)

    check_users_loaded(message.chat.id)

    count = len(config.USERS)
    if (count==1):
        okon = ''
    elif (count==2) or (count==3) or (count==4):
        okon = 'а'
    else:
        okon = 'ов'
    msg = 'Сейчас в чате зарегестрировано '+str(len(config.USERS))+' участник'+okon+':\n'

    for i in range(len(config.USERS)):
        msg = str(msg) +'- '+bot.get_chat_member(message.chat.id,config.USERS[i]).user.first_name+' ['+str(config.USERS[i])+']'
        msg = str(msg) + '\n'   
    bot.send_message(message.chat.id, msg,parse_mode='html')


@bot.message_handler(commands=['yell'])
def execute(message):
    amb.log('/yell executed, Executor: '+message.from_user.first_name)

    global yelling
    global yellmaster
    global yellmsgid
    global yelmas
    global yellmsg

    txt = str(message.text)
    x = str(message.text).split(' ',1)

    ### Errors and var checks ###
    check_users_loaded(message.chat.id)

    try:
        x[1] = x[1]
        if (yelling != 0):
            amb.log('/yell execution failed, Code: another /yell is running, Executor: '+message.from_user.first_name)
            bot.send_message(message.chat.id, 'Ты не завершил другой <b>/yell</b> !' ,parse_mode='html')
            return  
        if (txt.find('<') != -1) or (txt.find('>') != -1):
            amb.log('/yell execution failed, Code: html tag abuse, Executor: '+message.from_user.first_name)
            bot.send_message(message.chat.id, 'Клуб хейтеров питона обьявляет хтмл государственной религией. Ты написал запрещенный символ("<" или ">") !')
            return
    except NameError:
        yelling = 0
    except IndexError:
        amb.log('/yell execution failed, Code: no /yell msg, Executor: '+message.from_user.first_name)
        bot.send_message(message.chat.id, 'Ты не написал <b>аргумент</b> (<b>само сообщение</b>)!' ,parse_mode='html')
        return

    ### Code starts here ###   
    yelling = 1
    yelmas = []
    yellmaster = message.from_user.id

    #Inline buttons
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Могу ответить 🤙", callback_data='good')
    item2 = types.InlineKeyboardButton("Хз 🤐", callback_data='bad')
    markup.add(item1, item2)

    #Building yellmsg (include question and usr who asks)
    mention = '<a href="tg://user?id='+str(message.from_user.id)+'">'+message.from_user.first_name+'</a>'
    yellmsg = x[1]+'\n - от <b>'+mention+'</b>\n'
        
    #Building submsg (include buttons and usrs who answer) and yellmas   
    submsg = ' - не ответили '
    for i in range(len(config.USERS)):
        usr_i = bot.get_chat_member(message.chat.id,config.USERS[i]).user
        print('checking 1 '+str(usr_i)+'///'+usr_i.first_name)
        if (usr_i.id != message.from_user.id):
            print('checking 2 '+str(usr_i))
            mention = '<a href="tg://user?id='+str(usr_i.id)+'">'+usr_i.first_name+'</a>'
            submsg = submsg + '<b>' + mention + '</b>, '
            yelmas.append(usr_i.id)

    #Debug and sending
    amb.debug('yelling: '+str(yelling)+', yelmas: '+str(yelmas))
    yellmsgid = bot.send_message(message.chat.id, yellmsg+submsg[0:len(submsg)-2] ,parse_mode='html', reply_markup=markup)



@bot.message_handler(commands=['yellend'])
def execute(message):
    amb.log('/yellend executed, Executor: '+message.from_user.first_name)


@bot.message_handler(content_types=['text'])
def lalala(message):
    txt = str(message.text)
    x = txt.split(' ')
    msg = ''

    if x[0] == '!list':
        amb.log(x[0]+' executed, Executor: '+message.from_user.first_name)
        count = bot.get_chat_members_count(message.chat.id)
        if (count==1):
        	okon = ''
        elif (count==2) or (count==3) or (count==4):
        	okon = 'а'
        else:
        	okon = 'ов'
        msg = 'Сейчас в чате зарегестрировано '+str(len(config.USERS))+' участник'+okon+':\n'

        for i in range(len(config.USERS)):
            # usr = bot.get_chat_member(message.chat.id,1).user
            # bot.send_message(message.chat.id, usr.first_name+' - '+usr.username)
            msg = str(msg) +'- '+bot.get_chat_member(message.chat.id,config.USERS[i]).user.first_name+' ['+str(config.USERS[i])+']'
            msg = str(msg) + '\n'	
            # bot.send_message(message.chat.id, msg.format(message.from_user, bot.get_me()),parse_mode='html')
        bot.send_message(message.chat.id, msg,parse_mode='html')

    elif x[0] == '!myid':
    	amb.log(x[0]+' executed, Executor: '+message.from_user.first_name)
    	bot.send_message(message.chat.id, 'Your id is '+str(message.from_user.id))
    	# amb.debug(bot.get_chat_member(message.chat.id,message.from_user.id).user.username)
    	# message.from_user.id

    elif x[0] == '!yell':
        global yelling
        global yellmaster
        global yellmsgid
        try:
            if yelling == -228:
                pass
        except NameError:
            yelling = 0
        try:
            if (yelling == 0):
                if (x[1]==1):
                	pass
                amb.log(x[0]+' executed, Executor: '+message.from_user.first_name)

                global yelmas
                global yellmsg
                yelling = 1
                yelmas = []
                yellmaster = message.from_user.id

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Могу ответить 🤙", callback_data='good')
                item2 = types.InlineKeyboardButton("Хз 🤐", callback_data='bad')
    	 
                markup.add(item1, item2)
                mention = '<a href="tg://user?id='+str(message.from_user.id)+'">'+message.from_user.first_name+'</a>'
                msg = txt[6:len(txt)]+'\n - от <b>'+mention+'</b>\n'
                yellmsg = msg
                submsg = ' - не ответили '
                for i in range(len(config.USERS)):
                	usr_i = bot.get_chat_member(message.chat.id,config.USERS[i]).user
                	if (usr_i.id != message.from_user.id):
                            # mention = '<a href="tg://user?id='+str(usr_i.id)+'">@'+usr_i.first_name+'</a>'
                            mention = '<a href="tg://user?id='+str(usr_i.id)+'">'+usr_i.first_name+'</a>'
                            submsg = submsg + '<b>' + mention + '</b>, '

                            yelmas.append(usr_i.id)
                amb.debug('yelling: '+str(yelling)+', yelmas: '+str(yelmas))

                yellmsgid = bot.send_message(message.chat.id, msg+submsg[0:len(submsg)-2] ,parse_mode='html', reply_markup=markup)
            else:
                amb.log(x[0]+' execution failed, Executor: '+message.from_user.first_name)
                bot.send_message(message.chat.id, 'Ты не завершил другой <b>!yell</b> !' ,parse_mode='html')

	       	# bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="Всё ок!")

        except telebot.apihelper.ApiException:
        	amb.log(x[0]+' execution failed, Executor: '+message.from_user.first_name)
        	bot.send_message(message.chat.id, 'Клуб хейтеров питона обьявляет хтмл государственной религией. Ты не закрыл <b>тег</b>!' ,parse_mode='html')
        except IndexError:
            amb.log(x[0]+' execution failed, Executor: '+message.from_user.first_name)
            bot.send_message(message.chat.id, 'Ты не написал <b>аргумент</b> (<b>само сообщение</b>)!' ,parse_mode='html')
    
    elif x[0] == '!yellend':
        status = bot.get_chat_member(message.chat.id,message.from_user.id).status
        try:
            if  (status == "administrator") or (status == "creator") or (message.from_user.id == yellmaster):
                strid = '<a href="tg://user?id='+str(message.from_user.id)+'">@'+message.from_user.first_name+'</a>'
                
                # yellmsgid.message_id
                if len(yelmas) != 0:
                    bot.send_message(message.chat.id, '<b>'+strid+'</b> заврешил <b>!yell</b>' ,parse_mode='html')
                    submsg = ' - не ответили '
                    for i in range(len(yelmas)):
                        # mention = '<a href="tg://user?id='+str(usr_i.id)+'">@'+usr_i.first_name+'</a>'
                        usr_i = bot.get_chat_member(yellmsgid.chat.id,yelmas[i]).user
                        mention = '<a href="tg://user?id='+str(usr_i.id)+'">'+usr_i.first_name+'</a>'
                        submsg = submsg + '<b>' + mention + '</b>, '
                    
                    yelling = 0
                        
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("Результаты 💼", callback_data='res')
                    markup.add(item1)

                    bot.edit_message_text(chat_id=yellmsgid.chat.id, message_id=yellmsgid.message_id, text=yellmsg+submsg[0:len(submsg)-2],reply_markup=markup,parse_mode='html')
                else:
                    bot.send_message(message.chat.id, 'Дурачёк? <b>!yell</b> уже завершён (Совершённый вид глагола)!' ,parse_mode='html')

            else:
                bot.send_message(message.chat.id, 'Ты не создатель <b>!yell</b> и не админ!' ,parse_mode='html')
        except NameError:
            yellmaster = 0
            bot.send_message(message.chat.id, 'Ты не создатель <b>!yell</b> и не админ!' ,parse_mode='html')
    else:
        # mrsg = bot.send_message(message.chat.id, message.text)
        amb.log('msg sent: '+message.text+' chat id: '+str(message.chat.id))
        # time.sleep(0.5)
        # bot.edit_message_text(chat_id = message.chat.id,message_id = mrsg.message_id,text = mrsg.text+' - идиотический посыл сообщения')

@bot.message_handler(content_types=['voice'])
def pizdec(message):
	# fle = InputMediaPhoto
	# 	fle = open('content/voicemsg.jpg', 'r')
	bot.send_photo(chat_id = message.chat.id,photo = 'https://imgur.com/a/sAxEB5X')
	print(' voice: '+str(message.voice.duration))

@bot.message_handler(content_types=['new_chat_members'])
def mem_counter_add(message):
    check_users_loaded(message.chat.id)

    for i in range(len(message.new_chat_members)):
    	amb.debug('Members update => New Member: '+str(message.new_chat_members[i]))
    	config.USERS.append(str(message.new_chat_members[i].id))
    amb.log('USERS array update: '+str(config.USERS))


	#writing
    f = open("content/members.txt"+str(message.chat.id), "w")
    desplit = ''
    for i in range(len(config.USERS)):
    	desplit = desplit+str(config.USERS[i])+' '
    f.write(desplit)
    f.close()

@bot.message_handler(content_types=['left_chat_member'])
def mem_counter_leave(message):
    amb.debug('Members update => Member Leaved: '+str(message.left_chat_member))
    check_users_loaded(message.chat.id)
    if (str(message.left_chat_member.id) in str(config.USERS)):
        check_users_loaded(message.chat.id)

        config.USERS.remove(str(message.left_chat_member.id))

		#writing
        f = open("content/members.txt"+str(message.chat.id), "w")
        desplit = ''
        for i in range(len(config.USERS)):
        	desplit = desplit+str(config.USERS[i])+' '
        f.write(desplit)
        f.close()

        amb.log('USERS array update: '+str(config.USERS))
    else:
    	amb.log('USERS array update: '+str(config.USERS)+'\n      Id('+str(message.left_chat_member.id)+') wasn`t in array!')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if (call.from_user.id in yelmas):
                if call.data == 'good':
                    mention = '<a href="tg://user?id='+str(call.from_user.id)+'">'+call.from_user.first_name+'</a>'
                    bot.send_message(call.message.chat.id, '<b>'+mention+'</b> может ответить!',parse_mode='html', reply_to_message_id = call.message.message_id)
                elif call.data == 'bad':
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="Печально")

                amb.log('!yell answered, Answerer: '+call.from_user.first_name)

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Могу ответить 🤙", callback_data='good')
                item2 = types.InlineKeyboardButton("Хз 🤐", callback_data='bad')

                # txt = yellmsg
         
                markup.add(item1, item2)
                # msg = txt[6:len(txt)]+'\n - от <b>'+call.from_user.first_name+'</b>\n'

                amb.debug(str(yelmas)+'/'+str(call.from_user.id))
                yelmas.remove(call.from_user.id)
                if len(yelmas) != 0:
                    submsg = ' - не ответили '
                    for i in range(len(yelmas)):
                        # mention = '<a href="tg://user?id='+str(usr_i.id)+'">@'+usr_i.first_name+'</a>'
                        usr_i = bot.get_chat_member(call.message.chat.id,yelmas[i]).user
                        mention = '<a href="tg://user?id='+str(usr_i.id)+'">'+usr_i.first_name+'</a>'
                        submsg = submsg + '<b>' + mention + '</b>, '
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=yellmsg+submsg[0:len(submsg)-2],reply_markup=markup,parse_mode='html')
                else:
                    submsg = ' - <b>все</b> ответили! '

                    global yelling
                    yelling = 0
                        
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("Результаты 💼", callback_data='res')
                    markup.add(item1)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=yellmsg+submsg[0:len(submsg)-2],reply_markup=markup,parse_mode='html')


                amb.debug('yelling: '+str(yelling)+', yelmas: '+str(yelmas))

            elif call.data == 'res':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="Не доступно (")    
            else:
                if (str(call.from_user.id) in str(config.USERS)):
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="Вы уже ответили или вы создатель !yell!")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="Вы не зарагестрированы!")
 
            # remove inline buttons


            # bot.send_message(message.chat.id, msg+submsg[0:len(submsg)-2] ,parse_mode='html', reply_markup=markup)

    except Exception as e:
        print(repr(e))
	


bot.polling(none_stop=True)


