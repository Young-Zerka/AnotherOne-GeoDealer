import json
import os

import tkinter
import tkinter as tk
import tkintermapview
import phonenumbers
import opencage
from phonenumbers import geocoder, carrier

from tkinter import *
from tkinter import messagebox

from opencage.geocoder import OpenCageGeocode

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

######################################
####### Config Includes ##############
######################################
key = config["key"]
######################################
####### Config Includes ##############
######################################

root = tkinter.Tk()
root.title("GeoDealеr")
root.geometry("700x480")
root.iconbitmap("icon.ico") 

label1 = Label(text="GeoDealеr")
label1.pack()

def getResult():
    num = number.get("1.0", END)
    try:
        num1 = phonenumbers.parse(num)
    except:
        messagebox.showerror("Error", "Number box is empty or the input is not numeric !!")

    location = geocoder.description_for_number(num1, "en")
    service_provider = carrier.name_for_number(num1, "en")

    ocg = OpenCageGeocode(key)
    query = str(location)
    results = ocg.geocode(query)

    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    my_label = LabelFrame(root)
    my_label.pack(pady=20)

    map_widget = tkintermapview.TkinterMapView(my_label, width=450, corner_radius=5)
    map_widget.set_position(lat, lng)
    map_widget.set_marker(lat, lng, text = "Phone Location")
    map_widget.set_zoom(10)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    map_widget.pack()

    result.insert(END, "The country of this number is: " + location)
    result.insert(END, "\nThe sim card of this number is: " + service_provider)
    
    result.insert(END, "\nLatitude is: " + str(lat))
    result.insert(END, "\nLongitude is: " + str(lng))

    adr = tkintermapview.convert_coordinates_to_address(lat, lng)

    if adr:
        result.insert(END, "\nStreet Address is: " + adr.street if adr.street else "\nStreet Address is not available")
        result.insert(END, "\nCity Address is: " + adr.city if adr.city else "\nCity Address is not available")
        result.insert(END, "\nPostal Code is: " + adr.postal if adr.postal else "\nPostal Code is not available")
    else:
        result.insert(END, "\nAddress information is not available")

number = Text(height=1)
number.pack()

button=Button(text="Search", bg="white", bd=0, command=getResult)
button.pack(pady = 10, padx=100)

result = Text(height=7)
result.pack()

root.mainloop()