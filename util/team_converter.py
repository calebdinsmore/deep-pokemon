import sys
import re


# NICKNAME|SPECIES|ITEM|ABILITY|MOVES|NATURE|EVS|GENDER|IVS|SHINY|LEVEL|HAPPINESS,POKEBALL,HIDDENPOWERTYPE
class Pokemon:
    def __init__(self):
        self.nickname = ''
        self.species = ''
        self.item = ''
        self.ability = ''
        self.moves = []
        self.nature = ''
        self.evs = []
        self.gender = ''
        self.ivs = []
        self.shiny = ''
        self.level = ''
        self.happiness = ''
        self.poke_ball = ''
        self.hidden_power_type = ''

    @property
    def packed(self):
        moves = ','.join(self.moves) if self.moves else ''
        evs = ','.join(self.evs) if self.evs else ''
        ivs = ','.join(self.ivs) if self.ivs else ''
        return f'{self.nickname}|{self.species}|{self.item}|{self.ability}|{moves}|{self.nature}|{evs}|{self.gender}|{ivs}|{self.shiny}|{self.level}|{self.happiness},{self.poke_ball},{self.hidden_power_type}'


def main():
    print('Paste team from Pokemon Showdown (Ctrl-D when complete)')
    team = sys.stdin.readlines()

    pokemon_lines = []
    packed_teams = []
    for line in team:
        if line.strip() != '':
            pokemon_lines.append(line)
        else:
            poke = process_pokemon(pokemon_lines)
            packed_teams.append(poke.packed)
            pokemon_lines = []
    print(']'.join(packed_teams))


def process_pokemon(pokemon_lines):
    new_poke = Pokemon()
    name, species, gender, item = name_species_gender_item(pokemon_lines.pop(0))
    new_poke.nickname = name
    new_poke.species = species
    new_poke.gender = gender
    new_poke.item = item

    ability_string = ability(pokemon_lines.pop(0))
    new_poke.ability = ability_string

    next_line = pokemon_lines.pop(0)
    if 'shiny' in next_line.lower():
        shiny_val = shiny_value(next_line)
        new_poke.shiny = shiny_val
        ev_array = evs_array(pokemon_lines.pop(0))
        new_poke.evs = ev_array
    else:  # EVs
        ev_array = evs_array(next_line)
        new_poke.evs = ev_array

    nature_string = nature(pokemon_lines.pop(0))
    new_poke.nature = nature_string

    next_line = pokemon_lines.pop(0)
    if 'IVs' in next_line:
        iv_array = ivs_array(next_line)
        new_poke.ivs = iv_array
    else:
        move_array = []
        move = get_move(next_line)
        move_array.append(move)
        for move_line in pokemon_lines:
            move_array.append(get_move(move_line))
        new_poke.moves = move_array
    return new_poke


def name_species_gender_item(name_line):
    match = re.search(r"(\w+)\s(\(\w+\)\s)?(\(\w\)\s)?@", name_line)
    name, species, gender = match.groups()
    name = '' if name is None else name.strip()
    species = '' if species is None else species.strip()
    gender = '' if gender is None else gender.strip()
    parens = ['(', ')']
    species = remove_chars(parens, species)
    gender = remove_chars(parens, gender)

    # if species is actually gender
    if len(species) == 1:
        gender = species
        species = ''

    match = re.search(r'@\s(.*)', name_line)
    item, = match.groups()
    item = lowercase_smoosh(item.strip())
    return name, species, gender, item


def ability(ability_line):
    match = re.search(r'Ability:\s(.*)', ability_line)
    ability_string, = match.groups()
    ability_string = lowercase_smoosh(ability_string.strip())
    return ability_string


def shiny_value(shiny_line):
    match = re.search(r'Shiny:\s(.*)', shiny_line)
    shiny_string, = match.groups()
    shiny_string = lowercase_smoosh(shiny_string.strip())
    value = 'S' if shiny_string == 'yes' else ''
    return value


def evs_array(evs_line):
    # HP, Atk, Def, SpA, SpD, Spe
    match = re.search(r'EVs:\s(.*)', evs_line)
    array = ['', '', '', '', '', '']
    evs_string, = match.groups()
    evs_string = lowercase_smoosh(evs_string)
    evs_split = evs_string.split('/')  # results in ['252atk', '4hp', '252spd']
    for ev_value in evs_split:
        if 'hp' in ev_value:
            array[0] = ev_value.replace('hp', '')
        elif 'atk' in ev_value:
            array[1] = ev_value.replace('atk', '')
        elif 'def' in ev_value:
            array[2] = ev_value.replace('def', '')
        elif 'spa' in ev_value:
            array[3] = ev_value.replace('spa', '')
        elif 'spd' in ev_value:
            array[4] = ev_value.replace('spd', '')
        else:
            array[5] = ev_value.replace('spe', '')
    return array


def nature(nature_line):
    match = re.search(r'(\w+)\sNature', nature_line)
    nature_string, = match.groups()
    nature_string = lowercase_smoosh(nature_string)
    return nature_string


def ivs_array(ivs_line):
    match = re.search(r'IVs:\s(.*)', ivs_line)
    array = ['', '', '', '', '', '']
    ivs_string, = match.groups()
    ivs_string = lowercase_smoosh(ivs_string)
    ivs_split = ivs_string.split('/')  # results in ['252atk', '4hp', '252spd']
    for iv_value in ivs_split:
        if 'hp' in iv_value:
            array[0] = iv_value.replace('hp', '')
        elif 'atk' in iv_value:
            array[1] = iv_value.replace('atk', '')
        elif 'def' in iv_value:
            array[2] = iv_value.replace('def', '')
        elif 'spa' in iv_value:
            array[3] = iv_value.replace('spa', '')
        elif 'spd' in iv_value:
            array[4] = iv_value.replace('spd', '')
        else:
            array[5] = iv_value.replace('spe', '')
    return array


def get_move(move_line):
    move = remove_chars(['-', '\n'], move_line)
    move = lowercase_smoosh(move)
    return move


def remove_chars(chars_to_remove, string):
    for char in chars_to_remove:
        string = string.replace(char, '')
    return string


def lowercase_smoosh(string):
    """
    Some things like items and abilities shouldn't have spaces for some reason
    :param string: string to lowercase and "smoosh" (remove spaces)
    :return: lowercased and smooshed string
    """
    string = string.lower()
    string = string.replace(' ', '')
    return string


if __name__ == '__main__':
    main()
