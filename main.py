from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
import db
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import config

bot = Bot(config.API_TOKEN,parse_mode='HTML') 
dp = Dispatcher(bot,storage=MemoryStorage()) 

admin = config.admin

class Data(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()

class Spam(StatesGroup):
    q1 = State()

class Add_drugs(StatesGroup):
    q1 = State()

class Delete_drugs(StatesGroup):
    q1 = State()

def get_price(amount: float):
    s = requests.get(f'https://pokur.su/rub/btc/{amount}/')
    soup = BeautifulSoup(s.text, 'html.parser')
    rate = soup.find('input', attrs={'data-role': 'secondary-input'})
    return rate['value']

@dp.message_handler(commands="start",state='*')
async def start(message: types.Message,state:FSMContext):
    await db.users(message.from_user.id)
    if admin != message.from_user.id:
        button = buttons.main_buttons
        await message.answer('''Маркетплейс 🛍  <b>HYDRA</b>  🤖
Удобно. Надёжно. Безопасно.
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Сервер и сайт <b>Hydra не доступны.</b>
Все продажи через бота ✅
Мы сделаем рассылку когда сайт заработает 🔔‼️
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Для перезапуска бота нажмите /start''',reply_markup=button)
        await state.finish()
    elif admin == message.from_user.id:
        await message.answer('Админ',reply_markup=buttons.admin_buttons)

@dp.message_handler(text='Добавить товар',state='*')
async def admin_10(message:types.Message,state:FSMContext):
	if admin == message.from_user.id:
		await state.finish()
		await message.answer(f'Введите товар\nПример: <code>Марихуана:0.5:1000:Вещество</code>')
		await Add_drugs.first()

@dp.message_handler(state=Add_drugs.q1)
async def admin_8(message:types.Message,state:FSMContext):
	check = await db.add_tovar(message.text)
	if check is False:
		await message.answer('<b>Произошла ошибка!</b>')
	else:
		await message.answer('<b>Товар успешно добавлен.</b>')
	await state.finish()

@dp.message_handler(text='Удалить товар',state='*')
async def admin_10(message:types.Message,state:FSMContext):
	if admin == message.from_user.id:
		await state.finish()
		await message.answer(f'<b>Введите товар\nПример:</b> <code>Марихуана:0.5</code>')
		await Delete_drugs.first()

@dp.message_handler(state=Delete_drugs.q1)
async def admin_8(message:types.Message,state:FSMContext):
	if admin == message.from_user.id:
		check = await db.delete_tovar(message.text)
		if check is False:
			await message.answer('<b>Произошла ошибка!</b>')
		else:
			await message.answer('<b>Район успешно удален.</b>')
		await state.finish()

@dp.message_handler(text='Статистика',state='*')
async def admin_9(message:types.Message,state:FSMContext):
	if admin == message.from_user.id:
		await state.finish()
		all = await db.all_user()
		await message.answer(f'<b>Всего людей:</b> {all}')

@dp.message_handler(text='Рассылка',state='*')
async def admin_10(message:types.Message,state:FSMContext):
	if admin == message.from_user.id:
		await state.finish()
		await message.answer(f'<b>Введите сообщение:</b>')
		await Spam.first()

@dp.message_handler(state=Spam.q1)
async def admin_11(message:types.Message,state:FSMContext):
	with sqlite3.connect('db.db') as c:
		all_users = c.execute("SELECT * FROM users").fetchall()
	for user in all_users:
		await bot.send_message(user[0],text=message.text)
	await state.finish()

@dp.message_handler(text="📖 Меню",state='*')
async def menu(message: types.Message,state:FSMContext):
    await state.finish()
    await message.answer("<b>Введите ваш город:</b>")
    await Data.q1.set()

@dp.message_handler(state=Data.q1)
async def cities(message: types.Message,state:FSMContext):
	check = await buttons.check_city(message.text)
	if check is True:
		await state.update_data(city=message.text)
		await message.answer("<b>Введите ваш район:</b>")
		await Data.next()
	else:
		await message.answer("Такого города у нас нет")

@dp.message_handler(state=Data.q2)
async def cities10(message:types.Message,state: FSMContext):
	drug = await buttons.ret_type()
	await message.answer("<b>Выберите тип :</b>",reply_markup=drug)
	await state.update_data(street=message.text)
	await Data.next()

@dp.callback_query_handler(text_startswith="type",state=Data.q3)
async def cities10(callback:types.CallbackQuery,state: FSMContext):
	c = callback.data.split("|")[1]
	drug = await buttons.drugs(c)
	await callback.message.edit_text("<b>Выберите товар:</b>",reply_markup=drug)
	await state.update_data(type=c)
	await Data.next()	

@dp.callback_query_handler(text_startswith='drug',state=Data.q4)
async def call(callback: types.CallbackQuery,state:FSMContext):
	global gjgkg
	gjgkg = callback.data.split('_')[1]
	await state.update_data(drug=gjgkg)
	button = await buttons.drugs_2(gjgkg)
	await callback.message.edit_text('<b>Выберите вес:</b>',reply_markup=button)
	await Data.next()

@dp.callback_query_handler(text_startswith='drugs2',state=Data.q5)
async def call(callback: types.CallbackQuery,state:FSMContext):
	call = callback.data.split('_')
	await state.update_data(gramm=call[1],price=call[2])
	button = await buttons.pay()
	await callback.message.edit_text('Выбери 6',reply_markup=button)
	await Data.next()

@dp.callback_query_handler(text_startswith='value',state=Data.q6)
async def call(callback: types.CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text='<b>⏳ Обрабатываю запрос...</b>')
    a = 4
    call = callback.data.split('_')[1]
    all = await state.get_data()
    print(all)
    city = all.get('city')
    street = all.get('street')
    drug = all.get('drug')
    gramm = all.get('gramm')
    price = all.get('price')
    button = await buttons.cheakpay()
    type = all.get("type")
    pays = {
        'Карта': '<b>Город: {}\nУлица: {}\nТип:{}\nТовар: {}\nКоличество: {}\nЦена:</b> <code>{}</code>\nКарта: <code>' + config.CARD + '</code>\n\n<b>Проверка платежа автоматическая.</b>\n<i>После оплаты вы получите адрес, фото, описание и GPS координаты.</i>',
        'QIWI': '<b>Город: {}\nУлица: {}\nТип:{}\nТовар: {}\nКоличество: {}\nЦена:</b> <code>{}</code> Руб\nQIWI: <code>' + config.QIWI + '</code>\n\n<b>В коментарии укажите:</b> <code>651602823</code>\n<b>Проверка платежа автоматическая.</b>\n<i>После оплаты вы получите адрес, фото, описание и GPS координаты.</i>',
        'BTC': '<b>Город: {}\nУлица: {}\nТип:{}\nТовар: {}\nКоличество: {}\nЦена:</b> <code>'+get_price(price)+'</code> BTC\nBTC: <code>' + config.BTC + '</code>\n\n<b>Проверка платежа автоматическая.</b>\n<i>После оплаты вы получите адрес, фото, описание и GPS координаты</i>'
    }
    time.sleep(a)
    await callback.message.edit_text(text=pays.get(call).format(city,street,type,drug,gramm,price), reply_markup=button)
    await state.finish()

@dp.callback_query_handler(text_startswith="back",state='*')
async def backss(callback: types.CallbackQuery,state: FSMContext):
	if callback.data.startswith('back_0'):
		await state.reset_state(with_data=False)
		await Data.first()
		button = await buttons.buttons()
	elif callback.data.startswith('back_1'):
		await state.reset_state(with_data=False)
		await Data.q3.set()
		button = await buttons.ret_type()
	elif callback.data.startswith('back_2'):
		await state.reset_state(with_data=False)
		await Data.q4.set()
		button = await buttons.drugs()
	elif callback.data.startswith('back_3'):
		await state.reset_state(with_data=False)
		await Data.q5.set()
		button = await buttons.drugs_2(gjgkg)
	await callback.message.edit_text("<b>Вы вернулись.</b>", reply_markup=button)
    
@dp.callback_query_handler(lambda c: c.data == 'cheakk')
async def mainstartbuy(call: types.CallbackQuery):
    await call.answer(text='Оплата еще не поступила.')

executor.start_polling(dp)
