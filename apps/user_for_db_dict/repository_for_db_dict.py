# from typing import Dict, Any, Optional, List
#
# from typing import Optional
#
# from DATABASES.db_dict.database_store_dct import ContextManagerDB, \
#     IdCounterUser
#
#
# def get_user_by_email_from_db(email: str) -> Optional[dict]:
#     with ContextManagerDB() as db:
#         print("Проверка email в базе данных!")
#         db_dct = db.get_store()
#         for user in db_dct.values():
#             if user['email'] == email:
#                 print(f'Пользователь с email: {email} найден!')
#                 return user
#         print("Пользователь с таким email не найден!")
#         return None
#
#
# def create_user_in_db(user_data: dict) -> dict:
#     with ContextManagerDB() as db:
#         new_id = IdCounterUser._get_next_id()
#
#         db_dct = db.get_store()
#         user_data['id'] = new_id
#         db_dct[new_id] = user_data
#
#         print(f'В БД создан пользователь:\n'
#               f' {new_id}\n'
#               f' {user_data['email']}\n'
#               f' {user_data['password']}')
#
#         return db_dct.get(new_id)
#
#
# def get_user_by_id_from_db(user_id: int) -> Optional[dict]:
#     with ContextManagerDB() as db:
#         db_dct = db.get_store()
#         return db_dct.get(user_id, None)
#
#
# def get_users_by_ids_from_db(user_ids: List[int]) -> List[dict]:
#     with ContextManagerDB() as db:
#         db_dct = db.get_store()
#         return [db_dct[id_value] for id_value in user_ids if id_value in db_dct]
#
#
# def get_all_users_from_db() -> List[dict]:
#     with ContextManagerDB() as db:
#         db_dct = db.get_store()
#         return list(db_dct.values())
#
#
# def update_user_in_db(user_id: int,
#                       update_data: dict) -> Optional[dict]:
#     with ContextManagerDB() as db:
#         db_dct = db.get_store()
#         if user_id not in db_dct:
#             return None
#
#         # Обновление данных
#         db_dct[user_id].update(update_data)
#         return db_dct[user_id]
#
#
# def delete_user_from_db(user_id: int) -> Optional[dict]:
#     with ContextManagerDB() as db:
#         db_dct = db.get_store()
#         if user_id not in db_dct:
#             return None
#
#         deleted_user = db_dct.pop(user_id)
#         return deleted_user
