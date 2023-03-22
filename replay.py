import base64
import json
import zipfile
from io import BytesIO

from char import CharMap
from stage import StageMap


def decode(battle_replay):
    binary_data = base64.b64decode(battle_replay)
    try:
        with BytesIO(binary_data) as bytes_io:
            with zipfile.ZipFile(bytes_io) as zip_file:
                for file_name in zip_file.namelist():
                    # file_info = zip_file.getinfo(file_name)
                    # print(file_info)
                    with zip_file.open(file_name) as file:
                        decrypted_data = file.read()
        if decrypted_data is not None:
            return json.loads(decrypted_data.decode("utf-8"))
    except Exception as ex:
        print(f"Error while decrypting battle replay: {ex}")
    return None


def encode(data):
    try:
        with BytesIO() as bytes_io:
            with zipfile.ZipFile(bytes_io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                with zip_file.open('default_entry', mode='w') as file:
                    file.write(json.dumps(data).encode())
                # for file_name in zip_file.namelist():
                #     file_info = zip_file.getinfo(file_name)
                #     print(file_info)
                binary_data = bytes_io.getvalue()
                base64_data = base64.b64encode(binary_data).decode()
                return base64_data
    except Exception as ex:
        print(f"Error while processing battle replay: {ex}")
    return None


class BattleReplay:
    def __init__(self):
        self.data = None
        self.squad = []
        self.log = []
        self.meta = {}

    def load(self, path: str, mode: str = "e"):
        '''
        e: encrypted
        d: decrypted
        '''
        if mode == "d":
            with open(path) as file:
                self.data = json.load(file)
        elif mode == "e":
            with open(path) as file:
                battle_replay = file.read()
            self.data = decode(battle_replay)


    def save(self, path: str, mode: str = "e"):
        '''
        e: encrypted
        d: decrypted
        '''
        if mode == "d":
            with open(path, "w") as file:
                json.dump(self.data, file, indent=4)
        elif mode == "e":
            battle_replay = encode(self.data)
            with open(path, "w") as file:
                file.write(battle_replay)


    def parse(self, char_map: CharMap, stage_map: StageMap):
        self.parse_meta(stage_map)
        self.parse_squad(char_map)
        self.parse_log(char_map)


    def parse_meta(self, stage_map: StageMap):
        meta = self.data.get("journal").get("metadata")
        # stage
        stage_id = meta.get("stageId")
        stage = stage_map.get(stage_id)
        if stage_id[-2:] == "f#":
            stage = stage + "(突袭)"

        # time
        save_time = meta.get("saveTime")
        day = save_time.split("T")[0]
        day_frac = save_time.split("T")[1].split(".")[0]

        self.meta["stage"] = stage
        self.meta["stage_id"] = stage_id
        self.meta["day"] = day
        self.meta["day_frac"] = day_frac


    def parse_squad(self, char_map:CharMap):
        squad = self.data.get("journal").get("squad")
        for char in squad:
            id = char.get("skinId").split("#")[0]
            name = char_map.get(id)
            self.squad.append(name)


    def parse_log(self, char_map: CharMap):
        logs = self.data.get("journal").get("logs")
        for log in logs:
            # time
            time_stamp = log.get("timestamp")
            time_sec = int(time_stamp)
            time_frame = int(30 * (time_stamp - time_sec))

            # char
            id = log.get("signiture").get("charId")
            name = char_map.get(id)

            # direction
            dir_map = ["上", "右", "下", "左"]
            dir_index = log.get("direction")
            dir = dir_map[dir_index]

            # position
            pos = log.get("pos")
            pos_x = pos.get("row")
            pos_y = pos.get("col")

            self.log.append([time_sec, time_frame, name, dir, pos_x, pos_y])


    def save_log(self, path: str):
        with open(path, "w", encoding='utf-8') as file:
            file.write("时间(s), 时间(帧), 干员, 方向, 坐标(x), 坐标(y)\n")
            for log in self.log:
                file.write(f"{log[0]}, {log[1]}, {log[2]}, {log[3]}, {log[4]}, {log[5]}\n")


    def get(self, key) -> map:
        return self.data.get(key)
    
    
    def show_info(self):
        print("代理作战概要:")
        print(f"  - 关卡: {self.meta['stage']} ({self.meta['stage_id']})")
        print(f"  - 时间: {self.meta['day']} {self.meta['day_frac']}")
        print(f"  - 阵容: {self.squad}")
