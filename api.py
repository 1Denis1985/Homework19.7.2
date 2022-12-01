import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def result_json(self, respose) -> json:
        """Возвращает статус и результат тела запроса в json или text"""
        status = respose.status_code
        try:
            result = respose.json()
        except json.decoder.JSONDecodeError:
            result = respose.text
        return status, result

    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""
        headers = {
            'email': email,
            'password': passwd,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        return self.result_json(res)

    def get_list_of_pets(self, auth_key, filter='') -> json:
        """ Get запрос на получение списка питомцев, включает в себя необязательный параметр
        filter="", filter="my_pets" - возвращает список моих питомцев..."""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        return self.result_json(res)

    def post_create_pet_simple(self, auth_key, name: str, animal_type: str, age: int) -> json:
        """Post запрос создающий питомца на сайте, без фото"""
        headers = {'auth_key': auth_key['key']}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        return self.result_json(res)

    def post_add_pets(self,auth_key, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Post запрос позволяющий добавить информацию о новом питомце"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        return self.result_json(res)

    def post_update_or_add_photo_pets(self, auth_key, pet_id, pet_photo) -> json:
        """POST запрос обновляет или добавляет фото"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type
                   }

        res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)
        return self.result_json(res)

    def delete_pets(self, auth_key, pet_id) -> json:
        """Delete запрос удаляет питомца по его id"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + f'/api/pets/{pet_id}', headers=headers)
        return self.result_json(res)

    def delete_all_my_pets(self, auth_key) -> json:
        """Delete запрос удаляет всех питомцев"""
        _, result = self.get_list_of_pets(auth_key, filter='my_pets')
        headers = {'auth_key': auth_key['key']}

        while len(result['pets']) > 0:
            pet_id = result['pets'][len(result['pets'])-1]['id']
            res = requests.delete(self.base_url + f'/api/pets/{pet_id}', headers=headers)
            result['pets'].pop(len(result['pets'])-1)
        return self.result_json(res)

    def put_update_info_pets(self,
                             auth_key,
                             pet_id,
                             name: None, animal_type: None, age: None) -> json:
        """PUT запрос, обновляет данные питомца по его id"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + f'/api/pets/{pet_id}', headers=headers, data=data)
        return self.result_json(res)

