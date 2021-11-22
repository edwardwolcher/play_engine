import random
import sys
import copy
import time


class Cue:
    def __init__(self, line, play, idx) -> None:
        self.play = play
        self.idx = idx
        self.variation = False
        if line[0] == '[':
            self.type = "stage_direction"
            self.text = line.strip()
        else:
            self.type = "line"
            try:
                colon_idx = line.index(':')
                self.character = line[:colon_idx]
                self.text = line[colon_idx + 1:].strip()
            except ValueError:
                sys.exit(f"Script mis-formatted at line {idx}: {line}")

    def __str__(self) -> str:
        if self.type == 'stage_direction':
            return f"{self.text}\n"
        else:
            return f"{self.character}: {self.text}\n"

    def make_variation(self, variation_function,  max_depth):
        if self.type != "line":
            return
        prompt = f"{self.character}:"
        depth = 1
        while depth < max_depth and self.idx - depth >= 0:
            cue = self.play.cues[self.idx - depth]
            if cue.type == "line":
                prompt = str(cue) + prompt
            depth += 1
        new_text = variation_function(prompt)
        if len(new_text) > 0 and new_text[-1].isalpha():
            new_text += '—'
        self.text = new_text.strip()
        self.variation = True


class Play:
    def __init__(self, script, variation_function) -> None:
        self.cues = []
        with open(script, 'r') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                if len(line) < 1:
                    continue
                cue = Cue(line, self, idx)
                self.cues.append(cue)
        self.original = copy.deepcopy(self.cues)
        self.variation_function = variation_function

    def print_play(self, variations_only=False):
        for cue in self.cues:
            if variations_only and cue.variation:
                print(cue)
            else:
                print(cue)

    def print_changes(self):
        for cue in self.cues:
            if cue.variation:
                print(
                    f"[ORIGINAL] {self.original[cue.idx]}\n[VARIATION] {cue}")

    def run_play(self, speed=4):
        for cue in self.cues:
            print(cue)
            time.sleep(speed)

    def make_variations(self, chance=0.1, overwrite_variations=False, protected_lines=0, depth=10, log=False):
        print(
            f"Making variations to script with chance [{chance}] based on depth [{depth}]...")
        for cue in self.cues:
            if cue.idx + 1 < protected_lines or (cue.variation and not overwrite_variations):
                continue
            if random.random() < chance:
                cue.make_variation(self.variation_function, depth)
                if log:
                    print(
                        f"[ORIGINAL] {self.original[cue.idx]}\n[VARIATION] {cue}")

    def save_current_script(self, filename, mark_variations=True):
        with open(filename, "w") as f:
            for cue in self.cues:
                line = str(cue)
                if cue.variation and mark_variations:
                    line = line.strip() + " <variation>\n"
                f.write(line)
