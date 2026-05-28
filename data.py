"""Seed team data for the Football Simulator.

Ratings are intentionally editable. They are a practical 1-100 game scale,
not an official ranking. Continental team lists are seeded from 2025/26 UEFA
league-phase line-ups.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class Team:
    name: str
    country: str
    league: str
    attack: int
    midfield: int
    defence: int
    star_player: str

    @property
    def overall(self) -> int:
        return round((self.attack * 0.34) + (self.midfield * 0.33) + (self.defence * 0.33))

    def to_dict(self) -> dict:
        data = asdict(self)
        data["overall"] = self.overall
        return data


# Editable, game-balanced ratings. Bigger clubs receive higher baseline ratings.
RATINGS: Dict[str, dict] = {
    # England
    "Arsenal": {"country": "England", "league": "Premier League", "attack": 91, "midfield": 91, "defence": 92, "star_player": "Bukayo Saka"},
    "Aston Villa": {"country": "England", "league": "Premier League", "attack": 84, "midfield": 84, "defence": 83, "star_player": "Ollie Watkins"},
    "Chelsea": {"country": "England", "league": "Premier League", "attack": 87, "midfield": 86, "defence": 84, "star_player": "Cole Palmer"},
    "Crystal Palace": {"country": "England", "league": "Premier League", "attack": 81, "midfield": 80, "defence": 80, "star_player": "Eberechi Eze"},
    "Liverpool": {"country": "England", "league": "Premier League", "attack": 91, "midfield": 88, "defence": 87, "star_player": "Mohamed Salah"},
    "Man City": {"country": "England", "league": "Premier League", "attack": 92, "midfield": 93, "defence": 88, "star_player": "Erling Haaland"},
    "Manchester United": {"country": "England", "league": "Premier League", "attack": 82, "midfield": 80, "defence": 78, "star_player": "Bruno Fernandes"},
    "Newcastle": {"country": "England", "league": "Premier League", "attack": 85, "midfield": 84, "defence": 83, "star_player": "Alexander Isak"},
    "Nottingham Forest": {"country": "England", "league": "Premier League", "attack": 80, "midfield": 79, "defence": 80, "star_player": "Morgan Gibbs-White"},
    "Tottenham": {"country": "England", "league": "Premier League", "attack": 85, "midfield": 83, "defence": 80, "star_player": "Son Heung-min"},
    "AFC Bournemouth": {"country": "England", "league": "Premier League", "attack": 80, "midfield": 80, "defence": 79, "star_player": "Antoine Semenyo"},
    "Brentford": {"country": "England", "league": "Premier League", "attack": 79, "midfield": 79, "defence": 78, "star_player": "Bryan Mbeumo"},
    "Brighton": {"country": "England", "league": "Premier League", "attack": 82, "midfield": 82, "defence": 80, "star_player": "Kaoru Mitoma"},
    "Burnley": {"country": "England", "league": "Premier League", "attack": 73, "midfield": 74, "defence": 75, "star_player": "Josh Brownhill"},
    "Everton": {"country": "England", "league": "Premier League", "attack": 78, "midfield": 78, "defence": 79, "star_player": "Jordan Pickford"},
    "Fulham": {"country": "England", "league": "Premier League", "attack": 79, "midfield": 80, "defence": 78, "star_player": "João Palhinha"},
    "Leeds United": {"country": "England", "league": "Premier League", "attack": 76, "midfield": 77, "defence": 76, "star_player": "Ethan Ampadu"},
    "Sunderland": {"country": "England", "league": "Premier League", "attack": 75, "midfield": 76, "defence": 76, "star_player": "Granit Xhaka"},
    "West Ham United": {"country": "England", "league": "Premier League", "attack": 80, "midfield": 80, "defence": 78, "star_player": "Jarrod Bowen"},
    "Wolverhampton Wanderers": {"country": "England", "league": "Premier League", "attack": 77, "midfield": 77, "defence": 77, "star_player": "Matheus Cunha"},

    # Spain
    "Athletic Club": {"country": "Spain", "league": "La Liga", "attack": 82, "midfield": 82, "defence": 83, "star_player": "Nico Williams"},
    "Atlético Madrid": {"country": "Spain", "league": "La Liga", "attack": 87, "midfield": 86, "defence": 88, "star_player": "Antoine Griezmann"},
    "Barcelona": {"country": "Spain", "league": "La Liga", "attack": 91, "midfield": 90, "defence": 85, "star_player": "Lamine Yamal"},
    "Celta": {"country": "Spain", "league": "La Liga", "attack": 78, "midfield": 77, "defence": 76, "star_player": "Iago Aspas"},
    "Real Betis": {"country": "Spain", "league": "La Liga", "attack": 82, "midfield": 82, "defence": 79, "star_player": "Isco"},
    "Real Madrid": {"country": "Spain", "league": "La Liga", "attack": 94, "midfield": 92, "defence": 90, "star_player": "Kylian Mbappé"},
    "Rayo Vallecano": {"country": "Spain", "league": "La Liga", "attack": 77, "midfield": 77, "defence": 77, "star_player": "Álvaro García"},
    "Villarreal": {"country": "Spain", "league": "La Liga", "attack": 83, "midfield": 82, "defence": 79, "star_player": "Gerard Moreno"},

    # Italy
    "AC Milan": {"country": "Italy", "league": "Serie A", "attack": 86, "midfield": 84, "defence": 82, "star_player": "Rafael Leão"},
    "Atalanta": {"country": "Italy", "league": "Serie A", "attack": 85, "midfield": 84, "defence": 83, "star_player": "Ademola Lookman"},
    "Bologna": {"country": "Italy", "league": "Serie A", "attack": 80, "midfield": 81, "defence": 81, "star_player": "Riccardo Orsolini"},
    "Fiorentina": {"country": "Italy", "league": "Serie A", "attack": 81, "midfield": 81, "defence": 80, "star_player": "Moise Kean"},
    "Inter Milan": {"country": "Italy", "league": "Serie A", "attack": 89, "midfield": 89, "defence": 90, "star_player": "Lautaro Martínez"},
    "Juventus": {"country": "Italy", "league": "Serie A", "attack": 84, "midfield": 83, "defence": 84, "star_player": "Dušan Vlahović"},
    "Napoli": {"country": "Italy", "league": "Serie A", "attack": 87, "midfield": 85, "defence": 84, "star_player": "Khvicha Kvaratskhelia"},
    "Roma": {"country": "Italy", "league": "Serie A", "attack": 83, "midfield": 83, "defence": 81, "star_player": "Paulo Dybala"},

    # Germany
    "Bayer Leverkusen": {"country": "Germany", "league": "Bundesliga", "attack": 88, "midfield": 88, "defence": 86, "star_player": "Florian Wirtz"},
    "Bayern Munich": {"country": "Germany", "league": "Bundesliga", "attack": 92, "midfield": 90, "defence": 87, "star_player": "Harry Kane"},
    "Borussia Dortmund": {"country": "Germany", "league": "Bundesliga", "attack": 85, "midfield": 84, "defence": 81, "star_player": "Julian Brandt"},
    "Frankfurt": {"country": "Germany", "league": "Bundesliga", "attack": 82, "midfield": 81, "defence": 80, "star_player": "Omar Marmoush"},
    "Freiburg": {"country": "Germany", "league": "Bundesliga", "attack": 79, "midfield": 80, "defence": 80, "star_player": "Vincenzo Grifo"},
    "Mainz": {"country": "Germany", "league": "Bundesliga", "attack": 78, "midfield": 78, "defence": 79, "star_player": "Jonathan Burkardt"},
    "RB Leipzig": {"country": "Germany", "league": "Bundesliga", "attack": 85, "midfield": 84, "defence": 82, "star_player": "Xavi Simons"},
    "Stuttgart": {"country": "Germany", "league": "Bundesliga", "attack": 82, "midfield": 82, "defence": 80, "star_player": "Deniz Undav"},

    # France
    "Lille": {"country": "France", "league": "Ligue 1", "attack": 82, "midfield": 82, "defence": 82, "star_player": "Jonathan David"},
    "Lyon": {"country": "France", "league": "Ligue 1", "attack": 83, "midfield": 82, "defence": 80, "star_player": "Alexandre Lacazette"},
    "Marseille": {"country": "France", "league": "Ligue 1", "attack": 83, "midfield": 82, "defence": 80, "star_player": "Pierre-Emerick Aubameyang"},
    "Monaco": {"country": "France", "league": "Ligue 1", "attack": 84, "midfield": 83, "defence": 81, "star_player": "Aleksandr Golovin"},
    "Nice": {"country": "France", "league": "Ligue 1", "attack": 80, "midfield": 80, "defence": 82, "star_player": "Terem Moffi"},
    "Paris Saint-Germain": {"country": "France", "league": "Ligue 1", "attack": 94, "midfield": 91, "defence": 89, "star_player": "Ousmane Dembélé"},
    "Strasbourg": {"country": "France", "league": "Ligue 1", "attack": 78, "midfield": 78, "defence": 77, "star_player": "Emanuel Emegha"},

    # Portugal
    "Benfica": {"country": "Portugal", "league": "Liga Portugal", "attack": 86, "midfield": 85, "defence": 83, "star_player": "Ángel Di María"},
    "Braga": {"country": "Portugal", "league": "Liga Portugal", "attack": 81, "midfield": 80, "defence": 78, "star_player": "Ricardo Horta"},
    "Porto": {"country": "Portugal", "league": "Liga Portugal", "attack": 84, "midfield": 83, "defence": 82, "star_player": "Diogo Costa"},
    "Sporting CP": {"country": "Portugal", "league": "Liga Portugal", "attack": 87, "midfield": 85, "defence": 83, "star_player": "Viktor Gyökeres"},
    "Santa Clara": {"country": "Portugal", "league": "Liga Portugal", "attack": 74, "midfield": 74, "defence": 75, "star_player": "Gabriel Silva"},

    # USA / MLS
    "Inter Miami": {"country": "USA", "league": "MLS", "attack": 83, "midfield": 80, "defence": 74, "star_player": "Lionel Messi"},
    "LAFC": {"country": "USA", "league": "MLS", "attack": 78, "midfield": 76, "defence": 75, "star_player": "Denis Bouanga"},
    "LA Galaxy": {"country": "USA", "league": "MLS", "attack": 77, "midfield": 76, "defence": 74, "star_player": "Riqui Puig"},
    "Columbus Crew": {"country": "USA", "league": "MLS", "attack": 77, "midfield": 77, "defence": 75, "star_player": "Cucho Hernández"},
    "Seattle Sounders": {"country": "USA", "league": "MLS", "attack": 76, "midfield": 76, "defence": 76, "star_player": "Jordan Morris"},
    "Atlanta United": {"country": "USA", "league": "MLS", "attack": 75, "midfield": 75, "defence": 72, "star_player": "Thiago Almada"},

    # Saudi Arabia
    "Al Hilal": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 86, "midfield": 84, "defence": 83, "star_player": "Aleksandar Mitrović"},
    "Al Nassr": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 85, "midfield": 82, "defence": 79, "star_player": "Cristiano Ronaldo"},
    "Al Ittihad": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 83, "midfield": 82, "defence": 79, "star_player": "Karim Benzema"},
    "Al Ahli": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 82, "midfield": 81, "defence": 78, "star_player": "Riyad Mahrez"},
    "Al Qadsiah": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 77, "midfield": 77, "defence": 76, "star_player": "Pierre-Emerick Aubameyang"},

    # Brazil
    "Botafogo": {"country": "Brazil", "league": "Brasileirão", "attack": 80, "midfield": 79, "defence": 79, "star_player": "Tiquinho Soares"},
    "Corinthians": {"country": "Brazil", "league": "Brasileirão", "attack": 78, "midfield": 77, "defence": 77, "star_player": "Memphis Depay"},
    "Flamengo": {"country": "Brazil", "league": "Brasileirão", "attack": 83, "midfield": 82, "defence": 81, "star_player": "Pedro"},
    "Fluminense": {"country": "Brazil", "league": "Brasileirão", "attack": 79, "midfield": 79, "defence": 78, "star_player": "Ganso"},
    "Grêmio": {"country": "Brazil", "league": "Brasileirão", "attack": 78, "midfield": 78, "defence": 77, "star_player": "Cristaldo"},
    "Palmeiras": {"country": "Brazil", "league": "Brasileirão", "attack": 82, "midfield": 82, "defence": 82, "star_player": "Raphael Veiga"},
    "São Paulo": {"country": "Brazil", "league": "Brasileirão", "attack": 79, "midfield": 79, "defence": 79, "star_player": "Lucas Moura"},
}

UCL_2025_26 = [
    "Ajax", "Arsenal", "Atalanta", "Athletic Club", "Atlético Madrid", "Borussia Dortmund",
    "Barcelona", "Bayern Munich", "Benfica", "Bodø/Glimt", "Chelsea", "Club Brugge",
    "Copenhagen", "Frankfurt", "Galatasaray", "Inter Milan", "Juventus", "Kairat Almaty",
    "Bayer Leverkusen", "Liverpool", "Man City", "Marseille", "Monaco", "Napoli",
    "Newcastle", "Olympiacos", "Pafos", "Paris Saint-Germain", "PSV Eindhoven", "Qarabağ",
    "Real Madrid", "Slavia Praha", "Sporting CP", "Tottenham", "Union SG", "Villarreal",
]

UEL_2025_26 = [
    "Aston Villa", "Basel", "Bologna", "Braga", "Brann", "Celta", "Celtic", "Crvena Zvezda",
    "FCSB", "Fenerbahçe", "Ferencváros", "Feyenoord", "Freiburg", "Genk", "GNK Dinamo",
    "Go Ahead Eagles", "Lille", "Ludogorets", "Lyon", "Malmö", "Maccabi Tel-Aviv",
    "Midtjylland", "Nice", "Nottingham Forest", "Panathinaikos", "PAOK", "Porto", "Rangers",
    "Real Betis", "Roma", "Salzburg", "Sturm Graz", "Stuttgart", "Utrecht", "Viktoria Plzeň", "Young Boys",
]

UECL_2025_26 = [
    "Noah", "SK Rapid", "Zrinjski", "Rijeka", "AEK Larnaca", "Omonoia", "Sigma Olomouc", "Sparta Praha",
    "Crystal Palace", "KuPS Kuopio", "Strasbourg", "Mainz", "Lincoln Red Imps", "AEK Athens", "Breidablik",
    "Fiorentina", "Drita", "Hamrun Spartans", "AZ Alkmaar", "Shkëndija", "Jagiellonia Białystok",
    "Lech Poznań", "Legia Warszawa", "Raków Częstochowa", "Shamrock Rovers", "Shelbourne",
    "Universitatea Craiova", "Aberdeen", "Slovan Bratislava", "Celje", "Rayo Vallecano", "Häcken",
    "Lausanne-Sport", "Samsunspor", "Dynamo Kyiv", "Shakhtar Donetsk",
]

CONTINENTAL = {
    "Champions League 2025/26": {"teams": UCL_2025_26, "league_rounds": 8, "kind": "uefa"},
    "Europa League 2025/26": {"teams": UEL_2025_26, "league_rounds": 8, "kind": "uefa"},
    "Conference League 2025/26": {"teams": UECL_2025_26, "league_rounds": 6, "kind": "uefa"},
}

PREMIER_LEAGUE_2025_26 = [
    "Arsenal", "Aston Villa", "AFC Bournemouth", "Brentford", "Brighton", "Burnley",
    "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool",
    "Man City", "Manchester United", "Newcastle", "Nottingham Forest", "Sunderland",
    "Tottenham", "West Ham United", "Wolverhampton Wanderers",
]

FA_CUP_SEED_TEAMS = PREMIER_LEAGUE_2025_26 + [
    "Leicester City", "Ipswich Town", "Southampton", "Norwich City", "Coventry City", "Middlesbrough",
    "West Brom", "Sheffield United", "Sheffield Wednesday", "Derby County", "Blackburn Rovers",
    "Stoke City", "Queens Park Rangers", "Portsmouth", "Bristol City", "Watford", "Millwall",
    "Hull City", "Swansea City", "Cardiff City", "Preston North End", "Wrexham", "Plymouth Argyle",
    "Birmingham City", "Bolton Wanderers", "Charlton Athletic", "Reading", "Barnsley", "Blackpool",
    "Peterborough United", "Wigan Athletic", "Rotherham United", "Wycombe Wanderers", "Oxford United",
    "Lincoln City", "Port Vale", "Stockport County", "Bradford City", "Mansfield Town", "Walsall",
    "Doncaster Rovers", "Notts County", "Gillingham", "Tranmere Rovers", "AFC Wimbledon",
    "Swindon Town", "Newport County", "Grimsby Town", "Carlisle United", "Salford City",
    "Harrogate Town", "Accrington Stanley", "Barrow", "Morecambe", "Crewe Alexandra",
    "Chesterfield", "Bromley", "Colchester United", "Cheltenham Town", "Exeter City", "Leyton Orient",
]

DOMESTIC = {
    "Premier League": {
        "teams": PREMIER_LEAGUE_2025_26,
        "kind": "league",
        "format_note": "20 clubs, 38 matchdays, home and away fixtures. Ratings are editable game estimates.",
    },
    "FA Cup": {
        "teams": FA_CUP_SEED_TEAMS[:64],
        "kind": "knockout",
        "format_note": "64-team single-match knockout with random draws, extra time and penalties. Giant-killing is possible but weighted by team strength.",
    },
}

COUNTRY_DEFAULTS = {
    "England": 82, "Spain": 81, "Italy": 81, "Germany": 80, "France": 79, "Portugal": 78,
    "Netherlands": 76, "Turkey": 76, "Scotland": 73, "Belgium": 73, "Brazil": 77, "USA": 74,
    "Saudi Arabia": 78, "Greece": 72, "Switzerland": 71, "Austria": 71, "Czechia": 70, "Ukraine": 72,
}

TEAM_COUNTRY_HINTS = {
    "Ajax": ("Netherlands", "Eredivisie"), "Bodø/Glimt": ("Norway", "Eliteserien"), "Club Brugge": ("Belgium", "Belgian Pro League"),
    "Copenhagen": ("Denmark", "Superliga"), "Galatasaray": ("Turkey", "Süper Lig"), "Kairat Almaty": ("Kazakhstan", "Premier League"),
    "Olympiacos": ("Greece", "Super League Greece"), "Pafos": ("Cyprus", "First Division"), "PSV Eindhoven": ("Netherlands", "Eredivisie"),
    "Qarabağ": ("Azerbaijan", "Premier League"), "Slavia Praha": ("Czechia", "Czech First League"), "Union SG": ("Belgium", "Belgian Pro League"),
    "Basel": ("Switzerland", "Swiss Super League"), "Brann": ("Norway", "Eliteserien"), "Celtic": ("Scotland", "Scottish Premiership"),
    "Crvena Zvezda": ("Serbia", "Serbian SuperLiga"), "FCSB": ("Romania", "Liga I"), "Fenerbahçe": ("Turkey", "Süper Lig"),
    "Ferencváros": ("Hungary", "NB I"), "Feyenoord": ("Netherlands", "Eredivisie"), "Genk": ("Belgium", "Belgian Pro League"),
    "GNK Dinamo": ("Croatia", "HNL"), "Go Ahead Eagles": ("Netherlands", "Eredivisie"), "Ludogorets": ("Bulgaria", "First League"),
    "Malmö": ("Sweden", "Allsvenskan"), "Maccabi Tel-Aviv": ("Israel", "Premier League"), "Midtjylland": ("Denmark", "Superliga"),
    "Panathinaikos": ("Greece", "Super League Greece"), "PAOK": ("Greece", "Super League Greece"), "Rangers": ("Scotland", "Scottish Premiership"),
    "Salzburg": ("Austria", "Bundesliga"), "Sturm Graz": ("Austria", "Bundesliga"), "Utrecht": ("Netherlands", "Eredivisie"),
    "Viktoria Plzeň": ("Czechia", "Czech First League"), "Young Boys": ("Switzerland", "Swiss Super League"),
    "Noah": ("Armenia", "Premier League"), "SK Rapid": ("Austria", "Bundesliga"), "Zrinjski": ("Bosnia and Herzegovina", "Premier League"),
    "Rijeka": ("Croatia", "HNL"), "AEK Larnaca": ("Cyprus", "First Division"), "Omonoia": ("Cyprus", "First Division"),
    "Sigma Olomouc": ("Czechia", "Czech First League"), "Sparta Praha": ("Czechia", "Czech First League"), "KuPS Kuopio": ("Finland", "Veikkausliiga"),
    "Lincoln Red Imps": ("Gibraltar", "National League"), "AEK Athens": ("Greece", "Super League Greece"), "Breidablik": ("Iceland", "Besta deild karla"),
    "Drita": ("Kosovo", "Superleague"), "Hamrun Spartans": ("Malta", "Premier League"), "AZ Alkmaar": ("Netherlands", "Eredivisie"),
    "Shkëndija": ("North Macedonia", "First League"), "Jagiellonia Białystok": ("Poland", "Ekstraklasa"), "Lech Poznań": ("Poland", "Ekstraklasa"),
    "Legia Warszawa": ("Poland", "Ekstraklasa"), "Raków Częstochowa": ("Poland", "Ekstraklasa"), "Shamrock Rovers": ("Republic of Ireland", "Premier Division"),
    "Shelbourne": ("Republic of Ireland", "Premier Division"), "Universitatea Craiova": ("Romania", "Liga I"), "Aberdeen": ("Scotland", "Scottish Premiership"),
    "Slovan Bratislava": ("Slovakia", "Super Liga"), "Celje": ("Slovenia", "PrvaLiga"), "Häcken": ("Sweden", "Allsvenskan"),
    "Lausanne-Sport": ("Switzerland", "Swiss Super League"), "Samsunspor": ("Turkey", "Süper Lig"), "Dynamo Kyiv": ("Ukraine", "Premier League"),
    "Shakhtar Donetsk": ("Ukraine", "Premier League"),
}


TEAM_COUNTRY_HINTS.update({
    "Leicester City": ("England", "Championship"), "Ipswich Town": ("England", "Championship"),
    "Southampton": ("England", "Championship"), "Norwich City": ("England", "Championship"),
    "Coventry City": ("England", "Championship"), "Middlesbrough": ("England", "Championship"),
    "West Brom": ("England", "Championship"), "Sheffield United": ("England", "Championship"),
    "Sheffield Wednesday": ("England", "Championship"), "Derby County": ("England", "Championship"),
    "Blackburn Rovers": ("England", "Championship"), "Stoke City": ("England", "Championship"),
    "Queens Park Rangers": ("England", "Championship"), "Portsmouth": ("England", "Championship"),
    "Bristol City": ("England", "Championship"), "Watford": ("England", "Championship"),
    "Millwall": ("England", "Championship"), "Hull City": ("England", "Championship"),
    "Swansea City": ("Wales", "Championship"), "Cardiff City": ("Wales", "Championship"),
    "Preston North End": ("England", "Championship"), "Wrexham": ("Wales", "League One"),
    "Plymouth Argyle": ("England", "Championship"), "Birmingham City": ("England", "League One"),
    "Bolton Wanderers": ("England", "League One"), "Charlton Athletic": ("England", "League One"),
    "Reading": ("England", "League One"), "Barnsley": ("England", "League One"),
    "Blackpool": ("England", "League One"), "Peterborough United": ("England", "League One"),
    "Wigan Athletic": ("England", "League One"), "Rotherham United": ("England", "League One"),
    "Wycombe Wanderers": ("England", "League One"), "Oxford United": ("England", "Championship"),
    "Lincoln City": ("England", "League One"), "Port Vale": ("England", "League Two"),
    "Stockport County": ("England", "League One"), "Bradford City": ("England", "League Two"),
    "Mansfield Town": ("England", "League One"), "Walsall": ("England", "League Two"),
    "Doncaster Rovers": ("England", "League Two"), "Notts County": ("England", "League Two"),
    "Gillingham": ("England", "League Two"), "Tranmere Rovers": ("England", "League Two"),
    "AFC Wimbledon": ("England", "League Two"), "Swindon Town": ("England", "League Two"),
    "Newport County": ("Wales", "League Two"), "Grimsby Town": ("England", "League Two"),
    "Carlisle United": ("England", "League Two"), "Salford City": ("England", "League Two"),
    "Harrogate Town": ("England", "League Two"), "Accrington Stanley": ("England", "League Two"),
    "Barrow": ("England", "League Two"), "Morecambe": ("England", "League Two"),
    "Crewe Alexandra": ("England", "League Two"), "Chesterfield": ("England", "League Two"),
    "Bromley": ("England", "League Two"), "Colchester United": ("England", "League Two"),
    "Cheltenham Town": ("England", "League Two"), "Exeter City": ("England", "League One"),
    "Leyton Orient": ("England", "League One"),
})



# ---------------------------------------------------------------------------
# International mode data
# ---------------------------------------------------------------------------
# Player ratings are a game scale only. They are intentionally close-feel,
# editable estimates, not official EA/FC, FIFA, Opta or scouting ratings.
# Squads are representative real-player cores so goals/assists/cards feel real.

def p(name: str, pos: str, rating: int) -> dict:
    return {"name": name, "position": pos, "rating": rating}


# Representative club squad cores for the domestic modes. These are editable game
# estimates so the simulator can pick real-feeling scorers/assisters instead of
# generic generated names for Premier League and FA Cup teams.
CLUB_SQUADS: Dict[str, List[dict]] = {
    "Arsenal": [p("Bukayo Saka", "RW", 89), p("Martin Ødegaard", "AM", 89), p("Kai Havertz", "ST", 84), p("Declan Rice", "DM", 89), p("William Saliba", "CB", 90), p("Gabriel Magalhães", "CB", 87), p("David Raya", "GK", 84), p("Gabriel Martinelli", "LW", 84)],
    "Aston Villa": [p("Ollie Watkins", "ST", 86), p("Morgan Rogers", "AM", 82), p("Youri Tielemans", "CM", 82), p("John McGinn", "CM", 80), p("Pau Torres", "CB", 84), p("Emiliano Martínez", "GK", 88), p("Leon Bailey", "RW", 81), p("Amadou Onana", "DM", 82)],
    "AFC Bournemouth": [p("Antoine Semenyo", "ST", 82), p("Justin Kluivert", "AM", 80), p("Evanilson", "ST", 81), p("Ryan Christie", "CM", 78), p("Lewis Cook", "CM", 78), p("Illia Zabarnyi", "CB", 82), p("Milos Kerkez", "LB", 82), p("Kepa Arrizabalaga", "GK", 81)],
    "Brentford": [p("Bryan Mbeumo", "RW", 84), p("Yoane Wissa", "ST", 82), p("Kevin Schade", "LW", 78), p("Christian Nørgaard", "DM", 80), p("Mikkel Damsgaard", "AM", 78), p("Nathan Collins", "CB", 80), p("Ethan Pinnock", "CB", 78), p("Mark Flekken", "GK", 78)],
    "Brighton": [p("Kaoru Mitoma", "LW", 84), p("João Pedro", "ST", 83), p("Georginio Rutter", "AM", 80), p("Carlos Baleba", "CM", 81), p("Yankuba Minteh", "RW", 79), p("Lewis Dunk", "CB", 80), p("Jan Paul van Hecke", "CB", 79), p("Bart Verbruggen", "GK", 79)],
    "Burnley": [p("Josh Brownhill", "CM", 76), p("Lyle Foster", "ST", 78), p("Zeki Amdouni", "FW", 77), p("Sander Berge", "CM", 80), p("Maxime Estève", "CB", 77), p("James Trafford", "GK", 76), p("Connor Roberts", "RB", 75), p("Jacob Bruun Larsen", "LW", 76)],
    "Chelsea": [p("Cole Palmer", "AM", 89), p("Nicolas Jackson", "ST", 82), p("Christopher Nkunku", "FW", 84), p("Enzo Fernández", "CM", 86), p("Moisés Caicedo", "DM", 86), p("Reece James", "RB", 84), p("Levi Colwill", "CB", 82), p("Robert Sánchez", "GK", 80)],
    "Crystal Palace": [p("Eberechi Eze", "AM", 85), p("Jean-Philippe Mateta", "ST", 82), p("Ismaïla Sarr", "RW", 80), p("Adam Wharton", "CM", 82), p("Jefferson Lerma", "DM", 79), p("Marc Guéhi", "CB", 84), p("Daniel Muñoz", "RB", 80), p("Dean Henderson", "GK", 79)],
    "Everton": [p("Jordan Pickford", "GK", 84), p("Dominic Calvert-Lewin", "ST", 79), p("Dwight McNeil", "LW", 80), p("Iliman Ndiaye", "AM", 80), p("James Tarkowski", "CB", 80), p("Jarrad Branthwaite", "CB", 82), p("Idrissa Gueye", "DM", 79), p("Abdoulaye Doucouré", "CM", 78)],
    "Fulham": [p("Raúl Jiménez", "ST", 79), p("Alex Iwobi", "AM", 80), p("Andreas Pereira", "CM", 80), p("João Palhinha", "DM", 85), p("Emile Smith Rowe", "AM", 80), p("Antonee Robinson", "LB", 81), p("Bernd Leno", "GK", 82), p("Calvin Bassey", "CB", 79)],
    "Leeds United": [p("Ethan Ampadu", "DM", 80), p("Wilfried Gnonto", "LW", 79), p("Joel Piroe", "ST", 78), p("Daniel James", "RW", 78), p("Pascal Struijk", "CB", 78), p("Illan Meslier", "GK", 77), p("Junior Firpo", "LB", 77), p("Brenden Aaronson", "AM", 77)],
    "Liverpool": [p("Mohamed Salah", "RW", 91), p("Darwin Núñez", "ST", 84), p("Luis Díaz", "LW", 86), p("Dominik Szoboszlai", "AM", 87), p("Alexis Mac Allister", "CM", 87), p("Virgil van Dijk", "CB", 90), p("Trent Alexander-Arnold", "RB", 86), p("Alisson", "GK", 89)],
    "Man City": [p("Erling Haaland", "ST", 94), p("Phil Foden", "AM", 88), p("Bernardo Silva", "CM", 88), p("Rodri", "DM", 94), p("Kevin De Bruyne", "CM", 89), p("Rúben Dias", "CB", 88), p("Joško Gvardiol", "CB", 86), p("Ederson", "GK", 88)],
    "Manchester United": [p("Bruno Fernandes", "AM", 88), p("Rasmus Højlund", "ST", 82), p("Marcus Rashford", "LW", 82), p("Alejandro Garnacho", "LW", 81), p("Kobbie Mainoo", "CM", 80), p("Lisandro Martínez", "CB", 84), p("Noussair Mazraoui", "RB", 81), p("André Onana", "GK", 84)],
    "Newcastle": [p("Alexander Isak", "ST", 88), p("Anthony Gordon", "LW", 84), p("Bruno Guimarães", "CM", 86), p("Sandro Tonali", "CM", 84), p("Joelinton", "CM", 82), p("Sven Botman", "CB", 83), p("Kieran Trippier", "RB", 82), p("Nick Pope", "GK", 82)],
    "Nottingham Forest": [p("Morgan Gibbs-White", "AM", 82), p("Chris Wood", "ST", 81), p("Callum Hudson-Odoi", "LW", 79), p("Anthony Elanga", "RW", 80), p("Nicolás Domínguez", "CM", 79), p("Murillo", "CB", 82), p("Nikola Milenković", "CB", 80), p("Matz Sels", "GK", 79)],
    "Sunderland": [p("Granit Xhaka", "DM", 86), p("Jobe Bellingham", "CM", 79), p("Wilson Isidor", "ST", 77), p("Patrick Roberts", "RW", 76), p("Dan Ballard", "CB", 78), p("Anthony Patterson", "GK", 76), p("Trai Hume", "RB", 76), p("Chris Rigg", "CM", 76)],
    "Tottenham": [p("Son Heung-min", "LW", 87), p("James Maddison", "AM", 84), p("Dejan Kulusevski", "RW", 83), p("Dominic Solanke", "ST", 82), p("Rodrigo Bentancur", "CM", 82), p("Cristian Romero", "CB", 86), p("Micky van de Ven", "CB", 84), p("Guglielmo Vicario", "GK", 83)],
    "West Ham United": [p("Jarrod Bowen", "RW", 84), p("Lucas Paquetá", "AM", 84), p("Mohammed Kudus", "RW", 83), p("Tomáš Souček", "CM", 80), p("Edson Álvarez", "DM", 81), p("Max Kilman", "CB", 80), p("Aaron Wan-Bissaka", "RB", 80), p("Alphonse Areola", "GK", 80)],
    "Wolverhampton Wanderers": [p("Matheus Cunha", "FW", 84), p("Jørgen Strand Larsen", "ST", 80), p("Hwang Hee-chan", "LW", 80), p("João Gomes", "CM", 80), p("Mario Lemina", "DM", 79), p("Rayan Aït-Nouri", "LB", 81), p("Toti Gomes", "CB", 78), p("José Sá", "GK", 80)],
    "Leicester City": [p("Jamie Vardy", "ST", 78), p("Stephy Mavididi", "LW", 77), p("Harry Winks", "CM", 77), p("Wout Faes", "CB", 77), p("Mads Hermansen", "GK", 77)],
    "Ipswich Town": [p("Liam Delap", "ST", 78), p("Omari Hutchinson", "RW", 78), p("Leif Davis", "LB", 77), p("Sam Morsy", "CM", 76), p("Arijanet Muric", "GK", 76)],
    "Southampton": [p("Adam Armstrong", "ST", 77), p("Mateus Fernandes", "CM", 77), p("Taylor Harwood-Bellis", "CB", 77), p("Kyle Walker-Peters", "RB", 78), p("Aaron Ramsdale", "GK", 80)],
    "Coventry City": [p("Haji Wright", "ST", 77), p("Ellis Simms", "ST", 76), p("Ben Sheaf", "CM", 76), p("Milan van Ewijk", "RB", 75), p("Bobby Thomas", "CB", 75)],
    "Plymouth Argyle": [p("Morgan Whittaker", "RW", 76), p("Ryan Hardie", "ST", 74), p("Adam Randell", "CM", 73), p("Bali Mumba", "WB", 74), p("Conor Hazard", "GK", 72)],
}


NATIONAL_RATINGS: Dict[str, dict] = {
    "Argentina": {"attack": 93, "midfield": 90, "defence": 88, "star_player": "Lionel Messi", "confederation": "CONMEBOL"},
    "France": {"attack": 94, "midfield": 91, "defence": 91, "star_player": "Kylian Mbappé", "confederation": "UEFA"},
    "England": {"attack": 92, "midfield": 91, "defence": 88, "star_player": "Harry Kane", "confederation": "UEFA"},
    "Spain": {"attack": 91, "midfield": 94, "defence": 89, "star_player": "Lamine Yamal", "confederation": "UEFA"},
    "Brazil": {"attack": 92, "midfield": 88, "defence": 87, "star_player": "Vinícius Júnior", "confederation": "CONMEBOL"},
    "Portugal": {"attack": 91, "midfield": 90, "defence": 88, "star_player": "Cristiano Ronaldo", "confederation": "UEFA"},
    "Netherlands": {"attack": 87, "midfield": 88, "defence": 90, "star_player": "Virgil van Dijk", "confederation": "UEFA"},
    "Germany": {"attack": 89, "midfield": 91, "defence": 87, "star_player": "Jamal Musiala", "confederation": "UEFA"},
    "Belgium": {"attack": 87, "midfield": 88, "defence": 83, "star_player": "Kevin De Bruyne", "confederation": "UEFA"},
    "Italy": {"attack": 84, "midfield": 87, "defence": 88, "star_player": "Gianluigi Donnarumma", "confederation": "UEFA"},
    "Croatia": {"attack": 84, "midfield": 88, "defence": 84, "star_player": "Luka Modrić", "confederation": "UEFA"},
    "Uruguay": {"attack": 86, "midfield": 87, "defence": 86, "star_player": "Federico Valverde", "confederation": "CONMEBOL"},
    "Colombia": {"attack": 86, "midfield": 84, "defence": 82, "star_player": "Luis Díaz", "confederation": "CONMEBOL"},
    "Ecuador": {"attack": 81, "midfield": 82, "defence": 84, "star_player": "Moisés Caicedo", "confederation": "CONMEBOL"},
    "Paraguay": {"attack": 77, "midfield": 78, "defence": 79, "star_player": "Miguel Almirón", "confederation": "CONMEBOL"},
    "Morocco": {"attack": 84, "midfield": 84, "defence": 86, "star_player": "Achraf Hakimi", "confederation": "CAF"},
    "United States": {"attack": 81, "midfield": 82, "defence": 79, "star_player": "Christian Pulisic", "confederation": "CONCACAF"},
    "Mexico": {"attack": 80, "midfield": 80, "defence": 79, "star_player": "Santiago Giménez", "confederation": "CONCACAF"},
    "Canada": {"attack": 80, "midfield": 78, "defence": 77, "star_player": "Alphonso Davies", "confederation": "CONCACAF"},
    "Japan": {"attack": 83, "midfield": 84, "defence": 82, "star_player": "Takefusa Kubo", "confederation": "AFC"},
    "South Korea": {"attack": 82, "midfield": 81, "defence": 81, "star_player": "Son Heung-min", "confederation": "AFC"},
    "Australia": {"attack": 77, "midfield": 77, "defence": 78, "star_player": "Harry Souttar", "confederation": "AFC"},
    "Iran": {"attack": 80, "midfield": 79, "defence": 78, "star_player": "Mehdi Taremi", "confederation": "AFC"},
    "Saudi Arabia": {"attack": 78, "midfield": 77, "defence": 76, "star_player": "Salem Al-Dawsari", "confederation": "AFC"},
    "Qatar": {"attack": 77, "midfield": 76, "defence": 75, "star_player": "Akram Afif", "confederation": "AFC"},
    "Uzbekistan": {"attack": 76, "midfield": 76, "defence": 77, "star_player": "Eldor Shomurodov", "confederation": "AFC"},
    "Jordan": {"attack": 75, "midfield": 74, "defence": 73, "star_player": "Mousa Al-Taamari", "confederation": "AFC"},
    "New Zealand": {"attack": 74, "midfield": 73, "defence": 74, "star_player": "Chris Wood", "confederation": "OFC"},
    "Senegal": {"attack": 84, "midfield": 82, "defence": 84, "star_player": "Sadio Mané", "confederation": "CAF"},
    "Egypt": {"attack": 82, "midfield": 79, "defence": 78, "star_player": "Mohamed Salah", "confederation": "CAF"},
    "Algeria": {"attack": 80, "midfield": 80, "defence": 78, "star_player": "Riyad Mahrez", "confederation": "CAF"},
    "Tunisia": {"attack": 75, "midfield": 76, "defence": 77, "star_player": "Ellyes Skhiri", "confederation": "CAF"},
    "Ghana": {"attack": 78, "midfield": 78, "defence": 76, "star_player": "Mohammed Kudus", "confederation": "CAF"},
    "Cape Verde": {"attack": 73, "midfield": 72, "defence": 72, "star_player": "Ryan Mendes", "confederation": "CAF"},
    "South Africa": {"attack": 74, "midfield": 75, "defence": 76, "star_player": "Lyle Foster", "confederation": "CAF"},
    "Ivory Coast": {"attack": 81, "midfield": 80, "defence": 79, "star_player": "Franck Kessié", "confederation": "CAF"},
    "Cameroon": {"attack": 79, "midfield": 78, "defence": 79, "star_player": "André Onana", "confederation": "CAF"},
    "Austria": {"attack": 82, "midfield": 84, "defence": 82, "star_player": "Marcel Sabitzer", "confederation": "UEFA"},
    "Norway": {"attack": 86, "midfield": 84, "defence": 78, "star_player": "Erling Haaland", "confederation": "UEFA"},
    "Scotland": {"attack": 78, "midfield": 81, "defence": 79, "star_player": "Scott McTominay", "confederation": "UEFA"},
    "Turkey": {"attack": 83, "midfield": 84, "defence": 80, "star_player": "Arda Güler", "confederation": "UEFA"},
    "Czech Republic": {"attack": 79, "midfield": 80, "defence": 80, "star_player": "Patrik Schick", "confederation": "UEFA"},
    "Switzerland": {"attack": 80, "midfield": 84, "defence": 83, "star_player": "Granit Xhaka", "confederation": "UEFA"},
    "Denmark": {"attack": 81, "midfield": 83, "defence": 82, "star_player": "Rasmus Højlund", "confederation": "UEFA"},
    "Poland": {"attack": 80, "midfield": 78, "defence": 77, "star_player": "Robert Lewandowski", "confederation": "UEFA"},
    "Serbia": {"attack": 82, "midfield": 80, "defence": 79, "star_player": "Dušan Vlahović", "confederation": "UEFA"},
    "Iraq": {"attack": 74, "midfield": 73, "defence": 72, "star_player": "Aymen Hussein", "confederation": "AFC"},
    "Panama": {"attack": 74, "midfield": 74, "defence": 73, "star_player": "Adalberto Carrasquilla", "confederation": "CONCACAF"},
    "Curaçao": {"attack": 72, "midfield": 72, "defence": 71, "star_player": "Juninho Bacuna", "confederation": "CONCACAF"},
    "Haiti": {"attack": 73, "midfield": 72, "defence": 71, "star_player": "Duckens Nazon", "confederation": "CONCACAF"},
    "Hungary": {"attack": 80, "midfield": 81, "defence": 78, "star_player": "Dominik Szoboszlai", "confederation": "UEFA"},
    "Albania": {"attack": 75, "midfield": 75, "defence": 76, "star_player": "Armando Broja", "confederation": "UEFA"},
    "Slovenia": {"attack": 78, "midfield": 77, "defence": 79, "star_player": "Benjamin Šeško", "confederation": "UEFA"},
    "Romania": {"attack": 76, "midfield": 77, "defence": 77, "star_player": "Radu Drăgușin", "confederation": "UEFA"},
    "Slovakia": {"attack": 76, "midfield": 78, "defence": 80, "star_player": "Milan Škriniar", "confederation": "UEFA"},
    "Ukraine": {"attack": 81, "midfield": 80, "defence": 79, "star_player": "Artem Dovbyk", "confederation": "UEFA"},
    "Georgia": {"attack": 78, "midfield": 75, "defence": 74, "star_player": "Khvicha Kvaratskhelia", "confederation": "UEFA"},
}

NATIONAL_SQUADS: Dict[str, List[dict]] = {
    "Argentina": [p("Lionel Messi", "RW", 94), p("Lautaro Martínez", "ST", 89), p("Julián Álvarez", "ST", 86), p("Alexis Mac Allister", "CM", 87), p("Enzo Fernández", "CM", 86), p("Rodrigo De Paul", "CM", 85), p("Cristian Romero", "CB", 87), p("Emiliano Martínez", "GK", 88)],
    "France": [p("Kylian Mbappé", "ST", 95), p("Antoine Griezmann", "AM", 88), p("Ousmane Dembélé", "RW", 88), p("Aurélien Tchouaméni", "DM", 88), p("Eduardo Camavinga", "CM", 87), p("William Saliba", "CB", 90), p("Theo Hernández", "LB", 87), p("Mike Maignan", "GK", 89)],
    "England": [p("Harry Kane", "ST", 92), p("Jude Bellingham", "AM", 93), p("Bukayo Saka", "RW", 89), p("Phil Foden", "AM", 88), p("Declan Rice", "DM", 89), p("Cole Palmer", "AM", 88), p("John Stones", "CB", 86), p("Jordan Pickford", "GK", 84)],
    "Spain": [p("Lamine Yamal", "RW", 90), p("Pedri", "CM", 88), p("Nico Williams", "LW", 86), p("Rodri", "DM", 94), p("Dani Olmo", "AM", 86), p("Dani Carvajal", "RB", 86), p("Marc Cucurella", "LB", 84), p("Unai Simón", "GK", 85)],
    "Brazil": [p("Vinícius Júnior", "LW", 92), p("Rodrygo", "RW", 88), p("Neymar", "AM", 88), p("Raphinha", "RW", 87), p("Bruno Guimarães", "CM", 86), p("Casemiro", "DM", 84), p("Marquinhos", "CB", 87), p("Alisson", "GK", 89)],
    "Portugal": [p("Cristiano Ronaldo", "ST", 89), p("Bernardo Silva", "AM", 88), p("Bruno Fernandes", "AM", 88), p("Vitinha", "CM", 88), p("Rafael Leão", "LW", 86), p("João Félix", "FW", 83), p("Rúben Dias", "CB", 90), p("Diogo Costa", "GK", 86)],
    "Netherlands": [p("Virgil van Dijk", "CB", 90), p("Frenkie de Jong", "CM", 88), p("Cody Gakpo", "LW", 85), p("Memphis Depay", "ST", 83), p("Xavi Simons", "AM", 84), p("Ryan Gravenberch", "CM", 85), p("Matthijs de Ligt", "CB", 85), p("Bart Verbruggen", "GK", 82)],
    "Germany": [p("Jamal Musiala", "AM", 91), p("Florian Wirtz", "AM", 91), p("Kai Havertz", "ST", 85), p("Joshua Kimmich", "DM", 88), p("Leroy Sané", "RW", 86), p("Antonio Rüdiger", "CB", 88), p("Nico Schlotterbeck", "CB", 84), p("Marc-André ter Stegen", "GK", 87)],
    "Belgium": [p("Kevin De Bruyne", "CM", 91), p("Romelu Lukaku", "ST", 86), p("Jérémy Doku", "LW", 84), p("Youri Tielemans", "CM", 83), p("Amadou Onana", "DM", 84), p("Loïs Openda", "ST", 84), p("Thibaut Courtois", "GK", 90), p("Arthur Theate", "CB", 81)],
    "Italy": [p("Gianluigi Donnarumma", "GK", 89), p("Nicolò Barella", "CM", 88), p("Alessandro Bastoni", "CB", 88), p("Federico Chiesa", "RW", 84), p("Sandro Tonali", "CM", 86), p("Federico Dimarco", "LB", 86), p("Mateo Retegui", "ST", 82), p("Davide Frattesi", "CM", 82)],
    "Croatia": [p("Luka Modrić", "CM", 87), p("Mateo Kovačić", "CM", 86), p("Joško Gvardiol", "CB", 88), p("Ivan Perišić", "LW", 82), p("Andrej Kramarić", "FW", 83), p("Marcelo Brozović", "DM", 84), p("Dominik Livaković", "GK", 82), p("Lovro Majer", "AM", 81)],
    "Uruguay": [p("Federico Valverde", "CM", 91), p("Darwin Núñez", "ST", 85), p("Ronald Araújo", "CB", 88), p("Rodrigo Bentancur", "CM", 84), p("Manuel Ugarte", "DM", 84), p("Nicolás de la Cruz", "CM", 82), p("José Giménez", "CB", 84), p("Sergio Rochet", "GK", 80)],
    "Colombia": [p("Luis Díaz", "LW", 88), p("James Rodríguez", "AM", 84), p("Jefferson Lerma", "DM", 81), p("Jhon Durán", "ST", 83), p("Davinson Sánchez", "CB", 82), p("Daniel Muñoz", "RB", 82), p("Juan Cuadrado", "RW", 80), p("Camilo Vargas", "GK", 80)],
    "Ecuador": [p("Moisés Caicedo", "DM", 86), p("Piero Hincapié", "CB", 84), p("Pervis Estupiñán", "LB", 82), p("Willian Pacho", "CB", 83), p("Kendry Páez", "AM", 80), p("Enner Valencia", "ST", 80), p("Gonzalo Plata", "RW", 78), p("Alexander Domínguez", "GK", 76)],
    "Paraguay": [p("Miguel Almirón", "AM", 80), p("Julio Enciso", "FW", 80), p("Ramón Sosa", "LW", 78), p("Omar Alderete", "CB", 78), p("Gustavo Gómez", "CB", 80), p("Mathías Villasanti", "CM", 78), p("Diego Gómez", "CM", 79), p("Roberto Fernández", "GK", 74)],
    "Morocco": [p("Achraf Hakimi", "RB", 88), p("Yassine Bounou", "GK", 86), p("Hakim Ziyech", "RW", 83), p("Azzedine Ounahi", "CM", 82), p("Youssef En-Nesyri", "ST", 83), p("Sofyan Amrabat", "DM", 82), p("Noussair Mazraoui", "FB", 84), p("Nayef Aguerd", "CB", 82)],
    "United States": [p("Christian Pulisic", "LW", 86), p("Weston McKennie", "CM", 82), p("Giovanni Reyna", "AM", 81), p("Tyler Adams", "DM", 80), p("Yunus Musah", "CM", 79), p("Folarin Balogun", "ST", 81), p("Sergiño Dest", "RB", 80), p("Matt Turner", "GK", 78)],
    "Mexico": [p("Edson Álvarez", "DM", 82), p("Santiago Giménez", "ST", 83), p("Raúl Jiménez", "ST", 80), p("Hirving Lozano", "RW", 81), p("Alexis Vega", "LW", 78), p("César Montes", "CB", 79), p("Jorge Sánchez", "RB", 77), p("Guillermo Ochoa", "GK", 78)],
    "Canada": [p("Alphonso Davies", "LB", 86), p("Jonathan David", "ST", 84), p("Tajon Buchanan", "RW", 79), p("Stephen Eustáquio", "CM", 79), p("Cyle Larin", "ST", 78), p("Ismaël Koné", "CM", 78), p("Moïse Bombito", "CB", 77), p("Maxime Crépeau", "GK", 76)],
    "Japan": [p("Takefusa Kubo", "RW", 85), p("Kaoru Mitoma", "LW", 84), p("Takumi Minamino", "AM", 81), p("Wataru Endo", "DM", 82), p("Daichi Kamada", "AM", 81), p("Takehiro Tomiyasu", "CB", 84), p("Junya Ito", "RW", 80), p("Zion Suzuki", "GK", 78)],
    "South Korea": [p("Son Heung-min", "LW", 88), p("Lee Kang-in", "AM", 83), p("Kim Min-jae", "CB", 88), p("Hwang Hee-chan", "FW", 81), p("Hwang In-beom", "CM", 80), p("Cho Gue-sung", "ST", 78), p("Seol Young-woo", "FB", 77), p("Jo Hyeon-woo", "GK", 77)],
    "Australia": [p("Harry Souttar", "CB", 78), p("Jackson Irvine", "CM", 78), p("Craig Goodwin", "LW", 76), p("Conor Metcalfe", "CM", 75), p("Mitchell Duke", "ST", 75), p("Aziz Behich", "LB", 75), p("Mathew Ryan", "GK", 78), p("Keanu Baccus", "CM", 75)],
    "Iran": [p("Mehdi Taremi", "ST", 83), p("Sardar Azmoun", "ST", 81), p("Alireza Jahanbakhsh", "RW", 79), p("Ali Gholizadeh", "AM", 77), p("Saeid Ezatolahi", "DM", 77), p("Hossein Hosseini", "GK", 76), p("Alireza Beiranvand", "GK", 77), p("Sadegh Moharrami", "RB", 76)],
    "Saudi Arabia": [p("Salem Al-Dawsari", "LW", 80), p("Firas Al-Buraikan", "ST", 77), p("Mohamed Kanno", "CM", 77), p("Salman Al-Faraj", "CM", 76), p("Mohammed Al-Owais", "GK", 76), p("Sultan Al-Ghannam", "RB", 76), p("Hassan Tambakti", "CB", 76), p("Saleh Al-Shehri", "ST", 75)],
    "Qatar": [p("Akram Afif", "LW", 80), p("Almoez Ali", "ST", 78), p("Hassan Al-Haydos", "AM", 76), p("Pedro Miguel", "RB", 75), p("Meshaal Barsham", "GK", 76), p("Bassam Al-Rawi", "CB", 75), p("Abdulaziz Hatem", "CM", 75), p("Tarek Salman", "CB", 74)],
    "Uzbekistan": [p("Eldor Shomurodov", "ST", 79), p("Abdukodir Khusanov", "CB", 80), p("Abbosbek Fayzullaev", "AM", 78), p("Jaloliddin Masharipov", "LW", 76), p("Oston Urunov", "AM", 75), p("Utkir Yusupov", "GK", 74), p("Odiljon Khamrobekov", "DM", 74), p("Sherzod Nasrullayev", "LB", 74)],
    "Jordan": [p("Mousa Al-Taamari", "RW", 79), p("Yazan Al-Naimat", "ST", 77), p("Nizar Al-Rashdan", "CM", 75), p("Noor Al-Rawabdeh", "DM", 74), p("Yazid Abu Laila", "GK", 74), p("Ali Olwan", "FW", 74), p("Baha Faisal", "ST", 73), p("Salim Obaid", "CB", 72)],
    "New Zealand": [p("Chris Wood", "ST", 81), p("Sarpreet Singh", "AM", 75), p("Matthew Garbett", "CM", 74), p("Liberato Cacace", "LB", 75), p("Joe Bell", "CM", 74), p("Michael Boxall", "CB", 73), p("Tyler Bindon", "CB", 74), p("Max Crocombe", "GK", 73)],
    "Senegal": [p("Sadio Mané", "LW", 86), p("Kalidou Koulibaly", "CB", 86), p("Édouard Mendy", "GK", 82), p("Pape Matar Sarr", "CM", 82), p("Nicolas Jackson", "ST", 83), p("Idrissa Gueye", "DM", 80), p("Ismaïla Sarr", "RW", 81), p("Iliman Ndiaye", "AM", 80)],
    "Egypt": [p("Mohamed Salah", "RW", 91), p("Omar Marmoush", "ST", 85), p("Trézéguet", "LW", 78), p("Mohamed Elneny", "DM", 77), p("Mostafa Mohamed", "ST", 78), p("Ahmed Hegazy", "CB", 78), p("Mohamed El Shenawy", "GK", 78), p("Hamdi Fathi", "CM", 77)],
    "Algeria": [p("Riyad Mahrez", "RW", 84), p("Houssem Aouar", "CM", 80), p("Ismaël Bennacer", "CM", 83), p("Amine Gouiri", "FW", 80), p("Ramy Bensebaini", "CB", 79), p("Youcef Atal", "RB", 77), p("Aïssa Mandi", "CB", 77), p("Baghdad Bounedjah", "ST", 77)],
    "Tunisia": [p("Youssef Msakni", "LW", 77), p("Ellyes Skhiri", "DM", 81), p("Aïssa Laïdouni", "CM", 77), p("Montassar Talbi", "CB", 78), p("Bechir Ben Saïd", "GK", 75), p("Naïm Sliti", "AM", 75), p("Mohamed Dräger", "RB", 74), p("Seifeddine Jaziri", "ST", 74)],
    "Ghana": [p("Mohammed Kudus", "AM", 85), p("Thomas Partey", "DM", 84), p("Iñaki Williams", "ST", 82), p("Jordan Ayew", "FW", 78), p("Antoine Semenyo", "ST", 80), p("Tariq Lamptey", "RB", 78), p("Mohammed Salisu", "CB", 79), p("Alexander Djiku", "CB", 78)],
    "Cape Verde": [p("Ryan Mendes", "LW", 76), p("Bebé", "FW", 75), p("Garry Rodrigues", "RW", 75), p("Vozinha", "GK", 73), p("Stopira", "LB", 72), p("Logan Costa", "CB", 77), p("Jovane Cabral", "LW", 75), p("Jamiro Monteiro", "CM", 74)],
    "South Africa": [p("Lyle Foster", "ST", 78), p("Percy Tau", "RW", 77), p("Ronwen Williams", "GK", 79), p("Teboho Mokoena", "CM", 77), p("Themba Zwane", "AM", 76), p("Mothobi Mvala", "CB", 75), p("Khuliso Mudau", "RB", 75), p("Aubrey Modiba", "LB", 75)],
    "Ivory Coast": [p("Sébastien Haller", "ST", 81), p("Simon Adingra", "LW", 80), p("Franck Kessié", "CM", 84), p("Seko Fofana", "CM", 82), p("Ibrahim Sangaré", "DM", 81), p("Serge Aurier", "RB", 77), p("Ousmane Diomande", "CB", 81), p("Yahia Fofana", "GK", 76)],
    "Cameroon": [p("André Onana", "GK", 84), p("André-Frank Zambo Anguissa", "CM", 84), p("Bryan Mbeumo", "RW", 84), p("Vincent Aboubakar", "ST", 80), p("Eric Maxim Choupo-Moting", "FW", 78), p("Nouhou Tolo", "LB", 76), p("Jean-Charles Castelletto", "CB", 78), p("Georges-Kévin Nkoudou", "LW", 77)],
    "Austria": [p("David Alaba", "CB", 84), p("Marcel Sabitzer", "CM", 84), p("Marko Arnautović", "ST", 78), p("Christoph Baumgartner", "AM", 80), p("Konrad Laimer", "CM", 82), p("Nicolas Seiwald", "DM", 79), p("Kevin Danso", "CB", 81), p("Patrick Pentz", "GK", 77)],
    "Norway": [p("Erling Haaland", "ST", 94), p("Martin Ødegaard", "AM", 90), p("Alexander Sørloth", "ST", 84), p("Oscar Bobb", "RW", 80), p("Sander Berge", "CM", 80), p("Kristoffer Ajer", "CB", 78), p("Julian Ryerson", "RB", 80), p("Ørjan Nyland", "GK", 76)],
    "Scotland": [p("Scott McTominay", "CM", 82), p("Andrew Robertson", "LB", 85), p("John McGinn", "CM", 80), p("Billy Gilmour", "CM", 79), p("Kieran Tierney", "CB", 81), p("Ché Adams", "ST", 77), p("Callum McGregor", "CM", 79), p("Angus Gunn", "GK", 76)],
    "Turkey": [p("Hakan Çalhanoğlu", "CM", 87), p("Arda Güler", "AM", 84), p("Kenan Yıldız", "LW", 82), p("Kerem Aktürkoğlu", "LW", 81), p("Zeki Çelik", "RB", 77), p("Merih Demiral", "CB", 80), p("Orkun Kökçü", "CM", 82), p("Mert Günok", "GK", 77)],
    "Czech Republic": [p("Patrik Schick", "ST", 82), p("Tomáš Souček", "CM", 82), p("Vladimír Coufal", "RB", 79), p("Adam Hložek", "FW", 79), p("Ladislav Krejčí", "CB", 79), p("Antonín Barák", "AM", 78), p("Jindřich Staněk", "GK", 76), p("David Jurásek", "LB", 76)],
    "Switzerland": [p("Granit Xhaka", "DM", 87), p("Manuel Akanji", "CB", 86), p("Yann Sommer", "GK", 85), p("Breel Embolo", "ST", 80), p("Dan Ndoye", "RW", 79), p("Ruben Vargas", "LW", 79), p("Denis Zakaria", "DM", 81), p("Remo Freuler", "CM", 80)],
    "Denmark": [p("Christian Eriksen", "CM", 82), p("Rasmus Højlund", "ST", 82), p("Pierre-Emile Højbjerg", "DM", 84), p("Andreas Christensen", "CB", 84), p("Kasper Schmeichel", "GK", 80), p("Mikkel Damsgaard", "AM", 78), p("Joakim Mæhle", "WB", 80), p("Jannik Vestergaard", "CB", 79)],
    "Poland": [p("Robert Lewandowski", "ST", 88), p("Piotr Zieliński", "CM", 83), p("Jakub Kiwior", "CB", 79), p("Nicola Zalewski", "WB", 78), p("Sebastian Szymański", "AM", 80), p("Matty Cash", "RB", 79), p("Karol Świderski", "ST", 77), p("Łukasz Skorupski", "GK", 79)],
    "Serbia": [p("Dušan Vlahović", "ST", 84), p("Aleksandar Mitrović", "ST", 83), p("Sergej Milinković-Savić", "CM", 85), p("Dušan Tadić", "AM", 82), p("Filip Kostić", "WB", 81), p("Strahinja Pavlović", "CB", 80), p("Nikola Milenković", "CB", 80), p("Predrag Rajković", "GK", 79)],
    "Iraq": [p("Aymen Hussein", "ST", 77), p("Ali Jasim", "LW", 76), p("Zidane Iqbal", "CM", 76), p("Mohanad Ali", "ST", 74), p("Bashar Resan", "AM", 74), p("Amir Al-Ammari", "CM", 73), p("Jalal Hassan", "GK", 73), p("Hussein Ali", "RB", 72)],
    "Panama": [p("Adalberto Carrasquilla", "CM", 77), p("Yoel Bárcenas", "RW", 75), p("José Fajardo", "ST", 74), p("Aníbal Godoy", "DM", 74), p("Michael Murillo", "RB", 76), p("Fidel Escobar", "CB", 74), p("Orlando Mosquera", "GK", 73), p("Éric Davis", "LB", 73)],
    "Curaçao": [p("Juninho Bacuna", "CM", 76), p("Leandro Bacuna", "CM", 74), p("Jürgen Locadia", "ST", 75), p("Kenji Gorré", "LW", 73), p("Eloy Room", "GK", 73), p("Sherel Floranus", "RB", 73), p("Rangelo Janga", "ST", 72), p("Cuco Martina", "CB", 72)],
    "Haiti": [p("Duckens Nazon", "ST", 76), p("Frantzdy Pierrot", "ST", 75), p("Jean-Ricner Bellegarde", "CM", 78), p("Danley Jean Jacques", "DM", 75), p("Derrick Etienne Jr", "LW", 73), p("Johny Placide", "GK", 72), p("Wilde-Donald Guerrier", "LB", 72), p("Ricardo Adé", "CB", 73)],
    "Hungary": [p("Dominik Szoboszlai", "AM", 87), p("Roland Sallai", "RW", 80), p("Willi Orbán", "CB", 82), p("Péter Gulácsi", "GK", 81), p("Milos Kerkez", "LB", 82), p("Ádám Nagy", "DM", 77), p("Barnabás Varga", "ST", 78), p("Dénes Dibusz", "GK", 76)],
    "Albania": [p("Armando Broja", "ST", 78), p("Jasir Asani", "RW", 76), p("Nedim Bajrami", "AM", 77), p("Elseid Hysaj", "RB", 77), p("Berat Djimsiti", "CB", 80), p("Ylber Ramadani", "DM", 76), p("Thomas Strakosha", "GK", 77), p("Rey Manaj", "ST", 76)],
    "Slovenia": [p("Benjamin Šeško", "ST", 83), p("Jan Oblak", "GK", 90), p("Jaka Bijol", "CB", 80), p("Sandi Lovrić", "CM", 77), p("Adam Gnezda Čerin", "CM", 77), p("Timi Max Elšnik", "CM", 76), p("Petar Stojanović", "RB", 75), p("Jan Mlakar", "FW", 75)],
    "Romania": [p("Radu Drăgușin", "CB", 82), p("Nicolae Stanciu", "AM", 78), p("Dennis Man", "RW", 78), p("Valentin Mihăilă", "LW", 77), p("Marius Marin", "DM", 76), p("Ianis Hagi", "AM", 76), p("Florin Niță", "GK", 76), p("Andrei Burcă", "CB", 76)],
    "Slovakia": [p("Milan Škriniar", "CB", 84), p("Stanislav Lobotka", "CM", 85), p("Martin Dúbravka", "GK", 79), p("Dávid Hancko", "CB", 82), p("Lukáš Haraslín", "LW", 78), p("Tomáš Suslov", "AM", 76), p("Róbert Boženík", "ST", 75), p("Juraj Kucka", "CM", 75)],
    "Ukraine": [p("Artem Dovbyk", "ST", 84), p("Viktor Tsygankov", "RW", 82), p("Mykhailo Mudryk", "LW", 80), p("Oleksandr Zinchenko", "CM", 82), p("Georgiy Sudakov", "AM", 81), p("Illia Zabarnyi", "CB", 82), p("Anatoliy Trubin", "GK", 82), p("Roman Yaremchuk", "ST", 78)],
    "Georgia": [p("Khvicha Kvaratskhelia", "LW", 88), p("Giorgi Mamardashvili", "GK", 85), p("Georges Mikautadze", "ST", 81), p("Giorgi Chakvetadze", "AM", 77), p("Giorgi Kochorashvili", "CM", 76), p("Otar Kiteishvili", "CM", 76), p("Guram Kashia", "CB", 75), p("Solomon Kverkvelia", "CB", 74)],
}

WORLD_CUP_2026_TEAMS = [
    "Canada", "Mexico", "United States", "Japan", "New Zealand", "Iran", "Argentina", "Uzbekistan",
    "South Korea", "Jordan", "Australia", "Brazil", "Ecuador", "Uruguay", "Paraguay", "Colombia",
    "Morocco", "Tunisia", "Egypt", "Algeria", "Ghana", "Cape Verde", "South Africa", "Senegal",
    "Ivory Coast", "Cameroon", "England", "France", "Spain", "Portugal", "Netherlands", "Belgium",
    "Germany", "Croatia", "Austria", "Norway", "Scotland", "Turkey", "Czech Republic", "Switzerland",
    "Denmark", "Poland", "Iraq", "Qatar", "Saudi Arabia", "Panama", "Curaçao", "Haiti",
]

EURO_2024_TEAMS = [
    "Germany", "Scotland", "Hungary", "Switzerland", "Spain", "Croatia", "Italy", "Albania",
    "Slovenia", "Denmark", "Serbia", "England", "Poland", "Netherlands", "Austria", "France",
    "Belgium", "Slovakia", "Romania", "Ukraine", "Turkey", "Georgia", "Portugal", "Czech Republic",
]

INTERNATIONAL = {
    "World Cup 2026-style": {
        "teams": WORLD_CUP_2026_TEAMS,
        "groups": 12,
        "advance_top": 2,
        "best_thirds": 8,
        "format_note": "48 teams, 12 groups of four, top two plus eight best third-placed teams reach the Round of 32.",
    },
    "EURO / European Championship": {
        "teams": EURO_2024_TEAMS,
        "groups": 6,
        "advance_top": 2,
        "best_thirds": 4,
        "format_note": "24 teams, six groups of four, top two plus four best third-placed teams reach the Round of 16.",
    },
}


def national_team(name: str) -> dict:
    rating = NATIONAL_RATINGS[name]
    team = Team(
        name=name,
        country=name,
        league="International",
        attack=rating["attack"],
        midfield=rating["midfield"],
        defence=rating["defence"],
        star_player=rating["star_player"],
    ).to_dict()
    team["id"] = _slug(name)
    team["confederation"] = rating.get("confederation", "International")
    team["players"] = NATIONAL_SQUADS.get(name, [])
    team["is_national_team"] = True
    return enrich_team(team)


def _slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")


COUNTRY_FLAGS = {
    "England": "🏴", "Wales": "🏴", "Scotland": "🏴", "Republic of Ireland": "🇮🇪",
    "Spain": "🇪🇸", "Italy": "🇮🇹", "Germany": "🇩🇪", "France": "🇫🇷", "Portugal": "🇵🇹",
    "Netherlands": "🇳🇱", "Belgium": "🇧🇪", "Brazil": "🇧🇷", "USA": "🇺🇸", "United States": "🇺🇸",
    "Saudi Arabia": "🇸🇦", "Turkey": "🇹🇷", "Greece": "🇬🇷", "Switzerland": "🇨🇭", "Austria": "🇦🇹",
    "Czechia": "🇨🇿", "Czech Republic": "🇨🇿", "Ukraine": "🇺🇦", "Norway": "🇳🇴", "Denmark": "🇩🇰",
    "Sweden": "🇸🇪", "Poland": "🇵🇱", "Romania": "🇷🇴", "Serbia": "🇷🇸", "Croatia": "🇭🇷",
    "Argentina": "🇦🇷", "Canada": "🇨🇦", "Mexico": "🇲🇽", "Japan": "🇯🇵", "New Zealand": "🇳🇿",
    "Iran": "🇮🇷", "Uzbekistan": "🇺🇿", "South Korea": "🇰🇷", "Jordan": "🇯🇴", "Australia": "🇦🇺",
    "Ecuador": "🇪🇨", "Uruguay": "🇺🇾", "Paraguay": "🇵🇾", "Colombia": "🇨🇴", "Morocco": "🇲🇦",
    "Tunisia": "🇹🇳", "Egypt": "🇪🇬", "Algeria": "🇩🇿", "Ghana": "🇬🇭", "Cape Verde": "🇨🇻",
    "South Africa": "🇿🇦", "Senegal": "🇸🇳", "Ivory Coast": "🇨🇮", "Cameroon": "🇨🇲", "Iraq": "🇮🇶",
    "Qatar": "🇶🇦", "Panama": "🇵🇦", "Curaçao": "🇨🇼", "Haiti": "🇭🇹", "Hungary": "🇭🇺",
    "Albania": "🇦🇱", "Slovenia": "🇸🇮", "Slovakia": "🇸🇰", "Georgia": "🇬🇪", "World": "🏳️",
}

TEAM_COLOURS = {
    "Arsenal": ("#dc2626", "#ffffff"), "Liverpool": ("#b91c1c", "#facc15"), "Man City": ("#38bdf8", "#ffffff"),
    "Manchester United": ("#dc2626", "#111827"), "Chelsea": ("#1d4ed8", "#ffffff"), "Tottenham": ("#f8fafc", "#0f172a"),
    "Newcastle": ("#111827", "#f8fafc"), "Aston Villa": ("#7f1d1d", "#60a5fa"), "Everton": ("#2563eb", "#ffffff"),
    "West Ham United": ("#7f1d1d", "#93c5fd"), "Brighton": ("#2563eb", "#ffffff"), "Crystal Palace": ("#1d4ed8", "#ef4444"),
    "Real Madrid": ("#f8fafc", "#facc15"), "Barcelona": ("#7f1d1d", "#1d4ed8"), "Bayern Munich": ("#dc2626", "#ffffff"),
    "Paris Saint-Germain": ("#1e3a8a", "#ef4444"), "Inter Milan": ("#1d4ed8", "#111827"), "AC Milan": ("#dc2626", "#111827"),
}


def _abbr(name: str) -> str:
    words = [w for w in name.replace("AFC", "").replace("FC", "").replace("United", "Utd").split() if w]
    if len(words) == 1:
        return words[0][:3].upper()
    return "".join(w[0] for w in words[:3]).upper()[:3]


def _colour_pair(name: str) -> tuple[str, str]:
    if name in TEAM_COLOURS:
        return TEAM_COLOURS[name]
    palette = [
        ("#16a34a", "#f8fafc"), ("#0ea5e9", "#f8fafc"), ("#9333ea", "#f8fafc"),
        ("#f97316", "#111827"), ("#e11d48", "#f8fafc"), ("#facc15", "#111827"),
        ("#14b8a6", "#0f172a"), ("#64748b", "#f8fafc"),
    ]
    return palette[sum(ord(c) for c in name) % len(palette)]


def enrich_team(team: dict) -> dict:
    primary, secondary = _colour_pair(team["name"])
    team["flag"] = COUNTRY_FLAGS.get(team.get("country"), COUNTRY_FLAGS.get(team.get("name"), "🏳️"))
    team["abbr"] = _abbr(team["name"])
    team["crest_primary"] = primary
    team["crest_secondary"] = secondary
    return team


def default_team(name: str) -> Team:
    country, league = TEAM_COUNTRY_HINTS.get(name, ("World", "Custom / Other"))
    base = COUNTRY_DEFAULTS.get(country, 68)
    # Small deterministic wobble so generic teams don't all feel identical.
    wobble = (sum(ord(c) for c in name) % 7) - 3
    overall = max(55, min(88, base + wobble))
    return Team(
        name=name,
        country=country,
        league=league,
        attack=max(50, min(99, overall + ((len(name) % 5) - 2))),
        midfield=max(50, min(99, overall + ((len(name) % 3) - 1))),
        defence=max(50, min(99, overall - ((len(name) % 4) - 1))),
        star_player=f"{name} Star",
    )


def build_team_database() -> List[dict]:
    names = set(RATINGS.keys()) | set(UCL_2025_26) | set(UEL_2025_26) | set(UECL_2025_26) | set(PREMIER_LEAGUE_2025_26) | set(FA_CUP_SEED_TEAMS)
    built: List[dict] = []
    for name in sorted(names):
        if name in RATINGS:
            t = Team(name=name, **RATINGS[name])
        else:
            t = default_team(name)
        team = t.to_dict() | {"id": _slug(t.name), "is_national_team": False, "players": CLUB_SQUADS.get(t.name, [])}
        built.append(enrich_team(team))
    for name in sorted(NATIONAL_RATINGS.keys()):
        built.append(national_team(name))
    return built


def team_lookup() -> Dict[str, dict]:
    return {t["name"]: t for t in build_team_database()}


TEAMS = build_team_database()
