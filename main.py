"""
Coded by: Lysandre Roussianos / 28.04.2022

This program is developed for SCP (Swiss Car Park) in Lausanne to automate their car park system.
It allows for the display of available car park spaces, issuance of unique tickets on entry,
and calculation of parking fees based on the duration of stay.
The system also have parking restrictions and charges an extra fee for overstaying.
"""
import math
from datetime import datetime
import os
from colorama import Fore, Back, Style
import time

car_data = []
daily_takings = 0
amount_cars_parked = 0
new_ticket = 0
total_minute_spent = 0
overstayed_cars = 0

def check_yes_no(question):
    while True:
        ans = input(question).strip().upper()
        if ans == "Y" or ans == "N":
            return ans
        else:
            print(Fore.RED + "Please enter Y or N")
            print(Style.RESET_ALL)


def checkstr(question):
    while True:
        ans = input(question)
        if ans.isalpha():
            return ans
        else:
            print(Fore.RED + "Only input letters")
            print(Style.RESET_ALL)


def checkint(question):
    while True:
        try:
            ans = int(input(question))
            if ans >= 0:
                return ans
        except ValueError:
            print(Fore.RED + "Only input positive numbers")
            print(Style.RESET_ALL)


def retrieve_entry_time(ticket):
    for car in car_data:
        if car[0] == ticket:
            entry_time = datetime.strptime(car[1], '%H:%M')
            entry_time_str = entry_time.strftime('%H:%M:%S')
            return entry_time_str
    return None


def reset_parking():
    global car_data, daily_takings, amount_cars_parked, new_ticket, total_minute_spent, overstayed_cars
    while True:
        car_data = []
        daily_takings = 0
        amount_cars_parked = 0
        new_ticket = 0
        total_minute_spent = 0
        overstayed_cars = 0
        print(Fore.BLUE + "All data has been erased")
        print(Style.RESET_ALL)
        print("Press " + Fore.BLUE + "[ENTER]" + Style.RESET_ALL + " to exit")
        user_choice = input("")
        if user_choice == "":
            break



def banner():
    print(Fore.GREEN + """
 _____          _           _____             ______          _    
/  ___|        (_)         /  __ \            | ___ \        | |   
\ `--.__      ___ ___ ___  | /  \/ __ _ _ __  | |_/ /_ _ _ __| | __
 `--. \ \ /\ / / / __/ __| | |    / _` | '__| |  __/ _` | '__| |/ /
/\__/ /\ V  V /| \__ \__ \ | \__/\ (_| | |    | | | (_| | |  |   < 
\____/  \_/\_/ |_|___/___/  \____/\__,_|_|    \_|  \__,_|_|  |_|\_|
    """)
    print(Style.RESET_ALL)


def entry_parking():
    global car_data, amount_cars_parked, new_ticket

    while True:
        if len(car_data) < 100:
            new_ticket += 1
            print("Entry Time (E.g 12:30 / 24h Clock)")
            current_time = input("> ")
            while True:
                if len(current_time) == 5 and current_time[2] == ':' and current_time[:2].isdigit() and current_time[3:].isdigit() and 0 <= int(current_time[:2]) <= 23 and 0 <= int(current_time[3:]) <= 59:
                    car_data.append([new_ticket, current_time])
                    print(f"Your Entry Time {current_time}")
                    print(f"Your Ticket Number {new_ticket}")
                    amount_cars_parked += 1
                    break
                else:
                    print(Fore.RED + "Please enter your departure time in the format hours:minutes (xx:xx)")
                    print(Style.RESET_ALL)
                    current_time = input("> ")

        else:
            print("Sorry, the car park is full.")
        print("Press " + Fore.YELLOW + "[ENTER]" + Style.RESET_ALL + " to exit.")
        user_choice = input("")
        if user_choice == "":
            os.system("clear")
            break


def exit_parking():
    while True:
        global car_data, daily_takings, total_minute_spent, overstayed_cars
        fee = 0
        ticket_number = checkint("Enter your ticket number: ")
        entry_time = retrieve_entry_time(ticket_number)
        print("Your entry time: " + Fore.GREEN + str(entry_time))
        print(Style.RESET_ALL)
        car_ticket = None
        for i in range(len(car_data)):
            if car_data[i][0] == ticket_number:
                car_ticket = car_data[i]
                del car_data[i]
                break
        if car_ticket is not None:
            entry_time = datetime.strptime(car_ticket[1], '%H:%M')
            print("Please enter your departure time (E.g 12:30 / 24h Clock)")
            while True:
                try:
                    departure_time = datetime.strptime(input("> "), '%H:%M')
                    if departure_time > entry_time:
                        break
                    else:
                        print(Fore.RED + "The departure time needs to be later than entry time.")
                        print(Style.RESET_ALL)
                except ValueError:
                    print(Fore.RED + "Please enter your departure time in the format hours:minutes (xx:xx)")
                    print(Style.RESET_ALL)
            time_spent_car = departure_time - entry_time
            hours_spent = int(time_spent_car.total_seconds() / 3600)
            minute_spent = int(time_spent_car.total_seconds() / 60)
            if departure_time > entry_time:
                fee += 1.5
            rounded_hours_spent = round(hours_spent, 2)
            fee += rounded_hours_spent * 1.5
            print(f"You have stayed {hours_spent} hours in the parking.")
            if rounded_hours_spent >= 8:
                print(Fore.YELLOW + "You have overstayed more than 8 hours.")
                print(Style.RESET_ALL)
                extra_fee = 100
                overstayed_cars += 1
                fee += extra_fee
            print(f"Your parking fee is {round(fee, 2)} CHF")
            print("Press " + Fore.RED + "[ENTER]" + Style.RESET_ALL + " to pay")
            user_choice = input("")
            if user_choice == "":
                daily_takings += fee
                total_minute_spent += minute_spent
                os.system("clear")
                break
        else:
            print(Fore.RED + "Invalid ticket number.")
            print(Style.RESET_ALL)
            time.sleep(1)
        os.system("clear")
        break


def daily_stats_reset():
    while True:
        if amount_cars_parked == 0:
            avg_charge_car = 0
            avg_length_stay = 0
        else:
            avg_charge_car = round(daily_takings / amount_cars_parked, 2)
            avg_length_stay = (total_minute_spent / amount_cars_parked) / 60
            avg_length_stay = round(avg_length_stay, 2)
        print(f"Total daily takings: {Fore.GREEN} {daily_takings} CHF")
        print(Style.RESET_ALL)
        print(f"Amount of cars that have used the parking: {Fore.GREEN} {amount_cars_parked}")
        print(Style.RESET_ALL)
        print(f"Amount of cars that have overstayed: {Fore.GREEN} {overstayed_cars}")
        print(Style.RESET_ALL)
        print(f"Average charge per car: {Fore.GREEN} {avg_charge_car} CHF")
        print(Style.RESET_ALL)
        print(f"Average length of stay per car: {Fore.GREEN} {avg_length_stay} hours ")
        print(Style.RESET_ALL)
        print("Do you wish to reset the parking Y/N")
        user_choice = check_yes_no("> ")
        if user_choice == "Y":
            reset_parking()
            os.system("clear")
            break
        elif user_choice == "N":
            os.system("clear")
            break


def main_menu():
    while True:
        spaces_left = 100 - len(car_data)
        banner()
        print("1 - Enter parking")
        print("2 - Exit parking")
        print("3 - Daily stats/Reset parking")
        print(Fore.GREEN + f"{spaces_left} Places Left")
        print(Style.RESET_ALL)
        while True:
            try:
                user_choice = int(input("> "))
                if user_choice in [1, 2, 3]:
                    break
                else:
                    print(Fore.RED + "Please enter 1, 2, or 3")
                    print(Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Only input numbers")
                print(Style.RESET_ALL)

        if user_choice == 1:
            print(
                "The car park charges 1.50CHF per hour, or part of hour. An extra of 100CHF will be charged if you stay more than eight hours")
            print("")
            print("Enter Parking Y/N")
            user_choice = check_yes_no("> ")
            if user_choice == "Y":
                entry_parking()
        elif user_choice == 2:
            exit_parking()
        elif user_choice == 3:
            daily_stats_reset()


main_menu()
