
import json
from pprint import pprint

with open('C:\Users\TalBY\Downloads\\resultsfile.json') as data_file:    
    data = json.load(data_file)

print(data)
print(data[0].keys())
[1 for d in data if d['human'] != d['model']].count
sum([1 for d in data if 0 != d['model']])
sum([1 for d in data if 1 != d['model']])
