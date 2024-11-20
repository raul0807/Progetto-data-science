# importo le varie librerie e i file necessari
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modu import carica_file
hotel_ex, guest_ex, preferences_ex = carica_file()

# creo una nuova colonna (rooms) in quel file e la faccio uguale a quella delle stanze disponibili
hotel_ex['stanze_disponibili']=hotel_ex['rooms'].copy()

# ordino gli hotel in base al prezzo crescente
hotel_ex=hotel_ex.sort_values(by='price')

# creo un dizionario per i guadagni di ogni hotel
guadagni_hotel= {hotel: 0 for hotel in hotel_ex['hotel']}

# importo una funzione
from modu import stats
ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()

# itero su ogni riga ignorando l'indice (_,)
for _, guest_row in guest_ex.iterrows():
    
    # estraggo per ogni riga il nome e lo sconto associati
    guest=guest_row['guest']
    discount=guest_row['discount']
    
    # faccio in modo che questa variabile contenga le preferenze dell'ospite in questione
    preferenze_ospite = preferences_ex[preferences_ex['guest'] == guest]
    
    # trovo tra le preferenze del cliente, in ordine, l'hotel più economico con almeno una stanza libera
    # grazie ad isin posso selezionare gli hotel con almeno una stanza libera tra quelli nelle preferenze, inoltre li avevo gia ordinati in base al prezzo grazie a sort
    hotels_preferiti=preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili']>0]['hotel'])]
    
    if not hotels_preferiti.empty:
        # qua sto prendendo gli elementi di hotel preferiti e grazie a merge che prende
        # la colonna in comune tra hotels preferiti e hotel ex e poi aggiunge la colonna price a
        # hotels preferiti e li ordina in base al prezzo 
        hotels_preferiti=hotels_preferiti.merge(hotel_ex[['hotel', 'price']], on='hotel').sort_values(by='price')
        
        # seleziono il primo hotel (.iloc[0]) perchè so che in hotels preferiti prima li ho ordinati
        # in base al prezzo quindi il primo sarà quello col prezzo più basso
        hotel_selezionato=hotels_preferiti.iloc[0]['hotel']
        
        # se l'hotel selezionato è tra le preferenze dell'ospite posso aumentare il valore degli ospiti soddisfatti
        if hotel_selezionato in preferenze_ospite['hotel'].values:
            ospiti_soddisfatti += 1
    else:
        # se non ci sono preferenze valide skippiamo il cliente e non viene allocato
        continue
    
    # prendo il prezzo dell'hotel selezionato e calcolo lo sconto
    prezzo_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].iloc[0]['price']
    prezzo_finale=prezzo_hotel*(1-discount)
    
    # aggiungo ogni volta un nuovo elemento alla lista allocazioni
    # il nuovo elemento è un dizionario che contiene le informazioni: cliente, hotel e prezzo
    allocazioni.append({
        'cliente':guest,
        'hotel_f':hotel_selezionato,
        'prezzo_pagato':prezzo_finale
    })
    
    # trovo l'indice dalla riga di hotel_ex che corrisponde all'hotel selezionato
    indice_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].index
    
    # diminuisco di 1 le stanze disponibili nell'hotel da cui abbiamo trovato l'indice 
    # utilizziamo loc appunto per modificcare uno specifico valore all'interno di hotel_ex
    hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -=1
    
    # aggiorno le statistiche
    ospiti_allocati+=1
    stanze_occupate+=1
    
    # aggiungo all'insieme degli hotel occupati l'hotel selezionato
    hotel_occupati.add(hotel_selezionato)
    
    # aumento i guadagni di ogni singolo hotel in base a quello che viene selezionato di volta in volta
    guadagni_hotel[hotel_selezionato] += prezzo_finale
    
    # se non ci sono stanze disponibili in nessun hotel interrompo il loop
    if hotel_ex['stanze_disponibili'].sum()==0:
        print('Stanze sold out')
        break

# creo i dataframe
allocazioni_df_3 = pd.DataFrame(allocazioni)
guadagni_df_3=pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno Totale'])
numero_hotel_occupati= len(hotel_occupati)

# f mi serve per inserire variabili all'interno di stringe
print(f'Nuero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Numero di ospiti soddisfatti: {ospiti_soddisfatti}')
# n mi permette di separare con una riga vuota quello che stampo da quello che ho stampato subito prima
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df_3)
print('\nAllocazioni degli ospiti:')
print(allocazioni_df_3)

# nome delle porzioni del grafico 
labels = ['Ospiti soddisfatti', 'Ospiti non soddisfatti']
# varaibili che rappresentano le due porzioni 
sizes = [ospiti_soddisfatti, len(guest_ex)-ospiti_soddisfatti]
# colori delle porzioni
colors = ['green', 'red']
# grandezza della figura
plt.figure(figsize=(4, 4))
# grafico a torta in percentuali decimali
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=40)
# titolo
plt.title('Soddisfazione degli Ospiti', fontsize=14)
# deve essere un cerchio
plt.axis('equal')
# comando per ottenere il grafico
plt.show()