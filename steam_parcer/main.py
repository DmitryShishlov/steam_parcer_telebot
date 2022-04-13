from telebot import *
from configure import config
from random_game import get_data

client = telebot.TeleBot(config['token'])


@client.message_handler(commands=['help'])
def help_command(message):
    client.send_message(message.chat.id, "Я могу /game")


@client.message_handler(commands=['game'])
def game_command(message):
    markup_inline = types.InlineKeyboardMarkup()
    popular_new = types.InlineKeyboardButton(text='Популярные новинки', callback_data='pn')
    top_sellers = types.InlineKeyboardButton(text='Лидеры продаж', callback_data='ts')
    other_plays = types.InlineKeyboardButton(text='Во что играют другие', callback_data='op')
    future_products = types.InlineKeyboardButton(text='Будущие продукты', callback_data='fp')

    markup_inline.add(popular_new, top_sellers, other_plays, future_products)

    client.send_message(message.chat.id, 'Найти случайную бесплатную игру из разделов:',
                        reply_markup=markup_inline
                        )


@client.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'back':
        markup_inline = types.InlineKeyboardMarkup()
        popular_new = types.InlineKeyboardButton(text='Популярные новинки', callback_data='pn')
        top_sellers = types.InlineKeyboardButton(text='Лидеры продаж', callback_data='ts')
        other_plays = types.InlineKeyboardButton(text='Во что играют другие', callback_data='op')
        future_products = types.InlineKeyboardButton(text='Будущие продукты', callback_data='fp')

        markup_inline.add(popular_new, top_sellers, other_plays, future_products)
        client.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text='Найти случайную бесплатную игру из разделов:',
                                 reply_markup=markup_inline
                                 )
    elif call.data == 'pn' or call.data == 'ts' or call.data == 'op' or call.data == 'fp':
        markup_inline = types.InlineKeyboardMarkup()
        if call.data == 'pn':
            game_button = types.InlineKeyboardButton(text='Да', callback_data='pn_get')
            markup_inline.add(game_button)
        elif call.data == 'ts':
            game_button = types.InlineKeyboardButton(text='Да', callback_data='ts_get')
            markup_inline.add(game_button)
        elif call.data == 'op':
            game_button = types.InlineKeyboardButton(text='Да', callback_data='op_get')
            markup_inline.add(game_button)
        elif call.data == 'fp':
            game_button = types.InlineKeyboardButton(text='Да', callback_data='fp_get')
            markup_inline.add(game_button)
        back_button = types.InlineKeyboardButton(text='Назад', callback_data='back')

        markup_inline.add(back_button)
        client.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text='Найти игру?',
                                 reply_markup=markup_inline
                                 )
    elif call.data == 'pn_get':
        game = get_data('Популярные новинки')
        markup_inline = types.InlineKeyboardMarkup()
        game_button = types.InlineKeyboardButton(text='Еще', callback_data='pn_get')
        back_button = types.InlineKeyboardButton(text='Назад', callback_data='back')
        markup_inline.add(game_button, back_button)
        # client.send_message(call.message.chat.id, f"{game['Ссылка']}")
        client.send_message(call.message.chat.id, f"{game['Название']}\n{game['Тэги']}\n{game['Ссылка']}",
                            reply_markup=markup_inline)
    elif call.data == 'ts_get':
        game = get_data('Лидеры продаж')
        markup_inline = types.InlineKeyboardMarkup()
        game_button = types.InlineKeyboardButton(text='Еще', callback_data='ts_get')
        back_button = types.InlineKeyboardButton(text='Назад', callback_data='back')
        markup_inline.add(game_button, back_button)

        client.send_message(call.message.chat.id, f"{game['Название']}\n{game['Тэги']}\n{game['Ссылка']}",
                            reply_markup=markup_inline)
    elif call.data == 'op_get':
        game = get_data('Во что играют другие')
        markup_inline = types.InlineKeyboardMarkup()
        game_button = types.InlineKeyboardButton(text='Еще', callback_data='op_get')
        back_button = types.InlineKeyboardButton(text='Назад', callback_data='back')
        markup_inline.add(game_button, back_button)

        client.send_message(call.message.chat.id, f"{game['Название']}\n{game['Тэги']}\n{game['Ссылка']}",
                            reply_markup=markup_inline)
    elif call.data == 'fp_get':
        game = get_data('Будущие продукты')
        markup_inline = types.InlineKeyboardMarkup()
        game_button = types.InlineKeyboardButton(text='Еще', callback_data='fp_get')
        back_button = types.InlineKeyboardButton(text='Назад', callback_data='back')
        markup_inline.add(game_button, back_button)

        client.send_message(call.message.chat.id, f"{game['Название']}\n{game['Тэги']}\n{game['Ссылка']}",
                            reply_markup=markup_inline)


client.polling(none_stop=True, interval=0)
