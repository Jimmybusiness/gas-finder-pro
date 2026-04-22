import math
import requests
import streamlit as st
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(page_title='Essence Pas Chere', page_icon='⛽')

def main():
    st.title('⛽ Essence Pas Chere')
    loc = streamlit_geolocation()
    if loc and loc.get('latitude'):
        user_lat, user_lon = loc['latitude'], loc['longitude']
        st.success('Position detectee')
    else:
        user_lat, user_lon = 47.90296, 1.90925
        st.info('Localisation par defaut (Orleans)')
    
    fuel = st.selectbox('Carburant', ['Gazole', 'SP95', 'SP95-E10', 'SP98', 'E85', 'GPLc'])
    radius = st.slider('Rayon (km)', 1, 50, 5)
    
    # API logic here (simplified for initial push)
    st.write('Recherche des stations...')

if __name__ == '__main__': main()