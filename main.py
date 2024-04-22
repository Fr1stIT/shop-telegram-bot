import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, CallbackQuery
import keyboards as kb
from aiogram.fsm.context import FSMContext
from conf import bot_api
from aiogram.filters.command import Command
from db_postgres import Database
from states import *


from aiogram.filters import CommandStart, CommandObject



bot = Bot(token=bot_api)
dp = Dispatcher()

admin_id = (1061467560,)

async def main():
    await dp.start_polling(bot)

db_params = {
    "host": "localhost",
    "database": "TgShop",
    "user": "postgres",
    "password": "7292",
    "port": "5432"
}
db = Database(db_params)


@dp.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject, state: FSMContext):
    if db.get_info(message.from_user.id) == []:
        print('Попытка добавления пользователя...')
        db.add_user(message.from_user.id, message.from_user.username)
    # print(db.get_info(message.from_user.id))
    args = command.args
    print(f'Переход по ссылке с аргументом: {args}')
    data = db.get_info_product_id(args)
    data = data[0]
    # print(data[5])
    stringformat = f'<b>🛒 Вы собираетесь купить товар:</b> 🛒\n<b>💫 Название</b> - {data[1]}\n💫 <b>Описание</b> - {data[3]}\n💫 <b>Стоимость</b> - <b>{data[2]}</b>'

    await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile(path=data[4]), caption=stringformat, reply_markup=kb.ver_button('Купить', 'Отмена'), parse_mode='html')
    await state.update_data(order=data[0], cost=data[2])
    await state.set_state(Buy_item.address)


@dp.message(Command('start'))
async def strt_command (message: Message):
    if message.from_user.id in admin_id:
        await message.answer('Вы администратор!', reply_markup=kb.main_kb_admin)
    else:
        await message.answer(text='Добро пожаловать! Для заказа товара перейдите в наш телеграм канал t.me/xxx', reply_markup=kb.main_kb)
        try:
            print('Попытка добавления пользователя...')
            db.add_user(message.from_user.id, message.from_user.username)
        except:
            pass



###########################################################################################################################


@dp.message(F.text == 'Добавить товары')
async def add_new_it (message: Message, state: FSMContext):
    if message.from_user.id in admin_id:
        await message.reply('Введите название товара')
        await state.set_state(Add_new_prod.name)


@dp.message(F.text == 'Удалить товар')
async def delete_it (message: Message, state: FSMContext):
    if message.from_user.id in admin_id:
        await message.reply('Выберите товар для удаления', reply_markup=kb.prod_button(db.get_products()))
        await state.set_state(Delete_prod.name_of_it)

############################################################################################################################


@dp.callback_query(Delete_prod.name_of_it)
async def get_name_of_the_prd(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    data = db.get_info_product(callback.data)
    data = data[0]
    print(data)
    await callback.message.answer(f'Вы собираетесь удалить товар:\n<b>Название</b> - {data[1]}\n<b>Описание</b> - {data[3]}\n<b>Стоимость</b> - {data[2]}', reply_markup=kb.ver_button('Да','Нет'), parse_mode='html')
    await state.update_data(name_of_it=data[1])
    await state.set_state(Delete_prod.rep)

@dp.callback_query(Delete_prod.rep)
async def get_name_of_the_prd(callback: CallbackQuery, state: FSMContext):

    if callback.data == 'Да':
        data = await state.get_data()
        data = data["name_of_it"]
        await callback.answer('')
        await callback.message.answer(f'<b>🗑 Вы удалили товар:</b> {data}', parse_mode='html')
        db.delete_item(data)

    elif callback.data == 'Нет':
        await callback.answer('')
        await callback.message.answer('Вы отменили удаление товара!')
    await state.clear()


#######################################################################################################################################


@dp.message(Add_new_prod.name)
async def name_of_prd (message: Message, state: FSMContext):
    if message.from_user.id in admin_id:
        await state.update_data(name=message.text)
        await message.reply('Напишите описание товара')
        await state.set_state(Add_new_prod.about)

@dp.message(Add_new_prod.about)
async def about_prd (message: Message, state: FSMContext):
    if message.from_user.id in admin_id:
        await state.update_data(about=message.text)
        await message.reply('Укажите цену товара')
        await state.set_state(Add_new_prod.price)





@dp.message(Add_new_prod.price)
async def price_of_prd (message: Message, state: FSMContext):

    await message.answer('Отправите фотографию товара')
    await state.update_data(price=message.text)
    await state.set_state(Add_new_prod.photo)


@dp.message(Add_new_prod.photo)
async def process_photo(message: types.Message, state: FSMContext):
    data1 = await state.get_data()
    file_name = f"img/{data1['name']}.jpg"
    await message.bot.download(file=message.photo[-1].file_id, destination=file_name)
    await message.reply(f'✅ Ваш товар: \n<b>Название</b> - {data1["name"]}\n<b>Описание</b> - {data1["about"]}\n<b>Стоимость</b> - {data1["price"] + "₽"}', parse_mode='html')
    product_id = db.add_product(data1["name"], data1["about"], data1["price"], file_name)
    await message.answer(f'🔗 https://t.me/fristshop_bot?start={product_id[0]} 🔗')


#########################################################################################################################################################


@dp.callback_query(Buy_item.address)
async def item_buy(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Отмена':
        await state.clear()
        await callback.answer('Вы отменили покупку товара :(')
    else:
        await callback.answer('')
        await callback.message.answer(
            f'🏠 Укажите свой адрес. Пример: г.Санкт-Петербург, ул.Исаакиевская пл.4',)

        await state.set_state(Buy_item.phone_number)



@dp.message(Buy_item.phone_number)
async def item_buy (message: Message, state: FSMContext):
    await message.answer(
        f'👤 Укажите свои Имя и Фамилию')
    await state.update_data(address = message.text)
    await state.set_state(Buy_item.name)


@dp.message(Buy_item.name)
async def item_buy (message: Message, state: FSMContext):
    await message.answer(
        f'📞 Укажите свой номер телефона. Например: +7952812999')
    await state.update_data(name = message.text)
    await state.set_state(Buy_item.order)



@dp.message(Buy_item.order)
async def item_buy (message: Message, state: FSMContext):
    phone_number = message.text
    data = await state.get_data()
    print(data)
    db.order(data["name"],message.from_user.id, data["order"], data["address"], phone_number)
    await message.answer(
        f'✅ <b>Заказ номер {message.from_user.id} открыт!</b> ✅\n🏠 <b>Адрес доставки:</b> {data["address"]}\n📞 <b>Номер телефона:</b> {phone_number}\n<b>Чтобы отменить его, напишите /cancel</b>\n💸 Оплатите на карту Сбербанка по номеру <b>+79951714556 (Елена Р.)</b> сумму <b>{data["cost"]}</b> и пришлите чек в этот чат.', parse_mode='html')

    await state.set_state(Buy_item.check)




@dp.message(Buy_item.check and Command('cancel'))
async def canccel_but (message: Message, state: FSMContext):
    await state.clear()
    await message.reply('❌ Вы отменили покупку товара! ❌')
    #Запрос к базе данных (удаление ордера)
    db.cancel_order(message.from_user.id)



@dp.message(Buy_item.check)
async def verify_buy (message: Message, state: FSMContext):
    #Пересылка сообщения другому человеку (по user_id указанному заранее)
    if message.photo or message.document:
        data = await state.get_data()
        cost = data["cost"]
        orderss = db.check_order(message.from_user.id)[0]
        print(orderss)
        string = f'<b>Заказ №{orderss[0]}</b>. <b>{orderss[2]}</b>\n<b>Товар</b> - {db.get_info_product_id(orderss[4])[0][1]}.\n<b>Адрес</b>: {orderss[5]}\n<b>Номер телефона:</b> {orderss[6]}\n<b>Стоитмость товара:</b> {cost}\n<b>Юзернейм:</b> {message.from_user.username}'
        await bot.send_message(chat_id=admin_id[0], text='<b>Поступил новый заказ!</b>', parse_mode='html')
        await message.send_copy(chat_id=admin_id[0])
        await bot.send_message(admin_id[0], string, reply_markup=kb.submit_payment(str(orderss[0])), parse_mode='html')

        await message.reply('🧾 Ваш чек был отправлен администратору, ожидайте ответ!')
        await state.clear()
    else:
        await message.reply('Отправьте фотографию или документ!')


##################################################################################################################################################################


@dp.callback_query()
async def item_buy (callback: CallbackQuery, state: FSMContext):
   if callback.from_user.id in admin_id:
       if callback.data.startswith("PIN"):
           try:
                print(db.get_open_order(callback.data[3:]))
                if db.get_open_order(callback.data[3:]) is None:
                    print('Get pos code вернул: '+ str(db.get_post_code(user_id=callback.data[3:])[0]))
                    if db.get_post_code(user_id=callback.data[3:])[0] is None:
                       await callback.answer('')
                       await callback.message.answer('Отправте код отправления')
                       await state.update_data(id=int(callback.data[3:]))
                       await state.set_state(Send_post_code.wait_for_post_code)
                    else:
                        await callback.answer('У этого заказа уже есть код!')
                else:
                    await callback.answer('')
                    await callback.message.answer('Вы еще не подтвердили оплату товара! ')
           except TypeError as e:
               print(e)
               await callback.answer('Вы еще не подтвердили оплату товара!')
       else:
        await callback.answer('')
        db.move_data_to_orders(int(callback.data))
        await bot.send_message(int(callback.data), '🧾 Ваша оплата подтверждена аднимистратором! Ожидайте, с Вами свяжутся. ☑️')





@dp.message(Send_post_code.wait_for_post_code)
async def resend_post_code(message: Message, state: FSMContext):
    user_id = await state.get_data()
    user_id = user_id["id"]
    await bot.send_message(chat_id=user_id, text=f'<b>Ваш код отправления</b> <code>{message.text}</code>', parse_mode='html')
    await message.answer('Код отправления был успешно доставлен покупателю!')
    id_of_order = db.get_last_row_by_user_id(user_id)
    print(id_of_order)
    db.set_post_code(user_id, id_of_order, message.text)
    await state.clear()

##################################################################################################################################################################
@dp.message(F.text == 'Главная')
async def pick (message: Message):
    await message.reply('Вы на главной странице!', reply_markup=kb.main_kb)


@dp.message(F.text == 'Поддержка')
async def pick (message: Message):
    await message.reply('Для получения поддержки напишите нам: @Fr1st')



@dp.message(F.text == 'Товары')
async def pick (message: Message):
    if message.from_user.id in admin_id:
        products = db.get_products()
        for product in products:
            await message.answer(f'<b>Товар:</b> {product[1]}, <b>Стоимость:</b> {product[2]}\n 🔗 <b>Ссылка:</b> https://t.me/fristshop_bot?start={product[0]} 🔗', parse_mode='html')
    else:
        await message.reply('🔝 Для покупки товара, перейдите по специальной ссылке в карточке товара, доступной в нашем телеграм канале ')


@dp.message(F.text == 'Чеки')
async def pick (message: Message):
    if message.from_user.id in admin_id:
        db.export_orders()
        #отправка файла в чат админу
        await bot.send_document(admin_id[0], types.FSInputFile('orders_export.csv'))



if __name__ == '__main__':
    asyncio.run(main())

