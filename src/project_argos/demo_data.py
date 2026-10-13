from project_argos.models.game_entry import GameEntry


def create_demo_entries() -> list[GameEntry]:
    game_p5r = GameEntry("Persona 5 Royal")
    game_p5r.cover_art = "test_assets/p5r_test_1.png"
    game_p5r.add_alternative_title("P5R")
    game_p5r.add_category("JRPG")
    game_p5r.add_custom_tag("Persona series")

    game_firemb = GameEntry("Fire Emblem Shadow Dragon")
    game_firemb.add_custom_tag("Fire Emblem Series")
    game_firemb.cover_art = "test_assets/firemb_test_1.png"

    game_p4g = GameEntry("Persona 4 Golden")
    game_p4g.add_custom_tag("Persona series")
    game_p4g.cover_art = "test_assets/p4g_test_1.png"

    print("Demo data has been created!")

    return [
        game_p5r,
        game_firemb,
        game_p4g,
        GameEntry("Clair Obscur: Expedition 33"),
        GameEntry("Bastion"),
        GameEntry("Persona 3 Reload"),
        GameEntry("NieR:Automata"),
        GameEntry("Hades"),
    ]