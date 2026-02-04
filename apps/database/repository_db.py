from typing import Optional

from apps.database.database_store_dct import ContextManagerDB, IdCounterUser


def get_user_by_email_from_db(email: str) -> Optional[dict]:
    with ContextManagerDB() as db:
        print("Проверка email в базе данных!")
        db_dct = db.get_store()
        for user in db_dct.values():
            if user['email'] == email:
                print(f'Пользователь с email: {email} найден!')
                return user
        print("Пользователь с таким email не найден!")
        return None


def create_user_in_db(user_data: dict) -> dict:
    with ContextManagerDB() as db:
        new_id = IdCounterUser._get_next_id()

        db_dct = db.get_store()
        user_data['id'] = new_id
        db_dct[new_id] = user_data

        print(f'В БД создан пользователь:\n'
              f' {new_id}\n'
              f' {user_data['username']}\n'
              f' {user_data['email']}\n'
              f' {user_data['password']}')

        return db_dct.get(new_id)
