from fastapi import Request, status, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from apps.auth.repository_token import decode_token

PROTECTED_PATHS = ('/api/v1/profile_via_middleware',)
# if path.startswith("/docs") or path.startswith("/openapi.json"):


def get_token_from_header(request: Request) -> str | None:
    """Извлекает JWT-токен из заголовка Authorization."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        # Формат: "Bearer <token>"
        return auth_header.split(" ")[1]
    return None


async def jwt_authentication_middleware(request: Request, call_next):
    """ Функция Middleware."""
    # 1. Определяем, нужно ли применять аутентификацию
    # Мы пропускаем  всех кроме "/api/v1/profile_via_middleware"
    path = request.scope.get("path")

    if not path.startswith(PROTECTED_PATHS):
        # Передаем запрос дальше без изменений.
        response = await call_next(request)
        return response

    # 2. Для всех остальных путей пытаемся аутентифицировать
    token = get_token_from_header(request)

    if not token:
        print('Токена нет в заголовке!')
        # Токен отсутствует, но это не публичный маршрут.
        # Если это НЕ публичный маршрут, требуем аутентификации.
        return JSONResponse(
            content={
                "detail": "Необходим действительный токен аутентификации"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # 3. Декодируем токен
    payload = decode_token(token)
    print('payload или decode_token(token)', payload)

    if not payload:
        print('Токен недействителен!')
        # Токен недействителен
        return JSONResponse(
            content={"detail": "Неверный или истекший токен"},
            status_code=status.HTTP_403_FORBIDDEN,
            # 403 часто лучше для невалидного токена
        )

    # 4. Успешная аутентификация

    # Добавляем данные пользователя в состояние запроса
    # Здесь вы можете добавить user_id, roles и т.д., из payload
    email = payload.get("email", None)
    if not email:
        return JSONResponse(
            status_code=403,
            content={"detail": "Invalid token payload"}
        )
    request.state.email = payload.get('email', None)
    print("request.state.__dict__:", request.state.__dict__)

    # Передаем запрос дальше
    response = await call_next(request)
    return response


# --------------------------------------------------------------------
# 1. Middleware для Аутентификации # Middleware через класс
# --------------------------------------------------------------------
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
