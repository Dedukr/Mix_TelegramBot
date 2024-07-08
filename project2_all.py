import asyncio
import logging
import requests
import translate as trans
from aiogram import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import *
from bs4 import BeautifulSoup as BS
from pyowm.owm import OWM
from config import *


def weather(city):
    owm=OWM(owm)
    mgr = owm.weather_manager()
    w = mgr.weather_at_place(city).weather
    return w


def time(city):
    r = requests.get(f'https://time100.ru/{city}')
    html = BS(r.content, 'lxml')
    time_now = html.find(class_="time")
    return time_now.text


def translate(text):
    translator = trans.Translator(from_lang='en', to_lang='ru')
    a = translator.translate(text).lower()
    if a == "очистить":
        a = 'чистое небо'
    elif a == "облака":
        a = 'облачно'
    return a


def isdigit(a):
    prob = "".join(a.split(":")).isdigit()
    try:
        if prob:
            if ':' in a:
                a = a.split(":")
                if len(a) == 2:
                    if 0 <= int(a[0]) <= 23:
                        if 0 <= int(a[1]) <= 59:
                            if len(a[0]) == 1:
                                if a[0] == '0':
                                    a[0] = '00'
                                else:
                                    a[0] = str(int(a[0]) + 12)
                            if len(a[1]) == 1:
                                if int(a[1]) <= 5:
                                    a[1] = "0" + a[1]
                                else:
                                    return False, a
                            return True, a
        return False, a
    except:
        return False, a


b1 = KeyboardButton('/Меню')
b2 = KeyboardButton('/Кошик')
b3 = KeyboardButton('/Доставка')
b4 = KeyboardButton('/Інфо')
b5 = KeyboardButton('/Відгуки')
key = ReplyKeyboardMarkup(resize_keyboard=True)
key.add(b1).row(b2, b3).row(b4, b5)

memory_box = MemoryStorage()
logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot, storage=memory_box)

users = []
basket = {}
basket_fullness = False
price = 0
info_for_dost = {}


@dp.message_handler(commands=['users'])
async def users_now(a):
    text = ''
    for i in users:
        text += f'{i}\n'
    if text:
        await bot.send_message(chat_id=admin_id, text=text)
    else:
        await bot.send_message(chat_id=admin_id, text="None")


@dp.message_handler(commands=['weather'])
async def weather_get(message: types.Message):
    city = message.get_args()
    if city == "":
        await message.answer("Після команди /weather, через пробіл,\nвкажіть місто, в якому бажаєте дізнатися погоду.")
    else:
        try:
            w = weather(city)
            temp = w.temperature("celsius")['temp']
            t = time(city)
            if 'mymemory' in translate(w.status).lower():
                a = f'В городе {city} сейчас {t}, {round(temp)}℃'
            else:
                a = f'В городе {city} сейчас {t}, {round(temp)}℃ и {translate(w.status)}'
            await message.answer(a)
        except:
            await message.answer('Невірно вказана назва міста')


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    if message.text == "/start":
        if message.from_user.full_name not in users:
            users.append(message.from_user.full_name)
            await bot.send_message(chat_id=admin_id,
                                   text=f"Користувач {message.from_user.full_name} приєднався.{users}")
        await bot.send_message(message.from_user.id,
                               f"Привіт, {message.from_user.first_name}, я крутий бот ресторану\n<b>'THE MIX SPIRIT OF WORLD'😉</b>",
                               reply_markup=key)
    if message.text == "/help":
        await bot.send_message(message.from_user.id,
                               "В мене є ось такі команди:\n--/start - Запуск бота ресторану!\n--/help - Допомога\n--/weather місто - Погода та час у місті")


@dp.message_handler(commands=['Меню'])
async def menu(message: types.Message):
    key_menu = InlineKeyboardMarkup(row_width=3)
    b_m1 = InlineKeyboardButton(text='Популярні', callback_data='favorite')
    b_m2 = InlineKeyboardButton(text='Перші страви', callback_data='at_first')
    b_m3 = InlineKeyboardButton(text='Wok та паста', callback_data='pasta')
    b_m4 = InlineKeyboardButton(text='Піцца', callback_data='pizza')
    b_m5 = InlineKeyboardButton(text='Суші', callback_data='sushi')
    b_m6 = InlineKeyboardButton(text='Салати', callback_data='salaty')
    b_m7 = InlineKeyboardButton(text='Десерти', callback_data='deserty')
    b_m8 = InlineKeyboardButton(text='Напої', callback_data='napoi')
    b_m_all = InlineKeyboardButton(text='Все меню', callback_data='all')
    key_menu.add(b_m1, b_m2, b_m3).add(b_m4, b_m5, b_m6).add(b_m7, b_m8).add(b_m_all)
    await bot.send_message(message.from_user.id, "Оберіть страву з категорії, або перегляньте меню повністю:",
                           reply_markup=key_menu)


@dp.callback_query_handler(text='favorite')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='at_first')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='pasta')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='pizza')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='sushi')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='salaty')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='deserty')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='napoi')
async def favorite(callback: types.CallbackQuery):
    await offer(callback)
    await callback.answer()


@dp.callback_query_handler(text='all')
async def favorite(callback: types.CallbackQuery):
    a = ['favorite', 'at_first', 'pasta', 'pizza', 'sushi', 'salaty', 'deserty', 'napoi']
    for kind in a:
        await offer(callback, kind, True)
    await callback.answer()


@dp.message_handler(commands=['dish'])
async def offer(callback, kind='', all_is=False):
    if all_is:
        callback.data = kind
    r = requests.get(f"https://themix.com.ua/{callback.data}/")
    html = BS(r.content, 'html.parser')
    block_with_dishes = html.find_all(class_="product-item", limit=4)
    for i in block_with_dishes:
        name = i.find(class_="product-item-title").text.strip()
        price_ = i.find(class_="product-item-price-current").text.strip()[:-5]
        about = i.find(class_="text-dark d-none d-sm-block")
        img = open(f'D:\\Python_projects\\Kodland\\project2\\img_menu\\{name}.jpg', 'rb')
        text = '\n'
        if about is not None:
            about = about.text.strip()
            text = f'\n\nОпис:\n<i>{about}</i>\n'
        await callback.message.answer_photo(img)
        if 'Курячий бульйон' in name:
            name = 'Курячий бульйон'
        elif 'Гарбузовий крем-суп' in name:
            name = 'Гарбузовий крем-суп'
        elif 'підсмаженим лососем' in name:
            name = 'Салат з лососем та мідіями'
        elif 'Автентичний' in name:
            name = 'Грецький салат'
        elif 'копченим вугрем' in name:
            name = 'Салат з вугрем'
        elif 'Профітролі' in name:
            name = 'Профітролі'
        elif 'Сильногазовані' in name:
            text = '\n'
            name = 'Pepsi'
        elif 'Вода' in name:
            text = '\n'
            name = 'Вода'
        await bot.send_message(callback.from_user.id, f"<b>{name}</b>{text}\n{price_} грн",
                               reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                   InlineKeyboardButton(f'Додати в кошик', callback_data=f'add_{name}_{int(price_)}'),
                                   InlineKeyboardButton(f'Видалити з кошика',
                                                        callback_data=f'del_{name}_{int(price_)}')))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('add_'))
async def add_to_bag(callback: types.CallbackQuery):
    name = f'{callback.data.split("_")[1]}'
    price_ = f'{callback.data.split("_")[2]}'
    pers = callback.from_user.full_name
    if pers not in basket:
        basket[pers] = []
    for i in basket[pers]:
        if i[0] == name:
            basket[pers][basket[pers].index(i)][1] += 1
            break
    else:
        basket[pers] += [[name, 1, price_]]
    await callback.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_'))
async def del_to_bag(callback: types.CallbackQuery):
    name = f'{callback.data.split("_")[1]}'
    pers = callback.from_user.full_name
    if pers not in basket:
        await callback.answer('Кошик порожній')
    else:
        for i in basket[pers]:
            if i[0] == name:
                if i[1] == 1:
                    basket[pers].remove(i)
                else:
                    basket[pers][basket[pers].index(i)][1] -= 1
                break
        else:
            await callback.answer('У кошику немає такої страви')
    await callback.answer()


@dp.message_handler(commands=['Кошик'])
async def bag(message: types.Message):
    global price, basket_fullness
    if message.from_user.full_name in basket:
        basket_fullness = True
        text = ""
        price = 0
        for i in basket[message.from_user.full_name]:
            price += int(i[1]) * int(i[2])
            text += f'Страва: {i[0]} | Порцій: {i[1]} | Вартість: {str(int(i[1]) * int(i[2]))}грн\n{"-" * 69}\n'
        if text == "":
            basket_fullness = False
            await bot.send_message(message.from_user.id, 'Кошик порожній')
        else:
            await bot.send_message(message.from_user.id,
                                   f'{message.from_user.full_name}:\n{text}<b>Загальна вартість: {price}грн</b>')
    else:
        basket_fullness = False
        await bot.send_message(message.from_user.id, 'Кошик порожній')


@dp.message_handler(commands=['Доставка'])
async def delivery(message: types.Message):
    b_access = KeyboardButton("/Оформити")
    b_back = KeyboardButton("/Назад")
    key_access = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    key_access.row(b_access, b_back)
    await bag(message)
    if basket_fullness:
        if price >= 300:
            price_delivery = f"Безкоштовна доставка від 300 грн 😉\nДо сплати: {price}грн"
        else:
            price_delivery = f'Доставка коштує: 30 грн\nДо сплати: {price + 30}грн'
        await bot.send_message(message.from_user.id, price_delivery, reply_markup=key_access)


class FSMDost(StatesGroup):
    place = State()
    adress = State()
    time = State()


@dp.message_handler(commands=['Оформити'], state=None)
async def arrange(message: types.Message):
    await FSMDost.place.set()
    await message.answer("Введіть назву свого міста")
    info_for_dost[message.from_user.full_name] = []


@dp.message_handler(state=FSMDost.place)
async def place(message: types.Message):
    info_for_dost[message.from_user.full_name].append(message.text)
    await FSMDost.next()
    await message.answer("Тепер вкажіть свою адресу")


@dp.message_handler(state=FSMDost.adress)
async def adress(message: types.Message):
    info_for_dost[message.from_user.full_name].append(message.text)
    await FSMDost.next()
    await message.answer(
        "Вкажіть час, на який треба доставити ваше замовлення.\nБудь-ласка, вкажіть час в форматі - <b>години:хвилини</b>")


@dp.message_handler(state=FSMDost.time)
async def time_2(message: types.Message, state: FSMContext):
    a, b = isdigit(message.text)
    if a:
        info_for_dost[message.from_user.full_name].append(message.text)
        b_yes = KeyboardButton("/Підтверджую")
        b_no = KeyboardButton("/Скасувати")
        key_access = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        key_access.row(b_yes, b_no)
        await delivery(message)
        await message.answer(
            f'Замовлення буде доставлено на {info_for_dost[message.from_user.full_name][1]} м.{info_for_dost[message.from_user.full_name][0]} в {":".join(b)}\n\nПідтверджуєте замовлення?',
            reply_markup=key_access)
        del info_for_dost[message.from_user.full_name]
        await state.finish()
    else:
        await message.answer(
            "Неправильно вказаний час.\nБудь-ласка, вкажіть час у форматі - <b>години:хвилини</b>")
        await FSMDost.last()


@dp.message_handler(commands=['Підтверджую'])
async def okay(message: types.Message):
    await message.answer("Замовлення успішно оформлено", reply_markup=key)
    del basket[message.from_user.full_name]


@dp.message_handler(commands=['Скасувати', 'Назад'])
async def back(message: types.Message):
    await message.answer("Окей", reply_markup=key)


@dp.message_handler(commands=['Інфо'])
async def info(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Ми зібрали найвідоміші страви з усього світу і запропонували нашим гостям в одному місці спробувати смаки різних кухонь.\
Тільки у нас можна водночас насолодитися хумусом -закускою із традиційної східної кухні;\
спробувати суп Том-Ям, що народився у Таїланді чи скуштувати найвідоміший американський салат Цезар;\
китайський WOK, італійську пасту чи японський смак супу Рамен…\n\n\
Посилання на сайт для повного ознайомлення:\n\t\t<a href="https://themix.com.ua/"><b>THE MIX SPIRIT OF WORLD</b></a>\n\n\
Адреса:\n\t\t<a href="https://goo.gl/maps/Gy7chnSSe5MCZEsM7">Проспект Тараса Шевченка, 25, Суми, Україна</a>\n\
Час роботи:\n\t\tКожного дня с 11:00 до 22:00\n\
Контакти для зв\'язку:\n\t\tТелефон: <a href="tel:+380953489333">+380953489333</a>')


@dp.message_handler(commands=['Відгуки'])
async def reviews(message: types.Message):
    r = requests.get("https://objor.com/7187-the-mix.html")
    html = BS(r.content, 'html.parser')
    block_with_reviews = html.find_all(class_="commennnnty", limit=6)
    block_with_reviews = block_with_reviews[4:]
    for i in block_with_reviews:
        name_and_date = i.find_all("span")
        name = name_and_date[0]
        date = name_and_date[1]
        sms = i.find(class_="commmmm")
        await bot.send_message(message.from_user.id,
                               f"<b>{name.text}</b>\n<i>{date.text[:len(date.text) - 5]}</i>\n\n{sms.text}")
    await bot.send_message(message.from_user.id,
                           "<a href='https://objor.com/7187-the-mix.html'>Переглянути всі відгуки</a>",
                           disable_web_page_preview=True)


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text=f'Бот працює')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True)
