import json

with open('gjuhetHuaja.json', 'r') as f:
    gjuhet = json.load(f)

for gjuha in gjuhet:
    print(gjuha)

