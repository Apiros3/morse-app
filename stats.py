# Keep track of stats, rating, and store them in a json file
streak = 0
session_sum = [0,0] 

def query(result):
    if (result):
        streak += 1
        session_sum[0] += 1
    else:
        streak = 0
        session_sum[1] += 1