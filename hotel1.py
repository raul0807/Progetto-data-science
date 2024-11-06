import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

# prendiamo i file Excel 
hotel_ex = pd.read_excel("/Users/raulspano/Desktop/progetto hotel/hotels.xlsx")
guest_ex = pd.read_excel('/Users/raulspano/Desktop/progetto hotel/guests.xlsx')
preferences_ex = pd.read_excel('/Users/raulspano/Desktop/progetto hotel/preferences.xlsx')

##creiamo una colonna che rappresenta le stanze disponibili
hotel_ex['stanze_disponibili'] = hotel_ex['rooms'].copy()

##creiamo un dizionario per tracciare i guadagni per ogni hotel
guadagni_hotel={hotel: 0 for hotel in hotel_ex['hotel']}

##variabili per le statistiche
ospiti_allocati=0
stanze_occupate=0
hotel_occupati=set()
ospiti_soddisfatti=0

##creiamo una lista in cui possiamo aggiungere le allocazioni
allocazioni=[]

for _, guest_row in guest_ex.iterrows():
    guest=guest_row['guest']
    discount=guest_row['discount']
    ##dobbiamo prendere in considerazione le preferenze dell'ospite
    preferenze_ospite=preferences_ex[preferences_ex['guest']== guest]
    ##dobbiamo trovare stanze disponibili nelle preferenze del cliente
    hotels_preferiti=preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili']>0]['hotel'])]
    if not hotels_preferiti.empty:
        ## se ci sono preferenze disponibili selezionarne una casualmente
        hotel_selezionato= np.random.choice(hotels_preferiti['hotel'])
        ospiti_soddisfatti += 1 ##vuol dire che l'ospite ha ottenuto un hotel preferito
    else:
        ## se non ci sono preferenze valide seleziona un hotel a caso tra quelli con stanze disponibili
        hotels_disponibili=hotel_ex[hotel_ex['stanze_disponibili']>0]
        if hotels_disponibili.empty:
            print('Non ci sono hotel disponibili')
            continue ##se non ci sono hotel disponibili passa al prossimo ospite
        ##selezioniamo casualmente un hotel disponibile
        hotel_selezionato= np.random.choice(hotels_disponibili['hotel'])
    
    ##recuperare il prezzo dell'hotel selezionato
    prezzo_hotel= hotel_ex[hotel_ex['hotel']==hotel_selezionato].iloc[0]
    price=prezzo_hotel['price']
    
    #calcoliamo lo sconto
    prezzo_finale= price*(1-discount)
    
    #salviamo le allocazioni
    allocazioni.append({
        'cliente':guest,
        'hotel_f': hotel_selezionato,
        'prezzo_pagato': prezzo_finale
    })
    
    ##dobbiamo ovviamente ridurre il numero di stanze disponibili nell'hotel
    indice_hotel=hotel_ex[hotel_ex['hotel']==hotel_selezionato].index
    hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -=1
    
    ##dobbiamo aggiornare le statistiche
    ospiti_allocati += 1
    stanze_occupate +=1
    hotel_occupati.add(hotel_selezionato)
    guadagni_hotel[hotel_selezionato] += prezzo_finale

##creiamo un dataframe dalle allocazionni
allocazioni_df= pd.DataFrame(allocazioni)        

##calcoliamo il risultato finale
numero_hotel_occupati= len(hotel_occupati)
print(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
print(f'Numero di stanze occupate: {stanze_occupate}')
print(f'Numero di hotel occupati: {numero_hotel_occupati}')
print(f'Ospiti soddisfatti: {ospiti_soddisfatti}')

##calcoliamo i guadagni totali
guadagni_df= pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno Totale'])
print('\nGuadagni totali di ogni hotel:')
print(guadagni_df)

plt.figure(figsize=(6, 4))
plt.bar(['Ospiti Soddisfatti', 'Ospiti Non Soddisfatti'], [ospiti_soddisfatti, ospiti_allocati - ospiti_soddisfatti], color=['green', 'red'])
plt.ylabel('Numero di Ospiti')
plt.title('Soddisfazione degli Ospiti')
plt.show()
##qui utilizzo un grafico per mostrare quanti ospiti sono soddisfatti rispetto a quelli che non lo sono