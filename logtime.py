import requests
from bs4 import BeautifulSoup
import json
import datetime
import getpass
import sys

username = input("Please enter your username: ") # Ask'a the User for username input
password = getpass.getpass(prompt="Please enter your password: ") # Ask's the User for their password

url = "https://signin.intra.42.fr/users/sign_in"

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

login_data = {
    'utf8': '✓',
    'user[login]': username,
    'user[password]': password,
    'commit': 'Sign in'
}

def print_hours(s):
    h = s // 3600
    m = (s % 3600) // 60
    second = ((s % 3600) % 60)
    time = "{0}:{1}:{2}".format(h, m, second)
    print(time)

# Error handling

def error_handling(status_code):
    if status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        sys.exit()

with requests.Session() as session:
    response = session.get(url)
    error_handling(response.status_code) # Check for HTTP codes other than 200
    soup = BeautifulSoup(response.content, "html5lib")
    login_data["authenticity_token"] = soup.find("meta", attrs = {"name": "csrf-token"})["content"]
    response = session.post(url, data = login_data, headers = headers)
    error_handling(response.status_code) # Check for HTTP codes other than 200
    soup = BeautifulSoup(response.content, "html5lib")
    try:
        soup.find("span", attrs = {"class": "login"})["data-login"] != username
    except:
        print("Username or password does not match")
        sys.exit()

    while True:
        login_name = input("Enter an username to see Logtime of them OR Press Enter to Quit: ")
        # Exiting program
        if not login_name:
            print("BYe")
            sys.exit()
        response = session.get("https://profile.intra.42.fr/users/"+login_name+"/locations_stats")
        # Check if user exists
        if response.status_code != 200:
            print("The username you entered does not exist")
            continue
        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        d = datetime.datetime.strptime("2019-10-01", "%Y-%m-%d")
        h = 0;
        for key in data:
            if datetime.datetime.strptime(key, "%Y-%m-%d") >= d:
                h += ((int(data[key].split(":")[0]) * 3600) + (int(data[key].split(":")[1]) * 60) + (int(data[key].split(":")[2].split(".")[0])))
        print_hours(h)
