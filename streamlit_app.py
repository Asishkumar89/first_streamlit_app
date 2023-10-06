import streamlit as sl
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
sl.title("My Parents New Healthy Diner")
sl.header('Breakfast Favorites')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free Range Egg')
sl.text('🥑🍞 Avocado toast')
sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = sl.multiselect("Pick some fruits:", list (my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

sl.header('Fruityvice Fruit Advice')
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  if not fruit_choice:
    sl.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    # This will give it in array 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # Show in df
    sl.dataframe(fruityvice_normalized)
except URLError as e:
  sl.error()
  
#dont run anything past here till we debug
sl.stop()
my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
sl.header("The fruit load list contains:")
sl.dataframe(my_data_rows)
add_my_fruit = sl.text_input('What fruit would you like to add','Jackfruit')
sl.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')")
