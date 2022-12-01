import secrets
import string
#================== ТЕСТОВЫЕ ДАННЫЕ ===================

valid_email = 'test@testeristers.ru'
valid_password = '123456'
valid_user = valid_email, valid_password

not_valid_email = '0887815276@345.ru'
not_valid_password = 'aksldfn'

not_valid_user = not_valid_email, not_valid_password

not_valid_key = {
  "key": "ea738148a1f19838e1c5d14144444444444444444444444444444444"
}

data_list_response = ["age", "animal_type", "created_at", "id", "name", "pet_photo", "user_id"]


def generate_alphanum_crypt_string(length) -> str:
    """Функция генерирует строку из цифр и букв length=длина текста"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(secrets.choice(letters_and_digits) for i in range(length))

