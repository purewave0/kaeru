# pyright: reportAttributeAccessIssue=false
# pyright doesn't work well with PySide6; lots of type errors even in code from the
# documentation

import argparse
from collections.abc import Sequence
import json
import logging
import random
import sys
from typing import Any
import sqlite3

from PySide6.QtWidgets import QDialog, QMainWindow, QApplication
from PySide6.QtCore import Slot, QTimer
from PySide6.QtGui import QScreen

from ui.ui_kaeru import Ui_MainWindow
from ui.ui_about import Ui_Dialog
from inflection import (
    AdjectiveType, AdjectiveInflection,
    VerbType, VerbInflection
)
import conjugator
import dbapi
from constants import DATABASE_PATH


class AboutKaeru(QDialog):
    """About dialog."""
    ui: Ui_Dialog
    """Loaded from the compiled about.ui."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


class Kaeru(QMainWindow):
    ui: Ui_MainWindow
    """Loaded from the compiled kaeru.ui."""
    words: Sequence[dict[str, Any]]
    """Words available for the quiz."""
    correct_answer: str
    """The correctly conjugated word."""
    reveal_answer_on_failure: bool
    """Whether the correct answer should be revealed when the user gets it wrong."""
    current_streak: int
    """The number of words the user has conjugated correctly in a row."""
    highest_streak: int
    """The highest number of words the user has conjugated correctly in a row."""
    conn: sqlite3.Connection
    """The database connection."""

    SCORE_COLOUR_FLASH_DURATION = 700
    """For how many milliseconds the score colour changes to indicate a score change."""
    FEEDBACK_DURATION = 2_000
    """For how many milliseconds the feedback is displayed."""

    def __init__(self, words: Sequence[dict[str, Any]]):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        feedback_size_policy = self.ui.feedback.sizePolicy()
        feedback_size_policy.setRetainSizeWhenHidden(True)
        self.ui.feedback.setSizePolicy(feedback_size_policy)
        self.ui.feedback.hide()

        self.ui.answer_button.clicked.connect(self.process_answer)
        self.ui.answer.returnPressed.connect(self.ui.answer_button.click)

        self.conn = sqlite3.connect(DATABASE_PATH)
        dbapi.create_table_and_user_if_nexists(self.conn)

        self.ui.option_show_kana_reading.toggled.connect(
            self.toggle_showing_kana_reading
        )
        self.ui.option_show_word_type.toggled.connect(
            self.toggle_showing_word_type
        )
        self.ui.option_reveal_answer_on_failure.toggled.connect(
            self.toggle_revealing_answer_on_failure
        )
        self.ui.action_about.triggered.connect(self.show_about_dialog)

        self.ui.option_show_kana_reading.setChecked(
            dbapi.get_show_kana_reading(self.conn)
        )
        self.ui.option_show_word_type.setChecked(
            dbapi.get_show_word_type(self.conn)
        )
        self.reveal_answer_on_failure = dbapi.get_reveal_answer_on_failure(self.conn)
        self.ui.option_reveal_answer_on_failure.setChecked(
            self.reveal_answer_on_failure
        )

        self.current_streak = 0
        self.highest_streak = dbapi.get_highest_streak(self.conn)
        self.update_scores()
        self.words = words
        self.ask_new_random_word()

    @Slot()
    def show_about_dialog(self) -> None:
        """Show the About dialog."""
        dialog = AboutKaeru()
        dialog.exec()

    def show_verb_inflection(self, inflection: VerbInflection) -> None:
        """Show the nondefault features of the given verb inflection."""
        nondefault_features = []
        if inflection.base_form is VerbInflection.BaseForm.POLITE:
            nondefault_features.append(self.tr('POLITE'))
        elif inflection.base_form is VerbInflection.BaseForm.TE:
            nondefault_features.append(self.tr('て-FORM'))

        if inflection.tense is VerbInflection.Tense.PAST:
            nondefault_features.append(self.tr('PAST'))
        if inflection.polarity is VerbInflection.Polarity.NEGATIVE:
            nondefault_features.append(self.tr('NEGATIVE'))
        self.ui.conjugation.setText(' '.join(nondefault_features))

    def show_adjective_inflection(self, inflection: AdjectiveInflection) -> None:
        """Show the nondefault features of the given adjective inflection."""
        nondefault_features = []
        if inflection.polarity is AdjectiveInflection.Polarity.NEGATIVE:
            nondefault_features.append(self.tr('NEGATIVE'))
        if inflection.tense is AdjectiveInflection.Tense.PAST:
            nondefault_features.append(self.tr('PAST'))
        if inflection.politeness is AdjectiveInflection.Politeness.POLITE:
            nondefault_features.append(self.tr('POLITE'))
        self.ui.conjugation.setText(' '.join(nondefault_features))

    def ask_new_random_word(self) -> None:
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
                logging.error(
                    f'verb {dictionary_form_word} of illegal type "{type_str}"'
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
                logging.error(
                    f'adjective {dictionary_form_word} of illegal type "{type_str}"'
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
            logging.error(
                f'word {dictionary_form_word} of illegal type "{type_str}".'
            )
            exit(4)

    def notify_answer_was_correct(self) -> None:
        """Flash the current streak's value green to indicate the answer was correct."""
        self.ui.feedback.hide()
        self.ui.current_streak.setStyleSheet('color: #7ddf64;')
        QTimer.singleShot(
            Kaeru.SCORE_COLOUR_FLASH_DURATION,
            self.reset_score_colour_change
        )

    def notify_answer_was_incorrect(self) -> None:
        """Temporarily flash the current streak's value red and show error feedback.
        Include the correct answer if 'Reveal answer on failure' is checked.
        """
        self.ui.current_streak.setStyleSheet('color: #ff4b3e')
        QTimer.singleShot(
            Kaeru.SCORE_COLOUR_FLASH_DURATION, self.reset_score_colour_change
        )
        if self.reveal_answer_on_failure:
            self.ui.feedback.setText(
                self.tr(f'The correct answer is')
                + f' <b>{self.correct_answer}</b>.'
            )
        else:
            self.ui.feedback.setText(self.tr('Incorrect answer; try again.'))
        self.ui.feedback.show()
        QTimer.singleShot(
            Kaeru.FEEDBACK_DURATION, self.hide_feedback
        )

    @Slot()
    def reset_score_colour_change(self) -> None:
        """Reset the current streak's value colour."""
        self.ui.current_streak.setStyleSheet('')

    @Slot()
    def hide_feedback(self) -> None:
        """Hide the error feedback."""
        self.ui.feedback.hide()

    def update_scores(self) -> None:
        """Update the current streak and the highest streak value labels."""
        self.ui.current_streak.setText(str(self.current_streak))
        self.ui.highest_streak.setText(str(self.highest_streak))

    Slot()
    def process_answer(self) -> None:
        """If the answer is correct, ask a new one. Otherwise, show error feedback.

        Update scores accordingly.
        """
        if self.ui.feedback.isVisible():
            return

        answer = self.ui.answer.text().strip()
        if not answer:
            return
        is_correct = answer == self.correct_answer
        if is_correct:
            self.current_streak += 1
            self.notify_answer_was_correct()
            self.ask_new_random_word()
        else:
            self.current_streak = 0
            self.notify_answer_was_incorrect()

        beat_highest_streak = self.highest_streak < self.current_streak
        if beat_highest_streak:
            self.highest_streak = self.current_streak
            dbapi.set_highest_streak(self.conn, self.highest_streak)
        self.update_scores()

    Slot()
    def toggle_showing_kana_reading(self, checked: bool) -> None:
        """Display the kana reading if this option is checked, and store it in the
        database.
        """
        if checked:
            self.ui.kana_reading.show()
        else:
            self.ui.kana_reading.hide()
        dbapi.set_show_kana_reading(self.conn, checked)

    Slot()
    def toggle_showing_word_type(self, checked: bool) -> None:
        """Display the word type if this option is checked, and store it in the
        database.
        """
        if checked:
            self.ui.word_type.show()
        else:
            self.ui.word_type.hide()
        dbapi.set_show_word_type(self.conn, checked)

    Slot()
    def toggle_revealing_answer_on_failure(self, checked: bool) -> None:
        """Show the correct answer after incorrect attempts if this option is checked,
        and store it in the database.
        """
        self.reveal_answer_on_failure = checked
        dbapi.set_reveal_answer_on_failure(self.conn, checked)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description='Japanese verb & adjective conjugation trainer (GUI).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i',
        '--vocab-file',
        help='path to the JSON with verbs and adjectives for the quiz',
        type=str,
        default='vocab.json',
    )
    args = parser.parse_args()

    words: list[dict]
    try:
        with open(args.vocab_file) as vocab_file:
            words = json.load(vocab_file)
    except FileNotFoundError:
        logging.error(
            f'"{args.vocab_file}" does not exist. run `python3 gen-vocab.py`'
            + ' to build a vocab file.'
        )
        exit(1)
    except OSError:
        logging.error(f'could not open "{args.vocab_file}".')
        raise
    except json.decoder.JSONDecodeError:
        logging.error(
            f'{args.vocab_file} is malformed. run `python3 gen-vocab.py`'
            + ' to build a new vocab file.'
        )
        exit(2)

    if not words:
        logging.error(
            f'{args.vocab_file} is malformed. run `python3 gen-vocab.py`'
            + ' to build a new vocab file.'
        )
        exit(2)

    logging.info(f'{len(words)} words loaded.')

    app = QApplication([])

    kaeru = Kaeru(words)
    kaeru.resize(800, 700)
    kaeru.show()

    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geometry = kaeru.frameGeometry()
    geometry.moveCenter(center)
    kaeru.move(geometry.topLeft())

    sys.exit(app.exec())
