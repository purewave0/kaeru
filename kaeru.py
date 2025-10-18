# pyright: reportAttributeAccessIssue=false
# pyright doesn't work well with PySide6; lots of type errors even in code from the
# documentation

from collections.abc import Sequence
import json
import random
import sys
from typing import Any

from PySide6 import QtCore, QtWidgets, QtGui

from inflection import (
    AdjectiveType, AdjectiveInflection,
    VerbType, VerbInflection
)
import conjugator


class Kaeru(QtWidgets.QWidget):
    word_to_conjugate: QtWidgets.QLabel
    """Shows the word to be conjugated, in dictionary form."""
    kana_reading: QtWidgets.QLabel
    """The kana reading, if needed, of the word to conjugate."""
    word_type: QtWidgets.QLabel
    """Shows the type of word (see AdjectiveType, VerbType)."""
    conjugation_helper_text: QtWidgets.QLabel
    conjugation: QtWidgets.QLabel
    """The conjugation being requested."""
    answer: QtWidgets.QLineEdit
    """The answer field."""
    answer_button: QtWidgets.QPushButton
    """The button to send the answer."""

    correct_answer: str
    """The correctly conjugated word."""

    def __init__(self, words: Sequence[dict[str, Any]]):
        super().__init__()

        self.word_to_conjugate = QtWidgets.QLabel(
            '…',
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            textInteractionFlags=QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.kana_reading = QtWidgets.QLabel(
            '…',
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.word_type = QtWidgets.QLabel(
            '…',
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        self.conjugation_helper_text = QtWidgets.QLabel(
            'Conjugate to:',
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.conjugation = QtWidgets.QLabel(
            '…',
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.answer = QtWidgets.QLineEdit(
            '',
            placeholderText="Your answer",
        )
        self.answer_button = QtWidgets.QPushButton(
            'Answer',
            autoDefault=True,
        )

        self.answer_button.clicked.connect(self.process_answer)
        self.answer.returnPressed.connect(self.answer_button.click)

        # fonts

        large_font = QtGui.QFont()
        large_font.setPointSize(64)
        medium_font = QtGui.QFont()
        medium_font.setPointSize(28)
        small_font = QtGui.QFont()
        small_font.setPointSize(14)

        self.word_to_conjugate.setFont(large_font)
        self.kana_reading.setFont(small_font)
        self.word_type.setFont(small_font)
        self.conjugation_helper_text.setFont(small_font)
        self.conjugation.setFont(medium_font)
        self.answer.setFont(medium_font)
        self.answer_button.setFont(medium_font)

        # layout

        self.answer.setMaximumWidth(600)
        self.answer.setTextMargins(8, 8, 8, 8)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(24)

        self.layout.addStretch()
        self.layout.addWidget(self.word_to_conjugate)
        self.layout.addWidget(self.kana_reading)
        self.layout.addWidget(self.word_type)
        self.layout.addStretch()
        self.layout.addWidget(self.conjugation_helper_text)
        self.layout.addWidget(self.conjugation)
        self.layout.addWidget(self.answer)
        self.layout.addWidget(self.answer_button)
        self.layout.addStretch()

        self.words = words
        self.ask_new_random_word()

    def ask_new_random_word(self):
        """Ask to conjugate a new random word."""
        random_word = random.choice(self.words)
        dictionary_form_word: str = random_word['word']
        word_kana_reading: str | None = random_word['kana']

        self.word_to_conjugate.setText(dictionary_form_word)
        self.kana_reading.setText(
            f'（{word_kana_reading}）'
            if word_kana_reading is not None else '　'  # still occupy space
        )
        self.answer.setText('')

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
            self.word_type.setText(verb_type.label)
            self.conjugation.setText(random_inflection.formatted())
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
            self.word_type.setText(adjective_type.label)
            self.conjugation.setText(random_inflection.formatted())
        else:
            print(
                f'error: word {dictionary_form_word} of illegal type'
                + f' "{type_str}"',
                file=sys.stderr
            )
            exit(4)

    @QtCore.Slot()
    def process_answer(self):
        """If the answer is correct, ask a new one. Otherwise, show an error."""
        is_correct = self.answer.text().strip() == self.correct_answer
        if is_correct:
            # TODO: proper notification
            print('correct!')
            self.ask_new_random_word()
        else:
            # TODO: proper notification
            print('incorrect.')


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

    app = QtWidgets.QApplication([])

    kaeru = Kaeru(words)
    kaeru.resize(800, 600)
    kaeru.show()

    sys.exit(app.exec())
