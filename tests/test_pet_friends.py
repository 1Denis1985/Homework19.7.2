import os
from api import PetFriends
from settings import *


class TestPet:
    def setup(self):
        self.pf = PetFriends()

    def test_get_api_key_for_valid_user(self):
        status, result = self.pf.get_api_key(*valid_user)
        assert status == 200
        assert 'key' in result

    def test_get_api_key_for_not_valid_user(self):
        status, result = self.pf.get_api_key(*not_valid_user)
        assert status == 403
        assert 'This user wasn&#x27;t found in database' in result

    def test_get_all_pets_with_valid_key(self):
        _, auth_key = self.pf.get_api_key(*valid_user)
        status, result = self.pf.get_list_of_pets(auth_key)
        assert status == 200
        assert len(result['pets']) > 0

    def test_get_all_pets_with_not_valid_key(self):
        status, result = self.pf.get_list_of_pets(not_valid_key)
        assert status == 403

    def test_get_pets_with_filters_and_valid_key(self, filter='my_pets'):
        _, auth_key = self.pf.get_api_key(*valid_user)
        self.pf.post_create_pet_simple(auth_key, name='Фильтр', animal_type='Тест', age=1)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_create_pet_simple_valid(self):
        _, auth_key = self.pf.get_api_key(*valid_user)
        status, result = self.pf.post_create_pet_simple(auth_key,
                                                        name='простая собака', animal_type='без имейджа', age=0)
        assert status == 200
        for item in data_list_response:
            assert item in result

    def test_create_p_simple_not_valid_field(self):
        """Тест падает потому что не ограничено количество символов в полях инициализации карточки питомца"""
        _, auth_key = self.pf.get_api_key(*valid_user)
        status, result = self.pf.post_create_pet_simple(auth_key,
                                                        name=generate_alphanum_crypt_string(10000),
                                                        animal_type='Негативный тест',
                                                        age=generate_alphanum_crypt_string(10000))
        assert status == 400

    def test_create_p_simple_empty_field(self):
        """Тест падает потому что можно добавить питомца с пустыми полями"""
        _, auth_key = self.pf.get_api_key(*valid_user)
        status, _ = self.pf.post_create_pet_simple(auth_key,
                                                    name='', animal_type='', age='')
        assert status == 400

    def test_add_pets_valid(self,
                            name='тестовая кошка',
                            animal_type='с тестовой породой',
                            age='0',
                            pet_photo='images/first.jpeg'):

        _, auth_key = self.pf.get_api_key(*valid_user)
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.pf.post_add_pets(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        for item in data_list_response:
            assert item in result

    def test_add_pets_not_valid_extension_photo(self,
                                                name='Текст',
                                                animal_type='негативный тест',
                                                age='0',
                                                pet_photo='images/test.txt'):
        """Тест падает потому что можно загрузить на сервер текстовый файл вместо фото"""

        _, auth_key = self.pf.get_api_key(*valid_user)
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.pf.post_add_pets(auth_key, name, animal_type, age, pet_photo)
        assert status == 400

    def test_update_photo(self, pet_photo='images/original.jpg'):
        _, auth_key = self.pf.get_api_key(*valid_user)
        self.pf.post_create_pet_simple(auth_key, name='Фоткин', animal_type='Апдейтин', age=0)
        _, result = self.pf.get_list_of_pets(auth_key, filter='my_pets')
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        pet_id = result['pets'][0]['id']
        status, result = self.pf.post_update_or_add_photo_pets(auth_key, pet_id, pet_photo)
        assert status == 200

    def test_delete_pets(self):
        _, auth_key = self.pf.get_api_key(*valid_user)
        self.pf.post_create_pet_simple(auth_key, name='Коте', animal_type='Удалятор', age= 3000)
        self.pf.post_create_pet_simple(auth_key, name='СуперКотэ', animal_type='неУдалятор', age=6000)
        _, result = self.pf.get_list_of_pets(auth_key, filter='my_pets')
        pet_id = result['pets'][0]['id']
        pet_name = result['pets'][0]['name']
        status, result = self.pf.delete_pets(auth_key, pet_id)
        assert status == 200
        _, result = self.pf.get_list_of_pets(auth_key, filter='my_pets')
        assert pet_name != result['pets'][0]['name']

    def test_delete_pets_with_not_valid_key(self):
        _, auth_key = self.pf.get_api_key(*valid_user)
        _, result = self.pf.get_list_of_pets(auth_key, filter='my_pets')
        pet_id = result['pets'][0]['id']
        status, result = self.pf.delete_pets(not_valid_key, pet_id)
        assert status == 403

    def test_put_update_info_pets(self, name='ВасилийАпгрейд', animal_type='КиберВася', age='3'):
        _, auth_key = self.pf.get_api_key(*valid_user)
        self.pf.post_create_pet_simple(auth_key, name='Котун', animal_type='Заменятор', age=9)
        _, pet_dict = self.pf.get_list_of_pets(auth_key, filter='my_pets')
        pet_id = pet_dict['pets'][0]['id']
        status, result = self.pf.put_update_info_pets(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        for item in data_list_response:
            assert item in result
        assert result['name'] == 'ВасилийАпгрейд'
        assert result['name'] != 'Котун'

    def test_delete_all_my_pets(self):
        _, auth_key = self.pf.get_api_key(*valid_user)
        status, _ = self.pf.delete_all_my_pets(auth_key)
        assert status == 200
        _, result = self.pf.get_list_of_pets(auth_key, filter='my_pets')
        assert result['pets'] == []


