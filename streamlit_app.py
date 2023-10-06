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

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  # This will give it in array 
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  # Show in df
  return fruityvice_normalized

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
    back_from_function = get_fruityvice_data(fruit_choice)
    sl.dataframe(back_from_function)
except URLError as e:
  sl.error()
  
sl.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

if sl.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  sl.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('" + new_fruit + "')")
      return 'Thanks for adding ' + new_fruit

add_my_fruit = sl.text_input('What fruit would you like to add')

if sl.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  sl.text(back_from_function)




