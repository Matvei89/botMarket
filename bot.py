import telebot
from telebot import types
TOKEN = '7084003544:AAFBwstlctq2cwX-qeoLtKbLAv9qMfZos6A'

bot = telebot.TeleBot(TOKEN)

products = [
    {'id': 1, 'name': 'Samsung 23 ultra', 'price': 100000},
    {'id': 2, 'name': 'iphone 15', 'price': 190000},
    {'id': 3, 'name': 'xiaomi 10c', 'price': 15000},
    {'id': 4, 'name': 'oppo a96', 'price': 20000},
    {'id': 5, 'name': 'dexp', 'price': 6000}
]

carts = []

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('👤 Профиль'),
        types.KeyboardButton('📰 Каталог'),
        types.KeyboardButton('🏧 Корзина'),
        types.KeyboardButton('🛠 Мои заказы'),
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
   chat_id = message.chat.id
   bot.send_message(chat_id, f'Добро пожаловать в наш магазин!✅\nНаши контакты!', reply_markup=main_menu())


@bot.message_handler(func=lambda message: message.text == '📰 Каталог')
def catalog(message):
    for product in products:
        bot.send_message(message.chat.id, f'{product['name']} - {product['price']}', reply_markup=add_cart_button(product['id']))


def add_cart_button(id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Добавить в корзину', callback_data=f'add_to_cart_{id}')
    )
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_') )
def add_cart(call):
    txt = call.data
    txt_s = txt.split('_')
    id_product = int(txt_s[3])
    carts.append(id_product)
    bot.answer_callback_query(call.id, 'Товар добавлен в корзину!')
    #bot.send_message(call.id, 'Товар добавлен в корзину!',reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == '🏧 Корзина')
def cart(message):
    total_s = 0
    for product in products:
        if product['id'] in carts:
            bot.send_message(message.chat.id, f'{product['name']} - {product['price']} руб.')
            total_s += product['price']

    if len(carts) == 0:
        bot.send_message(message.chat.id, 'Корзина пуста', reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, f'Общая сумма заказа {total_s} руб.', reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == '👤 Профиль')
def profil(message):
   bot.send_message(message.chat.id,'Ваш профиль')
   bot.send_message(message.chat.id, f'Ваше имя: {message.from_user.first_name}\nВаш никнейм: {message.from_user.username}\nВаш id: {message.from_user.id}')
   if message.from_user.is_premium == None:
       bot.send_message(message.chat.id,'Телеграм премиум отсутсвует')
   else:
       bot.send_message(message.chat.id, 'Телеграм премиум активирован')


bot.polling()
#ДЗ сделать профиль пользователя
#В профиле вывести данные пользователя имя, фамилия, username