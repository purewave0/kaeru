"""Quiz adjective and verb conjugations on the command line."""

from argparse import ArgumentParser
import json
import random
import sqlite3
import sys
from time import sleep
import readline
assert readline  # silence linter error

import conjugator

from inflection import (
    AdjectiveType, AdjectiveInflection,
    VerbType, VerbInflection
)
import dbapi
from constants import DATABASE_PATH


def formatted_adjective_question(
    adjective: str,
    kana_reading: str | None,
    type: AdjectiveType | None,
    inflection: AdjectiveInflection
) -> str:
    """Return the given adjetcive + inflection info as a question."""
    return (
        f'word: {adjective}' + ('' if not kana_reading else f' ({kana_reading})')
        + (f'\ntype: {type.value}' if type else '\n')
        + f'\nconjugate to: {inflection.formatted()}'
    )


def formatted_verb_question(
    verb: str,
    kana_reading: str | None,
    type: VerbType | None,
    inflection: VerbInflection
) -> str:
    """Return the given verb + inflection info as a question."""
    return (
        f'word: {verb}' + ('' if not kana_reading else f' ({kana_reading})')
        + (f'\ntype: {type.label}' if type else '\n')
        + f'\nconjugate to: {inflection.formatted()}'
    )


def formatted_scores(current_streak: int, highest_streak: int) -> str:
    return (
        f'current streak: {current_streak}'
        + f'\thighest streak: {highest_streak}'
    )


ATTEMPT_INTERVAL_SECONDS = 0.5

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Practise Japanese verb & adjective inflections.'
    )
    parser.add_argument(
        '-K',
        '--hide-kana',
        action='store_true',
        help="don't display kana readings for words with kanji"
    )
    parser.add_argument(
        '-T',
        '--hide-word-type',
        action='store_true',
        help="""don't display the word type ("5-dan verb", "い-adjective", etc.)"""
    )
    args = parser.parse_args()

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

    print(f'{len(words)} words loaded.')

    conn = sqlite3.connect(DATABASE_PATH)
    dbapi.create_table_and_user_if_nexists(conn)

    current_streak = 0
    highest_streak = dbapi.get_highest_streak(conn)
    print(formatted_scores(current_streak, highest_streak) + '\n')

    while True:
        random_word: dict = random.choice(words)
        kana_reading: str | None = random_word['kana']
        dictionary_form_word: str = random_word['word']
        type_str: str = random_word['type']

        correctly_conjugated_word = None
        question = None
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
            correctly_conjugated_word = conjugator.conjugate_verb(
                dictionary_form_word, verb_type, random_inflection,
            )
            question = formatted_verb_question(
                dictionary_form_word,
                kana_reading if not args.hide_kana else None,
                verb_type if not args.hide_word_type else None,
                random_inflection,
            )
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
            correctly_conjugated_word = conjugator.conjugate_adjective(
                dictionary_form_word, adjective_type, random_inflection,
            )
            question = formatted_adjective_question(
                dictionary_form_word,
                kana_reading if not args.hide_kana else None,
                adjective_type if not args.hide_word_type else None,
                random_inflection,
            )
        else:
            print(
                f'error: word {dictionary_form_word} of illegal type'
                + f' "{type_str}"',
                file=sys.stderr
            )
            exit(4)

        while True:
            try:
                print(question)
                user_answer = input('your answer: ').strip().lower()
            except KeyboardInterrupt:
                print('\nenter "q" or hit CTRL+D to quit.\n')
                continue
            except EOFError:
                print()
                quit(0)

            if user_answer == 'q':
                exit(0)

            if user_answer == correctly_conjugated_word:
                current_streak += 1
                beat_highest_streak = highest_streak < current_streak
                if beat_highest_streak:
                    highest_streak = current_streak
                    dbapi.set_highest_streak(conn, highest_streak)

                print(f'correct!\t{formatted_scores(current_streak, highest_streak)}')
                print('next one…\n')
                sleep(ATTEMPT_INTERVAL_SECONDS)
                break

            current_streak = 0
            print('wrong answer! try again.\n')
            sleep(ATTEMPT_INTERVAL_SECONDS)
