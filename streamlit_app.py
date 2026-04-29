import math
import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit_geolocation import streamlit_geolocation

ICON_URL = "https://static.prod-images.emergentagent.com/jobs/0ea31682-e703-443e-9b36-d0c5d54ebbbd/images/ea8e3ff600ec402be743ac5a217eaf9a3a8bdf739042fabaae3f65025a2120ed.jpeg"

st.set_page_config(page_title="Essence Pas Chère", page_icon=ICON_URL)

def inject_ios_icon():
    components.html(f"""
    <script>
        var link = window.parent.document.createElement('link');
        link.rel = 'apple-touch-icon';
        link.href = '{ICON_URL}';
        window.parent.document.head.appendChild(link);
    </script>
    """, height=0)

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif !important; background-color: #F2F2F7 !important; }
.block-container { max-width: 480px !important; padding: 0.5rem 1rem !important; }
#MainMenu, footer, header { display: none !important; }
.app-header { background: linear-gradient(135deg, #34C759 0%, #F5C518 100%); border-radius: 0 0 20px 20px; padding: 15px; margin: -0.5rem -1rem 15px -1rem; color: white; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; }
.app-header img { width: 50px; height: 50px; border-radius: 12px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
.app-header h1 { font-size: 22px !important; margin: 0 !important; color: white !important; }
.gps-box { background: white; border-radius: 12px; padding: 12px; margin-bottom: 15px; text-align: center; border: 1px solid #E5E5EA; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.station-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #8E8E93; position: relatius; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.station-card.best { border-left-color: #34C759; }
.best-badge { position: absolute; top: 0; right: 0; background: #34C759; color: white; font-size: 9px; font-weight: 800; padding: 2px 8px; border-radius: 0 12px 0 8px; }
.price { font-size: 26px; font-weight: 900; color: #1C1C1E; }
.price.green { color: #34C759; }
.action-btn { display: block; width: 100%; text-align: center; padding: 10px; border-radius: 8px; text-decoration: none !important; font-size: 14px; font-weight: 700; color: white !important; background: linear-gradient(135deg, #34C759 0%, #30B350 100%); margin-top: 12px; }
</style>
""", unsafe_allow_html=True)

def fetch_stations(lat, lon, radius_km, fuel_label):
    fuel_key = fuel_label.lower().replace("-","_") + "_prix"
    API_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records"
    params = {"select": f"adresse,ville,cp,geom,{fuel_key}", "where": f"distance(geom, geom'POINT({lon} {lat})', {radius_km}km) AND {fuel_key} is not null", "order_by": f"{fuel_key} asc", "limit": 20}
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        return resp.json().get("results", [])
    except: return []

def main():
    inject_ios_icon()
    inject_css()
    st.markdown(f'<div class="app-header"><img src="{ICON_URL}"><h1>Essence Pas Chère</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="gps-box"><b>📍 Localisation GPS</b>', unsafe_allow_html=True)
    loc = streamlit_geolocation()
    if loc and loc.get('latitude'):
        user_lat, user_lon = loc['latitude'], loc['longitude']
        st.markdown('<p style="color:green; font-weight:600; margin:5px 0 0 0">✅ Position détectée</p>', unsafe_allow_html=True)
    else:
        user_lat, user_lon = 47.90296, 1.90925
        st.markdown('<p style="color:#FF9500; font-size:13px; margin:5px 0 0 0">👆 Cliquez sur l\'icône cible pour vous localiser</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])
    with col1: fuel = st.selectbox("Carburant", ["Gazole", "SP95", "SP95-E10", "SP98", "E85", "GPLc"])
    with col2: radius = st.number_input("Rayon (km)", 1, 50, 5)
    raw = fetch_stations(user_lat, user_lon, radius, fuel)
    if not raw: st.warning("Aucune station trouvée."); return
    for i, r in enumerate(raw):
        price = r.get(fuel.lower().replace("-","_") + "_prix")
        is_best = i == 0
        gmaps = f"https://www.google.com/maps/dir/?api=1&destination={r['geom']['lat']},{r['geom']['lon']}"
        badge = '<div class="best-badge">🏆 MEILLEUR PRIX</div>' if is_best else ""
        html = f"""<div class="station-card {'best' if is_best else ''}">{badge}<div style="display:flex;justify-content:space-between;align-items:center"><div><b style="font-size:15px">{r['adresse']}</b><br><span style="font-size:12px;color:#8E8E93">{r['cp']} {r['ville']}</span></div><div class="price {'green' if is_best else ''}">{price:.3f}<small style="font-size:10px">€/L</small></div></div><a href="{gmaps}" target="_blank" class="action-btn">📍 Itinéraire Google Maps</a></div>"""
        st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__": main()
