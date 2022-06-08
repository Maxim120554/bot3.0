from aiogram.utils import executor
import database
import handlers
from create_bot import dp



async def on_startup(_):
    print('Бот онлайн')
    database.start_sql()


def main():
    handlers.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
