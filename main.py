from replay import BattleReplay
from char import CharMap
from stage import StageMap


if __name__ == "__main__":
    char_map = CharMap("data/char_table.json")
    stage_map = StageMap("data/stage_table.json")

    replay = BattleReplay()
    replay.load("tmp/replay.dat", mode="e")
    replay.save("tmp/replay.json", mode="d")

    replay.parse(char_map, stage_map)
    replay.show_info()
    replay.save_log("tmp/battle_log.csv")
