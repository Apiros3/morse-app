# Keep track of stats, rating, and store them in a json file
rating = [0,0]
streak = [0,0]
session_sum = [0,0] 

# get rating, streak, and session_sum info from json
def init():
    return

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
    return
