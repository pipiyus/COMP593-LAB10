'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
from image_lib import download_image, save_image_file
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    poke_info = download_pokemon_artwork("pikachu")
    print(poke_info)
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

# TODO: Define function that gets a list of all Pokemon names from the PokeAPI
def get_pokemon_names():
    """Gets a list of all Pokemon names from the PokeAPI.

    Returns:
        list: List of Pokemon names, if successful. Otherwise None.
    """
    # Send GET request for Pokemon list
    print('Getting list of all Pokemon names...', end='')
    
    url = POKE_API_URL + "?limit=100000&offset=0"
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return list of Pokemon names
         # Get JSON data
        data = resp_msg.json()
        
        # Extract names of Pokémon
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        
        
        return pokemon_names
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

# TODO: Define function that downloads and saves Pokemon artwork
def download_pokemon_artwork(pokemon):
    """Downloads and saves the official artwork for a specified Pokemon.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        bool: True, if successful. False, if unsuccessful.
    """
    # Get Pokemon info
    poke_info = get_pokemon_info(pokemon)
    
    # Check if Pokemon info was retrieved
    if poke_info is None:
        return False

    # Get the URL of the official artwork
    artwork_url = poke_info['sprites']['other']['official-artwork']['front_default']

    # Download the image
    image_data = download_image(artwork_url)

    # Check if image was downloaded successfully
    if image_data is None:
        return False

    # Save the image file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'images')
    image_path = os.path.join(images_dir, f'{pokemon}.png')
    save_image_file(image_data, image_path)
    return image_path

if __name__ == '__main__':
    main()