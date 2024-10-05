import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import Registor
from button import menu, computer_button, computers, send_contact, location_button
from baza import computers_info, phone_info
from inline_button import menu_inline, phones_inf_mapping

TOKEN = "token"
ADMIN_ID = [0,0,0]

dp = Dispatcher()

# start
@dp.message(CommandStart())
async def command_start_handler(message: Message, state:FSMContext):
    full_name = message.from_user.full_name
    text = f"Salom {full_name}, Shop bot \nRo'yxatdan o'tish uchun ma'limotlarni kiriting !  \nIsmingizni kiriting"
    await message.answer(text)
    await state.set_state(Registor.ism)
# endstart

# About
@dp.message(F.text=="💁🏻‍♂️ About us")
async def about_button(message: Message):
    text = "Biz sizga istalgan turdagi telefon yoki noutbuklarni sotib olishingizda yordam beramiz !"
    pic_url = "https://i.pinimg.com/originals/40/a9/c3/40a9c329dba2278c9775798067ebae2d.jpg"
    await message.answer_photo(pic_url, caption=text)
# endabout

# contact
@dp.message(F.text=="☎️ Contact admin")
async def contact_button(message: Message):
    text = "Bot adminiga murojat qilish uchun: \nTel: +998 99 999 99 99"
    await message.answer(text)
# endcontact

@dp.message(F.text=="📍 Location")
async def location(message: Message):
    text = "Bizning savdo markazimizning lokatsiyasi!"
    lat = 40.102607
    lon = 65.37462
    await message.answer_location(lat, lon)
    await message.answer(text)

# latitude bilan longitude olish kodi 
# @dp.message(F.location)
# async def location(message: Message):
#     lat = message.location.latitude
#     lon = message.location.longitude

#     text = f"latitude:<code>{lat}</code>\n"
#     text += f"longitude:<code>{lon}</code>"

#     await message.answer(text, parse_mode="html")



@dp.message(F.text=="💻 Laptop")
async def my_computers(message:Message):
    text = "Noutbuk turini tugmalardan tanlang !"
    await message.answer(text,reply_markup=computer_button)

@dp.message(F.text.func(lambda computer: computer in computers))
async def computer_info(message:Message):
    info = computers_info.get(message.text)

    photo = info.get("rasm")
    price = info.get("narxi")
    color = info.get("rangi")
    pamyat = info.get("xotira")

    text = f"{message.text}\nnarxi: {price}$\nrangi: {color}\nxotira: {pamyat}"

    await message.answer_photo(photo=photo,caption=text)

# phones kodi
@dp.message(F.text=="📱 Phones")
async def phones(message:Message):
    text = "Telefon turini tugmalardan tanlang !"
    await message.answer(text,reply_markup=menu_inline)

@dp.callback_query(lambda callback: callback.data in phones_inf_mapping)
async def phones_info(callback: CallbackQuery):
    phone_key = phones_inf_mapping.get(callback.data)

    await callback.answer(phone_key)

    phone = phone_info.get(phone_key)
    photo = phone.get("rasm")

    if phone:
        await callback.message.answer_photo(photo, caption=f"Telefon ma'lumotlari: {phone['rangi']}\nNarxi: {phone['narxi']} $\nXotirasi: {phone['xotira']} GB")
    else:
        await callback.message.answer("Telefon ma'lumotlari topilmadi.")

# ruyxatdan utish kodi
# @dp.message(Command("reg"))
# async def register(message: Message, state:FSMContext):
#     await message.answer("Ro'yxatdan o'tish uchun ma'limotlarni kiriting !  \nIsmingizni kiriting ")
#     await state.set_state(Registor.ism)

# First_name
@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    ism = message.text 
    await state.update_data(name = ism)
    await state.set_state(Registor.familiya)
    await message.answer("Familiyani kiriting")

# Agar kiritilgan qiymat text bo'lmasa ushbu kod ishga tushadi
@dp.message(Registor.ism)
async def register_ism_del(message:Message, state:FSMContext):
    await message.answer(text= "Ismimgizni to'g'ri kiriting ❗️")
    await message.delete()

# end First_name

@dp.message(F.text, Registor.familiya)
async def register_familiya(message: Message, state:FSMContext):
    familiya = message.text  
    await state.update_data(surname = familiya)
    await state.set_state(Registor.yosh)
    await message.answer("Yoshingizni kiriting")

@dp.message(Registor.familiya)
async def register_familiya_del(message: Message, state:FSMContext):
    await message.answer(text= "Familiyngizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.yosh)
async def register_yosh(message: Message, state:FSMContext):
    yosh = message.text
    await state.update_data(age = yosh)
    await state.set_state(Registor.tel)
    await message.answer("Telefon raqamni kiriting", reply_markup=send_contact)

@dp.message(Registor.yosh)
async def register_yosh_del(message: Message, state:FSMContext):
    await message.answer(text= "Yoshingizni tug'ri kiriting ❗️")
    await message.delete()

# Phone_number  F.contact | F.text, SingUp.tel
@dp.message(F.contact | F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), Registor.tel)
async def register_tel(message: Message, state:FSMContext):

    if message.contact:
        tel = message.contact.phone_number 
    else:
        tel = message.text

    await state.update_data(tel = tel)
    await state.set_state(Registor.location)
    await message.answer("Locatsiyani kiriting", reply_markup=location_button)

@dp.message(Registor.tel)
async def register_tel_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Telefon raqamni to'g'ri kiriting ❗️")

# end Phone_number

# location

@dp.message(F.location , Registor.location)
async def register_location(message: Message, state:FSMContext):
    
    lat = message.location.latitude
    lon = message.location.longitude

    await state.update_data(lat = lat)
    await state.update_data(lon = lon)
    await state.set_state(Registor.email)
    await message.answer("Emailingizni kiriting")

# end location  

@dp.message(F.text.regexp(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"), Registor.email)
async def register_email(message: Message, state:FSMContext):
    email = message.text
    await state.update_data(email = email)
    await state.set_state(Registor.kurs)
    await message.answer("Kurs nomini kiriting")

@dp.message(Registor.email)
async def register_email_del(message: Message, state:FSMContext):
    await message.answer(text= "Emailingizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.kurs)
async def register_kurs(message: Message, state:FSMContext):
    kurs = message.text
    await state.update_data(kurs = kurs)
    await state.set_state(Registor.viloyat)
    await message.answer("Viloyat nomini kiriting")

@dp.message(Registor.kurs)
async def register_kurs_del(message: Message, state:FSMContext):
    await message.answer(text= "Kursingizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.viloyat)
async def register_viloyat(message: Message, state:FSMContext):
    viloyat = message.text
    await state.update_data(viloyat = viloyat)
    await state.set_state(Registor.tuman)
    await message.answer("Tuman nomini kiriting")

@dp.message(Registor.viloyat)
async def register_viloyat_del(message: Message, state:FSMContext):
    await message.answer(text= "Viloyatni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.tuman)
async def register_tuman(message: Message, state:FSMContext):
    tuman = message.text
    await state.update_data(tuman = tuman)
    await state.set_state(Registor.kocha)
    await message.answer("Kocha nomini kiriting")

@dp.message(Registor.tuman)
async def register_tuman_del(message: Message, state:FSMContext):
    await message.answer(text= "Tumaningizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.kocha)
async def register_kocha(message: Message, state:FSMContext):
    kocha = message.text
    await state.update_data(kocha = kocha)
    await state.set_state(Registor.maktab)
    await message.answer("Maktabingizni kiriting")

@dp.message(Registor.kocha)
async def register_kocha_del(message: Message, state:FSMContext):
    await message.answer(text= "Ko'changizni tug'ri kiriting ❗️")
    await message.delete()

@dp.message(F.text, Registor.maktab)
async def register_maktab(message: Message, state:FSMContext):
    data = await state.get_data()

    ism = data.get("name")
    familiya = data.get("surname")
    yosh = data.get("age")
    tel = data.get("tel")
    lat = data.get("lat")
    lon = data.get("lon")
    email = data.get("email")
    kurs = data.get("kurs") 
    viloyat = data.get("viloyat")
    tuman = data.get("tuman")
    kocha = data.get("kocha")
    maktab = message.text

    text = f"Ism : {ism} \nFamiliya : {familiya} \nYosh : {yosh} \nTel : {tel} \nEmail: {email} \nKurs : {kurs} \nViloyat: {viloyat} viloyati \nTuman: {tuman} tumani \nKo'cha: {kocha} ko'chasi \nMaktab: {maktab}"
    await message.answer("Siz ro'yxatdan o'tdingiz!", reply_markup=menu)

    for admin in ADMIN_ID:
        await bot.send_message(chat_id= admin, text=text)
        await bot.send_location(chat_id= admin, latitude = lat, longitude=lon)
    await state.clear()

@dp.message(Registor.maktab)
async def register_maktab_del(message: Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Maktabingizni tug'ri kiriting ❗️")

@dp.message(F.text=="Orqaga qaytish 🔙")
async def back_button(message: Message, state: FSMContext):
    text = "Menu"
    await state.clear() 
    await message.answer(text, reply_markup=menu)


@dp.startup()
async def bot_start(bot: Bot):
    for admin in ADMIN_ID:
        await bot.send_message(admin, "Tabriklaymiz 🎉 \nBotimiz ishga tushdi ")

@dp.shutdown()
async def bot_stop(bot: Bot):
    for admin in ADMIN_ID:
        await bot.send_message(admin, "Bot to'xtadi ❗️")
    
async def main():
    global bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
