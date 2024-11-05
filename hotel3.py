import pandas as pd

hotel_ex=pd.read_excel('/Users/raulspano/Desktop/progetto hotel/hotels.xlsx')
guest_ex=pd.read_excel('/Users/raulspano/Desktop/progetto hotel/guests.xlsx')
preferences_ex=pd.read_excel('/Users/raulspano/Desktop/progetto hotel/preferences.xlsx')

##creo colonna che rappresenta le stanze disponibili, la chiamo stanze_disponibili e ci inserisco tutte le stenze che sonon nella colonna rooms copiandola
hotel_ex['stanze_disponibili']=hotel_ex['rooms'].copy()

##ordino gli hotel in base al prezzo crescente
hotel_ex=hotel_ex.sort_values(by='price')

## creo un dizionario per i guadagni di ogni hotel
guadagni_hotel= {hotel: 0 for hotel in hotel_ex['hotel']}

## creo le variabili per i risultati che voglio
ospiti_allocati=0
stanze_occupate=0
hotel_occupati=set()
ospiti_soddisfatti=0

##lista per le allocazioni
allocazioni=[]

## loop per gli ospiti in ordine dal primo all'ultimo
for _, guest_row in guest_ex.iterrows():
    guest=guest_row['guest']
    discount=guest_row['discount']
    
    ##preferenze ospiti
    preferenze_ospite = preferences_ex[preferences_ex['guest'] == guest]
    
    ##trovo le stan<e disponibili nelle preferenze del cliente cercando l'hotel più economico
    ## grazie ad isin posso selezionare gli hotel con almeno una stanza libera tra quelli nelle preferenze, inoltre li avevo gia ordinati in base al prezzo grazie a sort
    hotels_preferiti=preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili']>0]['hotel'])]
    
    if not hotels_preferiti.empty:
        ## ordino i preferiti in base al prezzo crescente
        hotels_preferiti=hotels_preferiti.merge(hotel_ex[['hotel', 'price']], on='hotel').sort_values(by='price')
        ##seleziono il primo hotel con disponibilità in base al meno costoso
        hotel_selezionato=hotels_preferiti.iloc[0]['hotel']
        ospiti_soddisfatti += 1
    else:
        ##se non ci sono preferenze valide skippiamo il cliente e non viene allocato
        continue
    ##prendo il prezzp dell'hotel selezionato e calcolo lo sconto
    prezzo_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].iloc[0]['price']
    prezzo_finale=prezzo_hotel*(1-discount)
    
    ##aggiungo l'allocazione alla lista
    allocazioni.append({
        'cliente':guest,
        'hotel_f':hotel_selezionato,
        'prezzo_pagato':prezzo_finale
    })
    ##riduco le stanze disponibili
    indice_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].index
    hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -=1
    
    ##aggiorno le statistiche
    ospiti_allocati+=1
    stanze_occupate+=1
    hotel_occupati.add(hotel_selezionato)
    guadagni_hotel[hotel_selezionato] += prezzo_finale
    
    ## se non ci sono stanze disponibili in tutti gli hotel interrompo il loop
    if hotel_ex['stanze_disponibili'].sum()==0:
        print('Stanze sold out')
        break

##creo il dataframe
allocazioni_df_3 = pd.DataFrame(allocazioni)

numero_hotel_occupati= len(hotel_occupati)
print(f'Nuero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')

guadagni_df_3=pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno Totale'])
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df_3)

print('\nAllocazioni degli ospiti:')
print(allocazioni_df_3)