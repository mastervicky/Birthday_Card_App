import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import date
import io

# function to create a growth graph based on the birth year
def create_growth_graph(birth_year):
    current_year = date.today().year
    year = list(range(birth_year, current_year +1))
    ages = [y - birth_year for y in year]

    fig, ax = plt.subplots(figsize = (4, 2))
    ax.plot(year, ages, marker='o', color='blue')
    ax.set_title('Growth Chart')
    ax.set_xlabel('Year')
    ax.set_ylabel('Age')
    ax.grid(True)

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    return Image.open(buf)

# function to create a birthday card
def create_card(name, birth_year, upload_photo=None):
    card = Image.new("RGB", (800, 500), "lightyellow")
    draw = ImageDraw.Draw(card)
    # Font adjustment if needed
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_msg = ImageFont.truetype("arial.ttf", 20)
    except:
        font_title = font_msg = None

    draw.text((50, 50), f"Happy Birthday {name}!", fill="darkred", font=font_title)
    draw.text((50, 120), "Wishing you many more years of joy, good health and success!", fill="black", font=font_msg)

    if upload_photo:
        photo = Image.open(upload_photo).resize((300, 300))
        card.paste(photo, (20, 150))

    chart = create_growth_graph(birth_year).resize((400, 200))
    card.paste(chart, (350, 150))

    return card

# Streamlit Web UI
st.title("Birthday Card Generator")

name = st.text_input("Enter your name")
birth_year = st.number_input("Enter your year of birth", min_value=1900, max_value=date.today().year, value=2000)
photo = st.file_uploader("Upload your photo (JPEG or PNG)", type=["jpg", "jpeg", "png"])

if st.button("Generate Card"):
    if name and photo:
        card = create_card(name, birth_year, photo)
        st.image(card, caption="Your Birthday Card", use_column_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.download_button("Download Card", data=buf.getvalue(), file_name=f"{name}_birthday_card.png", mime="image/png")
    else:
        st.warning("Please enter your name and upload a photo.")