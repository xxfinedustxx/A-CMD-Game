from colorama import Fore, Style

ASTEROID_TYPES = {
    "xxs_rock": {
        "tier": 1,
        "name": "Metalic Tiny Tiny Rock",
        "hp": 10,
        "color": Style.DIM + Fore.WHITE,  
        "shape": [
            "o0"
        ],
        "drops": {"Fe": (5, 15),
                  "H2O": (1, 3)
                  }
    },
    "xs_rock": {
        "tier": 2,
        "name": "Metalic Tiny Rock",
        "hp": 20,
        "color": Fore.CYAN,  
        "shape": [
            " __ ",
            "(o \\",
            "\\__)"
        ],
        "drops": {
            "Fe": (5, 20),
            "Cu": (1, 5)
        }
    },
    "s_rock": {
        "tier": 3,
        "name": "Carbonic Small Rock",
        "hp": 40,
        "color": Fore.YELLOW,  
        "shape": [
            "  __  ",
            " [q \\ ",
            "/   0\\",
            "\\o   )",
            " \\__) "
        ],
        "drops": {
            "Fe": (10, 30),
            "Cu": (5, 10),
            "C": (1, 3),
            "H2O": (1, 2)
        }
    },
    "m_rock":{
        "tier": 4,
        "name": "Uranium Medium Rock",
        "hp": 80,
        "color": Fore.GREEN,  
        "shape": [
            "   ___   ",
            "  /   \\  ",
            " / o o \\ ",
            "|   0   |",
            " \\__^__/ "
        ],
        "drops": {
            "U": (20, 50),
            "Th": (10, 20),
            "C": (5, 10)
            }
        },
    
}