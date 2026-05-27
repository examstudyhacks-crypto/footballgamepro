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


def _slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")


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
    names = set(RATINGS.keys()) | set(UCL_2025_26) | set(UEL_2025_26) | set(UECL_2025_26)
    teams: List[Team] = []
    for name in sorted(names):
        if name in RATINGS:
            teams.append(Team(name=name, **RATINGS[name]))
        else:
            teams.append(default_team(name))
    return [t.to_dict() | {"id": _slug(t.name)} for t in teams]


def team_lookup() -> Dict[str, dict]:
    return {t["name"]: t for t in build_team_database()}


TEAMS = build_team_database()
