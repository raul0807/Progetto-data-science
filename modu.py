import pandas as pd
import matplotlib.pyplot as plt 

def carica_file():
    hotel_ex = pd.read_excel("/Users/raulspano/Desktop/progetto hotel/hotels.xlsx")
    guest_ex = pd.read_excel('/Users/raulspano/Desktop/progetto hotel/guests.xlsx')
    preferences_ex = pd.read_excel('/Users/raulspano/Desktop/progetto hotel/preferences.xlsx')
    return hotel_ex, guest_ex, preferences_ex


def stats():
    ospiti_allocati=0
    stanze_occupate=0
    hotel_occupati=set()
    ospiti_soddisfatti=0
    allocazioni=[]
    return ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni