import requests
from urllib.request import urlopen
import urllib.parse
import json
from datetime import datetime
from tealist.models import Vendor, Tea, TeaVariant, Variety
from djmoney.money import Money
import re
from thefuzz import fuzz

test_vendors = ["https://essenceoftea.com/", "https://kingteamall.com"]


def run(*args):
    varities = Variety.objects.all()

    text = args[0]

    def CheckAgainstAliases(text):
        for variety in varities:
            for a in variety.alias:
                print(f"{text},{a}: {fuzz.ratio(text, a)}")

    for word in text.split():
        CheckAgainstAliases(word)
