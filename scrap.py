from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.set_page_config(
    page_title="Web Scraper App",
    layout="wide",  # Use a wide layout
    initial_sidebar_state="expanded")

url=st.text_input("Enter the URL","https://www.worldometers.info/coronavirus/")

data_type = st.selectbox(
    "Select the type of data to extract",
    ("Links", "Images", "Paragraphs", "Headings"))


@st.cache_data
def get_data(url, data_type):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        if data_type == "Links":
            return [link.get("href") for link in soup.find_all("a", href=True)]
        elif data_type == "Images":
            return [img.get("src") for img in soup.find_all("img")]
        elif data_type == "Paragraphs":
            return [p.text for p in soup.find_all("p")]
        elif data_type == "Headings":
            return [h.text for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    except Exception as e:
        return str(e)
   
if st.button("Scrape"):
    extracted_data = get_data(url, data_type)
    if extracted_data is not None:
        st.subheader(f"Extracted {data_type}:")
        # Display the results in a formatted way
        st.write(extracted_data)