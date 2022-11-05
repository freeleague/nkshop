from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton,InlineKeyboardMarkup, KeyboardButton
import asyncio
import sqlite3

main_buttons = ReplyKeyboardMarkup(
	keyboard = [
		[
            KeyboardButton(text="📖 Меню")
		],
	],
	resize_keyboard=True
	)

admin_buttons = ReplyKeyboardMarkup(
	keyboard=[
        [
            KeyboardButton(text="📖 Меню")
		],
		[
			KeyboardButton(text="Добавить товар"),
			KeyboardButton(text="Удалить товар")
		],
		[
			KeyboardButton(text="Статистика"),
			KeyboardButton(text="Рассылка")
		],
	],
	resize_keyboard=True
)

async def drugs(arg):
    buttons = InlineKeyboardMarkup(row_width=2)
    with sqlite3.connect('work.db') as c:
        dr = c.execute('SELECT name FROM drugs WHERE tip = ?',(arg,)).fetchall()
    drugs = [dru[0] for dru in dr]
    drugs = list(set(drugs))
    for _ in drugs:
        buttons.add(InlineKeyboardButton(text=f"{_}",callback_data=f"drug_{_}"))
    buttons.add(InlineKeyboardButton(text=f"🔙", callback_data=f"back_1_arg"))
    return buttons

async def drugs_2(drug):
	buttons = InlineKeyboardMarkup()
	with sqlite3.connect('work.db') as c:
		dr = c.execute('SELECT gramm,price FROM drugs WHERE name = ?',(drug,)).fetchall()
	for gramm,price in dr:
		buttons.add(InlineKeyboardButton(text=f'Количество: {gramm}гр. Цена: {price} Руб.', callback_data=f"drugs2_{gramm}_{price}"))
	buttons.add(InlineKeyboardButton(text=f"🔙", callback_data=f"back_2"))
	return buttons

async def pay():
	buttons = InlineKeyboardMarkup()
	pays = {
		'Карта':'Карта',
		'QIWI':'QIWI',
		'BTC':'BTC'
	}
	for wallet,value in pays.items():
		buttons.add(InlineKeyboardButton(text=f'{wallet}',callback_data=f'value_{value}'))
	buttons.add(InlineKeyboardButton(text=f"🔙", callback_data=f"back_3"))
	return buttons

async def cheakpay():
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(text=f"🔘 Проверить платеж", callback_data=f"cheakk"))
    return buttons
    
async def check_city(word):
	with open("города.txt","r",encoding="utf-8") as c:
		checks = c.read().lower().split()
		return word.lower() in checks

async def ret_type():
	with sqlite3.connect("work.db") as c:
		all= c.execute("SELECT tip FROM drugs").fetchall()
		key = list({one[0] for one in all})
		button = InlineKeyboardMarkup()
		for i in key:
			button.add(
			InlineKeyboardButton(text=i,callback_data=f"type|{i}")
			)
		return button