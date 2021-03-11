import sys
import numpy as np
import json

_filenames = ["data_scenarios_a_example.in",
              "data_scenarios_b_mumbai.in",
              "data_scenarios_c_metropolis.in",
              "data_scenarios_d_polynesia.in",
              "data_scenarios_e_sanfrancisco.in",
              "data_scenarios_f_tokyo.in"]
if len(sys.argv) < 2:
    print("provide the file name!")
    exit()

_filename = sys.argv[1]

_W = 0
_H = 0
_N = 0
_M = 0
_R = 0
_Buildings = []
_Antennas = []


def score(building, antenna):
    dist = abs((building['x'] - antenna['x'])) + abs( (building['y'] - antenna['y']))
    if dist > antenna["range"]:
        return 0
    value = (building['connection'] * antenna['connection']) - building['latency'] * dist
    return value


def parse_file(filename):
    global _W, _H
    global _N, _M, _R
    global _Buildings, _Antennas

    f = open(filename, "r")
    lines = f.readlines()

    parts = lines[0].split()
    _W = int(parts[0])
    _H = int(parts[1])

    parts = lines[1].split()
    _N = int(parts[0])
    _M = int(parts[1])
    _R = int(parts[2])

    current_line = 2
    current_item = 0
    while current_line < 2 + _N:
        parts = lines[current_line].split()
        building = {"id": current_item,
                    "x": int(parts[0]),
                    "y": int(parts[1]),
                    "latency": int(parts[2]),
                    "connection": int(parts[3]),
                    "antenna_id": -1
                    }
        _Buildings.append(building)
        current_line = current_line + 1
        current_item = current_item + 1

    current_item = 0
    while current_line < 2 + _N + _M:
        parts = lines[current_line].split()
        antenna = {"id": current_item,
                   "range": int(parts[0]),
                   "connection": int(parts[1]),
                   "buildings": []
                   }
        _Antennas.append(antenna)
        current_line = current_line + 1
        current_item = current_item + 1


def closest_building(building):
    global _Buildings
    global _W, _H
    min_val = diff_position(0, 0, _W, _H)
    current_building = 0
    nearest_building = 0
    for b in _Buildings:

        val = diff_position(b["x"], b["y"], building["x"], building["y"])
        if b["antenna_id"] >= 0:
            if val < min_val and val != 0:
                min_val = val
                nearest_building = current_building
        current_building = current_building + 1
    return _Buildings[nearest_building]


def diff_towards(x, y, building):
    diff_x = building["x"] - x
    diff_y = building["y"] - y
    #
#    if abs(diff_x) > abs(diff_y):
#        return [1,0]
#    else
#        return [0, 1]


def diff_position(b1_x, b1_y, b2_x, b2_y):
    return abs(b1_x - b2_x) + abs(b1_y - b2_y)


def output(filename):
    total_antennas_used = [x for x in _Antennas if len(x["buildings"]) != 0]
    f = open("{}.solved".format(filename), "w+")
    print(len(total_antennas_used))
    f.write(str(len(total_antennas_used)) + "\n")
    for a in _Antennas:
        f.write("{} {} {}\n".format(a["id"], a["x"], a["y"]))
        print("{} {} {}".format(a["id"], a["x"], a["y"]))


def solve_input(filename):
    parse_file(filename)
    _Buildings.sort(key=lambda x: x["connection"], reverse=True)
    _Antennas.sort(key=lambda x: x["connection"], reverse=True)

    current_antenna = 0
    for _antenna in _Antennas:
        _antenna["x"] = _Buildings[current_antenna]["x"]
        _antenna["y"] = _Buildings[current_antenna]["y"]

        _Buildings[current_antenna]['antenna_id'] = _antenna["id"]
        _antenna["buildings"].append(_Buildings[current_antenna]["id"])
        if current_antenna >= len(_Buildings):
            break
        current_antenna = current_antenna + 1

    [x for x in _Antennas if x["id"] == 0]

    ###########

    current_item = 0
    total_file_score = 0
    for _a in _Antennas:
        total_file_score = total_file_score + (score(_Buildings[current_item], _a))
        current_item = current_item + 1
    print("total score ({}): {}".format(filename, total_file_score))
    return total_file_score


total_score = 0
for f in _filenames:
    total_score = total_score + solve_input(f)

print("total score : {}".format(total_score))