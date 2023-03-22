import json


class StageMap:
    def __init__(self, path: str):
        self.data = {}
        self.load(path)

    def load(self, path: str = "data/stage_table.json"):
        with open(path, encoding='utf-8') as file:
            self.data = json.load(file)

    def get(self, key):
        return self.data.get(key)


if __name__ == "__main__":
    stage_map = {}

    with open("data/stage_table_origin.json", encoding='utf-8') as file:
        stage_table = json.load(file).get("stages")

    for key, value in stage_table.items():
        stage_map[key] = value["name"]

    with open("data/stage_table.json", "w", encoding='utf-8') as file:
        json.dump(stage_map, file, indent=4, ensure_ascii=False)
    
    print("stage table dumped")

