from telebot import TeleBot, types
import logger as lg

TOKEN = ''
operation = []
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg: types.Message):
    lg.logging.info('Run command start')
    bot.send_message(msg.chat.id, f'Привет {msg.from_user.first_name}\n/menu - Вывести меню')

@bot.message_handler(commands=['menu'])
def menu(msg: types.Message):
    lg.logging.info('Run command menu')
    bot.send_message(msg.chat.id, f'/1. Произвести вычисления\n/2. Вывести log')

@bot.message_handler()
def warning(msg: types.Message):
    text = msg.text
    if msg.chat.type == 'private':
        if text == '/1':
            lg.logging.info('Selecting a Calculation Command')
            bot.send_message(msg.chat.id, 'Введите первое число')
            lg.logging.info('Entering the first number')
            bot.register_next_step_handler(msg, nums)

        elif text == '/2':
            lg.logging.info('Log command selection')
            bot.send_message(msg.chat.id, 'Вывожу лог')
            log(msg)

            
        else:
            lg.logging.info(f'Input Error {text}')    
            bot.send_message(msg.chat.id, 'Я ожидаю на вход /start')

def nums(msg: types.Message):
    if len(operation) < 3:
        text = msg.text
        
        if 'j' in text and len(operation) != 2:
            lg.logging.info(f'Processing a complex number {text}')
            operation.append(complex(text.replace(' ', '')))
            bot.send_message(msg.chat.id, 'Введите операцию\n+ - * /')
            bot.register_next_step_handler(msg, oper)

        elif 'j' in text and len(operation) == 2:
            lg.logging.info(f'Processing a complex number {text}')
            operation.append(complex(text.replace(' ', '')))
            bot.send_message(msg.chat.id, f'Результат: {vitch()}')

        elif text.isdigit() and len(operation) != 2:
            lg.logging.info(f'Rational number processing {text}')
            operation.append(float(text))
            bot.send_message(msg.chat.id, 'Введите операцию\n+ - * /')
            bot.register_next_step_handler(msg, oper)

        elif text.isdigit() and float(text) == 0 and operation[1] == '/':
            lg.logging.info(f'Division by zero')
            bot.send_message(msg.chat.id, 'Деление запрещено!')
            operation.clear()
        
        elif text.isdigit() and len(operation) == 2:
            lg.logging.info(f'Rational number processing {text}')
            operation.append(float(text))
            bot.send_message(msg.chat.id, f'Результат: {vitch()}')
            
        else:
            lg.logging.info(f'Input Error {text}')
            operation.clear()
            bot.send_message(msg.chat.id, 'Вы ввели хрень!')

def oper(msg: types.Message):
        text = msg.text
        lg.logging.info(f'Operation processing {text}')

        if text == '+':
            operation.append(text)
            bot.send_message(msg.chat.id, 'Введите второе число')
            bot.register_next_step_handler(msg, nums)

        elif text == '-':
            operation.append(text)
            bot.send_message(msg.chat.id, 'Введите второе число')
            bot.register_next_step_handler(msg, nums)

        elif text == '*':
            operation.append(text)
            bot.send_message(msg.chat.id, 'Введите второе число')
            bot.register_next_step_handler(msg, nums) 

        elif text == '/':
            operation.append(text)
            bot.send_message(msg.chat.id, 'Введите второе число')
            bot.register_next_step_handler(msg, nums)

        else:
            lg.logging.info(f'Input Error {text}')
            operation.clear()
            bot.send_message(msg.chat.id, 'Вы ввели херню') 

def vitch():
    lg.logging.info(f'Performing an operation {operation[1]}')

    if operation[1] == '+':
        result = operation[0] + operation[2]
        
    elif operation[1] == '-':
        result = operation[0] - operation[2]

    elif operation[1] == '*':
        result = operation[0] * operation[2]

    elif operation[1] == '/':
        result = operation[0] / operation[2]

    operation.clear()

    lg.logging.info(f'Output {result}')
    return result

@bot.message_handler(content_types=['text'])
def log(msg: types.Message):
    files = 'logger.log'
    with open(files, 'rb') as file:
        bot.send_chat_action(msg.from_user.id, 'upload_document')
        bot.send_document(msg.from_user.id, file)

bot.polling()
