# Streamlit Beer Pairing App

import streamlit as st
import pandas as pd

# Load the datasets
beer_data = pd.read_csv('beer_recipe.csv')
food_data = pd.read_csv('indian_food.csv')

def suggest_multiple_beer_pairing_with_styles(food_name, beer_data, food_data, num_beers=5):
    if food_name in food_data['name'].values:
        food_details = food_data[food_data['name'] == food_name].iloc[0]
    else:
        return []
    
    suggestions = []
    food_flavor = food_details['flavor_profile']
    if food_flavor == 'spicy':
        suggested_beers = beer_data[beer_data['abv'] > 7.0][['name', 'description']].values.tolist()
        suggestions.extend(suggested_beers[:num_beers])
    elif food_flavor == 'sweet':
        suggested_beers = beer_data[beer_data['abv'] <= 4.5][['name', 'description']].values.tolist()
        suggestions.extend(suggested_beers[:num_beers])
    elif food_flavor == 'sour':
        suggested_beers = beer_data[beer_data['name'].str.contains("Wheat", case=False) | 
                                    beer_data['description'].str.contains("fruity", case=False)][['name', 'description']].values.tolist()
        suggestions.extend(suggested_beers[:num_beers])
    else:
        suggested_beers = beer_data[(beer_data['abv'] > 4.5) & (beer_data['abv'] <= 7.0)][['name', 'description']].values.tolist()
        suggestions.extend(suggested_beers[:num_beers])
    
    return suggestions

# Streamlit App
st.title("Beer Pairing with Indian Food")
selected_food = st.selectbox("Choose a food item:", food_data['name'].unique())
if st.button("Get Beer Pairings"):
    results = suggest_multiple_beer_pairing_with_styles(selected_food, beer_data, food_data)
    for beer_name, beer_description in results:
        st.write(f"**{beer_name}** - {beer_description}")

