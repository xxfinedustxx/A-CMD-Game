# ASCII symbols for the game assets
ENTITYS = {
    "player": "@",
    "enemy_1": "∞",
    "enemy_2": "Ω",
    "enemy_3": "Σ",
}

SYMBOLS = {

}

MATERIALS = {
    "H":{
        "name":"Hydrogen",
        "tier":1,
        "is_fuel":True
    },
    "O":{
        "name":"Oxygen",
        "tier":1,
        "is_fuel":False
    },
    "Ag":{
        "name":"Silver",
        "tier":3,
        "is_fuel":False
    },
    "Al":{
        "name":"Aluminum",
        "tier":1,
        "is_fuel":False
    },
    "Fe": {
        "name": "Iron", 
        "tier":1,
        "is_fuel": False
    },
    "Cu": {
        "name": "Copper", 
        "tier":1,
        "is_fuel": False
    },
    "C": {
        "name": "Carbon", 
        "tier":1, 
        "is_fuel": True
    },
    "Au": {
        "name": "Gold",
        "tier":3,
        "is_fuel": False
    },
    "H2O": {
        "name": "Water", 
        "tier":1,
        "is_fuel": False 
    },
    "Th": {
        "name": "Thorium", 
        "tier":2, 
        "is_fuel": True
    },
    "U": {
        "name": "Uranium", 
        "tier":4, 
        "is_fuel": True
    },
    "Pu": {
        "name": "Plutonium", 
        "tier":5, 
        "is_fuel": True
    },
}

FUEL_PROPERTIES = {
    "C": {
        "base_output": 4,
        "heat_output": 0,
        "usage_rate": 1,
        "byproduct":None,
        "byproduct_amount": 0,
    },
    "Th":{
        "base_output": 14,
        "heat_output":10,
        "usage_rate":2,
        "byproduct":None,
        "byproduct_amount": 0.5,
    },
    "U": {
        "base_output": 28,
        "heat_output":20, 
        "usage_rate":2,
        "byproduct":"Pu",
        "byproduct_amount": 0.05,
    },
}

POWER_GEN_CONFIG = {
    "Pw1": {
        "name": "Basic Carbon Generator", 
        "tier":1, "output": 4, 
        "accept_fuels": ["C"], 
        "usage_rate": 1, 
        "needs_cooler":False
    },
    "Pw2": {
        "name": "Advanced Carbon Generator", 
        "tier":2, "output": 8, "accept_fuels": ["C"], 
        "usage_rate": 2,
        "needs_cooler":False
    },
    "Pw3": {"name": "Basic RTG Generator", 
            "tier":2, 
            "output": 14, 
            "accept_fuels": ["Th", "Pu"], 
            "usage_rate": 1,
            "needs_cooler":True
        },
    "Pw4": {
        "name": "Basic Nuclear Reactor", 
        "tier":3, 
        "output": 28, 
        "accept_fuels": ["Th", "Pu", "U"], 
        "usage_rate": 1,
        "needs_cooler":True
    },
}