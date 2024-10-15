import json
import requests
import os
import datetime
import glob
import sys

def check_api(user_input):
    retention  = 1
    current_time = datetime.datetime.now()
    retention_time = current_time - datetime.timedelta(days=retention)
    dir_json = './cache'
    search_in_dir = os.path.join(dir_json, '*.json')
    in_dir = glob.glob(search_in_dir)
    print(in_dir)
    len_dir = len(in_dir)
    if len_dir > 9:
        print("more than 10")
        for i in in_dir:
            os.remove(i)
    else:
        pass
    for i in in_dir:
        if user_input in i :
            t_mod = os.path.getmtime(i)
            t_mod = datetime.datetime.fromtimestamp(t_mod)
            if retention_time > t_mod:
                os.remove(i)
                return False
            else:
                with open(i,'r') as file:
                    json_data = json.load(file)
                    return json_data
        # create_json_file(user_input)


def get_api(user_input):
    api_key = "WMM4FWAB6K3B3ZFSJRUL3DQ3G"
    res = requests.request("GET",
                           url=f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{user_input}/?unitGroup=metric&include=days%2Chours&key={api_key}&contentType=json")
    data_json = res.json()
    return data_json


def filter_api(data_json):
    data_days = data_json['days']
    days_dict = {}
    for i in range(7):
        days_dict[i] = {"datetime": data_days[i]['datetime'], "temp": data_days[i]['temp'],"description": data_days[i]['description'],
                        "humidity": data_days[i]['humidity'],
                        "morning_temp": data_days[i]['hours'][8]['temp'],
                        "night_temp": data_days[i]['hours'][20]['temp']}
    dict_all = {"address": data_json["address"],
                "resolved": data_json["resolvedAddress"],
                "days": days_dict
                }
    return dict_all


def create_json_file(json_f,user_input):
        with open(f"./cache/{user_input}.json", 'w') as file:
            json.dump(json_f,file)
        return json_f

def read_json_file(user_input):
    with open(f'./cache/{user_input}.json', 'r') as file:
        json_data = json.load(file)
        return json_data

