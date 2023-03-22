import json


class CharMap:
    def __init__(self, path: str):
        self.data = {}
        self.load(path)

    def load(self, path: str = "data/char_table.json"):
        with open(path, encoding='utf-8') as file:
            self.data = json.load(file)

    def get(self, key):
        return self.data.get(key)


if __name__ == "__main__":
    char_map = {}

    with open("data/char_table_origin.json", encoding='utf-8') as file:
        char_table = json.load(file)

    for key, value in char_table.items():
        char_map[key] = value["name"]

    with open("data/char_table.json", "w", encoding='utf-8') as file:
        json.dump(char_map, file, indent=4, ensure_ascii=False)
    
    print("char table dumped")

