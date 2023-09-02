import json 

# Keep track of stats, rating, and store them in a json file
f = open('stats.json')
data = json.load(f)

rating = [0,0]
streak = [0,0]
session_sum = [0,0] 
difficulty = [0]

# get rating, streak, and session_sum info from json
def init():
    rating[0] = data['rating']['current']
    rating[1] = data['rating']['maximum']
    streak[0] = data['streak']['current']
    streak[1] = data['streak']['maximum']
    save()

def query(result, rating_mode):
    if (result):
        streak[0] += 1
        session_sum[0] += 1
    else:
        streak[0] = 0
        session_sum[1] += 1
    streak[1] = max(streak)
    
    save()

# update json file accordingly
def save():
    data['rating']['current'] = rating[0]
    data['rating']['maximum'] = rating[1]
    data['streak']['current'] = streak[0]
    data['streak']['maximum'] = streak[1]
    data['total']['AC'] = session_sum[0]
    data['total']['WA'] = session_sum[1]

    # print(data)
    json_file = json.dumps(data, indent=4)
    with open("stats.json", "w") as g:
        g.write(json_file)
