"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import math
import logging

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


MaxSpeed = {200: (200, 34), 300: (100, 32), 400: (100, 32), 600: (200, 30), 1000: (400, 28), 1300: (300, 26)}
MinSpeed = {200: (200, 15, 13.5), 300: (100, 15, 20), 400: (100, 15, 27), 600: (200, 15, 40), 1000: (400, 11.428, 75), 1300: (300, 13.333, 90)}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km

    remaining_dist = control_dist_km
    total_hours = 0
    total_minutes = 0.0

    if control_dist_km == 0:
        return brevet_start_time

    for keys in MaxSpeed:
        distance = keys
        length = MaxSpeed[keys][0]
        speed = MaxSpeed[keys][1]

        if control_dist_km - (distance) > 0:
            temp = length/speed
            hours = math.trunc(temp)
            minutes = (temp - hours) * 60
            total_hours += hours
            total_minutes += minutes
            remaining_dist -= length

        if control_dist_km - (distance) <= 0:
            dist = remaining_dist
            temp = dist/speed
            hours = math.trunc(temp)
            minutes = (temp - hours) * 60
            total_hours += hours
            total_minutes += minutes
            total_minutes = round(total_minutes)
            break

    return brevet_start_time.shift(hours=total_hours, minutes=total_minutes)

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    total_hours = 0
    total_minutes = 0.0
    remaining_dist = control_dist_km


    if control_dist_km >= (brevet_dist_km):
        hours = MinSpeed[brevet_dist_km][2]
        return brevet_start_time.shift(hours=hours)

    if control_dist_km == 0:
        return brevet_start_time.shift(hours=1)

    if control_dist_km <= 60:
        temp = control_dist_km/20
        hours = math.trunc(temp)
        minutes = (temp - hours) * 60
        hours += 1
        return brevet_start_time.shift(hours=hours, minutes=minutes)

    for keys in MinSpeed:
        distance = keys
        length = MinSpeed[keys][0]
        speed = MinSpeed[keys][1]
        end_time = MinSpeed[keys][2]

        if control_dist_km - (distance * 1.2) > 0:
            temp = length/speed
            hours = math.trunc(temp)
            minutes = (temp - hours) * 60
            total_hours += hours
            total_minutes += minutes
            remaining_dist -= length

        if control_dist_km - (distance * 1.2) <= 0:
            dist = remaining_dist
            temp = dist/speed
            hours = math.trunc(temp)
            minutes = (temp - hours) * 60
            total_hours += hours
            logging.debug(hours)
            logging.debug(total_hours)
            total_minutes += minutes
            total_minutes = round(total_minutes)
            break

    return brevet_start_time.shift(hours=total_hours, minutes=total_minutes)
