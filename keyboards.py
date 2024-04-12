from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

a = []
main_kb_button =[
    [KeyboardButton(text='Главная'),
     KeyboardButton(text='Товары ')],
    [KeyboardButton(text='Поддержка')]
]

main_kb = ReplyKeyboardMarkup(keyboard=main_kb_button, resize_keyboard=True)


main_kb_admin_button =[
    [KeyboardButton(text='Чеки'),
     KeyboardButton(text='Товары ')],
    [KeyboardButton(text='Добавить товары'),
     KeyboardButton(text='Удалить товар')]
]

main_kb_admin = ReplyKeyboardMarkup(keyboard=main_kb_admin_button, resize_keyboard=True)
def prod_button(list):
    sorted_list = sorted(list, key=lambda item: item[1])
    for temp in sorted_list:
        print(temp[1])
        a.append([InlineKeyboardButton(text=temp[1], callback_data=temp[1])])
    shop_kb = InlineKeyboardMarkup(inline_keyboard=a)
    a.clear()
    return shop_kb



def ver_button(first: str, second: str):
    kbb = [
        [InlineKeyboardButton(text=first, callback_data=first),
         InlineKeyboardButton(text=second, callback_data=second)]
    ]
    ver_kb = InlineKeyboardMarkup(inline_keyboard=kbb)
    return ver_kb



def submit_payment(callback_data):
    kbb = [
        [InlineKeyboardButton(text='Подтвердить' , callback_data=callback_data),
         ]
    ]

    ikb = InlineKeyboardMarkup(inline_keyboard=kbb)
    return ikb