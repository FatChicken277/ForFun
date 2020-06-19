#!/usr/bin/python3

"""This module contains some functions to print a pokemon using web scrapping.
"""

import requests
from bs4 import BeautifulSoup

"""DOMAIN"""

DOMAIN = "https://pokemondb.net"

"""FONT COLORS AND STYLES"""

COLORS = {
    "red": "\033[91m",
    "h_red": "\033[38;5;196m",
    "orange": "\033[38;5;166m",
    "yellow": "\033[38;5;226m",
    "green": "\033[38;5;28m",
    "h_green": "\033[38;5;46m",
    "blue": "\033[38;5;45m",
    "black": "\033[90m",
    "white": "\033[97m"
}

STYLES = {
    "dim": "\033[2m",
    "bold": "\033[1m",
    "reset": "\033[0m",
    "clear": chr(27)+'[2j' + '\033c' + '\x1bc'
}


def PrintWelcome():
    """PRINT WELCOME MESSAGE"""

    print(STYLES["clear"])
    print('''{}
                  ░▒▒█████████▒▒░
               ░██               ██░
            ░██                     ██░
         ░██                           ██░
       ░██                               ██░
     ░██                                   ██░
    ░██                                     ██░
   ░██                                       ██░
  ░██                  {}░███░{}                  ██░{}
  ░██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█     █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░
  ░██░░░░░░░░░░░░░░░░█       █░░░░░░░░░░░░░░░░██░
  ░██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█     █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░{}
  ░██                  {}░███░{}                  ██░
   ░██                                       ██░
    ░██                                     ██░
     ░██                                   ██░
       ░██                               ██░
         ░██                           ██░
            ░██                     ██░
               ░██               ██░
                  ░▒▒█████████▒▒░{}

          ! Welcome to Scrapped Pokedex ¡
                   '''.format(COLORS["red"], COLORS["black"],
                              COLORS["red"], COLORS["black"],
                              COLORS["white"], COLORS["black"],
                              COLORS["white"], STYLES["reset"]))


def Menu(limit, name):
    """SELECTION MENU"""

    PrintWelcome()
    choice = input(
        "Find Pokemons by:\n\n  1. Limit.\n  2. Name.\n  3. Exit.\n\n-> ")
    if choice == "1":
        limit = int(input("\nChoice a limit: "))
    elif choice == "2":
        name = input("\nEnter a pokemon name: ")
    elif choice == "3":
        name = print("\nSee you later :D\n")
        exit(0)
    else:
        print("\nInvalid option\n")
        exit(1)
    print(STYLES["clear"])
    return limit, name, choice


def WebConnection(sub_page=""):
    """CONNECT TO WEBSITE"""

    response = requests.get(DOMAIN + sub_page)
    if response.status_code != 200:
        raise SystemExit("Could not connect satisfactorily to the website")
    return response


def RankColor(cstr):
    """RANKS COLORS"""

    rank = int(cstr[-1])
    menu = ["h_red", "orange", "yellow", "green", "h_green", "blue"]
    rank_colop = menu[rank-1]
    color = COLORS[rank_colop]
    return color


def Graphic(porcent, color=STYLES["reset"]):
    """STATS GRAPHIC"""

    graph = ["░░"*10, "▒░", "██"]
    result = ""

    while porcent != 0:
        if porcent - 10 >= 0:
            result += graph[2]
            porcent -= 10
        else:
            result += graph[1]
            porcent -= porcent
    result += graph[0]

    return STYLES["dim"] + color + result[:20] + STYLES["reset"]


def PokemonCheckSubName(pokemon_sub_name, pokemon_soup):
    """CHECK IF POKEMON HAVE SUB NAME"""

    if pokemon_sub_name is not None:
        pokemon_ids = pokemon_soup.find("div", class_="tabs-tab-list")
        for pokemon_id in pokemon_ids.find_all("a"):
            if pokemon_sub_name.text == pokemon_id.text:
                pokemon_id = "tab-basic-"+pokemon_id["href"].split("-")[-1]
                pokemon_soup = pokemon_soup.find("div", id=pokemon_id)

    return pokemon_soup


def PokemonData(pokemon_soup, pokemon_sub_name):
    """GETS THE RELEVANT POKEMON DATA"""

    if pokemon_sub_name is None:
        pokemon_info = pokemon_soup.find("div", class_="tabs-panel-list")
    else:
        pokemon_info = pokemon_soup
    pokemon_data = pokemon_info.find("div",
                                     class_="grid-col span-md-6 span-lg-4")
    data_table = pokemon_data.find("table", class_="vitals-table").tbody
    table_row = data_table.find_all("tr", limit=3)
    pokemon_numb = table_row[0].td.strong.text
    pokemon_type = ", ".join(
        [typ.text for typ in table_row[1].td.find_all("a")])
    pokemon_specie = table_row[2].td.text

    return pokemon_numb, pokemon_type, pokemon_specie


def PrintPokemonName(name, sub_name):
    """PRINT POKEMON NAME"""

    print("\n{}{}[*] {}{}".format(STYLES["bold"], COLORS["red"], name,
                                  STYLES["reset"]))
    if sub_name is not None:
        print("    {}({}){}\n".format(STYLES["dim"], sub_name.text,
                                      STYLES["reset"]))
    else:
        print()


def PrintPokemonProperty(tittle, content):
    """PRINT A POKEMON PROPERTY"""

    print("  {}[+] {}:{}".format(COLORS["red"], tittle, STYLES["reset"]),
          end="")
    print("\t{}".format(content))


def PrintPokemonStats(pokemon_soup):
    """PRINT POKEMON STATS"""

    pokemon_stats = pokemon_soup.find("div",
                                      class_="grid-col span-md-12 span-lg-8")
    stats_table = pokemon_stats.find("table", class_="vitals-table").tbody
    print("  {}[+] Stats:{}\n".format(COLORS["red"], STYLES["reset"]))
    for stats_row in stats_table.find_all("tr"):
        stat_name = stats_row.find("th").text
        stat_columns = stats_row.find_all("td")
        stat_value = stat_columns[0].text
        porcent = (int(stat_value) / 180) * 100
        color = RankColor(stat_columns[1].div["class"][1])

        print("   {}[.]{} {}:\t{}| {}".format(
            STYLES["dim"], STYLES["reset"], stat_name,
            Graphic(int(porcent), color), stat_value))


def Pokemon():
    """PRINT POKEMON"""

    limit = 0
    name = ""
    limit, name, choice = Menu(limit, name)

    pokemons_subpage = "/pokedex/all"
    pokemons_html = WebConnection(pokemons_subpage).text
    pokemons_soup = BeautifulSoup(pokemons_html, "html.parser")
    pokedex_table = pokemons_soup.find("table", id="pokedex").tbody

    find = 0
    for row in pokedex_table.find_all("tr", limit=limit):
        column = row.find_all("td")

        pokemon_name = column[1].a.text
        if (name == pokemon_name or choice == "1"):
            find = 1
            pokemon_sub_name = column[1].small
            pokemon_href = column[1].a["href"]
            pokemon_html = WebConnection(pokemon_href).text
            pokemon_soup = BeautifulSoup(pokemon_html, "html.parser")

            pokemon_soup = PokemonCheckSubName(pokemon_sub_name, pokemon_soup)

            pokemon_numb, pokemon_type, pokemon_specie = PokemonData(
                pokemon_soup, pokemon_sub_name)

            print("="*50)
            PrintPokemonName(pokemon_name, pokemon_sub_name)
            PrintPokemonProperty("Number", pokemon_numb)
            PrintPokemonProperty("Type", pokemon_type)
            PrintPokemonProperty("Specie", pokemon_specie)
            print()
            PrintPokemonStats(pokemon_soup)
            print()

    if find == 0:
        print("\nPokemon not found!\n")
        exit(1)
    print("="*50)


if __name__ == "__main__":
    Pokemon()
