# importo le varie librerie e i file necessari
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modu import carica_file
hotel_ex, guest_ex, preferences_ex = carica_file()

# creo una nuova colonna (rooms) in quel file e la faccio uguale a quella delle stanze disponibili
hotel_ex['stanze_disponibili']=hotel_ex['rooms'].copy()

# ordino gli hotel in base alla disponibilità delle stanze, parto da quello con più stanze
hotel_ex=hotel_ex.sort_values(by='stanze_disponibili', ascending=False)

# creo il dizionario per i guadagni degli hotel
guadagni_hotel={hotel: 0 for hotel in hotel_ex['hotel']}

# importo le variabili
from modu import stats
ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()

# itero su ogni riga di guest ex ignorando l'indice(_,)
for _, guest_row in guest_ex.iterrows():
    
    # estraggo da ogni riga il valore corrispondente di guest e discount e li assegno alle variabili
    guest=guest_row['guest']
    discount=guest_row['discount']
    
    # filtro preferences_ex in modo tale che mi restituisca solo la riga in cui il valore
    # della colonna guest è uguale alla variabile guest
    preferenze_ospite=preferences_ex[preferences_ex['guest']==guest]
    
    # seleziono da hotel_ex gli hotel con almeno una stanza disponibile
    # estraggo solo la colonna hotel e verifico se c'è corrispondenza 
    # tra gli hotel preferiti dall'ospite  e quelli ottenuti, quindi creo hotels_preferiti
    hotels_preferiti=preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili']>0]['hotel'])]
    
    # se non è vuoto procedo altrimenti skippo questa parte
    if not hotels_preferiti.empty:
        
        # cerco di allocare l'ospite nell'hotel preferrito che ha più stanze disponibili
        # merge è come un join in sql e ci serve in questo caso per unire due colonne che hanno in comune 
        # la colonna hotel in modo tale che la scelta possa essere fatta in base alla richiesta specificata prima
        hotels_preferiti=hotels_preferiti.merge(hotel_ex[['hotel', 'stanze_disponibili']], on='hotel').sort_values(by='stanze_disponibili', ascending=False)
        
        # seleziono il primo hotel preferito (.iloc[0]) con più disponibilità di stanze
        hotel_selezionato=hotels_preferiti.iloc[0]['hotel']
        
        # aumento il numero di ospiti soddisfatti
        ospiti_soddisfatti += 1 
    else:
        continue
    
    # seleziono il valore nella colonna price della prima riga in cui hotel selezionato
    # è uguale al valore nella colonna hotel della riga di hotel_ex in questione
    prezzo_hotel=hotel_ex[hotel_ex['hotel']== hotel_selezionato].iloc[0]['price']
    
    # calcolo lo sconto
    prezzo_finale=prezzo_hotel*(1-discount)
    
    # aggiungo ogni volta un nuovo elemento alla lista allocazioni
    # il nuovo elemento è un dizionario che contiene le informazioni: cliente, hotel e prezzo
    allocazioni.append({
        'cliente':guest,
        'hotel_f':hotel_selezionato,
        'prezzo_pagato':prezzo_finale
    })
    
    # .index mi restituisce l'indice della riga in cui il valore della colonna hotel è uguale a hotel selezionato
    indice_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].index
    
    # riduco il numero di stanze disponibili, .loc invece serve per filtrare secondo un etichetta
    # in questo caso filtriamo attraerso indice hotel
    hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -= 1
    
    # aggiorno le statistiche delle variabili
    ospiti_allocati += 1
    guadagni_hotel[hotel_selezionato] += prezzo_finale
    stanze_occupate += 1
    
    # aggiungo al'insieme l'hotel selezionato ogni volta
    hotel_occupati.add(hotel_selezionato)
    
    # se non ci sono stanze disponibili interrompere il loop
    if hotel_ex['stanze_disponibili'].sum() ==0:
        print('Tutte le stanze sono occupate')
        break

# creo i dataframe, in quello dei gudagni voglio che sia creata una tabella
# in cui siano riportati gli hotel e i rispettivi guadagni totali
allocazioni_df_4 = pd.DataFrame(allocazioni)
guadagni_df_4 = pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno totale'])

# variabile che indica il numero degli hotel occuapti
numero_hotel_occupati = len(hotel_occupati)

# f mi serve per inserire una variabile in una stringa
print(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Numero di ospiti soddisfatti: {ospiti_soddisfatti}')

# n invece mi serve per lasciare una riga vuota tra quello che sto stampando ora e quello che ho stampato
# immediatamente prima
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df_4)
print('\nAllocazioni degli ospiti:')
print(allocazioni_df_4)

# nome delle porzioni del grafico a torta
labels = ['Ospiti soddisfatti', 'Ospiti non soddisfatti']
# necessito di questo condizionamento perchè altrimenti ci sarebbero problemi nel viualizzare il grafico
sizes = [ospiti_soddisfatti, len(guest_ex)-ospiti_soddisfatti]
if sizes[1] == 0:
    sizes[1] = 0.1
# i colori delle due porzioni
colors = ['green', 'red']
# grandezza del grafico
plt.figure(figsize=(4, 4))
# grafico a torta, con percentuali decimali
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=40)
# titolo del grafico
plt.title('Soddisfazione degli Ospiti', fontsize=14)
# deve essere un cerchio il grafico a torta
plt.axis('equal')
# comando per visualizzare l'immagine del grafico
plt.show()