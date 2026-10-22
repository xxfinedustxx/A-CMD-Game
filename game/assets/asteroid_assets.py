from colorama import Fore, Style

ASTEROID_TYPES = {
    "xxs_rock": {
        "name": "Metalic Tiny Tiny Rock",
        "hp": 10,
        "color": Style.DIM + Fore.WHITE,  # Prigušena bijela / siva
        "shape": [
            "o0"
        ],
        "drops": {"Fe": (5, 15)}
    },
    "xs_rock": {
        "name": "Metalic Tiny Rock",
        "hp": 20,
        "color": Fore.CYAN,  # Metalik cijan/plava
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
        "name": "Carbonic Small Rock",
        "hp": 40,
        "color": Fore.YELLOW,  # Žućkasta/smećkasta za ugljik
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
            "C": (1, 3)
        }
    },
}