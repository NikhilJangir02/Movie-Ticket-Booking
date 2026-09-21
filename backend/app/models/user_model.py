from datetime import datetime

def user_document(data):
    return {
        "name": data.name,
        "email": data.email,
        "password": data.password,
        "role": "user",
        "created_at": datetime.utcnow()

    }