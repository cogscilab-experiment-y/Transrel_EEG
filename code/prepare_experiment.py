import random
from os.path import join
import numpy as np
from psychopy import visual


def prepare_pair_to_draw(win, pair, size, sep_size, color, dist, pos, stimulus_type):
    ready_to_draw = []
    if stimulus_type == "image":
        ready_to_draw.append(visual.ImageStim(win, image=pair[0], size=size,     	    pos=(pos[0] + dist[0], pos[1])))
        ready_to_draw.append(visual.TextBox2(win,  text=pair[1],  letterHeight=sep_size, pos=(pos[0] + dist[1], pos[1]), color=color, alignment="centre"))
        ready_to_draw.append(visual.ImageStim(win, image=pair[2], size=size,             pos=(pos[0] + dist[2], pos[1])))
    elif stimulus_type == "text":
        ready_to_draw.append(visual.TextBox2(win, text=pair[0], letterHeight=size,     pos=(pos[0] + dist[0], pos[1]), color=color))
        ready_to_draw.append(visual.TextBox2(win, text=pair[1], letterHeight=sep_size, pos=(pos[0] + dist[1], pos[1]), color=color))
        ready_to_draw.append(visual.TextBox2(win, text=pair[2], letterHeight=size,     pos=(pos[0] + dist[2], pos[1]), color=color))
    return ready_to_draw


def prepare_to_draw(win, pair, pair_type, config):
    if pair_type == "stimulus":
        return prepare_pair_to_draw(win=win, pair=pair, size=config["stimulus_size"], sep_size=config["stimulus_separator_size"],
                                    color=config["stimulus_color"], dist=config["stimulus_dist"], pos=config["stimulus_pos"],
                                    stimulus_type=config["stimulus_type"])

    return prepare_pair_to_draw(win=win, pair=pair, size=config["answers_size"], sep_size=config["answers_separator_size"],
                                color=config["answers_color"], dist=config["answers_dist"], pos=config["answers_pos"][pair_type],
                                stimulus_type=config["stimulus_type"])


def prepare_trial(win, stimulus_list, separators, trial_type, config):
    elements = np.random.choice(stimulus_list, 2, replace=False)
    if trial_type == "control":
        stimulus = {"elements": [elements[0], separators["equal"], elements[1]], "type": "stimulus"}
        answers = np.random.choice([{"elements": [elements[0], separators["higher"], elements[1]], "type": "incorrect"},
                                    {"elements": [elements[1], separators["higher"], elements[0]], "type": "incorrect"},
                                    {"elements": [elements[0], separators["lower"],  elements[1]], "type": "incorrect"},
                                    {"elements": [elements[1], separators["lower"],  elements[0]], "type": "incorrect"}], 3, replace=False)
        answers = list(answers)
        answers.append({"elements": [elements[0], separators["equal"], elements[1]], "type": "correct"})
    else:
        separator = [separators["higher"], separators["lower"]]
        np.random.shuffle(separator)
        stimulus = {"elements": [elements[0], separator[0], elements[1]], "type": "stimulus"}
        answers = [{"elements": [elements[0], separator[1], elements[1]], "type": "incorrect"},
                   {"elements": [elements[1], separator[0], elements[0]], "type": "incorrect"},
                   {"elements": [elements[0], separators["equal"], elements[1]], "type": "incorrect"}]
        if trial_type == "easy":
            answers.append({"elements": [elements[0], separator[0], elements[1]], "type": "correct"})
        else:
            answers.append({"elements": [elements[1], separator[1], elements[0]], "type": "correct"})

    np.random.shuffle(answers)
    stimulus["draw"] = prepare_to_draw(win, stimulus["elements"], "stimulus", config)
    for n, answer in enumerate(answers):
        answer["draw"] = prepare_to_draw(win, answer["elements"], n, config)
    return {"trial_type": trial_type, "elements": elements, "stimulus": stimulus, "answers": answers}


def prepare_block(win, trials, config):
    # prepare stimulus list
    if config["stimulus_type"] == "image":
        stimulus_list = [join("images", "all_png", elem) for elem in config["stimulus_list"]]
    elif config["stimulus_type"] == "text":
        stimulus_list = config["stimulus_list"]
    else:
        raise Exception("Unknown stimulus_type. Chose from [image, text]")

    # prepare block
    block = []
    for trial_type, trail_n in trials.items():
        for i in range(trail_n):
            block.append(prepare_trial(win=win, stimulus_list=stimulus_list, separators=config["separators"], trial_type=trial_type, config=config))
    np.random.shuffle(block)
    return block
