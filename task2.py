import asyncio
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = "7067961074:AAERLRGNJg_41ZeZfw-TRHmz_ZjdA2IF7co"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

NOTES_FILE = 'notes.json'

# Завантажити/зберегти нотатки
def load_notes():
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

# Стани FSM
class AddNote(StatesGroup):
    waiting_for_note = State()

class SearchNote(StatesGroup):
    waiting_for_keyword = State()

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привіт! Я бот для роботи з нотатками. Спробуй команди: /add, /list, /search")

# Додати нотатку
@dp.message(Command("add"))
async def add_cmd(message: Message, state: FSMContext):
    await message.answer("Введи текст нотатки:")
    await state.set_state(AddNote.waiting_for_note)

@dp.message(AddNote.waiting_for_note)
async def save_note(message: Message, state: FSMContext):
    notes = load_notes()
    notes.append(message.text)
    save_notes(notes)
    await message.answer("✅ Нотатку збережено.")
    await state.clear()

# Показати всі нотатки
@dp.message(Command("list"))
async def list_cmd(message: Message):
    notes = load_notes()
    if not notes:
        await message.answer("Немає нотаток.")
    else:
        result = "\n\n".join(f"{i+1}. {note}" for i, note in enumerate(notes))
        await message.answer(f"📝 Список нотаток:\n\n{result}")

# Пошук нотаток
@dp.message(Command("search"))
async def search_cmd(message: Message, state: FSMContext):
    await message.answer("Введи ключове слово для пошуку:")
    await state.set_state(SearchNote.waiting_for_keyword)

@dp.message(SearchNote.waiting_for_keyword)
async def search_note(message: Message, state: FSMContext):
    keyword = message.text.lower()
    notes = load_notes()
    found = [note for note in notes if keyword in note.lower()]
    if found:
        result = "\n\n".join(found)
        await message.answer(f"🔍 Знайдено:\n\n{result}")
    else:
        await message.answer("😕 Нічого не знайдено.")
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
