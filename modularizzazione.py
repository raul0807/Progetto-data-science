def carica_file():
    hotel_ex = pd.read_excel("/Users/raulspano/Desktop/progetto hotel/hotels.xlsx")
    guest_ex = pd.read_excel('/Users/raulspano/Desktop/progetto hotel/guests.xlsx')
    preferences_ex = pd.read_excel('/Users/raulspano/Desktop/progetto hotel/preferences.xlsx')
    return hotel_ex, guest_ex, preferences_ex
    