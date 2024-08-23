import json
import os
from enum import Enum

#path to json, that holds information about convicts

# select whether messages are shown to other chat participents
ephemeral = False
# path to json dump
dict_path = "death.note"

#region classes
class Crime(str,Enum):
    blacklist = 1
    graylist = 2
    sus_manager = 3

class Criminal():
    def __init__(self,name:str,crime:Crime) -> None:
        self.name = name
        self.crime = crime
#endregion

#region conviction and helper methods
def read_dic() -> {str,str}:
    if os.path.isfile(dict_path):
        with open(dict_path) as f:
            return json.load(f)
    else:
        return {}

def save_json(dict:{str,str}):
    with open(dict_path, 'w') as f:
        json.dump(dict, f)

def condemn_subject(criminal:Criminal):
    dict = read_dic()
    dict[criminal.name] = criminal.crime
    save_json(dict)

#def condemn_subjects(criminals:list[Criminal]):
#    dict = read_dic()
#    for criminal in criminals:
#        dict[criminal.name] = criminal.crime
#    save_json(dict)
#endregion