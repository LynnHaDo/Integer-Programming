class TimeConverter:
    """
    Contains methods to convert time into integers
    """
    def __init__(self):
        self.DAY_MULTIPLIER = 10000

    def day_and_time_to_int(self, day: str, time: str):
        """
        Given a day in week (Monday, Tuesday, Wednesday, 
        Thursday, Friday, Saturday, Sunday) and time in the day
        (HH:MM format), convert it into integer for comparison
        """
        num = self.time_to_minutes(time)
        
        match (day):
            case "Monday":
                num += self.DAY_MULTIPLIER * 1
            case "Tuesday":
                num += self.DAY_MULTIPLIER * 2
            case "Wednesday":
                num += self.DAY_MULTIPLIER * 3
            case "Thursday":
                num += self.DAY_MULTIPLIER * 4
            case "Friday":
                num += self.DAY_MULTIPLIER * 5
            case "Saturday":
                num += self.DAY_MULTIPLIER * 6
            case "Sunday":
                num += self.DAY_MULTIPLIER * 7
                
        return num
        
    def time_to_minutes(self, time: str):
        """
        Convert a time in HH:MM format to minutes
        """
        h, m = time.split(":")
        
        h = int(h)
        m = int(m)
        
        return h * 60 + m