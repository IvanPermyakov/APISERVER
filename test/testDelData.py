import requests

Number={
    'phone_number': '85263214565'
}
Number2={
    'phone_number': '79458526532'
}

head = {'Content-type': 'application/json', 'Accept': 'text/plain'}
res = requests.post('http://127.0.0.1:8000/delete_user_data', json=Number, headers=head)
print(res.text)