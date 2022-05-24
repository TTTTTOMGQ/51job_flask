# -*- codeing = utf-8 -*-
import json

with open('keyword.txt', 'r') as f:
    klist = json.load(f)

print(klist['keyword'])