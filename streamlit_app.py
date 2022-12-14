import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(chosen_fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    return pandas.json_normalize(fruityvice_response.json())

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input("What fruit would you like information about?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        data_from_fruityvice = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(data_from_fruityvice)
except URLError as e:
    streamlit.error()

#snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()

def insert_fruit(fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('"+ fruit +"')")
        return "Thanks for adding " + fruit

if streamlit.button("Load fruit list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_list = get_fruit_load_list()
    streamlit.dataframe(my_data_list)
    my_cnx.close()

add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add fruit'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_added_fruit_msg = insert_fruit(add_my_fruit)
    streamlit.text(my_added_fruit_msg)
    my_cnx.close()
