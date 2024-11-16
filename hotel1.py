import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# importo i file excel necessari
from modu import carica_file
hotel_ex, guest_ex, preferences_ex = carica_file()

# creo una nuova colonna e un dizionario
hotel_ex['stanze_disponibili'] = hotel_ex['rooms'].copy()
guadagni_hotel = {hotel: 0 for hotel in hotel_ex['hotel']}

# importo le stas 
from modu import stats
ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()

# itero su ogni riga saltando la prima che ha i titoli delle colonne
for _, guest_row in guest_ex.iterrows():
    guest = guest_row['guest']
    discount = guest_row['discount']
    
    # controllo gli hotel con stanze disponibili
    hotels_disponibili = hotel_ex[hotel_ex['stanze_disponibili'] > 0]
    if hotels_disponibili.empty:
        print('Non ci sono hotel disponibili')
        continue

    # scelgo un hotel random tra quelli disponibili
    hotel_selezionato = np.random.choice(hotels_disponibili['hotel'])

    # controllo se l'hotel è tra le preferenze dell'ospite
    preferenze_ospite = preferences_ex[preferences_ex['guest'] == guest]
    if hotel_selezionato in preferenze_ospite['hotel'].values:
        ospiti_soddisfatti += 1
    
    # calcolo il prezzo con lo sconto
    prezzo_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].iloc[0]
    price = prezzo_hotel['price']
    prezzo_finale = price * (1 - discount)

    #aggiungo ai dati su ogni allocazione
    allocazioni.append({
        'cliente': guest,
        'hotel_f': hotel_selezionato,
        'prezzo_pagato': prezzo_finale
    })

    #aggiorno le stanze disponibili e gli hotel selezionati
    indice_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].index
    hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -= 1

    #aggiorno le statistiche dopo l'allocazione
    ospiti_allocati += 1
    stanze_occupate += 1
    hotel_occupati.add(hotel_selezionato)
    guadagni_hotel[hotel_selezionato] += prezzo_finale

#creo il dataframe per le allocazioni e per i guadagni totali
allocazioni_df = pd.DataFrame(allocazioni)
numero_hotel_occupati = len(hotel_occupati)
guadagni_df = pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno Totale'])

#voglio i risultati finali
print(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Ospiti soddisfatti: {ospiti_soddisfatti}')
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df)
print('\nAllocazioni degli ospiti:')
print(allocazioni_df)

labels = ['Ospiti soddisfatti', 'Ospiti non soddisfatti']
# nomi delle due porzioni del grafico
sizes = [ospiti_soddisfatti, len(guest_ex)-ospiti_soddisfatti]
# quali sono i dati di cui tener conto
colors = ['green', 'red']
#colore delle due porzioni
plt.figure(figsize=(4, 4))
#grandezza figura
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=40)
#grafico a torta
plt.title('Soddisfazione degli Ospiti', fontsize=14)
#titolo e grandezza
plt.axis('equal')
#serve per far si che sia un cerchio
plt.show()
#utilizzo un grafico per mostrare il grado di soddifazione degli ospiti