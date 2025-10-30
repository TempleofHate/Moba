
import json
import random
import os
import sys
from dataclasses import dataclass, asdict, field
from typing import List, Dict

# main.py
# Jogo de gerenciamento de equipe de esports de League of Legends (CLI)
# Crie, gerencie jogadores, contrate/demit, escolha draft, estratégias e jogue campeonatos.
# Salva/Carrega time em 'team.json' no mesmo diretório.


SAVE_FILE = "team.json"

CHAMPIONS = {
    "Top": [
        "Aatrox", "Akali", "Ambessa", "Aurora", "Camille", "Cassiopeia", "Cho'Gath", "Darius",
        "Dr.Mundo", "Fiora", "Gangplank", "Garen", "Gnar", "Gragas", "Gwen", "Heimerdinger",
        "Illaoi", "Irelia", "Jax", "Jayce", "K'Santem", "Kayle", "Kennen", "Kled", "Malphite",
        "Maokai", "Mordekaiser", "Nasus", "Olaf", "Ornn", "Pantheon", "Poppy", "Quinn",
        "Rek'Sai", "Renekton", "Riven", "Rumble", "Ryze", "Sett", "Shen", "Singed", "Sion",
        "Tahm Kench", "Teemo", "Trundle", "Tryndamere", "Udyr", "Urgot", "Varus", "Vayne",
        "Vladimir", "Volibear", "Warwick", "Wukong", "Yasuo", "Yone", "Yorick", "Zac"
    ],
    "Jungle": [
        "Amumu", "Bel'Veth", "Brand", "Briar", "Diana", "Dr. Mundo", "Ekko", "Elise",
        "Evelynn", "Fiddlesticks", "Gragas", "Graves", "Gwen", "Hecarim", "Ivern",
        "Jarvan IV", "Jax", "Karthus", "Kayn", "Kha'Zix", "Kindred", "Lee Sin", "Lillia",
        "Maokai", "Master Yi", "Morgana", "Naafiri", "Nidalee", "Nocturne", "Nunu e Willump",
        "Olaf", "Pantheon", "Poppy", "Qiyana", "Rammus", "Rek'Sai", "Rengar", "Sejuani",
        "Shaco", "Shyvana", "Skarner", "Sylas", "Taliyah", "Talon", "Teemo", "Trundle",
        "Udyr", "Vi", "Viego", "Volibear", "Warwick", "Wukong", "Xin Zhao", "Zac", "Zed",
        "Zyra"
    ],
    "Mid": [
        "Ahri", "Akali", "Akshan", "Anivia", "Annie", "Aurelion Sol", "Aurora", "Azir",
        "Brand", "Cassiopeia", "Cho'Gath", "Corki", "Diana", "Ekko", "Fizz", "Galio",
        "Heimerdinger", "Hwei", "Irelia", "Jayce", "Kassadin", "Katarina", "Kayle",
        "Kennen", "Leblanc", "Lissandra", "Lux", "Malphite", "Malzahar", "Mel",
        "Morgana", "Naafiri", "Neeko", "Orianna", "Qiyana", "Quinn", "Ryze", "Smolder",
        "Swain", "Sylas", "Syndra", "Taliyah", "Twisted Fate", "Veigar", "Vel'Koz",
        "Vex", "Viktor", "Vladimir", "Xerath", "Yasuo", "Yone", "Zed", "Ziggs", "Zoe"
    ],
    "ADC": [
        "Aphelios", "Ashe", "Aurelion Sol", "Caitlyn", "Corki", "Draven", "Ezreal",
        "Jhin", "Jinx", "Kai'Sa", "Kalista", "Karthus", "Kog'Maw", "Lucian", "Mel",
        "Miss Fortune", "Nilah", "Samira", "Senna", "Sivir", "Smolder", "Swain",
        "Tristana", "Twitch", "Varus", "Vayne", "Xayah", "Yunara", "Zeri", "Ziggs"
    ],
    "Support": [
        "Alistar", "Amumu", "Anivia", "Annie", "Bardo", "Blitzcrank", "Brand", "Braum",
        "Elise", "Fiddlesticks", "Galio", "Heimerdinger", "Ivern", "Janna", "Karma",
        "LeBlanc", "Leona", "Lulu", "Lux", "Maokai", "Mel", "Milio", "Morgana", "Nami",
        "Nautilus", "Neeko", "Nidalee", "Pantheon", "Poppy", "Pyke", "Rakan", "Rammus",
        "Rell", "Renata Glasc", "Senna", "Seraphine", "Shaco", "Shen", "Sona", "Soraka",
        "Swain", "Tahm Kench", "Taric", "Teemo", "Thresh", "Vel'Koz", "Xerath", "Yuumi",
        "Zilean", "Zoe", "Zyra"
    ]
}

ROLES = ["Top", "Jungle", "Mid", "ADC", "Support"]

# Ranking das regiões do melhor para o pior:
# 1. Coréia do Sul
# 2. China
# 3. Europa
# 4. América do Norte
# 5. Brasil
# 6. Japão
# 7. Turquia
# 8. LLA

REGIONS = {
    "Coréia do Sul": {
        "name_prefixes": ["KR", "Seoul", "Dragon", "Tiger", "Gen", "T1", "KT"],
        "name_suffixes": ["Gaming", "Esports", "Team", "Pro", "Stars", "Squad"],
        "player_cost_multiplier": 2.0,
        "region_strength": 1.3  # 1º lugar
    },
    "China": {
        "name_prefixes": ["CN", "Dragon", "Royal", "Imperial", "Eastern", "Legend"],
        "name_suffixes": ["Gaming", "Esports", "Team", "Pro", "Legion", "Dynasty"],
        "player_cost_multiplier": 1.8,
        "region_strength": 1.25  # 2º lugar
    },
    "Europa": {
        "name_prefixes": ["EU", "Royal", "Kings", "Nordic", "Lion", "Phoenix", "Elite"],
        "name_suffixes": ["Esports", "Gaming", "Team", "United", "Legion", "Squadron"],
        "player_cost_multiplier": 1.5,
        "region_strength": 1.2  # 3º lugar
    },
    "América do Norte": {
        "name_prefixes": ["NA", "Eagle", "Freedom", "Maple", "Coast", "Storm", "Tech"],
        "name_suffixes": ["Gaming", "Esports", "Team", "Squad", "Pro", "Academy"],
        "player_cost_multiplier": 1.5,
        "region_strength": 1.15  # 4º lugar
    },
    "Brasil": {
        "name_prefixes": ["BR", "Sampa", "Rio", "Nordeste", "Sul", "Verde", "Ouro", "Selva"],
        "name_suffixes": ["Gaming", "Team", "Esports", "Stars", "Gamers", "Legends", "Pro"],
        "player_cost_multiplier": 1.0,
        "region_strength": 1.1  # 5º lugar
    },
    "Japão": {
        "name_prefixes": ["JP", "Tokyo", "Sakura", "Ninja", "Samurai", "Rising"],
        "name_suffixes": ["Gaming", "Esports", "Team", "Squad", "Stars", "Legion"],
        "player_cost_multiplier": 1.3,
        "region_strength": 1.05  # 6º lugar
    },
    "Turquia": {
        "name_prefixes": ["TR", "Sultan", "Anatolian", "Ottoman", "Eagle", "Crescent"],
        "name_suffixes": ["Esports", "Gaming", "Team", "Squad", "Warriors", "Legion"],
        "player_cost_multiplier": 1.2,
        "region_strength": 1.0  # 7º lugar
    },
    "LLA": {
        "name_prefixes": ["Andes", "Condor", "Latino", "Sur", "Fuego", "Puma", "Azteca"],
        "name_suffixes": ["Gaming", "Team", "Esports", "Squad", "Warriors", "Legion"],
        "player_cost_multiplier": 1.0,
        "region_strength": 0.95  # 8º lugar
    }
}
TEAMS_BY_REGION = {
    "Coréia do Sul": {
        "fortes": ["T1", "Gen.G", "Hanwha Life", "KT Rolster", "NS RedForce"],
        "fracos": ["BNK FearX", "DN Freecs", "Dplus KIA", "DRX", "OK Brion"],
        "times": {
            "BNK FearX": {
                "jogadores": {
                    "Top": {"nome": "Clear", "skill": 75},
                    "Jungle": {"nome": "Raptor", "skill": 75},
                    "Mid": {"nome": "VicLa", "skill": 78},
                    "ADC": {"nome": "Dlable", "skill": 76},
                    "Support": {"nome": "Kellin", "skill": 77}
                }
            },
            "DN Freecs": {
                "jogadores": {
                    "Top": {"nome": "DuDu", "skill": 77},
                    "Jungle": {"nome": "Pyosik", "skill": 85, "world_champion": True, "best_player": True},
                    "Mid": {
                        "titular": {"nome": "BuLLDog", "skill": 78},
                        "reserva": {"nome": "Pungyeon", "skill": 75}
                    },
                    "ADC": {"nome": "Berserker", "skill": 80},
                    "Support": {"nome": "Life", "skill": 78}
                }
            },
            "Dplus KIA": {
                "jogadores": {
                    "Top": {"nome": "Siwoo", "skill": 77},
                    "Jungle": {"nome": "Lucid", "skill": 78},
                    "Mid": {"nome": "Showmaker", "skill": 88, "world_champion": True, "best_player": True},
                    "ADC": {"nome": "Aiming", "skill": 82},
                    "Support": {"nome": "BeryL", "skill": 83, "world_champion": True}
                }
            },
            "DRX": {
                "jogadores": {
                    "Top": {"nome": "Rich", "skill": 76},
                    "Jungle": {"nome": "Sponge", "skill": 77},
                    "Mid": {"nome": "Ucal", "skill": 78},
                    "ADC": {
                        "titular": {"nome": "LazyFeel", "skill": 79, "nacionalidade": "Vietnã"},
                        "reserva": {"nome": "Teddy", "skill": 77}
                    },
                    "Support": {"nome": "Andil", "skill": 76}
                }
            },
            "Gen.G": {
                "jogadores": {
                    "Top": {"nome": "Klin", "skill": 80},
                    "Jungle": {"nome": "Canyon", "skill": 87, "world_champion": True},
                    "Mid": {"nome": "Chovy", "skill": 90, "best_player": True},
                    "ADC": {"nome": "Ruler", "skill": 85},
                    "Support": {"nome": "Duro", "skill": 82}
                }
            },
            "Hanwha Life": {
                "jogadores": {
                    "Top": {"nome": "Zeus", "skill": 89, "world_champion": True, "best_player": True},
                    "Jungle": {"nome": "Peanut", "skill": 84},
                    "Mid": {"nome": "Zeka", "skill": 85, "world_champion": True},
                    "ADC": {"nome": "Viper", "skill": 86},
                    "Support": {"nome": "Delight", "skill": 82}
                }
            },
            "KT Rolster": {
                "jogadores": {
                    "Top": {"nome": "PerfecT", "skill": 80},
                    "Jungle": {"nome": "Cuzz", "skill": 83, "world_champion": True},
                    "Mid": {"nome": "Bdd", "skill": 87, "best_player": True},
                    "ADC": {"nome": "deokdam", "skill": 82},
                    "Support": {"nome": "Way", "skill": 81}
                }
            },
            "Nongshim RedForce": {
                "jogadores": {
                    "Top": {"nome": "Kingen", "skill": 82},
                    "Jungle": {"nome": "GIDEON", "skill": 78},
                    "Mid": {"nome": "Fisher", "skill": 79},
                    "ADC": {"nome": "Jiwoo", "skill": 80},
                    "Support": {"nome": "Lehends", "skill": 83}
                }
            },
            "OK Brion": {
                "jogadores": {
                    "Top": {"nome": "Morgan", "skill": 81, "world_champion": True},
                    "Jungle": {"nome": "HamBak", "skill": 76},
                    "Mid": {"nome": "Clozer", "skill": 78},
                    "ADC": {
                        "titular": {"nome": "Hype", "skill": 77},
                        "reserva": {"nome": "Bull", "skill": 75}
                    },
                    "Support": {"nome": "Pollu", "skill": 76}
                }
            },
            "T1": {
                "jogadores": {
                    "Top": {"nome": "Doran", "skill": 83},
                    "Jungle": {"nome": "Oner", "skill": 88, "world_champion": True},
                    "Mid": {"nome": "Faker", "skill": 95, "world_champion": True, "best_player": True, "goat": True},
                    "ADC": {
                        "titular": {"nome": "Gumayusi", "skill": 89, "world_champion": True},
                        "reserva": {"nome": "Smash", "skill": 80}
                    },
                    "Support": {"nome": "Keria", "skill": 90, "world_champion": True}
                }
            }
        }
    },
    "China": {
        "fortes": ["Anyone's Legends", "Bilibili Gaming", "FunPlus Phoenix", "Invictus Gaming", "Team WE", "Top Esports", "Weibo Gaming"],
        "fracos": ["Edward Gaming", "LGD Gaming", "LNG Esports", "Ninjas in Pyjamas", "TT Gaming", "Ultra Prime"],
        "times": {
            "Anyone's Legends": {
                "jogadores": {
                    "Top": {"nome": "Flandre", "skill": 80},
                    "Jungle": {"nome": "Tarzan", "skill": 85, "nacionalidade": "Coréia do Sul"},
                    "Mid": {"nome": "Shanks", "skill": 78},
                    "ADC": {"nome": "Hope", "skill": 80},
                    "Support": {"nome": "Kael", "skill": 78, "nacionalidade": "Coréia do Sul"}
                }
            },
            "Bilibili Gaming": {
                "jogadores": {
                    "Top": {"nome": "Bin", "skill": 88, "best_player": True},
                    "Jungle": {"nome": "Shad0w", "skill": 80},
                    "Mid": {"nome": "Knight", "skill": 86, "world_champion": True},
                    "ADC": {"nome": "Elk", "skill": 84},
                    "Support": {"nome": "ON", "skill": 82}
                }
            },
            "EDward Gaming": {
                "jogadores": {
                    "Top": {"nome": "Zdz", "skill": 77},
                    "Jungle": {"nome": "Xiaohao", "skill": 85, "best_player": True},
                    "Mid": {"nome": "Angel", "skill": 80},
                    "ADC": {"nome": "Ahn", "skill": 78},
                    "Support": {"nome": "Parukia", "skill": 77}
                }
            },
            "FunPlus Phoenix": {
                "jogadores": {
                    "Top": {"nome": "sheer", "skill": 76},
                    "Jungle": {
                        "titular": {"nome": "Iyy", "skill": 78},
                        "reserva": {"nome": "milkway", "skill": 75},
                        "reserva2": {"nome": "Jiejie", "skill": 80}
                    },
                    "Mid": {"nome": "Care", "skill": 80},
                    "ADC": {"nome": "JiaQi", "skill": 77},
                    "Support": {"nome": "Jwei", "skill": 76}
                }
            },
            "Invictus Gaming": {
                "jogadores": {
                    "Top": {"nome": "TheShy", "skill": 87, "world_champion": True},
                    "Jungle": {"nome": "Wei", "skill": 80},
                    "Mid": {"nome": "Rookie", "skill": 90, "nacionalidade": "Coréia do Sul", "best_player": True, "world_champion": True},
                    "ADC": {"nome": "GALA", "skill": 85},
                    "Support": {"nome": "Meiko", "skill": 88, "world_champion": True}
                }
            },
            "JD Gaming": {
                "jogadores": {
                    "Top": {"nome": "Xiaoxu", "skill": 78},
                    "Jungle": {"nome": "Xun", "skill": 80},
                    "Mid": {"nome": "Scout", "skill": 89, "nacionalidade": "Coréia do Sul", "best_player": True, "world_champion": True},
                    "ADC": {"nome": "Peyz", "skill": 85, "nacionalidade": "Coréia do Sul"},
                    "Support": {
                        "titular": {"nome": "Wink", "skill": 80},
                        "reserva": {"nome": "Zhuo", "skill": 77}
                    }
                }
            },
            "LGD Gaming": {
                "jogadores": {
                    "Top": {"nome": "sasl", "skill": 75},
                    "Jungle": {"nome": "Climber", "skill": 75},
                    "Mid": {"nome": "xqw", "skill": 75},
                    "ADC": {"nome": "Sav1ior", "skill": 75},
                    "Support": {"nome": "Ycx", "skill": 75}
                }
            },
            "LNG Esports": {
                "jogadores": {
                    "Top": {"nome": "Zika", "skill": 78},
                    "Jungle": {"nome": "xiaofang", "skill": 77},
                    "Mid": {"nome": "haichao", "skill": 78},
                    "ADC": {
                        "titular": {"nome": "LP", "skill": 80},
                        "reserva": {"nome": "fishone", "skill": 75}
                    },
                    "Support": {
                        "titular": {"nome": "Zhuo", "skill": 77},
                        "reserva": {"nome": "OvO", "skill": 75}
                    }
                }
            },
            "Ninjas in Pyjamas": {
                "jogadores": {
                    "Top": {"nome": "Solokill", "skill": 78, "nacionalidade": "Hong Kong"},
                    "Jungle": {"nome": "naiyou", "skill": 76},
                    "Mid": {"nome": "Doinb", "skill": 89, "nacionalidade": "Coréia do Sul", "best_player": True, "world_champion": True},
                    "ADC": {"nome": "Leave", "skill": 80},
                    "Support": {"nome": "Niket", "skill": 76}
                }
            },
            "Team WE": {
                "jogadores": {
                    "Top": {"nome": "Cube", "skill": 77},
                    "Jungle": {"nome": "Monki", "skill": 76},
                    "Mid": {"nome": "Karis", "skill": 80, "nacionalidade": "Coréia do Sul"},
                    "ADC": {"nome": "Taeyoon", "skill": 80, "nacionalidade": "Coréia do Sul"},
                    "Support": {"nome": "Vampire", "skill": 76}
                }
            },
            "TT Gaming": {
                "jogadores": {
                    "Top": {"nome": "HOYA", "skill": 78, "nacionalidade": "Coréia do Sul"},
                    "Jungle": {"nome": "Aki", "skill": 77},
                    "Mid": {"nome": "SeTab", "skill": 78, "nacionalidade": "Coréia do Sul"},
                    "ADC": {"nome": "1xn", "skill": 77},
                    "Support": {"nome": "Feather", "skill": 77}
                }
            },
            "Top Esports": {
                "jogadores": {
                    "Top": {"nome": "369", "skill": 85},
                    "Jungle": {"nome": "Kanavi", "skill": 88, "nacionalidade": "Coréia do Sul", "world_champion": True},
                    "Mid": {"nome": "Creme", "skill": 80},
                    "ADC": {"nome": "JackeyLove", "skill": 90, "world_champion": True, "best_player": True},
                    "Support": {"nome": "Hang", "skill": 80}
                }
            },
            "Ultra Prime": {
                "jogadores": {
                    "Top": {"nome": "1Jiang", "skill": 77, "nacionalidade": "Taiwan"},
                    "Jungle": {"nome": "Junhao", "skill": 75},
                    "Mid": {"nome": "Saber", "skill": 75},
                    "ADC": {"nome": "Baiye", "skill": 75},
                    "Support": {"nome": "Xiaoxia", "skill": 75}
                }
            },
            "Weibo Gaming": {
                "jogadores": {
                    "Top": {"nome": "Breathe", "skill": 82},
                    "Jungle": {"nome": "Tian", "skill": 88, "world_champion": True},
                    "Mid": {"nome": "Xiaohu", "skill": 89, "best_player": True},
                    "ADC": {"nome": "Light", "skill": 85},
                    "Support": {"nome": "Crisp", "skill": 87, "world_champion": True}
                }
            }
        }
    },
    "Europa": {
        "fortes": ["Movistar KOI", "G2 Esports", "Karmine Corp", "Fnatic"],
        "fracos": ["GIANTX", "Team Heretics", "Team Vitality", "Team BDS"]
    },
    "Turquia": {
        "fortes": ["Bushido Wildcats", "Misa Esports", "Besiktas Esports"],
        "fracos": ["ULF Esports", "Papara Supermassive", "BBL Dark Passage"]
    },
    "Brasil": {
        "fortes": ["Vivo Keyd Stars", "paiN Gaming", "LOUD", "RED Canids", "FURIA", "Fluxo"],
        "fracos": ["KaBuM! Esports", "INTZ", "Liberty", "Los Grandes"]
    },
    "LLA": {
        "fortes": ["Estral Esports", "Isurus", "Rainbow7"],
        "fracos": ["Team Aze", "INFINITY", "All Knights"]
    },
    "América do Norte": {
        "fortes": ["FlyQuest", "100Thieves", "Cloud9", "Team Liquid", "Dignitas", "NRG"],
        "fracos": ["Shopify Rebellion", "Immortals"]
    },
    "Japão": {
        "fortes": ["DetonatioN FocusMe", "Sengoku Gaming", "Fukuoka SoftBank HAWKS Gaming", "Rascal Jester", "Crest Gaming Act", "Burning Core"],
        "fracos": ["AXIZ", "V3 Esports"]
    }
}

STRATEGIES = {
    "Equilibrada": 1.0,
    "Agressiva": 1.07,
    "Defensiva": 0.98,
    "Teamfight": 1.05,
    "Dividir (Split-push)": 1.03
}

def clamp(x, a=0, b=100):
    return max(a, min(b, x))

@dataclass
class Player:
    name: str
    role: str
    skill: int  # 0-100
    nationality: str  # Region name
    preferred_champs: List[str] = field(default_factory=list)
    years_in_team: int = 0  # For import naturalization
    
    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        player = Player(
            d["name"], 
            d["role"], 
            d["skill"], 
            d.get("nationality", "Brasil"),  # Default for backward compatibility
            d.get("preferred_champs", [])
        )
        player.years_in_team = d.get("years_in_team", 0)
        return player

@dataclass
class Team:
    name: str
    region: str  # Team's region
    players: List[Player] = field(default_factory=list)
    money: int = 100000  # moeda do jogo
    season_year: int = 2025  # Current season year

    def to_dict(self):
        return {
            "name": self.name,
            "region": self.region,
            "players": [p.to_dict() for p in self.players],
            "money": self.money,
            "season_year": self.season_year
        }

    @staticmethod
    def from_dict(d):
        t = Team(
            name=d["name"],
            region=d.get("region", "Brasil"),  # Default region for backward compatibility
            players=[Player.from_dict(p) for p in d.get("players", [])],
            money=d.get("money", 100000)
        )
        t.season_year = d.get("season_year", 2025)  # Add season year
        return t

def save_team(team: Team):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(team.to_dict(), f, indent=2, ensure_ascii=False)

def create_new_team() -> Team:
    print("\n-- Criação de Nova Equipe --")
    name = input("Digite o nome da sua equipe: ").strip()
    
    print("\nEscolha sua região:")
    for i, region in enumerate(REGIONS.keys(), 1):
        print(f"{i}. {region}")
    
    while True:
        try:
            choice = int(input("Digite o número da região: ").strip())
            if 1 <= choice <= len(REGIONS):
                region = list(REGIONS.keys())[choice - 1]
                break
            print("Escolha inválida.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    return Team(name=name, region=region)

def load_team() -> Team:
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                team = Team.from_dict(data)
                if not hasattr(team, 'region'):  # Backward compatibility
                    team.region = 'Brasil'
                return team
        except Exception as e:
            print(f"Erro ao carregar time: {e}")
            return create_new_team()
    # se não existe, cria um time novo
    return create_new_team()

def format_player(p: Player) -> str:
    prefs = ", ".join(p.preferred_champs[:3]) if p.preferred_champs else "Nenhum"
    years = f" ({p.years_in_team} anos no time)" if p.years_in_team > 0 else ""
    special = ""
    if hasattr(p, 'world_champion') and p.world_champion:
        special += " [Campeão Mundial]"
    if hasattr(p, 'best_player') and p.best_player:
        special += " [Melhor do Time]"
    if hasattr(p, 'goat') and p.goat:
        special += " [GOAT]"
    return f"{p.name}{special} | Cargo: {p.role} | Skill: {p.skill} | Nacionalidade: {p.nationality}{years} | Champs: {prefs}"

def random_name(region: str = None) -> str:
    if region and region in REGIONS:
        prefixes = REGIONS[region]["name_prefixes"]
        suffixes = REGIONS[region]["name_suffixes"]
    else:
        prefixes = ["Alpha", "Beta", "Neo", "Dark", "Blue", "Red", "Lucky", "Prime", "Void", "Star"]
        suffixes = ["Blade", "Fox", "Tiger", "Wolf", "Dragon", "Storm", "Phoenix", "Ghost", "Rift", "Flash"]
    return random.choice(prefixes) + random.choice(suffixes) + str(random.randint(1,99))

def generate_free_agent(region: str = None, force_native: bool = False) -> Player:
    role = random.choice(ROLES)
    
    # Determine player nationality
    if force_native:
        nationality = region
    else:
        # 70% chance for native player if region is specified
        if region and random.random() < 0.7:
            nationality = region
        else:
            nationality = random.choice(list(REGIONS.keys()))
    
    # Generate name based on nationality
    name = random_name(nationality)
    
    # Skill calculation with regional strength bonuses
    base_skill = random.randint(40, 85)
    region_strength = REGIONS[nationality]["region_strength"]
    skill = min(100, int(base_skill * region_strength))  # Apply region strength directly
    
    # Get champions for the specific role
    available_champs = CHAMPIONS[role]  # Get champions specific to this role
    # Ensure we don't try to sample more champions than available
    num_prefs = min(3, len(available_champs))
    prefs = random.sample(available_champs, k=num_prefs)
    
    return Player(name=name, role=role, skill=skill, nationality=nationality, preferred_champs=prefs)

def count_imports(team: Team) -> int:
    non_naturalized = 0
    for p in team.players:
        if p.nationality != team.region and p.years_in_team < 2:
            non_naturalized += 1
    return non_naturalized

def calculate_player_cost(player: Player, team_region: str) -> int:
    base_cost = player.skill * 200
    if player.nationality != team_region:
        # Import cost multiplier based on region's prestige
        cost_multiplier = REGIONS[player.nationality]["player_cost_multiplier"]
        return int(base_cost * cost_multiplier)
    return base_cost

def hire_player(team: Team):
    print("\n-- Mercado de Free Agents --")
    
    # Generate a mix of native and foreign players
    candidates = []
    for _ in range(5):
        # Try to include more native players in the pool
        if random.random() < 0.6:
            candidates.append(generate_free_agent(team.region, force_native=True))
        else:
            candidates.append(generate_free_agent())
    
    current_imports = count_imports(team)
    
    for i, c in enumerate(candidates, 1):
        cost = calculate_player_cost(c, team.region)
        status = " (Import)" if c.nationality != team.region else ""
        print(f"{i}. {format_player(c)} - Nacionalidade: {c.nationality}{status} - Salário: ${cost}")
    
    choice = input("Escolha um jogador para contratar (número) ou enter para voltar: ").strip()
    if not choice:
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(candidates):
            player = candidates[idx]
            # Check import limits
            if player.nationality != team.region and count_imports(team) >= 2:
                print("Limite de imports atingido (máximo 2 jogadores).")
                return
                
            cost = calculate_player_cost(player, team.region)
            if team.money >= cost:
                team.players.append(player)
                team.money -= cost
                print(f"Contratado {player.name} por ${cost}. Saldo: ${team.money}")
            else:
                print("Dinheiro insuficiente.")
        else:
            print("Escolha inválida.")
    except ValueError:
        print("Entrada inválida.")

def fire_player(team: Team):
    if not team.players:
        print("Sem jogadores no time.")
        return
    print("\n-- Jogadores do Time --")
    for i, p in enumerate(team.players, 1):
        print(f"{i}. {format_player(p)}")
    choice = input("Escolha um jogador para demitir (número) ou enter para voltar: ").strip()
    if not choice:
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(team.players):
            p = team.players.pop(idx)
            refund = p.skill * 50
            team.money += refund
            print(f"{p.name} demitido. Recuperou ${refund}. Saldo: ${team.money}")
        else:
            print("Escolha inválida.")
    except ValueError:
        print("Entrada inválida.")

def view_players(team: Team):
    print(f"\n-- Jogadores de {team.name} (Saldo: ${team.money}) --")
    if not team.players:
        print("Nenhum jogador contratado.")
        return
    for p in team.players:
        print(format_player(p))

def advance_season(team: Team):
    team.season_year += 1
    print(f"\n-- Avançando para a Temporada {team.season_year} --")
    
    # Update years in team and check for naturalization
    for player in team.players:
        if player.nationality != team.region:
            player.years_in_team += 1
            if player.years_in_team >= 2:
                print(f"{player.name} foi naturalizado após {player.years_in_team} anos no time!")

def train_player(team: Team):
    if not team.players:
        print("Sem jogadores para treinar.")
        return
    print("\n-- Treinamento --")
    for i, p in enumerate(team.players, 1):
        print(f"{i}. {format_player(p)} - Custo: ${p.skill * 20}")
    choice = input("Escolha um jogador para treinar (número) ou enter para voltar: ").strip()
    if not choice:
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(team.players):
            p = team.players[idx]
            cost = p.skill * 20
            if team.money >= cost:
                improvement = random.randint(1, 6)
                p.skill = clamp(p.skill + improvement, 0, 100)
                team.money -= cost
                print(f"{p.name} treinado. +{improvement} skill -> {p.skill}. Custeio: ${cost}. Saldo: ${team.money}")
            else:
                print("Dinheiro insuficiente.")
        else:
            print("Escolha inválida.")
    except ValueError:
        print("Entrada inválida.")

def change_role(team: Team):
    if not team.players:
        print("Sem jogadores para alterar cargo.")
        return
    print("\n-- Alterar Cargo do Jogador --")
    for i, p in enumerate(team.players, 1):
        print(f"{i}. {format_player(p)}")
    choice = input("Escolha um jogador (número) ou enter para voltar: ").strip()
    if not choice:
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(team.players):
            p = team.players[idx]
            print("Cargos disponíveis:", ", ".join(ROLES))
            new = input(f"Novo cargo para {p.name} (atual: {p.role}): ").strip()
            if new in ROLES:
                p.role = new
                print(f"{p.name} agora é {new}.")
            else:
                print("Cargo inválido.")
        else:
            print("Escolha inválida.")
    except ValueError:
        print("Entrada inválida.")

def get_role_champions(role):
    # Role names in CHAMPIONS dictionary match exactly with ROLES list
    if role not in CHAMPIONS:
        raise ValueError(f"Invalid role: {role}")
    return CHAMPIONS[role]

def get_all_champions():
    """Return a list of all unique champions across all roles."""
    all_champs = set()
    for role_champs in CHAMPIONS.values():
        all_champs.update(role_champs)
    return sorted(list(all_champs))

def pick_lineup_and_draft(team: Team):
    print("\n-- Montar lineup (5 jogadores) e draft de campeões --")
    if len(team.players) < 5:
        print("Você precisa de pelo menos 5 jogadores para formar a lineup.")
        return None, None, None
    
    # selecionar lineup
    lineup = []
    players_copy = team.players.copy()
    # prefer jogadores por cargo ideal: tenta escolher um por role
    for role in ROLES:
        candidates = [p for p in players_copy if p.role == role]
        if candidates:
            best = max(candidates, key=lambda p: p.skill)
            lineup.append(best)
            players_copy.remove(best)
    # se faltarem posições, completar com melhores restantes
    while len(lineup) < 5:
        remaining = [p for p in team.players if p not in lineup]
        best = max(remaining, key=lambda p: p.skill)
        lineup.append(best)
    
    print("Lineup selecionada:")
    for i, p in enumerate(lineup):
        print(f"{ROLES[i]}: {p.name} (Skill {p.skill})")
    
    # Primeira Fase de Bans (3 bans por time)
    print("\n-- Primeira Fase de Bans (3 bans) --")
    banned_champions = set()
    all_champions = get_all_champions()
    
    for ban_round in range(3):
        # Seu ban
        print(f"\nSeu {ban_round + 1}º ban:")
        available_to_ban = [c for c in all_champions if c not in banned_champions]
        print("Exemplos de campeões disponíveis:")
        champs_to_show = available_to_ban[:15]
        for j in range(0, len(champs_to_show), 5):
            print(", ".join(champs_to_show[j:j+5]))
        
        while True:
            ban_choice = input("Escolha um campeão para banir: ").strip()
            if ban_choice in available_to_ban:
                banned_champions.add(ban_choice)
                print(f"Você baniu {ban_choice}")
                break
            else:
                print("Campeão inválido ou já banido. Tente novamente.")
        
        # Ban do oponente
        opponent_ban = random.choice([c for c in all_champions if c not in banned_champions])
        banned_champions.add(opponent_ban)
        print(f"Oponente baniu {opponent_ban}")
    
    print("\nCampeões banidos na primeira fase:", ", ".join(sorted(banned_champions)))
    
    # Primeira fase de picks (3 picks por time)
    print("\n-- Primeira Fase de Picks (3 primeiros picks) --")
    picks = {}
    used_champions = banned_champions.copy()
    
    for i in range(3):  # Primeiros 3 picks
        p = lineup[i]
        role = ROLES[i]
        role_champions = get_role_champions(role)
        available_champions = [c for c in role_champions if c not in used_champions]
        
        if not available_champions:
            print(f"Erro: Não há mais campeões disponíveis para {role}")
            return None, None, None
        
        suggested = next((c for c in p.preferred_champs if c in available_champions), None)
        
        print(f"\nPara {role} ({p.name})")
        if suggested:
            print(f"Campeão sugerido: {suggested}")
        print(f"Campeões disponíveis para {role}:")
        champs_to_show = available_champions[:15]
        for j in range(0, len(champs_to_show), 5):
            print(", ".join(champs_to_show[j:j+5]))
        
        choice = input(f"Escolha um campeão para {p.name} ou enter para sugerido: ").strip()
        
        if not choice:
            pick = suggested if suggested else random.choice(available_champions)
        else:
            if choice not in available_champions:
                print(f"Escolha inválida. Selecionando aleatoriamente.")
                pick = random.choice(available_champions)
            else:
                pick = choice
        
        picks[role] = pick
        used_champions.add(pick)
        print(f"Selecionado {pick} para {role}.")
    
    # Segunda Fase de Bans (2 bans por time)
    print("\n-- Segunda Fase de Bans (2 bans) --")
    for ban_round in range(2):
        # Seu ban
        print(f"\nSeu {ban_round + 1}º ban da segunda fase:")
        available_to_ban = [c for c in all_champions if c not in used_champions]
        print("Exemplos de campeões disponíveis:")
        champs_to_show = available_to_ban[:15]
        for j in range(0, len(champs_to_show), 5):
            print(", ".join(champs_to_show[j:j+5]))
        
        while True:
            ban_choice = input("Escolha um campeão para banir: ").strip()
            if ban_choice in available_to_ban:
                banned_champions.add(ban_choice)
                used_champions.add(ban_choice)
                print(f"Você baniu {ban_choice}")
                break
            else:
                print("Campeão inválido ou já banido. Tente novamente.")
        
        # Ban do oponente
        opponent_ban = random.choice([c for c in all_champions if c not in used_champions])
        banned_champions.add(opponent_ban)
        used_champions.add(opponent_ban)
        print(f"Oponente baniu {opponent_ban}")
    
    print("\nTodos os campeões banidos:", ", ".join(sorted(banned_champions)))
    
    # Segunda fase de picks (2 últimos picks)
    print("\n-- Segunda Fase de Picks (2 últimos picks) --")
    for i in range(3, 5):  # Últimos 2 picks
        p = lineup[i]
        role = ROLES[i]
        role_champions = get_role_champions(role)
        available_champions = [c for c in role_champions if c not in used_champions]
        
        if not available_champions:
            print(f"Erro: Não há mais campeões disponíveis para {role}")
            return None, None, None
        
        suggested = next((c for c in p.preferred_champs if c in available_champions), None)
        
        print(f"\nPara {role} ({p.name})")
        if suggested:
            print(f"Campeão sugerido: {suggested}")
        print(f"Campeões disponíveis para {role}:")
        champs_to_show = available_champions[:15]
        for j in range(0, len(champs_to_show), 5):
            print(", ".join(champs_to_show[j:j+5]))
        
        choice = input(f"Escolha um campeão para {p.name} ou enter para sugerido: ").strip()
        
        if not choice:
            pick = suggested if suggested else random.choice(available_champions)
        else:
            if choice not in available_champions:
                print(f"Escolha inválida. Selecionando aleatoriamente.")
                pick = random.choice(available_champions)
            else:
                pick = choice
        
        picks[role] = pick
        used_champions.add(pick)
        print(f"Selecionado {pick} para {role}.")
    
    return lineup, picks, used_champions

def simulate_match(my_lineup: List[Player], my_picks: Dict[str,str], my_strategy: str, opponent_team=None):
    # Gera adversário se não fornecido
    if opponent_team is None:
        opponent_lineup = [generate_free_agent() for _ in range(5)]
        # ajustar roles para cada posição
        for i, p in enumerate(opponent_lineup):
            p.role = ROLES[i]
        # Pick champions for each role from their respective pools
        opp_picks = {}
        for i, role in enumerate(ROLES):
            p = opponent_lineup[i]
            role_champs = get_role_champions(role)
            opp_picks[role] = random.choice(role_champs)
        opp_strategy = random.choice(list(STRATEGIES.keys()))
    else:
        opponent_lineup, opp_picks, opp_strategy = opponent_team

    def lineup_power(lineup, picks, strategy):
        total = 0.0
        for i, p in enumerate(lineup):
            role = ROLES[i]
            base = p.skill
            # bônus se jogador prefere o campeão
            champ = picks.get(role, "")
            pref_bonus = 1.06 if champ in p.preferred_champs else 1.0
            # cargo fit: se p.role == role, leve pequeno bônus
            role_fit = 1.05 if p.role == role else 0.95
            # random performance
            rng = random.uniform(0.9, 1.1)
            total += base * pref_bonus * role_fit * rng
        # strategy factor influencia
        strat = STRATEGIES.get(strategy, 1.0)
        total *= strat
        # pequena variação de equipe
        synergy = 1 + (len(set([p.name for p in lineup])) % 5) * 0.01
        return total * synergy

    my_power = lineup_power(my_lineup, my_picks, my_strategy)
    opp_power = lineup_power(opponent_lineup, opp_picks, opp_strategy)

    # resultado
    diff = my_power - opp_power
    prob_my_win = 1 / (1 + 10 ** (-diff / 50))  # logistic-like
    rnd = random.random()
    winner = "MinhaEquipe" if rnd < prob_my_win else "Adversário"
    return {
        "winner": winner,
        "my_power": my_power,
        "opp_power": opp_power,
        "my_strategy": my_strategy,
        "opp_strategy": opp_strategy,
        "opponent_lineup": opponent_lineup,
        "opponent_picks": opp_picks
    }

def choose_strategy() -> str:
    print("\n-- Escolher estratégia --")
    for i, s in enumerate(STRATEGIES.keys(), 1):
        print(f"{i}. {s}")
    choice = input("Escolha estratégia (número) ou enter para Equilibrada: ").strip()
    strat = "Equilibrada"
    if choice:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(STRATEGIES):
                strat = list(STRATEGIES.keys())[idx]
        except Exception:
            pass
    return strat

def play_match_menu(team: Team):
    lineup, picks, _ = pick_lineup_and_draft(team)
    if lineup is None:
        return
    strat = choose_strategy()
    result = simulate_match(lineup, picks, strat)
    print("\n-- Resultado da Partida --")
    print(f"Minha power: {result['my_power']:.1f} | Oponente power: {result['opp_power']:.1f}")
    print(f"Minha estratégia: {result['my_strategy']} | Oponente: {result['opp_strategy']}")
    if result["winner"] == "MinhaEquipe":
        reward = 20000
        team.money += reward
        print(f"Você venceu! Ganhou ${reward}. Saldo: ${team.money}")
    else:
        penalty = 5000
        team.money = max(0, team.money - penalty)
        print(f"Você perdeu. Perdeu ${penalty}. Saldo: ${team.money}")

def create_player_from_data(player_data, role):
    """Cria um jogador a partir dos dados do TEAMS_BY_REGION"""
    if isinstance(player_data, dict):
        if "titular" in player_data:  # Se tem titular/reserva, use o titular
            player_data = player_data["titular"]
        
        nome = player_data["nome"]
        skill = player_data["skill"]
        nationality = player_data.get("nacionalidade", "Coréia do Sul")  # Default para Coreia
        
        # Seleciona campeões apropriados para a role
        role_champs = CHAMPIONS[role]
        prefs = random.sample(role_champs, k=min(3, len(role_champs)))
        
        # Cria o jogador base
        player = Player(
            name=nome,
            role=role,
            skill=skill,
            nationality=nationality,
            preferred_champs=prefs
        )
        
        # Adiciona atributos especiais
        if player_data.get("world_champion"):
            player.world_champion = True
        if player_data.get("best_player"):
            player.best_player = True
        if player_data.get("goat"):
            player.goat = True
            
        return player
    return None

def generate_ai_team(region=None, team_name=None):
    # If no region specified, choose one randomly
    if not region:
        region = random.choice(list(REGIONS.keys()))
    
    players = []
    
    # Se temos dados do time real, use-os
    if region in TEAMS_BY_REGION:
        times_data = TEAMS_BY_REGION[region].get("times", {})
        if team_name and team_name in times_data:
            team_data = times_data[team_name]
            
            # Criar jogadores baseados nos dados do time
            for role in ROLES:
                role_key = "ADC" if role == "ADC" else role
                if role_key in team_data["jogadores"]:
                    player_data = team_data["jogadores"][role_key]
                    
                    # Se tem titular/reserva, use o titular
                    if isinstance(player_data, dict) and "titular" in player_data:
                        player_data = player_data["titular"]
                    
                    player = create_player_from_data(player_data, role)
                    if player:
                        # Adiciona atributos especiais se existirem
                        if isinstance(player_data, dict):
                            if player_data.get("world_champion"):
                                player.world_champion = True
                            if player_data.get("best_player"):
                                player.best_player = True
                            if player_data.get("goat"):
                                player.goat = True
                            if "nacionalidade" in player_data:
                                player.nationality = player_data["nacionalidade"]
                        players.append(player)
                        continue
                
                # Se não conseguiu criar o jogador dos dados, cria um genérico
                p = generate_free_agent(region, force_native=True)
                p.role = role
                players.append(p)
            
            return Team(
                name=team_name,
                region=region,
                players=players,
                money=random.randint(80000, 150000)
            )
    
    # Se não encontrou dados do time real ou não tem nome especificado
    if not team_name:
        team_name = random_name(region)
    
    # Create one player for each role
    for role in ROLES:
        # 70% chance for native player
        is_native = random.random() < 0.7
        p = generate_free_agent(region if is_native else None, force_native=is_native)
        p.role = role
        players.append(p)
    
    return Team(
        name=team_name,
        region=region,
        players=players,
        money=random.randint(50000, 150000)
    )

def play_championship(team: Team):
    print("\n-- Campeonato Internacional --")
    if len(team.players) < 5:
        print("Você precisa de pelo menos 5 jogadores para disputar um campeonato.")
        return

    # Monta bracket com times reais e o time do jogador
    num_teams = 8
    bracket = []
    regions = list(TEAMS_BY_REGION.keys())

    # Criar uma lista de todos os times disponíveis
    available_teams = []
    for region in regions:
        teams = TEAMS_BY_REGION[region]["fortes"] + TEAMS_BY_REGION[region]["fracos"]
        for team_name in teams:
            available_teams.append((region, team_name))
    
    # Remover o time do jogador da lista se ele estiver lá
    available_teams = [(r, t) for r, t in available_teams if t != team.name]
    
    # Fill bracket with randomly selected teams (without repetition)
    selected_teams = random.sample(available_teams, min(num_teams - 1, len(available_teams)))
    
    for region, team_name in selected_teams:
        ai = generate_ai_team(region, team_name)
        bracket.append(ai)

    # Add the player's team
    bracket.append(team)

    print("\n=== Times Participantes ===")
    for t in bracket:
        print(f"\n{t.name} ({t.region}):")
        for role in ROLES:
            for p in t.players:
                if p.role == role:
                    print(f"  {format_player(p)}")

    input("\nPressione Enter para começar o torneio")
    random.shuffle(bracket)

    round_num = 1
    current = bracket

    def build_lineup_from_team_local(t: Team):
        lineup_local = []
        for role in ROLES:
            matching_players = [p for p in t.players if p.role == role]
            if matching_players:
                lineup_local.append(max(matching_players, key=lambda p: p.skill))
            else:
                remaining = [p for p in t.players if p not in lineup_local]
                if remaining:
                    lineup_local.append(max(remaining, key=lambda p: p.skill))
        while len(lineup_local) < 5:
            remaining = [p for p in t.players if p not in lineup_local]
            if not remaining:
                break
            lineup_local.append(max(remaining, key=lambda p: p.skill))
        picks_local = {role: random.choice(get_role_champions(role)) for role in ROLES}
        strat_local = random.choice(list(STRATEGIES.keys()))
        return lineup_local, picks_local, strat_local

    while len(current) > 1:
        print(f"\n--- Rodada {round_num}: {len(current)} times ---")
        next_round = []
        for i in range(0, len(current), 2):
            t1 = current[i]
            t2 = current[i+1]
            print(f"\n=== Partida: {t1.name} vs {t2.name} ===")
            print(f"\n{t1.name}:")
            for role in ROLES:
                for p in t1.players:
                    if p.role == role:
                        print(f"  {format_player(p)}")
            print(f"\n{t2.name}:")
            for role in ROLES:
                for p in t2.players:
                    if p.role == role:
                        print(f"  {format_player(p)}")

            # If player's team is involved, allow interactive picks/strategy
            if t1 is team or t2 is team:
                player_team = team
                opponent = t2 if t1 is team else t1

                print("Você irá jogar esta partida!")
                lineup_player, picks_player, _ = pick_lineup_and_draft(player_team)
                if lineup_player is None:
                    print("Lineup inválida. Partida perdida automaticamente.")
                    winner = opponent
                    next_round.append(winner)
                    continue
                strat_player = choose_strategy()
                lineup_opp, picks_opp, strat_opp = build_lineup_from_team_local(opponent)
                res = simulate_match(lineup_player, picks_player, strat_player, opponent_team=(lineup_opp, picks_opp, strat_opp))
                winner = player_team if res["winner"] == "MinhaEquipe" else opponent
                print(f"Power: {res['my_power']:.1f} vs {res['opp_power']:.1f}")
                print(f"Vencedor: {winner.name}")
            else:
                # Both AI teams: simulate automatically
                lineup1_local, picks1_local, strat1_local = build_lineup_from_team_local(t1)
                lineup2_local, picks2_local, strat2_local = build_lineup_from_team_local(t2)
                res = simulate_match(lineup1_local, picks1_local, strat1_local, opponent_team=(lineup2_local, picks2_local, strat2_local))
                winner = t1 if res["winner"] == "MinhaEquipe" else t2
                print(f"Vencedor: {winner.name} (Power {res['my_power']:.1f} vs {res['opp_power']:.1f})")

            next_round.append(winner)
        # advance bracket
        current = next_round
        round_num += 1

    # finish
    champion = current[0]
    print(f"\n=== Campeão do Campeonato: {champion.name} ===")
    if champion is team:
        prize = 100000
        team.money += prize
        print(f"Parabéns! Você venceu o campeonato e ganhou ${prize}. Saldo: ${team.money}")
    else:
        print("Você não venceu o campeonato desta vez.")

def select_real_team():
    print("\n=== Escolha uma equipe real para treinar ===")
    region_list = list(TEAMS_BY_REGION.keys())
    for idx, region in enumerate(region_list, 1):
        print(f"{idx}. {region}")
    while True:
        try:
            region_choice = int(input("Escolha a região (número): ").strip())
            if 1 <= region_choice <= len(region_list):
                region = region_list[region_choice - 1]
                break
            else:
                print("Região inválida.")
        except ValueError:
            print("Digite um número válido.")
    print(f"\nTimes disponíveis em {region}:")
    teams = TEAMS_BY_REGION[region]["fortes"] + TEAMS_BY_REGION[region]["fracos"]
    for idx, team_name in enumerate(teams, 1):
        # Verifica se o time tem dados reais
        has_real_data = "times" in TEAMS_BY_REGION[region] and team_name in TEAMS_BY_REGION[region]["times"]
        special_mark = " ★" if has_real_data else ""  # Marca times com dados reais
        print(f"{idx}. {team_name}{special_mark}")
    while True:
        try:
            team_choice = int(input("Escolha o time (número): ").strip())
            if 1 <= team_choice <= len(teams):
                team_name = teams[team_choice - 1]
                break
            else:
                print("Time inválido.")
        except ValueError:
            print("Digite um número válido.")
            
    # Usa generate_ai_team para criar o time com jogadores reais se disponíveis
    team = generate_ai_team(region, team_name)
    
    # Ajusta o dinheiro inicial para um valor padrão
    team.money = 100000
    
    return team

def main_menu():
    team = select_real_team()
    while True:
        print(f"\n=== Gerenciamento de Esports - {team.name} ({team.region}) (Saldo: ${team.money}) ===")
        print("1. Ver jogadores")
        print("2. Contratar jogador")
        print("3. Demitir jogador")
        print("4. Treinar jogador")
        print("5. Alterar cargo de jogador")
        print("6. Montar lineup e jogar uma partida")
        print("7. Jogar campeonato")
        print("8. Salvar time")
        print("9. Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            view_players(team)
        elif choice == "2":
            hire_player(team)
        elif choice == "3":
            fire_player(team)
        elif choice == "4":
            train_player(team)
        elif choice == "5":
            change_role(team)
        elif choice == "6":
            play_match_menu(team)
        elif choice == "7":
            play_championship(team)
        elif choice == "8":
            save_team(team)
            print(f"Time salvo em {SAVE_FILE}.")
        elif choice == "9":
            print("Saindo...")
            save_team(team)
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    print("\nBem-vindo ao Gerenciador de Esports!")
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nSaindo. Progresso salvo.")
        # tenta salvar antes de sair
        try:
            save_team(load_team())
        except Exception:
            pass
        sys.exit(0)