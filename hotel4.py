import pandas as pd

from modu import carica_file
hotel_ex, guest_ex, preferences_ex = carica_file()

##creo come sempre la colonna per le stanze dispnibili copiando quella rooms
hotel_ex['stanze_disponibili']=hotel_ex['rooms'].copy()

##ordino gli hotel in base alla disponibilità delle stanze
##parto da quello con più stanze
hotel_ex=hotel_ex.sort_values(by='stanze_disponibili', ascending=False)

##creo il dizionario per i guadagni degli hotel
guadagni_hotel={hotel: 0 for hotel in hotel_ex['hotel']}

from modu import stats
ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()

##loop per gli ospiti ordinati dal primo all'ultimo
for _, guest_row in guest_ex.iterrows():
    guest=guest_row['guest']
    discount=guest_row['discount']
    ##preferenze degli ospiti
    preferenze_ospite=preferences_ex[preferences_ex['guest']==guest]
    ##stanze disponibili tra le preferenze del cliente negli hotel che hannoa almeno una stanza disponibile
    hotels_preferiti=preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili']>0]['hotel'])]
    if not hotels_preferiti.empty:
        ##cerco di allocare l'ospite nell'hotel preferrito che ha più stanze disponibili
        ## merge è come un join in sql e ci serve in questo caso per unire due colonne che hanno in comune la colonna hotel in modo tale che la scelta possa essere fatta in base alla richiesta specificata prima
        hotels_preferiti=hotels_preferiti.merge(hotel_ex[['hotel', 'stanze_disponibili']], on='hotel').sort_values(by='stanze_disponibili', ascending=False)
        ##seleziono il primo hotel preferito con più disponibilità di stanze
        hotel_selezionato=hotels_preferiti.iloc[0]['hotel']
        ospiti_soddisfatti += 1 
    else:
        continue
    
    ##prezzo dell'hotel selzionato
    prezzo_hotel=hotel_ex[hotel_ex['hotel']== hotel_selezionato].iloc[0]['price']
    ##calcolo lo sconto
    prezzo_finale=prezzo_hotel*(1-discount)
    
    ##aggiungo l'allocazione alla lista
    allocazioni.append({
        'cliente':guest,
        'hotel_f':hotel_selezionato,
        'prezzo_pagato':prezzo_finale
    })
    ##riduco il numero di stanze disponibili
    indice_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].index
    hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -= 1
    ##aggiorno le statistiche delle variabili
    ospiti_allocati += 1
    guadagni_hotel[hotel_selezionato] += prezzo_finale
    stanze_occupate += 1 
    hotel_occupati.add(hotel_selezionato)
    ##se non ci sono stanze disponibili interrompere il loop
    if hotel_ex['stanze_disponibili'].sum() ==0:
        print('Tutte le stanze sono occupate')
        break

allocazioni_df_4 = pd.DataFrame(allocazioni)
##Risultati finali
numero_hotel_occupati = len(hotel_occupati)
print(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Numero di ospiti soddisfatti: {ospiti_soddisfatti}')
##Guadagni totali di ogni hotel
guadagni_df_4 = pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno totale'])
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df_4)
##Allocazioni finali
print('\nAllocazioni degli ospiti:')
print(allocazioni_df_4)