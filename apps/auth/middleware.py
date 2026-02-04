# from fastapi import Request, status
# from fastapi.responses import JSONResponse
# from starlette.middleware.base import BaseHTTPMiddleware
#
#
# from apps.auth.repository_token import decode_token  # Импортируем функцию декодирования
#
#
# # --------------------------------------------------------------------
# # 1. Middleware для Аутентификации
# # --------------------------------------------------------------------
# class AuthMiddleware(BaseHTTPMiddleware):
#
#     async def dispatch(self, request: Request, call_next):
#
#         # 1. Определяем, нужно ли пропускать этот запрос (например, для Swagger UI или /auth/login)
#         path = request.url.path
#
#         # Пропускаем все, что начинается с /auth/ (регистрация, логин, refresh)
#         if path.startswith("/api/v1/auth/"):
#             return await call_next(request)
#
#         # Пропускаем документацию
#         if path.startswith("/docs") or path.startswith("/openapi.json"):
#             return await call_next(request)
#
#         # 2. Извлекаем токен из заголовка Authorization (Bearer Token)
#         auth_header = request.headers.get("Authorization")
#
#         if not auth_header:
#             # Если токена нет, и это не исключенный маршрут, возвращаем 401
#             return JSONResponse(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 content={"detail": "Authentication token missing"},
#             )
#
#         try:
#             # Предполагаем, что заголовок в формате "Bearer <token>"
#             scheme, token = auth_header.split()
#             if scheme.lower() != "bearer":
#                 raise ValueError("Invalid token scheme")
#
#         except ValueError:
#             return JSONResponse(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 content={"detail": "Invalid authorization header format"},
#             )
#
#         # 3. Валидация токена
#         try:
#             # Используем функцию декодирования из Auth Service
#             payload = decode_token(token)
#
#             user_id = payload.get("user_id")
#             email = payload.get("email")
#
#             if not user_id or not email:
#                 raise ValueError("Payload incomplete")
#
#             # 4. Если токен валиден: Добавляем данные пользователя в HTTP-запрос
#             # Это ключевой шаг: роуты смогут прочитать данные через request.state
#             request.state.user_id = user_id
#             request.state.email = email
#
#         except Exception:
#             # Любая ошибка JWT (Expired, Invalid Signature)
#             return JSONResponse(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 content={"detail": "Invalid or expired authentication token"},
#             )
#
#         # 5. Передаем управление дальше, если аутентификация прошла успешно
#         response = await call_next(request)
#         return response
