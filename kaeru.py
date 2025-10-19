# pyright: reportAttributeAccessIssue=false
# pyright doesn't work well with PySide6; lots of type errors even in code from the
# documentation

from collections.abc import Sequence
import json
import random
import sys
from typing import Any

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Slot

from ui.ui_kaeru import Ui_MainWindow
from inflection import (
    AdjectiveType, AdjectiveInflection,
    VerbType, VerbInflection
)
import conjugator


class Kaeru(QMainWindow):
    ui: Ui_MainWindow
    """Loaded from the compiled kaeru.ui."""
    words: Sequence[dict[str, Any]]
    """Words available for the quiz."""
    correct_answer: str
    """The correctly conjugated word."""
    current_streak: int
    """The number of words the user has conjugated correctly in a row."""
    highest_streak: int
    """The highest number of words the user has conjugated correctly in a row."""

    def __init__(self, words: Sequence[dict[str, Any]]):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.answer_button.clicked.connect(self.process_answer)
        self.ui.answer.returnPressed.connect(self.ui.answer_button.click)

        # TODO: load these preferences from a db
        self.ui.option_show_kana_reading.toggled.connect(
            self.toggle_showing_kana_reading
        )
        self.ui.option_show_word_type.toggled.connect(
            self.toggle_showing_word_type
        )

        self.current_streak = 0
        self.highest_streak = 0  # TODO: load this from a db?
        self.words = words
        self.ask_new_random_word()

    def show_verb_inflection(self, inflection: VerbInflection):
        """Show the nondefault features of the given verb inflection."""
        nondefault_features = []
        if inflection.base_form is VerbInflection.BaseForm.POLITE:
            nondefault_features.append('POLITE')
        elif inflection.base_form is VerbInflection.BaseForm.TE:
            nondefault_features.append('て-FORM')

        if inflection.tense is VerbInflection.Tense.PAST:
            nondefault_features.append('PAST')
        if inflection.polarity is VerbInflection.Polarity.NEGATIVE:
            nondefault_features.append('NEGATIVE')
        self.ui.conjugation.setText(' '.join(nondefault_features))

    def show_adjective_inflection(self, inflection: AdjectiveInflection):
        """Show the nondefault features of the given adjective inflection."""
        nondefault_features = []
        if inflection.polarity is AdjectiveInflection.Polarity.NEGATIVE:
            nondefault_features.append('NEGATIVE')
        if inflection.tense is AdjectiveInflection.Tense.PAST:
            nondefault_features.append('PAST')
        if inflection.politeness is AdjectiveInflection.Politeness.POLITE:
            nondefault_features.append('POLITE')
        self.ui.conjugation.setText(' '.join(nondefault_features))

    def ask_new_random_word(self):
        """Ask to conjugate a new random word."""
        random_word = random.choice(self.words)
        dictionary_form_word: str = random_word['word']
        word_kana_reading: str | None = random_word['kana']

        self.ui.word_to_conjugate.setText(dictionary_form_word)
        self.ui.kana_reading.setText(
            f'（{word_kana_reading}）'
            if word_kana_reading is not None else '　'  # still occupy space
        )
        self.ui.answer.setText('')

        type_str = random_word['type']
        if type_str.startswith('verb'):
            try:
                verb_type = VerbType(type_str)
            except ValueError:
                print(
                    f'error: verb {dictionary_form_word} of illegal type'
                    + f' "{type_str}"',
                    file=sys.stderr
                )
                exit(4)
            random_inflection = VerbInflection.generate_random()

            self.correct_answer = conjugator.conjugate_verb(
                dictionary_form_word,
                verb_type,
                random_inflection
            )
            self.ui.word_type.setText(verb_type.label)
            self.show_verb_inflection(random_inflection)
        elif type_str.startswith('adjective'):
            try:
                adjective_type = AdjectiveType(type_str)
            except ValueError:
                print(
                    f'error: adjective {dictionary_form_word} of illegal type'
                    + f' "{type_str}"',
                    file=sys.stderr
                )
                exit(4)
            random_inflection = AdjectiveInflection.generate_random(adjective_type)

            self.correct_answer = conjugator.conjugate_adjective(
                dictionary_form_word,
                adjective_type,
                random_inflection
            )
            self.ui.word_type.setText(adjective_type.label)
            self.show_adjective_inflection(random_inflection)
        else:
            print(
                f'error: word {dictionary_form_word} of illegal type'
                + f' "{type_str}"',
                file=sys.stderr
            )
            exit(4)

    def update_scores(self):
        """Update the current streak and the highest streak values."""
        self.ui.current_streak.setText(str(self.current_streak))
        self.ui.highest_streak.setText(str(self.highest_streak))

    Slot()
    def process_answer(self):
        """If the answer is correct, ask a new one. Otherwise, show an error.

        Update scores accordingly.
        """
        is_correct = self.ui.answer.text().strip() == self.correct_answer
        if is_correct:
            # TODO: proper notification
            print('correct!')
            self.current_streak += 1
            self.ask_new_random_word()
        else:
            self.current_streak = 0
            # TODO: proper notification
            print('incorrect.')

        beat_highest_streak = self.highest_streak < self.current_streak
        if beat_highest_streak:
            self.highest_streak = self.current_streak
        self.update_scores()

    Slot()
    def toggle_showing_kana_reading(self, checked: bool):
        """Display the kana reading if this option is checked; hide it otherwise."""
        if checked:
            self.ui.kana_reading.show()
        else:
            self.ui.kana_reading.hide()

    Slot()
    def toggle_showing_word_type(self, checked: bool):
        """Display the word type if this option is checked; hide it otherwise."""
        if checked:
            self.ui.word_type.show()
        else:
            self.ui.word_type.hide()


if __name__ == "__main__":
    words: list[dict]
    try:
        with open('vocab.json') as vocab_file:
            words = json.load(vocab_file)
    except FileNotFoundError:
        print(
            'error: the vocab.json file does not exist. please run'
            + ' `python3 make-vocab.py` to build it.',
            file=sys.stderr
        )
        exit(1)
    except OSError:
        print(
            'error: could not open vocab.json.',
            file=sys.stderr
        )
        raise
    except json.decoder.JSONDecodeError:
        print(
            'error: vocab.json is malformed. please rebuild it with'
            + ' `python3 make-vocab.py`.',
            file=sys.stderr
        )
        exit(2)

    if not words:
        print(
            'error: vocab.json is malformed. please rebuild it with'
            + ' `python3 make-vocab.py`.',
            file=sys.stderr
        )
        exit(2)

    print(f'{len(words)} words loaded.\n')

    app = QApplication([])

    kaeru = Kaeru(words)
    kaeru.resize(800, 600)
    kaeru.show()

    sys.exit(app.exec())
