import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize the geolocator
# We use a unique user_agent to comply with Nominatim's usage policy
geolocator = Nominatim(user_agent="my_cool_geocoder_app")

st.set_page_config(page_title="Uriv GeoPredictor Pro", page_icon="📍")

st.title("📍 GeoPredictor Pro")
st.markdown("Convert addresses to coordinates and vice versa instantly.")

# Create two tabs for a cleaner UI
tab1, tab2 = st.tabs(["Address ➡ Coordinates", "Coordinates ➡ Address"])

# --- TAB 1: GEOCODING ---
with tab1:
    st.header("Search by Address")
    address_input = st.text_input("Enter a full address:", placeholder="e.g., 1600 Amphitheatre Pkwy, Mountain View, CA")
    
    if st.button("Find Coordinates"):
        if address_input:
            try:
                location = geolocator.geocode(address_input)
                if location:
                    st.success(f"**Found it!**")
                    st.write(f"**Latitude:** {location.latitude}")
                    st.write(f"**Longitude:** {location.longitude}")
                    # Display on a map
                    st.map({"lat": [location.latitude], "lon": [location.longitude]})
                else:
                    st.error("Sorry, we couldn't find that location. Try being more specific.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter an address first.")

# --- TAB 2: REVERSE GEOCODING ---
with tab2:
    st.header("Search by Coordinates")
    col1, col2 = st.columns(2)
    with col1:
        lat_input = st.number_input("Latitude", format="%.6f", value=0.0)
    with col2:
        lon_input = st.number_input("Longitude", format="%.6f", value=0.0)
    
    if st.button("Find Address"):
        if lat_input != 0.0 or lon_input != 0.0:
            try:
                # Format: "Latitude, Longitude"
                coord_str = f"{lat_input}, {lon_input}"
                location = geolocator.reverse(coord_str)
                if location:
                    st.success("**Address Found:**")
                    st.info(location.address)
                    st.map({"lat": [lat_input], "lon": [lon_input]})
                else:
                    st.error("No address found for these coordinates.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter valid coordinates.")

st.divider()
st.caption("Powered by OpenStreetMap & Geopy")