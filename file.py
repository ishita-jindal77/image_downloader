import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

# Function to scrape Google Images and download them
def download_images(query, num_images):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')
    
    if not os.path.exists('downloaded_images'):
        os.makedirs('downloaded_images')

    images_downloaded = 0
    
    for i, img_tag in enumerate(image_tags[1:]):  # Skip the first image (Google logo)
        try:
            img_url = img_tag['src']
            img_response = requests.get(img_url)
            img = Image.open(BytesIO(img_response.content))
            img.save(f"downloaded_images/{query}_{i+1}.jpg")
            images_downloaded += 1
            if images_downloaded >= num_images:
                break
        except Exception as e:
            st.error(f"Error downloading image {i+1}: {e}")
            continue

    return images_downloaded

# Streamlit UI
st.title("Google Images Downloader")

query = st.text_input("Enter the type of images you want:")
num_images = st.number_input("Enter the number of images:", min_value=1, max_value=100, value=10)

if st.button("Download"):
    if query:
        with st.spinner(f"Downloading {num_images} images of {query}..."):
            images_downloaded = download_images(query, num_images)
            if images_downloaded > 0:
                st.success(f"Successfully downloaded {images_downloaded} images!")
                st.balloons()
            else:
                st.error("Failed to download images. Try again.")
    else:
        st.warning("Please enter a search query.")

# Display images in the Streamlit app (optional)
if os.path.exists('downloaded_images'):
    st.subheader("Downloaded Images")
    for img_file in os.listdir('downloaded_images'):
        img_path = os.path.join('downloaded_images', img_file)
        img = Image.open(img_path)
        st.image(img, caption=img_file)