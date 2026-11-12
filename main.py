from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Your Drafter Website")
set_website_framed(False)
set_site_information("Saumya Bhavsar", 
                     "F1 Tracker",
                    planning = "",
                    sources = "",
                    links = ["https://github.com/RaVen00-glitch/F1-Tracker"]
                    )

from dataclasses import dataclass, field
from drafter import *
# assert_equal is assumed to be available (add `from bakery import assert_equal` if your editor needs it)

# ======================================================================
# CONSTANTS - 2026 FORMULA 1 SEASON
# Standings snapshot: after Round 20 (Sao Paulo), November 8, 2026.
# The final three rounds are Las Vegas, Qatar, and Abu Dhabi.
# ======================================================================
POINTS_FOR_WIN = 25

DRIVER_TEAMS = {
    "Kimi Antonelli": "Mercedes",
    "Max Verstappen": "Red Bull Racing",
    "George Russell": "Mercedes",
    "Lewis Hamilton": "Ferrari",
    "Charles Leclerc": "Ferrari",
    "Lando Norris": "McLaren",
    "Oscar Piastri": "McLaren",
    "Isack Hadjar": "Red Bull Racing",
    "Liam Lawson": "Racing Bulls",
    "Pierre Gasly": "Alpine",
    "Arvid Lindblad": "Racing Bulls",
    "Franco Colapinto": "Alpine",
    "Oliver Bearman": "Haas F1 Team",
    "Gabriel Bortoleto": "Audi",
    "Nico Hulkenberg": "Audi",
    "Esteban Ocon": "Haas F1 Team",
    "Fernando Alonso": "Aston Martin",
    "Carlos Sainz": "Williams",
    "Alexander Albon": "Williams",
    "Yuki Tsunoda": "Racing Bulls",
    "Ryo Hirakawa": "Haas F1 Team",
    "Lance Stroll": "Aston Martin",
    "Valtteri Bottas": "Cadillac",
    "Sergio Perez": "Cadillac",
    "Rafael Camara": "Haas F1 Team",
}

# Official constructor standings are stored separately because driver points
# do not always add up directly to constructor points after driver changes.
CONSTRUCTOR_STANDINGS = {
    "Mercedes": 652,
    "Ferrari": 510,
    "Red Bull Racing": 415,
    "McLaren": 398,
    "Racing Bulls": 114,
    "Alpine": 69,
    "Haas F1 Team": 31,
    "Audi": 28,
    "Williams": 12,
    "Aston Martin": 7,
    "Cadillac": 0,
}

RACE_FORMATS = {
    "Grand Prix": "A standard weekend: practice, qualifying, then one race.",
    "Sprint weekend": "Includes a sprint race in addition to the Grand Prix.",
}

CAR_INFO = {
    "2026 F1 cars": "The 2026 season introduces a new generation of cars and power-unit regulations.",
    "McLaren MP4/4 (1988)": "Won 15 of the 16 races that season.",
    "Ferrari F2004 (2004)": "Won 15 of the 18 races that season.",
    "Mercedes W11 (2020)": "Won 13 of the 17 races that season.",
    "Red Bull RB19 (2023)": "Won 21 of the 22 races that season.",
}

BUILD_STAGES = {
    "1. Design": "Engineers design the car on computers, balancing speed and the rules.",
    "2. Testing ideas": "Wind tunnels and simulations check how air flows over the car.",
    "3. Manufacturing": "Mechanics and machinists build parts, many from carbon fiber.",
    "4. Assembly": "The team fits the engine, wings, and suspension into one car.",
    "5. Race weekend": "Mechanics adjust the car and perform pit stops during the race.",
}

QUIZ_QUESTIONS = [
    "What does DRS stand for? (three words)",
    "What is the first starting spot on the grid called? (two words)",
    "How many points does a Grand Prix winner get?",
]
QUIZ_ANSWERS = [
    "drag reduction system",
    "pole position",
    "25",
]


# ======================================================================
# DATACLASSES
# ======================================================================
@dataclass
class Race:
    track: str
    country: str
    format: str
    completed: bool
    winner: str
    date: str = ""


@dataclass
class State:
    season: list[Race]
    drivers: dict[str, int]   # driver name -> championship points
    selected_driver: str
    quiz_score: int
    question_number: int
    constructors: dict[str, int] = field(default_factory=dict)


# ======================================================================
# STARTING DATA - 2026 SEASON SNAPSHOT AFTER ROUND 20
# ======================================================================
def make_starting_state() -> State:
    """Returns the current 2026 season data snapshot."""
    season = [
        Race("Albert Park", "Australia", "Grand Prix", True, "George Russell", "Mar 6-8"),
        Race("Shanghai", "China", "Sprint weekend", True, "Kimi Antonelli", "Mar 13-15"),
        Race("Suzuka", "Japan", "Grand Prix", True, "Kimi Antonelli", "Mar 27-29"),
        Race("Miami", "United States", "Sprint weekend", True, "Kimi Antonelli", "May 1-3"),
        Race("Circuit Gilles-Villeneuve", "Canada", "Sprint weekend", True, "Kimi Antonelli", "May 22-24"),
        Race("Monaco", "Monaco", "Grand Prix", True, "Kimi Antonelli", "Jun 5-7"),
        Race("Barcelona-Catalunya", "Spain", "Grand Prix", True, "Lewis Hamilton", "Jun 12-14"),
        Race("Red Bull Ring", "Austria", "Grand Prix", True, "George Russell", "Jun 26-28"),
        Race("Silverstone", "United Kingdom", "Sprint weekend", True, "Charles Leclerc", "Jul 3-5"),
        Race("Spa-Francorchamps", "Belgium", "Grand Prix", True, "Kimi Antonelli", "Jul 17-19"),
        Race("Hungaroring", "Hungary", "Grand Prix", True, "Lando Norris", "Jul 24-26"),
        Race("Zandvoort", "Netherlands", "Sprint weekend", True, "Lando Norris", "Aug 21-23"),
        Race("Monza", "Italy", "Grand Prix", True, "Kimi Antonelli", "Sep 4-6"),
        Race("Madrid", "Spain", "Grand Prix", True, "Kimi Antonelli", "Sep 11-13"),
        Race("Baku City Circuit", "Azerbaijan", "Grand Prix", True, "George Russell", "Sep 24-26"),
        Race("Sakhir", "Bahrain", "Grand Prix", True, "Max Verstappen", "Oct 2-4"),
        Race("Marina Bay", "Singapore", "Sprint weekend", True, "Max Verstappen", "Oct 9-11"),
        Race("Circuit of The Americas", "United States", "Grand Prix", True, "Kimi Antonelli", "Oct 23-25"),
        Race("Autodromo Hermanos Rodriguez", "Mexico", "Grand Prix", True, "Max Verstappen", "Oct 30-Nov 1"),
        Race("Interlagos", "Brazil", "Grand Prix", True, "Lando Norris", "Nov 6-8"),
        Race("Las Vegas Strip Circuit", "United States", "Grand Prix", False, "", "Nov 19-21"),
        Race("Lusail", "Qatar", "Grand Prix", False, "", "Nov 27-29"),
        Race("Yas Marina", "United Arab Emirates", "Grand Prix", False, "", "Dec 4-6"),
    ]

    drivers = {
        "Kimi Antonelli": 390,
        "Max Verstappen": 279,
        "George Russell": 262,
        "Lewis Hamilton": 261,
        "Charles Leclerc": 249,
        "Lando Norris": 246,
        "Oscar Piastri": 152,
        "Isack Hadjar": 122,
        "Liam Lawson": 89,
        "Pierre Gasly": 42,
        "Arvid Lindblad": 38,
        "Franco Colapinto": 27,
        "Oliver Bearman": 23,
        "Gabriel Bortoleto": 14,
        "Nico Hulkenberg": 14,
        "Esteban Ocon": 7,
        "Fernando Alonso": 7,
        "Carlos Sainz": 7,
        "Alexander Albon": 5,
        "Yuki Tsunoda": 1,
        "Ryo Hirakawa": 1,
        "Lance Stroll": 0,
        "Valtteri Bottas": 0,
        "Sergio Perez": 0,
        "Rafael Camara": 0,
    }

    constructors = dict(CONSTRUCTOR_STANDINGS)
    return State(season, drivers, "", 0, 0, constructors)


starting = make_starting_state()
assert_equal(len(starting.season), 23)
assert_equal(starting.season[0].track, "Albert Park")
assert_equal(starting.season[0].completed, True)
assert_equal(len(starting.drivers), 25)
assert_equal(starting.selected_driver, "")
assert_equal(starting.quiz_score, 0)
assert_equal(starting.question_number, 0)


# ======================================================================
# HELPER FUNCTIONS (logic lives here; routes only build pages)
# ======================================================================
def find_next_race(season: list[Race]) -> str:
    """Returns the track of the first unfinished race, or "Season complete"."""
    for race in season:
        if not race.completed:
            return race.track
    return "Season complete"


assert_equal(find_next_race(make_starting_state().season), "Las Vegas Strip Circuit")
assert_equal(find_next_race([Race("A", "B", "Grand Prix", True, "Driver A")]), "Season complete")
assert_equal(find_next_race([]), "Season complete")


def rank_by_points(scores: dict[str, int]) -> list[str]:
    """Returns the names in `scores` ordered from most points to fewest.
    Uses list(...) to copy the keys and .remove(...) to delete an item from
    a list. Both are basic list tools, shown here with a while loop."""
    remaining = list(scores.keys())
    ranked = []
    while len(remaining) > 0:
        best = remaining[0]
        for name in remaining:
            if scores[name] > scores[best]:
                best = name
        ranked.append(best)
        remaining.remove(best)
    return ranked


assert_equal(rank_by_points({"A": 5, "B": 20, "C": 10}), ["B", "C", "A"])
assert_equal(rank_by_points({}), [])


def team_totals(drivers: dict[str, int], teams: dict[str, str]) -> dict[str, int]:
    """Adds up each team's driver points."""
    totals = {}
    for name in drivers:
        team = teams[name]
        if team in totals:
            totals[team] = totals[team] + drivers[name]
        else:
            totals[team] = drivers[name]
    return totals


assert_equal(team_totals({"A": 10, "B": 5, "C": 7}, {"A": "X", "B": "X", "C": "Y"}),
             {"X": 15, "Y": 7})


def count_wins(season: list[Race], name: str) -> int:
    """Counts how many races a driver has won."""
    wins = 0
    for race in season:
        if race.winner == name:
            wins = wins + 1
    return wins


def all_countries(season: list[Race]) -> list[str]:
    """Returns each country in the season once."""
    countries = []
    for race in season:
        if race.country not in countries:
            countries.append(race.country)
    return countries


assert_equal(all_countries(make_starting_state().season),
             ["Australia", "China", "Japan", "United States", "Canada",
              "Monaco", "Spain", "Austria", "United Kingdom", "Belgium",
              "Hungary", "Netherlands", "Italy", "Azerbaijan", "Bahrain",
              "Singapore", "Mexico", "Brazil", "Qatar", "United Arab Emirates"])


def races_in_country(season: list[Race], country: str) -> list[Race]:
    """Returns the races held in one country."""
    found = []
    for race in season:
        if race.country == country:
            found.append(race)
    return found


assert_equal(len(races_in_country(make_starting_state().season, "Italy")), 1)
assert_equal(len(races_in_country(make_starting_state().season, "Spain")), 2)


def unfinished_tracks(season: list[Race]) -> list[str]:
    """Returns the track names of races that have no result yet."""
    tracks = []
    for race in season:
        if not race.completed:
            tracks.append(race.track)
    return tracks


assert_equal(len(unfinished_tracks(make_starting_state().season)), 3)


def record_result(state: State, track: str, winner: str) -> str:
    """Records a race winner. Changes state.season and state.drivers.
    Returns a message saying what happened."""
    for race in state.season:
        if race.track == track:
            if race.completed:
                return "That race already has a result."
            if winner not in state.drivers:
                return "That driver is not on the grid."
            race.completed = True
            race.winner = winner
            state.drivers[winner] = state.drivers[winner] + POINTS_FOR_WIN
            team = DRIVER_TEAMS[winner]
            state.constructors[team] = state.constructors[team] + POINTS_FOR_WIN
            return winner + " won at " + track + "."
    return "Race not found."


test_state = make_starting_state()
assert_equal(record_result(test_state, "Las Vegas Strip Circuit", "Kimi Antonelli"),
             "Kimi Antonelli won at Las Vegas Strip Circuit.")
assert_equal(test_state.season[20].completed, True)
assert_equal(test_state.season[20].winner, "Kimi Antonelli")
assert_equal(test_state.drivers["Kimi Antonelli"], 415)
assert_equal(test_state.constructors["Mercedes"], 677)
assert_equal(record_result(test_state, "Las Vegas Strip Circuit", "Max Verstappen"),
             "That race already has a result.")
assert_equal(record_result(test_state, "Lusail", "Nobody"), "That driver is not on the grid.")
assert_equal(record_result(test_state, "Atlantis", "Kimi Antonelli"), "Race not found.")
assert_equal(find_next_race(test_state.season), "Lusail")


def check_answer(guess: str, correct: str) -> bool:
    """Compares a quiz answer, ignoring capital letters and extra spaces."""
    return guess.lower().strip() == correct.lower()


assert_equal(check_answer("DRS ", "drs"), True)
assert_equal(check_answer("drs", "pole position"), False)


# ======================================================================
# ROUTES (each one reads state, calls helpers, and returns a page)
# ======================================================================
def nav_bar() -> list:
    """Navigation buttons shown at the top of every page."""
    return [
        Button("Home", index),
        Button("Standings", standings),
        Button("Driver", driver_page),
        Button("Season", season_page),
        Button("Record result", record_form),
        Button("Cars", cars),
        Button("Quiz", quiz),
    ]


@route
def index(state: State) -> Page:
    next_race = find_next_race(state.season)
    if next_race == "Season complete":
        next_line = "The season is complete."
    else:
        next_line = "Next race: " + next_race
    return Page(state, nav_bar() + [
        Header("F1 Tracker"),
        "2026 Formula 1 season tracker.\n",
        next_line + "\n",
        "Standings snapshot: after the Sao Paulo Grand Prix, November 8, 2026. This is not a live feed.\n",
    ])


@route
def standings(state: State) -> Page:
    content = nav_bar() + [Header("Driver standings")]
    place = 1
    for name in rank_by_points(state.drivers):
        content.append(str(place) + ". " + name + " (" + DRIVER_TEAMS[name] + "): "
                       + str(state.drivers[name]) + " pts\n")
        place = place + 1

    content.append(Header("Constructor standings"))
    totals = state.constructors
    place = 1
    for team in rank_by_points(totals):
        content.append(str(place) + ". " + team + ": " + str(totals[team]) + " pts\n")
        place = place + 1

    content.append(Header("View a driver"))
    names = rank_by_points(state.drivers)
    content.append(SelectBox("driver_name", names, names[0]))
    content.append(Button("View stats", view_driver))
    return Page(state, content)


@route
def view_driver(state: State, driver_name: str) -> Page:
    state.selected_driver = driver_name
    return driver_page(state)


@route
def driver_page(state: State) -> Page:
    if state.selected_driver == "":
        return Page(state, nav_bar() + [
            Header("Driver"),
            "No driver selected yet. Pick one on the Standings page.\n",
        ])
    name = state.selected_driver
    return Page(state, nav_bar() + [
        Header(name),
        "Team: " + DRIVER_TEAMS[name] + "\n",
        "Points: " + str(state.drivers[name]) + "\n",
        "Wins this season: " + str(count_wins(state.season, name)) + "\n",
    ])


@route
def season_page(state: State) -> Page:
    content = nav_bar() + [Header("Season calendar")]
    content.append("Finished races:\n")
    for race in state.season:
        if race.completed:
            content.append(race.date + " - " + race.track + " (" + race.country + ") - winner: " + race.winner + "\n")
    content.append("Upcoming races:\n")
    for race in state.season:
        if not race.completed:
            content.append(race.date + " - " + race.track + " (" + race.country + ") - " + race.format + "\n")

    content.append(Header("Race formats"))
    for format_name in RACE_FORMATS:
        content.append(format_name + ": " + RACE_FORMATS[format_name] + "\n")

    content.append(Header("Filter by country"))
    countries = all_countries(state.season)
    content.append(SelectBox("country", countries, countries[0]))
    content.append(Button("Show races", filter_country))
    return Page(state, content)


@route
def filter_country(state: State, country: str) -> Page:
    content = nav_bar() + [Header("Races in " + country)]
    for race in races_in_country(state.season, country):
        content.append(race.track + " - " + race.format + "\n")
    content.append(Button("Back to season", season_page))
    return Page(state, content)


@route
def record_form(state: State) -> Page:
    tracks = unfinished_tracks(state.season)
    if len(tracks) == 0:
        return Page(state, nav_bar() + [Header("Record a result"),
                                        "Every race already has a result.\n"])
    names = rank_by_points(state.drivers)
    return Page(state, nav_bar() + [
        Header("Record a result"),
        "Race:\n",
        SelectBox("track", tracks, tracks[0]),
        "Winner:\n",
        SelectBox("winner", names, names[0]),
        Button("Save result", save_result),
    ])


@route
def save_result(state: State, track: str, winner: str) -> Page:
    message = record_result(state, track, winner)
    return Page(state, nav_bar() + [
        Header("Result"),
        message + "\n",
        Button("Back to season", season_page),
    ])


@route
def cars(state: State) -> Page:
    content = nav_bar() + [Header("Famous and current cars")]
    for car in CAR_INFO:
        content.append(car + ": " + CAR_INFO[car] + "\n")
    content.append(Header("How an F1 car is built"))
    for stage in BUILD_STAGES:
        content.append(stage + ": " + BUILD_STAGES[stage] + "\n")
    return Page(state, content)


@route
def quiz(state: State) -> Page:
    if state.question_number >= len(QUIZ_QUESTIONS):
        return Page(state, nav_bar() + [
            Header("Quiz finished"),
            "Final score: " + str(state.quiz_score) + " out of " + str(len(QUIZ_QUESTIONS)) + "\n",
            Button("Restart quiz", restart_quiz),
        ])
    return Page(state, nav_bar() + [
        Header("F1 quiz"),
        "Score: " + str(state.quiz_score) + "\n",
        QUIZ_QUESTIONS[state.question_number] + "\n",
        TextBox("answer", ""),
        LineBreak(),
        Button("Submit answer", submit_answer),
    ])


@route
def submit_answer(state: State, answer: str) -> Page:
    correct = QUIZ_ANSWERS[state.question_number]
    if check_answer(answer, correct):
        state.quiz_score = state.quiz_score + 1
        feedback = "Correct!"
    else:
        feedback = "Not quite. The answer was: " + correct
    state.question_number = state.question_number + 1
    return Page(state, nav_bar() + [feedback + "\n", Button("Next", quiz)])


@route
def restart_quiz(state: State) -> Page:
    state.quiz_score = 0
    state.question_number = 0
    return quiz(state)


start_server(make_starting_state())

