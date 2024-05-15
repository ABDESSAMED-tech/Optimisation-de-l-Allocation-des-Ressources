import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

def main():
    # Set page layout
    st.set_page_config(layout="wide")
    
    # Sidebar
    st.sidebar.title("Solar Panel and Electrical Pole Placement App")
    uploaded_file = st.sidebar.file_uploader("Upload csv file", type=["csv"])
    
    # Main content area
    st.title("Solar Panel and Electrical Pole Placement App")
    st.write("Upload your CSV file on the sidebar to get started.")
    
    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        # Preprocess latitude and longitude data
        df['Latitude'] = df['Latitude'].apply(parse_coordinates)
        df['Longitude'] = df['Longitude'].apply(parse_coordinates)
        
        # Display data
        st.write("Uploaded Data:")
        st.write(df)
        
        # Display map
        st.write("Map:")
        show_map(df)

def parse_coordinates(coord_str):
    parts = coord_str.split('°')
    degrees = float(parts[0])
    minutes = float(parts[1].split("'")[0])
    seconds = float(parts[1].split("'")[1].split('"')[0])
    direction = parts[1].split('"')[1].strip()

    # Calculate decimal degrees
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    
    # Add negative sign for southern and western coordinates
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    
    return decimal_degrees

def show_map(df):
    # Initialize map
    m = folium.Map(location=[30, 0], zoom_start=5, width='100%', height='80vh')
    
    # Marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Plot locations
    for index, row in df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            popup_text = f"Wilaya :{row['Wilayas']} - \n Centrales: {row['Centrales']} \n Superficie: {row['Superficie (Ha)']} Ha"
            folium.Marker(location=[row['Latitude'], row['Longitude']], 
                          popup=folium.Popup(popup_text, parse_html=True)).add_to(marker_cluster)
    
    # Display map
    folium_static(m)

if __name__ == "__main__":
    main()
