import json
import sys
import traceback
import requests

from functions import divar_get_phone


def all_posts(city, category='real-estate', divar_scrapping_pages=10):
    """
    :param category: real-estate, sofa-armchair, ...
    :param city: (string) e.g: "mashhad", "tehran"
    :param divar_scrapping_pages: (int) desc: number of scrapping pages
    :return:
    """
    try:
        first_page_url = "https://api.divar.ir/v8/web-search/" + city + "/" + category
        first_page_headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://divar.ir',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap'
                          ' Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://divar.ir/s/mashhad/real-estate',
            'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
            'Cookie': 'city=mashhad; did=f9b50faa-10e0-4a7a-893d-77807bce90f9;'
                      ' _ga=GA1.2.980301528.1583753802; _gcl_au=1.1.7257668.1583753804;'
                      ' _hjid=30d8e6b1-b454-44ce-908d-7303accb2bab; _gid=GA1.2.1287562973.1585029720;'
                      ' _gat_UA-158054152-1=1; _gat=1'

        }
        first_page_response = requests.request("GET", first_page_url, headers=first_page_headers)
        res = json.loads(first_page_response.text.encode('utf-8').decode())

        page_num = 1
        all_tokens = []
        while page_num <= divar_scrapping_pages:
            widget_list = res["widget_list"]
            all_tokens += [widget['data']['token'] for widget in widget_list]
            next_posts_page = res["last_post_date"]  # this one scraps older posts
            page_num += 1
            ''' GET NEXT PAGE'''
            url_base = "https://api.divar.ir/v8/search/3/real-estate"
            headers1 = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'Sec-Fetch-Dest': 'empty',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/80.0.3987.132 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Origin': 'https://divar.ir',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Referer': 'https://divar.ir/s/mashhad/real-estate',
                'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
                'Cookie': 'did=d3073d32-44e9-4a74-8c3c-19ca880df7c4; _ga=GA1.2.1635770579.1583808017; '
                          '_gid=GA1.2.1066926278.1583808017; city=mashhad; _gcl_au=1.1.391336390.1583808018; '
                          '_hjid=d0dfa631-dde5-4df1-a2ad-72aca380797a; _gat_UA-32884252-2=1'
            }
            payload = "{\"json_schema\":{\"category\":{\"value\":\"real-estate\"}},\"last-post-date\":" + str(
                next_posts_page) + "}"
            response = requests.request("POST", url_base, headers=headers1, data=payload)
            if response.status_code != 200:
                return 0
            res = json.loads(response.text.encode('utf-8').decode())

            ''' END GET NEXT PAGE'''
            if next_posts_page == -1:
                return 0

        return all_tokens
    except BaseException as _:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        print("\n Exception type : %s " % ex_type.__name__)
        print("\n Exception message : %s" % ex_value)
        print("\n Stack trace : %s" % stack_trace)
        return 0


def single_post_detail(token, authorization_code='NOT ASSIGNED'):
    """
    :param authorization_code:
    :param token:
    """
    additional_data = dict()
    url = "https://api.divar.ir/v5/posts/" + token
    payload = {}
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Dest': 'empty',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 Safari/537.36',
        'Origin': 'https://divar.ir',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://divar.ir/v/%D8%A7%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86%DB%B1%DB%B1%DB%'
                   'B5%D9%85%D8%AA%D8%B1%DB%8C-%D9%81%D9%88%D9%84-%D9%86%D8%A8%D9%88%D8%AA-%DB%B1%DB%B8_'
                   '%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86_%D9%85%D8%B4%D9%87%D8%AF_%D8%B7%D9%8'
                   '4%D8%A7%D8%A8_%D8%AF%DB%8C%D9%88%D8%A7%D8%B1/gXmdNoUs',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    detail = json.loads(response.text.encode('utf-8').decode())
    additional_data['categories'] = detail["widgets"]["breadcrumb"]["categories"]
    post_url = detail["data"]["share"]["web_url"]
    description = detail["data"]["share"]["description"]
    features = detail["widgets"]["list_data"]
    title = detail["widgets"]["header"]['title']
    # getting phone number through mobile authentication sessions
    phone_data = divar_get_phone(token, authorization_code)
    phone = phone_data['mobile']
    if phone_data['code'] != 200:
        # if the authentication code is invalid, get the partial number with "X" in the end
        phone = detail["widgets"]["contact"]['phone']
    if len(detail["widgets"]["images"]) > 0:
        image = detail["widgets"]["images"][0]
    else:
        image = ""
    address = detail["widgets"]["header"]["place"]
    url = post_url
    description = description
    for feature in features:
        feature_key = feature["title"]
        if feature["format"] == "string" and feature_key != "دسته‌بندی":
            feature_value = feature["value"]
            additional_data[feature_key] = feature_value
        if feature['format'] in ["group_info_row", "group_feature_row"]:
            for feature_group_items in feature['items']:
                if 'value' not in feature_group_items.keys():
                    additional_data[feature_group_items['title']] = True
                else:
                    additional_data[feature_group_items['title']] = feature_group_items['value']

        if "next_page" in feature.keys():
            if "widget_list" in feature['next_page'].keys():
                for feature_widget in feature['next_page']['widget_list']:
                    if feature_widget['widget_type'] == "FEATURE_ROW":
                        additional_data[feature_key] = feature_widget['data']['title']
                        continue
    return {
        'address': address,
        'title': title,
        'description': description,
        'token': token,
        'image': image,
        'phone': phone,
        'url': url,
        'additional_data': additional_data,
    }


if __name__ == '__main__':
    pass