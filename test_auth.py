from fastapi.testclient import TestClient

from apps.auth.repository_token import create_access_token, decode_token
from apps.database.repository_db import create_user_in_db
from main import app  # Ваш основной файл приложения

client = TestClient(app)

# Создаем тестовые данные
TEST_USER = {"email": "user@example.com", "password": "string"}
# ADMIN_USER = {"email": "admin@example.com", "role": "admin"}

VALID_TOKEN = create_access_token(TEST_USER)  # Токен для обычного пользователя
# ADMIN_TOKEN = create_access_token(ADMIN_USER)  # Токен для админа
INVALID_TOKEN = "dsdfdfg45645hgyh"


# 1. Тестирование аутентификации (доступно авторизованным пользователям)
def test_authorized_endpoint_success():
    user = create_user_in_db({"email": "user@example.com",
                              "password": "string"})
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    response = client.get("/api/v1/users/profile_via_middleware",
                          headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


# 2. Тестирование регистрации (доступно всем)
def test_public_endpoint_register():
    response = client.post("/api/v1/auth/register",
                           json={"email": "user2@example.com",
                                 "password": "string123"})
    assert response.status_code == 201


# 3. Тестирование публичных путей (должны работать без токена)
def test_public_endpoint_docs():
    print('test_public_endpoint_docs')
    response = client.get("/docs")

    assert response.status_code == 200


# 4. Тестирование публичных путей (должны работать без токена)
def test_root():
    print('test_root')
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Hello FastAPI World"


# # 2. Тестирование аутентификации (доступно всем авторизованным)
# def test_authorized_endpoint_success():
#     headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
#     response = client.get("/users/me", headers=headers)
#
#     # Middleware должен пропустить запрос, и роут должен вернуть 200
#     assert response.status_code == 200
#     assert response.json()["message"] == "Hello, testuser!"
#

# def test_unauthorized_access():
#     # Отсутствие токена
#     response = client.get("/users/me")
#     assert response.status_code == 401
#     assert "Authorization header missing" in response.json()["detail"]
#
#
# def test_invalid_token():
#     headers = {"Authorization": f"Bearer {INVALID_TOKEN}"}
#     response = client.get("/users/me", headers=headers)
#
#     # Middleware должен поймать ошибку декодирования и вернуть 401
#     assert response.status_code == 401
#     assert "Invalid or expired token" in response.json()["detail"]
#
#
# # 3. Тестирование Авторизации (Роли)
# def test_role_authorization_success_admin():
#     headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
#     response = client.get("/admin/panel", headers=headers)
#
#     # Роль 'admin' разрешена для панели
#     assert response.status_code == 200
#     assert "Secret" in response.json()["secret"]
#
#
# def test_role_authorization_failure_user():
#     headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
#     response = client.get("/admin/panel", headers=headers)
#
#     # Роль 'user' не разрешена для панели
#     assert response.status_code == 403
#     assert "Not enough permissions" in response.json()["detail"]