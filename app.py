import random
import numpy as np
from flask import Flask, url_for, render_template, redirect, request

app = Flask(__name__)

availablePokemon = [
    {
        'name': 'Charizard',
        'type': 'Fire',
        'moves': {'move1': 'Flamethrower', 'move2': 'Fly', 'move3': 'Blast Burn', 'move4': 'Fire Punch'},
        'EVs': {'ATTACK': 14, 'DEFENSE': 6}
    },
    {
        'name': 'Blastoise',
        'type': 'Water',
        'moves': {'move1': 'Water Gun', 'move2': 'Bubblebeam', 'move3': 'Hydro Pump', 'move4': 'Surf'},
        'EVs': {'ATTACK': 11, 'DEFENSE': 9}
    },
    {
        'name': 'Venusaur',
        'type': 'Grass',
        'moves': {'move1': 'Vine Wip', 'move2': 'Razor Leaf', 'move3': 'Earthquake', 'move4': 'Frenzy Plant'},
        'EVs': {'ATTACK': 7, 'DEFENSE': 13}
    },
    {
        'name': 'Ninetales ',
        'type': 'Fire',
        'moves': {'move1': 'Ember', 'move2': 'Scratch', 'move3': 'Tackle', 'move4': 'Fire Punch'},
        'EVs': {'ATTACK': 13, 'DEFENSE': 7}
    },
    {
        'name': 'Dewgong ',
        'type': 'Water',
        'moves': {'move1': 'Bubblebeam', 'move2': 'Tackle', 'move3': 'Headbutt', 'move4': 'Surf'},
        'EVs': {'ATTACK': 12, 'DEFENSE': 8}
    },
    {
        'name': 'Vileplume ',
        'type': 'Grass',
        'moves': {'move1': 'Vine Wip', 'move2': 'Razor Leaf', 'move3': 'Tackle', 'move4': 'Leech Seed'},
        'EVs': {'ATTACK': 9, 'DEFENSE': 11}

    },
]

game_mode = None
yourPokemonHealth = 0
opponentsPokemonHealth = 0
turn = 0
yourPokemon = None
opponentsPokemon = None
shield_active = False
took_potion = False
yourPokemonHealthDisplay = 0
opponentsPokemonHealthDisplay = 0
opponentsPokemonMove = 0


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/choice', methods=['GET', 'POST'])
def choice():
    global yourPokemonHealth
    global opponentsPokemonHealth
    global turn
    global game_mode
    yourPokemonHealth = 100
    opponentsPokemonHealth = 100
    game_mode = request.form.get('comp_select')
    turn = 0
    if game_mode == "Single player":
        return render_template('choice.html', availablePokemon=availablePokemon)
    elif game_mode == "Hot seats":
        return render_template('choice2.html', availablePokemon=availablePokemon)


@app.route('/choice2', methods=['GET', 'POST'])
def choice2():
    global yourPokemonHealth
    global opponentsPokemonHealth
    global turn
    global game_mode

    return render_template('choice2.html', availablePokemon=availablePokemon)


@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    global yourPokemon
    global opponentsPokemon
    global game_mode
    for pokemon in availablePokemon:
        if pokemon["name"] == request.form.get('comp_select'):
            yourPokemon = pokemon
        else:
            pass
    if game_mode == "Single player":
        opponentsPokemon = random.choice(availablePokemon)
        while yourPokemon["name"] == opponentsPokemon["name"]:
            opponentsPokemon = random.choice(availablePokemon)
    elif game_mode == "Hot seats":
        for pokemon in availablePokemon:
            if pokemon["name"] == request.form.get('comp2_select'):
                opponentsPokemon = pokemon
            else:
                pass
    return render_template('new_game.html',
                           availablePokemon=availablePokemon, yourPokemon=yourPokemon,
                           opponentsPokemon=opponentsPokemon)


@app.route('/game', methods=['GET', 'POST'])
def game():
    global yourPokemon
    global opponentsPokemon
    global yourPokemonHealth
    global opponentsPokemonHealth
    global turn
    global shield_active
    global took_potion
    global yourPokemonHealthDisplay
    global opponentsPokemonHealthDisplay
    yourPokemonHealth = yourPokemonHealth
    opponentsPokemonHealth = opponentsPokemonHealth
    shield_active = False
    took_potion = False
    turn = turn + 1

    yourPokemonHealthDisplay = '=' * yourPokemonHealth
    opponentsPokemonHealthDisplay = '=' * opponentsPokemonHealth
    if yourPokemonHealth <= 0:
        return render_template('result.html', gameWinner=opponentsPokemon["name"])
    if opponentsPokemonHealth <= 0:
        return render_template('result.html', gameWinner=yourPokemon["name"])

    return render_template('game.html', yourPokemon=yourPokemon, yourPokemonHealth=yourPokemonHealth,
                           yourPokemonHealthDisplay=yourPokemonHealthDisplay,
                           opponentsPokemonHealthDisplay=opponentsPokemonHealthDisplay,
                           opponentsPokemon=opponentsPokemon, opponentsPokemonHealth=opponentsPokemonHealth)


@app.route('/attack', methods=['GET', 'POST'])
def attack():
    global yourPokemon
    global opponentsPokemonHealth
    global yourPokemonHealth
    global opponentsPokemon
    global shield_active
    global took_potion
    yourPokemonMove = request.form.get('comp_select')
    if yourPokemonMove == "Shield":
        shield_active = True
    if yourPokemonMove == "Potion":
        if yourPokemonHealth > 40:
            yourPokemonHealth = 50
        else:
            yourPokemonHealth += 10
        took_potion = True
    version = ['Fire', 'Water', 'Grass']
    for i, k in enumerate(version):
        if yourPokemon["type"] == k:
            if opponentsPokemon["type"] == k:
                string_1_attack = 'Its not very effective...'
                string_2_attack = 'Its not very effective...'
            if opponentsPokemon["type"] == version[(i + 1) % 3]:
                string_1_attack = 'Its not very effective...'
                string_2_attack = 'Its super effective!'
                opponentsPokemon["EVs"]["ATTACK"] *= 2
                opponentsPokemon["EVs"]["DEFENSE"] *= 2
            if opponentsPokemon["type"] == version[(i + 2) % 3]:
                string_1_attack = 'Its super effective!'
                string_2_attack = 'Its not very effective...'
                yourPokemon["EVs"]["ATTACK"] *= 2
                opponentsPokemon["EVs"]["DEFENSE"] *= 2

    if shield_active:
        string_1_attack = 'Your pokemon blocked the opponents attack!'
    elif took_potion:
        string_1_attack = 'Your pokemons health increased!'
    else:
        opponentsPokemonHealth = opponentsPokemonHealth - yourPokemon["EVs"]["ATTACK"]

    return render_template('attack.html', yourPokemonMove=yourPokemonMove, yourPokemon=yourPokemon,
                           opponentsPokemon=opponentsPokemon,
                           string_1_attack=string_1_attack, string_2_attack=string_2_attack)


@app.route('/opponents_turn', methods=['GET', 'POST'])
def opponents_turn():
    global yourPokemon
    global opponentsPokemon
    global yourPokemonHealth
    global opponentsPokemonHealth
    global turn
    global shield_active
    global took_potion
    global yourPokemonHealthDisplay
    global opponentsPokemonHealthDisplay
    global game_mode
    yourPokemonHealth = yourPokemonHealth
    opponentsPokemonHealth = opponentsPokemonHealth
    shield_active = False
    took_potion = False

    yourPokemonHealthDisplay = '=' * yourPokemonHealth
    opponentsPokemonHealthDisplay = '=' * opponentsPokemonHealth
    if yourPokemonHealth <= 0:
        return render_template('result.html', gameWinner=opponentsPokemon["name"])
    if opponentsPokemonHealth <= 0:
        return render_template('result.html', gameWinner=yourPokemon["name"])
    if game_mode == "Single player":
        return redirect(url_for('attack2'))
    elif game_mode == "Hot seats":
        return render_template('opponents_turn.html', yourPokemon=yourPokemon, yourPokemonHealth=yourPokemonHealth,
                               yourPokemonHealthDisplay=yourPokemonHealthDisplay,
                               opponentsPokemonHealthDisplay=opponentsPokemonHealthDisplay,
                               opponentsPokemon=opponentsPokemon, opponentsPokemonHealth=opponentsPokemonHealth)


@app.route('/attack2', methods=['GET', 'POST'])
def attack2():
    global yourPokemon
    global opponentsPokemonHealth
    global opponentsPokemon
    global yourPokemonHealth
    global shield_active
    global game_mode
    global opponentsPokemonMove
    if game_mode == "Single player":
        key = random.choice(list(opponentsPokemon["moves"]))
        opponentsPokemonMove = opponentsPokemon["moves"][key]
    elif game_mode == "Hot seats":
        opponentsPokemonMove = request.form.get('comp_select')

    version = ['Fire', 'Water', 'Grass']
    for i, k in enumerate(version):
        if yourPokemon["type"] == k:
            if opponentsPokemon["type"] == k:
                string_1_attack = 'Its not very effective...'
                string_2_attack = 'Its not very effective...'
            if opponentsPokemon["type"] == version[(i + 1) % 3]:
                string_1_attack = 'Its not very effective...'
                string_2_attack = 'Its super effective!'
            if opponentsPokemon["type"] == version[(i + 2) % 3]:
                string_1_attack = 'Its super effective!'
                string_2_attack = 'Its not very effective...'

    if shield_active:
        pass
    else:
        yourPokemonHealth = yourPokemonHealth - opponentsPokemon["EVs"]["ATTACK"]

    return render_template('attack2.html', yourPokemon=yourPokemon,
                           opponentsPokemon=opponentsPokemon, opponentsPokemonMove=opponentsPokemonMove,
                           string_1_attack=string_1_attack, string_2_attack=string_2_attack)


@app.route('/bag')
def bag():
    global yourPokemon
    global yourPokemonHealth
    global yourPokemonHealthDisplay
    return render_template('bag.html', yourPokemon=yourPokemon, yourPokemonHealth=yourPokemonHealth,
                           yourPokemonHealthDisplay=yourPokemonHealthDisplay)


@app.route('/pokemon')
def pokemon():
    return render_template('pokemon.html')


@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True)
