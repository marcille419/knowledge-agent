from app.utils.jwt import (
    create_access_token,
    verify_token
)

token = create_access_token(
    {
        "user_id": 2,
        "username": "admin"
    }
)

print("TOKEN:")
print(token)

print()

payload = verify_token(token)

print("PAYLOAD:")
print(payload)