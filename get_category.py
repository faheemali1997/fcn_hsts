# -*- coding: utf-8 -*-
"""Get_Category.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f63HivfeEoGoNQEx-pipXcfHA4-MLxzn
"""

import requests
import json


def getcategory(domain):
  url = "https://www.klazify.com/api/categorize"

  payload = "{\"url\":\"https://www." + domain + "\"}\n"
  headers = {
      'Accept': "application/json",
      'Content-Type': "application/json",
      'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMzI1YjgzMTMyN2VjZWRkM2I5YTkyYTkyMGYyZDFhYjNmYjIwN2MwYmM3N2ZiMGI4ZGNhYWQxYmFkNjE3Zjk3OThhNmY0NWRlYjBjZTJmZGMiLCJpYXQiOjE2Mzg3NTM2NzQsIm5iZiI6MTYzODc1MzY3NCwiZXhwIjoxNjcwMjg5Njc0LCJzdWIiOiI1NDUzIiwic2NvcGVzIjpbXX0.syxjP8cGVFZiW4zmdnhWCj61JZ-LrccuqeHBO5FybmBp2gzN7tDpdCfLWV8Am4k0jYyY6gfkBa_r-5E4R_wQrA",
      'cache-control': "no-cache"
      }

  response = requests.request("POST", url, data=payload, headers=headers)
  if response.ok:
    response_native = json.loads(response.text)
    return response_native
  return None

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/FCN\ Project

import pandas as pd


df = pd.read_csv('chrome_pruned.csv')
df['Category'] = None
df['Confidence'] = 0.0


for i in range(3,len(df)):
  if i == 60:
    break
  domain = df.loc[i,"Domain Name"]
  val = getcategory(domain)
  if val is not None:
    print(i,val)
    df.loc[i,"Confidence"] = val['domain']['categories'][0]['confidence']
    df.loc[i,"Category"] = val['domain']['categories'][0]['name']