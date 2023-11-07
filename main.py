import atexit
import csv
import random
from os.path import join
from psychopy import visual, core, event


from code.load_data import load_config
from code.screen_misc import get_screen_res
from code.show_info import part_info, show_info, show_stim, show_clock, show_timer, draw_stim_list
from code.check_exit import check_exit
from code.prepare_experiment import prepare_block

RESULTS = []
PART_ID = ""


@atexit.register
def save_beh_results():
    num = random.randint(100, 999)
    with open(join('results', '{}_beh_{}.csv'.format(PART_ID, num)), 'w', newline='') as beh_file:
        dict_writer = csv.DictWriter(beh_file, RESULTS[0].keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(RESULTS)


def run_block(win, config, trials, block_type, fixation, clock, extra_text, clock_image, timer, feedback):
    for n, trial in enumerate(trials):
        reaction_time = None
        key_pressed = ""
        acc = -1

        # fixation
        show_stim(fixation, config["fixation_time"], clock, win)
        print(trial)
        draw_stim_list(trial["stimulus"]["draw"], True)
        for answer in trial["answers"]:
            draw_stim_list(answer["draw"], True)
        draw_stim_list(extra_text, True)
        win.callOnFlip(clock.reset)
        win.flip()
        while clock.getTime() < config["answer_time"]:
            show_clock(clock_image, clock, config)
            show_timer(timer, clock, config)
            key_pressed = event.getKeys(keyList=config["reaction_keys"])
            if key_pressed:
                reaction_time = clock.getTime()
                key_pressed = key_pressed[0]
                break
            check_exit()
            win.flip()

        draw_stim_list(trial["stimulus"]["draw"], False)
        for answer in trial["answers"]:
            draw_stim_list(answer["draw"], False)
        draw_stim_list(extra_text, False)
        win.callOnFlip(event.clearEvents)
        win.flip()

        if key_pressed:
            answer_idx = config["reaction_keys"].index(key_pressed)
            acc = 1 if trial["answers"][answer_idx]["type"] == "correct" else 0
        correct_answer_idx = [i for i, answer in enumerate(trial["answers"]) if answer["type"] == "correct"][0]
        correct_key = config["reaction_keys"][correct_answer_idx]

        trial_results = {"n": n,
                         "block_type": block_type,
                         "rt": reaction_time,
                         "acc": acc,
                         "trial_type": trial["trial_tye"],
                         "key_pressed": key_pressed,
                         "correct_key": correct_key,
                         "all_info": trial}
        RESULTS.append(trial_results)

        if config[f"fdbk_{block_type}"]:
            show_stim(feedback[acc], config["fdbk_show_time"], clock, win)

        wait_time = config["wait_time"] + random.random() * config["wait_jitter"]
        show_stim(None, wait_time, clock, win)


def main():
    global PART_ID
    config = load_config()
    info, PART_ID = part_info(test=config["procedure_test"])

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, units='pix', screen=0, color=config["screen_color"])
    mouse = event.Mouse()
    mouse.setVisible(False)

    clock = core.Clock()

    fixation = visual.TextBox2(win, color=config["fixation_color"], text=config["fixation_text"], letterHeight=config["fixation_size"],
                               pos=config["fixation_pos"], alignment="center")

    clock_image = visual.ImageStim(win, image=join('images', 'clock.png'), interpolate=True, size=config['clock_size'], pos=config['clock_pos'])

    timer = visual.TextBox2(win, color=config["timer_color"], text=config["answer_time"], letterHeight=config["timer_size"],
                            pos=config["timer_pos"], alignment="center")

    extra_text = [visual.TextBox2(win, color=text["color"], text=text["text"], letterHeight=text["size"],pos=text["pos"], alignment="center")
                  for text in config["extra_text_to_show"]]

    feedback_text = (config["fdbk_incorrect"], config["fdbk_no_answer"], config["fdbk_correct"])
    feedback = {i: visual.TextBox2(win, color=config["fdbk_color"], text=text, letterHeight=config["fdbk_size"], alignment="center")
                for (i, text) in zip([0, -1, 1], feedback_text)}

    # EXPERIMENT
    experiment_trials = prepare_block(win=win, trials=config["experiment_trials"], config=config)
    print(experiment_trials)
    # run training
    if config["do_training"]:
        training_trials = prepare_block(win=win, trials=config["training_trials"], config=config)

        show_info(win, join('.', 'messages', 'instruction_training.txt'), text_color=config["text_color"],
                  text_size=config["text_size"], screen_res=screen_res)

        run_block(win=win, config=config, trials=training_trials, block_type="training", fixation=fixation,
                  clock=clock, extra_text=extra_text, clock_image=clock_image, timer=timer, feedback=feedback)

    # run experiment

    show_info(win, join('.', 'messages', 'instruction_experiment.txt'), text_color=config["text_color"],
              text_size=config["text_size"], screen_res=screen_res)

    run_block(win=win, config=config, trials=experiment_trials, block_type="experiment", fixation=fixation,
              clock=clock, extra_text=extra_text, clock_image=clock_image, timer=timer, feedback=feedback)

    # end
    show_info(win, join('.', 'messages', 'end.txt'), text_color=config["text_color"],
              text_size=config["text_size"], screen_res=screen_res)


if __name__ == "__main__":
    main()