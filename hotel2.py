# importo le librerie necessarie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# importo i file excel necessari richiamando una funzione dal file modu.py
from modu import carica_file
hotel_ex, guest_ex, preferences_ex = carica_file()

# creo una nuova colonna in hotel_ex che sia uguale a quella definita come rooms
hotel_ex['stanze_disponibili']= hotel_ex['rooms'].copy()

# dictionary comprehension, cioè itero su ogni elemento della lista
# e per ogni elemento il nome diventa una chiave a cui assegno il valore 0
guadagni_hotel= {hotel: 0 for hotel in hotel_ex['hotel']}

# importo le variabili sempre da modu
from modu import stats
ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()

# itero su ogni riga saltando ignorando l'indicie (_,) (iterrows è utilizzabile grazie alla libreria pandas)
for _, guest_row in guest_ex.iterrows():
    
    # estraggo per ogni riga il nome e lo sconto associati
    guest=guest_row['guest']
    discount=guest_row['discount']
    
    # faccio in modo che la variabile preferenze_ospite contenga le preferenze dell'ospite in questione
    preferenze_ospite= preferences_ex[preferences_ex['guest']==guest]
    
    # troviamo tra gli hotel preferiti dall'ospite quelli che hanno almeno una stanza disponibile e .isin verifica proprio ciascun elemento di una colonna
    # per trovare quelli che soddisfano la richiesta
    hotels_preferiti= preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili']>0]['hotel'])]
    
    # se ci sono hotel disponibili tra quelli preferiti dal cliente
    if not hotels_preferiti.empty:
        
        # selezioniamo il primo hotel preferito con disponibilità e poi aggiungo 1 al numero degli ospiti soddisfatti
        hotel_selezionato= hotels_preferiti.iloc[0]['hotel']
        ospiti_soddisfatti += 1   
    else:
        # se non ci sono preferenze valide saltiamo l'ospite e non lo allochiamo
        continue
    
    
    # definisco il prezzo dell'hotel grazie ad .iloc che seleziona solo la prima riga
    # ottenuta dal filtraggio degli hotel
    prezzo_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].iloc[0]
    
    # definisco la variabli price
    price=prezzo_hotel['price']
    
    # calcolo lo sconto
    prezzo_finale= price*(1-discount)
    
    # aggiungo ogni volta un nuovo elemento alla lista allocazioni
    # il nuovo elemento è un dizionario che contiene le informazioni: cliente, hotel e prezzo
    allocazioni.append({
        'cliente': guest,
        'hotel_f':hotel_selezionato,
        'prezzo_pagato':prezzo_finale
        })
    
    # ottengo l'indice dell'hotel che soddisfa le condizioni indicate grazie a .index
    indice_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].index
    
    # riduco il numero di stanze disponibili dell'hotel selezionato
    # loc serve per avere un risultato in base ai nomi di righe e colonne invece che l'indice numerico come fa iloc
    hotel_ex.loc[indice_hotel, 'stanze_disponibili']-=1 
    
    # aggiorno le statistiche
    ospiti_allocati += 1
    stanze_occupate += 1
    # aggiungo all'insieme degli hotel occupati l'hotel selezionato
    hotel_occupati.add(hotel_selezionato)
    # aumento i guadagni di ogni singolo hotel in base a quello che viene selezionato di volta in volta
    guadagni_hotel[hotel_selezionato] += prezzo_finale
    
    # se tutti gli hotel sono pieni interrompo l'iterazione stampo il messaggio che voglio
    if hotel_ex['stanze_disponibili'].sum() == 0:
        print('Tutte le stanze sono occupate.')
        break

# creo un dataframe per allocazioni e per i guadagni
# quello dei guadagi sarà una tabella in cui verranno rappresentati gli hotel e i loro rispettivi guadagni
allocazioni_df_2=pd.DataFrame(allocazioni)
guadagni_df_2= pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno totale'])

# voglio un numero per gli hotel occupati
numero_hotel_occupati= len(hotel_occupati)

# f serve per poter inserire le variabili all'interno di una stringa
print(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Numero di ospiti soddisfatti: {ospiti_soddisfatti}')
# n invece è utile per creare uno spazio vuoto tra questo che voglio stampare adesso e quello che ho stampato prima
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df_2)
print('\nAllocazioni degli ospiti:')
print(allocazioni_df_2)

labels = ['Ospiti soddisfatti', 'Ospiti non soddisfatti']
# nomi delle due fette della torta
sizes = [ospiti_soddisfatti, len(guest_ex)-ospiti_soddisfatti]
# quantità delle due porzioni
colors = ['green', 'red']
# colori delle due porzioni
plt.figure(figsize=(4, 4))
# misura della figura
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=40)
# grafico a torta, dati in percentuali decimali
plt.title('Soddisfazione degli Ospiti', fontsize=14)
# titolo e grandezza
plt.axis('equal')
# deve essere circolare la torta
plt.show()
# comando per avere la figura