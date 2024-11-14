import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from modu import carica_file, stats

# Carica i file una volta sola
hotel_ex, guest_ex, preferences_ex = carica_file()

# Definisci le funzioni per ciascun modulo
def random():
    st.title("Allocazioni e guadagni random")
    
    # Copia il blocco di codice del primo modulo
    hotel_ex['stanze_disponibili'] = hotel_ex['rooms'].copy()
    guadagni_hotel = {hotel: 0 for hotel in hotel_ex['hotel']}
    ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()
    
    for _, guest_row in guest_ex.iterrows():
        guest = guest_row['guest']
        discount = guest_row['discount']
        hotels_disponibili = hotel_ex[hotel_ex['stanze_disponibili'] > 0]
        if hotels_disponibili.empty:
            st.write('Non ci sono hotel disponibili')
            continue
        hotel_selezionato = np.random.choice(hotels_disponibili['hotel'])
        preferenze_ospite = preferences_ex[preferences_ex['guest'] == guest]
        if hotel_selezionato in preferenze_ospite['hotel'].values:
            ospiti_soddisfatti += 1
        prezzo_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].iloc[0]
        prezzo_finale = prezzo_hotel['price'] * (1 - discount)
        allocazioni.append({
            'cliente': guest,
            'hotel_f': hotel_selezionato,
            'prezzo_pagato': prezzo_finale
        })
        indice_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].index
        hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -= 1
        ospiti_allocati += 1
        stanze_occupate += 1
        hotel_occupati.add(hotel_selezionato)
        guadagni_hotel[hotel_selezionato] += prezzo_finale

    allocazioni_df = pd.DataFrame(allocazioni)
    guadagni_df = pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno Totale'])
    st.write(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
    st.write(f'Numero di stanze occupate: {stanze_occupate}')
    st.write(f'Numero di hotel occupati: {len(hotel_occupati)}')
    st.write(f'Ospiti soddisfatti: {ospiti_soddisfatti}')
    st.subheader("Guadagni totali per ogni hotel")
    st.dataframe(guadagni_df)
    st.subheader("Allocazioni degli ospiti")
    st.dataframe(allocazioni_df)

    fig, ax = plt.subplots()
    ax.pie([ospiti_soddisfatti, len(guest_ex) - ospiti_soddisfatti], labels=['Ospiti soddisfatti', 'Ospiti non soddisfatti'], colors=['green', 'red'], autopct='%1.1f%%')
    ax.set_title('Soddisfazione degli Ospiti')
    st.pyplot(fig)

def customer_preference():
    st.title("Allocazione e guadagni in base alle preferenze degli ospiti")
    
    # Copia il blocco di codice del secondo modulo
    hotel_ex['stanze_disponibili'] = hotel_ex['rooms'].copy()
    guadagni_hotel = {hotel: 0 for hotel in hotel_ex['hotel']}
    ospiti_allocati, stanze_occupate, hotel_occupati, ospiti_soddisfatti, allocazioni = stats()
    
    for _, guest_row in guest_ex.iterrows():
        guest = guest_row['guest']
        discount = guest_row['discount']
        preferenze_ospite = preferences_ex[preferences_ex['guest'] == guest]
        hotels_preferiti = preferenze_ospite[preferenze_ospite['hotel'].isin(hotel_ex[hotel_ex['stanze_disponibili'] > 0]['hotel'])]
        
        if not hotels_preferiti.empty:
            hotel_selezionato = hotels_preferiti.iloc[0]['hotel']
            ospiti_soddisfatti += 1  
        else:
            continue
        
        prezzo_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].iloc[0]
        prezzo_finale = prezzo_hotel['price'] * (1 - discount)
        allocazioni.append({
            'cliente': guest,
            'hotel_f': hotel_selezionato,
            'prezzo_pagato': prezzo_finale
        })
        indice_hotel = hotel_ex[hotel_ex['hotel'] == hotel_selezionato].index
        hotel_ex.loc[indice_hotel, 'stanze_disponibili'] -= 1
        ospiti_allocati += 1
        stanze_occupate += 1
        hotel_occupati.add(hotel_selezionato)
        guadagni_hotel[hotel_selezionato] += prezzo_finale
    
    allocazioni_df_2 = pd.DataFrame(allocazioni)
    guadagni_df_2 = pd.DataFrame(list(guadagni_hotel.items()), columns=['Hotel', 'Guadagno Totale'])
    st.write(f'Numero di ospiti che hanno ottenuto una camera: {ospiti_allocati}')
    st.write(f'Numero di stanze occupate: {stanze_occupate}')
    st.write(f'Numero di hotel occupati: {len(hotel_occupati)}')
    st.write(f'Ospiti soddisfatti: {ospiti_soddisfatti}')
    st.subheader("Guadagni totali per ogni hotel")
    st.dataframe(guadagni_df_2)
    st.subheader("Allocazioni degli ospiti")
    st.dataframe(allocazioni_df_2)

    fig, ax = plt.subplots()
    ax.pie([ospiti_soddisfatti, len(guest_ex) - ospiti_soddisfatti], labels=['Ospiti soddisfatti', 'Ospiti non soddisfatti'], colors=['green', 'red'], autopct='%1.1f%%')
    ax.set_title('Soddisfazione degli Ospiti')
    st.pyplot(fig)

# Selettore di modulo
metodo_selezionato = st.selectbox("Seleziona il metodo da visualizzare", ("random", "customer_preference"))

# Visualizza il modulo selezionato
if metodo_selezionato == "random":
    random()
elif metodo_selezionato == "customer_preference":
    customer_preference()
