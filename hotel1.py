import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# importo i file excel necessari richiamando una funzione dal file modu.py
from modu import carica_file
hotel_ex, guest_ex, preferences_ex = carica_file()

# creo una nuova colonna 'rooms' in hotel_ex che sia uguale a quella definita come stanze disponibili
hotel_ex['stanze_disponibili'] = hotel_ex['rooms'].copy()

# dictionary comprehension, cioè itero su ogni elemento della lista
# e per ogni elemento il nome diventa una chiave a cui assegno il valore 0
guadagni_hotel = {hotel: 0 for hotel in hotel_ex['hotel']}

# iimporto le variabili sempre da modu
from modu import stats
ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()

# itero su ogni riga saltando la prima che ha i titoli delle colonne (iterrows è utilizzabile grazie alla libreria pandas)
# in questo caso grazie a _, salto la prima riga che nel file sono gli indici
for _, guest_row in guest_ex.iterrows():
    
    # estraggo per ogni riga il nome e lo sconto associati
    guest = guest_row['guest']
    discount = guest_row['discount']
    
    # filtro gli hotel per ottenere quelli che hanno almeno una stanza disponibile
    hotels_disponibili = hotel_ex[hotel_ex['stanze_disponibili'] > 0]
    
    # nel caso in cui il filtraggio di prima non ci dia più nessun hotel disponibile 
    # il codice mi deve restituire la frase sotto e poi continuare con le operazioni del loop
    if hotels_disponibili.empty:
        print('Non ci sono hotel disponibili')
        continue

    # faccio in modo che la scelta tra gli hotel disponibili sia casuale
    hotel_selezionato = np.random.choice(hotels_disponibili['hotel'])

    # faccio in modo che la variabile preferenze_ospite contenga le preferenze dell'ospite in questione
    preferenze_ospite = preferences_ex[preferences_ex['guest'] == guest]
    
    # se l'hotel che è stato selezionato randomicamente rientra tra le preferenze auentiamo il numero di ospiti soddisfatti
    if hotel_selezionato in preferenze_ospite['hotel'].values:
        ospiti_soddisfatti += 1
    
    # prendo dal file (hotel_ex) la prima riga (iloc[0]) corrispondendte all'hotel selezionato
    prezzo_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].iloc[0]
    
    # creo la variabile price
    price = prezzo_hotel['price']
    
    # calcolo il prezzo con lo sconto
    prezzo_finale = price * (1 - discount)

    # aggiungo alla lista allocazioni nuovi elementi che sono dei dizionari che rappresentano
    # un'allocazione di un ospite ad un hotel e il prezzo pagato
    allocazioni.append({
        'cliente': guest,
        'hotel_f': hotel_selezionato,
        'prezzo_pagato': prezzo_finale
    })

    # ottengo l'indice dell'hotel che soddisfa le condizioni indicate grazie a .index
    indice_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].index
    
    # diminuisco il numero di stanze disponibili di 1 nell'hotel che è stato selezionato
    hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -= 1

    #aggiorno le statistiche dopo l'allocazione
    ospiti_allocati += 1
    stanze_occupate += 1
    # aggiungo all'insieme hotel occupati l'hotel selzionato
    # se un hotel viene aggiunto più volte non darà errore e verrà registrato una sola volta l'hotel in questione
    hotel_occupati.add(hotel_selezionato)
    guadagni_hotel[hotel_selezionato] += prezzo_finale

#creo il dataframe per le allocazioni e per i guadagni totali
allocazioni_df = pd.DataFrame(allocazioni)
guadagni_df = pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno Totale'])

#creo la variabile del numero degli hotel occupati
numero_hotel_occupati = len(hotel_occupati)

#voglio i risultati finali
print(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
# inserisco f in modo tale che posso inserire delle variabili all'interno della stringa (formatted string)
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Ospiti soddisfatti: {ospiti_soddisfatti}')
print('\nGuadagni totali di ogni hotel:')
# \n serve per avere una riga vuota prima di questo output in modo da separare bene gli output
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