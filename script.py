import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time
from plyer import notification


age = 21
pincodes = ["110032" , "110006"]
num_days = 7

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0   

    for pincode in pincodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 

            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                if response_json["centers"]:
                    if(print_flag.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    print('Center Name : ' , center['name'])
                                    print('Available slots : ' , session['available_capacity'])
                                    print('Pincode : ' , pincode)
                                    print('Vaccine Name : ' , session['vaccine'])
                                    print('Date : ', session['date'])
                                    print('Price : ', center['fee_type'])
                                    print('----------------------------------')
                                    centerName = center['name']
                                    availbleSlots = session['available_capacity']
                                    dateOfSlot = session['date']
                                    vaccineName = session['vaccine']
                                    price = center['fee_type']
                                    notification.notify(
                                    title="Vaccine Slots Availble",
                                    # the body of the notification
                                    message=f"Center Name : {centerName}, {pincode} \nAvailable slots : {availbleSlots}, {price}\nVaccine : {vaccineName}, Date : {dateOfSlot}",
                                    app_icon = r"icon\icon.ico",
                                    timeout=5
                                    )
                                    print("\n")
                                    counter = counter + 1
            else:
                print("No Response!")

    if counter:
        mixer.init()
        mixer.music.load(r"sound\dingdong.wav")
        mixer.music.play()
        print("Search Completed!")
    else:
        mixer.init()
        mixer.music.load(r"sound\dingdong.wav")
        mixer.music.play()
        print("No Vaccination slot available!")

    dt = datetime.now() + timedelta(minutes=30)

    while datetime.now() < dt:
        time.sleep(10)
