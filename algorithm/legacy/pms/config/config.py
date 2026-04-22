import os
import sys

import yaml


class Config:
    def __init__(self):
        config_file_path = self.resource_path("config/config.yaml")  # window version
        with open(config_file_path, encoding="UTF8") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def resource_path(self, relative_path):  ### sim - 안씀
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_tag_info(self, tagname):  ### sim - 안씀
        for tag_info in self.tag_config["mapping"]:
            if tag_info["tagname"] is None:
                continue
            if tag_info["tagname"] in tagname:
                return (
                    tag_info["table"],
                    tag_info["eq_id"],
                    tag_info["column"],
                    tag_info["type"],
                )
            pass
        return "", "", "", ""

    def get_mapping_id(self, channel_id):
        #print('get_mapping_id - channel_id:', channel_id)
        #print('self.config["PMS_mapping"]:',self.config["PMS_mapping"])
        # next(item for item in self.tag_config['mapping'] if (item['tagname'] is not None) and (item['tagname'] in tagname))
        #print('self.config["PMS_mapping"][channel_id]',self.config["PMS_mapping"][channel_id])
        return self.config["PMS_mapping"][channel_id]

    def get_on_off_id(self, motor_id):
        # next(item for item in self.tag_config['mapping'] if (item['tagname'] is not None) and (item['tagname'] in tagname))
        return self.config["on_off"][motor_id]

    def get_frequency_value(self, scada_id):
        # next(item for item in self.tag_config['mapping'] if (item['tagname'] is not None) and (item['tagname'] in tagname))
        return self.config["frequency"][scada_id]

    def get_motor_id(self, id):
        return self.config["motor"][id]

    def get_pump_id(self, id):
        return self.config["pump"][id]

    def get_db_info(self):
        return (
            self.config["database"]["db_ip"],
            self.config["database"]["db_port"],
            self.config["database"]["db_name"],
            self.config["database"]["db_id"],
            self.config["database"]["db_pw"],
        )

    def save_taglist(self):  ### sim - 안씀
        self.tagset = set([])
        self.tagdict = {}

        for tag_info in self.tag_config["mapping"]:
            if tag_info["tagname"] is None:
                continue
            self.tagset.add(tag_info["tagname"])
        for tag_info in self.tag_config["mapping"]:
            if tag_info["tagname"] is None:
                continue
            self.tagdict[tag_info["tagname"]] = tag_info


config = Config()

if __name__ == "__main__":
    config = Config()
    # config.write_taglist()
