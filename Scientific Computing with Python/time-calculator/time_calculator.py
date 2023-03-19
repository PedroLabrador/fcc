def convert_24_or_12_hours(hour, default):
  if default == 24:
    start = 0 if hour + 12 == 24 else hour + 12
    return [start, None]
  else:
    start = hour - 12 if hour > 12 else hour
    shift = "PM" if hour >= 12 and hour < 24 else "AM"
    return [start, shift]

def format_minutes(minutes):
  return str(minutes).rjust(2, '0')

def add_time(start, duration, day_of_the_week = ""):
  days_of_the_week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
  new_time = ""
  start_current_time, day_or_night = start.split(" ")
  start_hours, start_minutes = start_current_time.split(":")
  duration_hours, duration_minutes = duration.split(":")

  # casting
  start_hours = int(start_hours)
  start_minutes = int(start_minutes)
  duration_hours = int(duration_hours)
  duration_minutes = int(duration_minutes)

  if day_or_night == "PM":
    start_hours, _ = convert_24_or_12_hours(start_hours, 24)

  add_hours = 0
  extra_days = int(duration_hours / 24)
  add_days = 0
  
  # calc next minutes 
  if start_minutes + duration_minutes > 60:
    end_diff_minutes = abs(start_minutes + duration_minutes - 60)
    add_hours += 1
    if start_hours == 23:
      add_days += 1
  else:
    end_diff_minutes = start_minutes + duration_minutes

  # calc next hours
  duration_hours += add_hours
  if start_hours + duration_hours > 24:
    # how many days are in duration_hours
    residue_hours = abs(duration_hours - (extra_days * 24))
    if start_hours + residue_hours > 24:
      end_diff_hours = abs(start_hours + residue_hours - 24)
      extra_days += 1
    else:
      end_diff_hours = start_hours + residue_hours
  else:
    end_diff_hours = start_hours + duration_hours

  extra_days += add_days

  converted_end_hours, current_shift = convert_24_or_12_hours(end_diff_hours, 12)

  new_time = str(converted_end_hours) + ":" + format_minutes(end_diff_minutes) + " " + current_shift

  # add day of the week
  if day_of_the_week != "":
    index_next_day_of_the_week = (days_of_the_week.index(day_of_the_week.lower()) + extra_days) % 7
    next_day_of_the_week = days_of_the_week[index_next_day_of_the_week]
    new_time += ", " + next_day_of_the_week.capitalize()

  # add days later
  if extra_days > 0:
    new_time += " ("
    if extra_days == 1:
      new_time += "next day)"
    else:
      new_time += str(extra_days) + " days later)"

  return new_time