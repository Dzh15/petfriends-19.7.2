from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0

def test_add_new_pet_with_valid_data(name='Пёсик мешочек', animal_type='volchOK',
                                         age='2', pet_photo='images/UKzYEu96yKs.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/sova.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#10testov
#1
def test_add_new_pet_with_big_age(name='Пёсик мешочек', animal_type='volchOK',
                                         age='1234567890123456789012345678901234567890', pet_photo='images/UKzYEu96yKs.jpg'):
    """Проверяем, что можно добавить питомца cо слишком большим значением в поле Age"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#2
def test_add_new_pet_without_name(name='', animal_type='volchOK',
                                     age='11', pet_photo='images/UKzYEu96yKs.jpg'):
    """Проверяем, что можно добавить питомца c пустым полем Name"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

#3
def test_get_api_key_for_not_valid_email(email='1010', password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403"""
    status, _ = pf.get_api_key(email, password)
    assert status == 403

#4
def test_delete_pets_invalid_pet_id():
    """Проверяем возможность удаления питомца с невалидным pet_id"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/sova.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = "ggg"
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

#5
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=-505):
    """Проверяем возможность обновления информации о питомце, ввод отрицательного возраста"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#6
def test_get_api_key_for_not_valid_password(email=valid_email, password='234'):
    """ Проверяем, что запрос api ключа возвращает статус 403"""
    status, _ = pf.get_api_key(email, password)
    assert status == 403

#7
def test_get_list_of_pets_with_filter(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#8
def test_add_new_pet_witout_age(name='Пёсик мешочек', animal_type='volchOK',
                                         age='', pet_photo='images/UKzYEu96yKs.jpg'):
    """Проверяем, что можно добавить питомца c пустым значением в поле Age"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#9
def test_delete_pet_with_last_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key,pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()

#10
def test_add_new_pet_without_animal_type(name='', animal_type='',
                                     age='11', pet_photo='images/UKzYEu96yKs.jpg'):
    """Проверяем, что можно добавить питомца c пустым полем animal_type"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200