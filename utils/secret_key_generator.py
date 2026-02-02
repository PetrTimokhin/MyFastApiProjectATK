import secrets
import base64

# 1. Генерируем 32 случайных байта. (32 байта = 256 бит, что является стандартом для сильных ключей)
raw_bytes = secrets.token_bytes(32)

# 2. Кодируем эти байты в строку, которую удобно использовать в конфиге (Base64 URL-safe)
secret_key_base64 = base64.urlsafe_b64encode(raw_bytes).decode()

print(f"Сгенерированный SECRET_KEY:\n{secret_key_base64}")
