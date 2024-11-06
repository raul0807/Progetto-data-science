import pandas as pd

## Carico i file excel necessari
from modu import carica_file
hotel_ex, guest_ex, preferences_ex = carica_file()

## creo una colonna che rappresenti le stanze disponibili
hotel_ex['stanze_disponibili']= hotel_ex['rooms'].copy()

##creo un dizionario per tracciare i guadagno per ogni hotel
guadagni_hotel= {hotel: 0 for hotel in hotel_ex['hotel']}

from modu import stats
ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()

## loop sugli ospiti ordinati dal primo all'ultimo
for _, guest_row in guest_ex.iterrows():
    ##iterrows serve per iterare su ogni riga in questo caso l'indice è _ e la riga è guest_row
    guest=guest_row['guest']
    discount=guest_row['discount']
    
    ##devo tener conto delle preferenze degli ospiti
    preferenze_ospite= preferences_ex[preferences_ex['guest']==guest]
    
    ##devo trovare stanze disponibili nelle preferenze del cliente
    hotels_preferiti= preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili']>0]['hotel'])]
    ## isin appunto serve per verificare se ciascun elemento di una colonna o di un DataFrame è presente in una lista di valori specificati
    ## in questo caso infatti stiamo cercando tra le preferenze del cliente un hotel che abbia almeno una stanza disponibile
    
    if not hotels_preferiti.empty:
        ##se ci sono preferenze disponibili selezioniamo il primo hotel preferito cond disponibilità
        hotel_selezionato= hotels_preferiti.iloc[0]['hotel']
        ospiti_soddisfatti += 1 ##così aggiungo un ospite a quelli soddisfatti   
    else:
        ##se non ci sono preferenze valide saltiamo l'ospite e non lo allochiamo
        continue
    
    
    ##devo prendere il prezzo dell'hotel selezionato
    ## iloc mi serve per accedere a righe e colonne in base alla posizione numerica (intger location) 
    ## in questo caso usiamo l'indice zero percchè ci serve il prezzo dell'hotel selezionato appunto
    prezzo_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].iloc[0]
    price=prezzo_hotel['price']
    
    ##calcolo lo sconto
    prezzo_finale= price*(1-discount)
    
    ##considero sempre le allocazioni
    allocazioni.append({
        'cliente': guest,
        'hotel_f':hotel_selezionato,
        'prezzo_pagato':prezzo_finale
        })
    ##riduco il numero di stanze disponibili
    indice_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].index
    hotel_ex.loc[indice_hotel, 'stanze_disponibili']-=1 
    ## loc invece serve per avere un risultato in base ai nomi di righe e colonne invece che l'indice numerico come fa iloc
    
    ##aggiorno le statistiche
    ospiti_allocati += 1
    stanze_occupate += 1
    hotel_occupati.add(hotel_selezionato)
    guadagni_hotel[hotel_selezionato] += prezzo_finale
    
    ##se tutti gli hotel sono pieni interrompo l'allocazione
    if hotel_ex['stanze_disponibili'].sum() == 0:
        print('Tutte le stanze sono occupate.')
        break

##infine creo un dataframe dalle allocazioni
allocazioni_df_2=pd.DataFrame(allocazioni)

##risultato finale
numero_hotel_occupati= len(hotel_occupati)
print(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Numero di ospiti soddisfatti: {ospiti_soddisfatti}')

##i guadagni totali di ogni hotel
guadagni_df_2= pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno totale'])
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df_2)

##allocazuoni finali
print('\nAllocazioni degli ospiti:')
print(allocazioni_df_2)