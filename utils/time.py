from datetime import datetime

DAY_CONST = 10000

def day_and_time_to_int(day: str, time: str):
    """
    Given a day in week (Monday, Tuesday, Wednesday, 
    Thursday, Friday, Saturday, Sunday) and time in the day
    (HH:MM format), convert it into integer for comparison
    """
    num = time_to_minutes(time)
    
    match (day):
        case "Monday":
            num += DAY_CONST * 1
        case "Tuesday":
            num += DAY_CONST * 2
        case "Wednesday":
            num += DAY_CONST * 3
        case "Thursday":
            num += DAY_CONST * 4
        case "Friday":
            num += DAY_CONST * 5
        case "Saturday":
            num += DAY_CONST * 6
        case "Sunday":
            num += DAY_CONST * 7
    
    return num
    
def time_to_minutes(time: str):
    """
    Convert a time in HH:MM format to minutes
    """
    h, m = time.split(":")
    
    h = int(h)
    m = int(m)
    
    return h * 60 + m