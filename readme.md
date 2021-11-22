# Play Variation Engine

This project is a python script for incorporating text generation systems (particularly GPT3) to iteratively re-write dialogue for the purposes of improvisational experimentation. The code powering the logic of the system is in `play_engine.py` (The `Play` class) The notebook `play_variations.ipynb` is the basic implementation of the system using the GPT3 API.

The primary artistic inspiration for this project is Samuel Beckett's 1963 one-act [_Play_ (Play)](<https://en.wikipedia.org/wiki/Play_(play)>), a devastatingly strange little piece that was made into an [excellent short film in 2001](https://www.youtube.com/watch?v=s2QJ0FYE3pw). In Beckett's script the instruction "[REPEAT PLAY]" is found as a stage direction near the end, with notes to explore variations on repetition. The play engine takes this stage direction and approaches it with a generative twist by gradually re-writing the dialogue using GPT3 on multiple iterations through the script.

In the current implementation, the engine generates 4 variations, each progressively more defined by gpt3 intervention. The final version contains only the first three lines of the original. The slow process and structure of the prompt system makes the shift gradual and relatively coherent, but beautiful and bizarre variations can and do emerge.

The system works for any correctly formatted script, however, so I have also experimented with the famous dialogue in Act II, Scene 1 of _The Taming of the Shrew_. The results for each experiment can be found in the "play_variations" and "shrew_variations" folders.

## Script Format

To run a script through the engine it must be formatted correctly in a text file.

- Each line of character of Dialogue must be on a single text line, starting with the name of the speaker followed by a colon (i.e. `Romeo:`)
- All stage directions must be on a single line encased in brackets (i.e. `[Exit: Stage Left]`)

## Class Methods

The `Play` class must be instantiated with a path to a .txt file with a properly formatted script as well as a `variation_function` which will return line variations based on an input prompt (such as the gpt3 method in the notebook). The class has the following helper methods:

- `print_play(variations_only<bool>)` will print the current version of the script to console. Pass "True" to the `variations_only` to print only the lines that have been varied.
- `print_changes()` will print a list of the changed lines (along with their original form) to the console. Useful for analyzing the tone of the variations.
- `run_play(speed)` will print the play to the console with a pause between each line (number of seconds defined by the speed variable). This is useful to create something like a live "reading" of the play
- `save_current_script(filename, mark_variations<bool>)` will save the current version of the script in a new text file. Pass `True` to the `mark_variations` argument to note the lines which have been altered. -`make_variations(chance, overwrite_variations<bool>, protected_lines, depth, log<bool>)` is the primary tool of the class. This will run through the script and make variations to the lines based on the chance variable (a float between 0 and 1). Pass `True` to the second argument to allow the system to rewrite a line that has already been varied, or `False` to lock in changes. `protected_lines` should be a positive integer and defines how many lines at the start of the script will never be rewritten. `depth` should be a positive integer and defines how many lines backwards the system will look when generating prompts for the variation algorithm (useful when tuning to different algorithms). Pass `True` to the log variable to live-print any changes made to the console for monitoring.
