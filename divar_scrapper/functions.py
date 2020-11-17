import json

import requests


def divar_get_phone(token, authorization_code=''):
    url = "https://api.divar.ir/v5/posts/" + str(token) + "/contact/"
    payload = {}
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'snap Chromium/81.0.4044.129 Chrome/81.0.4044.129 Safari/537.36',
        'Origin': 'https://divar.ir',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'authorization': 'Basic ' + authorization_code
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        result = json.loads(response.text.encode('utf8').decode())
        if 'widgets' in result.keys():
            phone_number = {"code": response.status_code, "mobile": result['widgets']['contact']['phone']}
        else:
            phone_number = {"code": response.status_code, "mobile": None}
    except:
        phone_number = {"code": 500, "mobile": None}
    return phone_number
