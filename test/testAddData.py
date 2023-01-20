import requests


reqJson = {
    'name': 'Саша',
    'surname': 'Александров',
    'patronymic_': '',
    'phone_number': '79458526532',
    'email_': 'Aleks@mail.ru',
    'country': 'Россия',
}
reqJson2 = {
    'name': 'Саша',
    'surname': 'Александров',
    'patronymic_': 'Алексеев',
    'phone_number': '79458526532',
    'email_': 'Aleks@mail.ru',
    'country': 'Россия',
}

head = {'Content-type': 'application/json', 'Accept': 'text/plain'}
res = requests.post('http://127.0.0.1:8000/save_user_data', json=reqJson2, headers=head)
print(res)