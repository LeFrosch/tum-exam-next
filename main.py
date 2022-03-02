#!/usr/bin/env python

# Author: Daniel Brauner
# Contributer: Luca Otting

from genericpath import isfile
import requests
import webbrowser
import random
import os

def getToken(isValid):
    if(not isValid):
        os.remove(".TOKEN")
    
    with open(".TOKEN", 'a+') as file:
        file.seek(0, 0)
        token = file.read().strip()
        if(not token):
            token = input("Access token: ")
            file.write(token)

        return token


def main():
    print("EIDI NEXT TOOL :)")

    problem = int(input("Problem number: "), 10)
    correction_pass = int(input("Correction pass: "), 10)

    # Token from the TUMExam cookie
    token = getToken(True)

    cookies = dict(token=token)

    url = "https://2021ws-in-eidi.hq.tumexam.de/api/exam/1/correction/?"
    url += "filter[problem]=%d" % problem
    url += "&filter[correction_pass]=%d" % correction_pass 
    url += "&filter[corrected]=False"
    url += "&filter%5Bavailable%5D=true"
    url += "&filter[locked]=False"
    url += "&page=1"

    while(True):
        response = requests.get(url, cookies=cookies)
        if(response.text.startswith("<")):
            print("Your access token is invalid. Did it expire?")
            cookies = dict(token=getToken(False))
            continue            

        maxPages = response.json()["max_page"]

        if (maxPages <= 0):
            print("No free exam found")

        else:
            newUrl = "%s%d" % (url[:len(url) - 1], random.randint(1, maxPages))

            response = requests.get(newUrl, cookies=cookies)
            results = response.json()["results"]

            exam = results[random.randint(0, len(results) - 1)]

            examUrl = "https://2021ws-in-eidi.hq.tumexam.de/exam/1/correction/%s/%d/%d?" % (exam["erid"], correction_pass, problem)
            examUrl += "filter[problem]=%d" % problem
            examUrl += "&filter[correction_pass]=%d" % correction_pass 
            examUrl += "&filter[corrected]=False"

            webbrowser.open(examUrl)

        print("\nPress Enter for Next or Q to exit:")
        userInput = input()

        if (len(userInput) > 0):
            break

main()
