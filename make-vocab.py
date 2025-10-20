"""This script prepares the vocabulary JSON used by the quizzer.

It fetches both JPDB's word frequency list and the Simplified JMdict dictionary to keep
the `N` most frequent words of each type: verbs and adjectives. Therefore, the final
word count should be `N`*2.

Verb and adjective types are filtered to discard archaic or rare forms.

The keys for each entry in the final JSON are:
{
    "word": the dictionary form word
    "kana": the kana reading if `word` contains kanji, else null
    "type": the type of word (see AdjectiveType and VerbType)
}

For example:
[
    {"name": "考える", "kana": "かんがえる", "type": "verb-ichidan"},
    {"name": "わかる", "kana": null, "type": "verb-godan"},
    {"name": "強い", "kana": "つよい", "type": "adjective-i"},
    ...
]
"""

import argparse
import json
import sys
import urllib.request
import shutil
import tempfile
from typing import Any
from os import path
import logging

from inflection import VerbType, AdjectiveType


def get_simplified_jmdict_json() -> list[dict[str, Any]]:
    """Fetch and return the Simplified JMdict JSON deserialised to a list."""
    with (
        tempfile.NamedTemporaryFile() as temp_file,
        tempfile.TemporaryDirectory() as temp_dir,
        urllib.request.urlopen(
            'https://github.com/scriptin/jmdict-simplified/releases/download'
            + '/3.6.1%2B20251013122507/jmdict-eng-common-3.6.1+20251013122507.json.zip'
        ) as jmdict_zip
    ):
        temp_file.write(jmdict_zip.read())
        shutil.unpack_archive(temp_file.name, temp_dir, 'zip')
        extracted_json_path = path.join(temp_dir, 'jmdict-eng-common-3.6.1.json')
        with open(extracted_json_path) as extracted_json:
            return json.load(extracted_json)['words']


def get_jpdb_frequency_list_json() -> list[list]:
    """Fetch and return the JPDB Frequency List JSON deserialised to a list."""
    with (
        tempfile.NamedTemporaryFile() as temp_file,
        tempfile.TemporaryDirectory() as temp_dir,
        urllib.request.urlopen(
            'https://github.com/Kuuuube/yomitan-dictionaries/raw/main/dictionaries'
            + '/JPDB_v2.2_Frequency_2024-10-13.zip'
        ) as jpdb_zip
    ):
        temp_file.write(jpdb_zip.read())
        shutil.unpack_archive(temp_file.name, temp_dir, 'zip')
        extracted_json_path = path.join(temp_dir, 'term_meta_bank_1.json')
        with open(extracted_json_path) as extracted_json:
            return json.load(extracted_json)


# the type of words we want to keep based on JMdict's tags
wanted_word_types = {
    # adjectives
    'adj-i':   AdjectiveType.I,
    'adj-ix':  AdjectiveType.I_YOI_II,
    'adj-na':  AdjectiveType.NA,
    # verbs
    'v1':    VerbType.ICHIDAN,
    # TODO: is 'v1-s' ('ichidan-kureru'), needed?
    'v5b':   VerbType.GODAN,
    'v5g':   VerbType.GODAN,
    'v5k':   VerbType.GODAN,
    'v5n':   VerbType.GODAN,
    'v5m':   VerbType.GODAN,
    'v5r':   VerbType.GODAN,
    'v5t':   VerbType.GODAN,
    'v5s':   VerbType.GODAN,
    'v5u':   VerbType.GODAN,
    'v5k-s': VerbType.GODAN,
    'v5r-i': VerbType.GODAN,  # treated as GODAN by japanese_verb_conjugator_v2
    # TODO: are the following needed?
    #'v5u-s': 'godan-u-ending-special',
    #'v5aru': 'godan-aru',
}


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description='Prepare the vocabulary JSON used by kaeru.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-n',
        '--limit_per_type',
        help='the maximum number of verbs and adjectives to fetch',
        type=int,
        default=100,
    )
    parser.add_argument(
        '-o',
        '--output',
        help='where to save the final JSON',
        type=str,
        default='vocab.json',
    )
    args = parser.parse_args()

    if path.isfile(args.output):
        answer = input(
            f'warning: "{args.output}" already exists. do you want to overwrite it?'
            + ' (y/N): '
        )
        if answer.strip().lower() not in ('y', 'yes'):
            print('cancelled.')
            exit(0)

    logging.info(
        f'building "{args.output}" with the {args.limit_per_type} most frequent verbs &'
        + f' adjectives (total {args.limit_per_type*2})\n'
    )

    print(
        '[1/4] fetching the JPDB frequency list'
        + ' @ https://github.com/Kuuuube/yomitan-dictionaries…'
    )
    try:
        frequency_json = get_jpdb_frequency_list_json()
    except Exception:
        logging.error('could not fetch the JPDB frequency list.')
        raise

    # first, we load the words from the JPDB frequency list json
    jpdb_words = {}
    for entry in frequency_json:
        word: str = entry[0]
        if len(word) == 1:
            # there are no 1-character-long verbs or adjectives
            continue

        try:
            frequency: int = entry[2]['value']
        except KeyError:
            frequency: int = entry[2]['frequency']['value']
        # we'll copy it to the appropriate dict (or discard the word altogether) later
        jpdb_words[word] = {'frequency': frequency}

    # the whole json is a bit heavy. we don't need it anymore
    del frequency_json

    print(
        '[2/4] fetching the Simplified JMdict'
        + ' @ https://github.com/scriptin/jmdict-simplified…'
    )
    try:
        jmdict_json = get_simplified_jmdict_json()
    except Exception:
        logging.error('could not fetch the Simplified JMdict.')
        raise

    # now we separate them into verbs and adjectives, also filling the type, kana, and
    # frequency data

    jpdb_verbs = []
    jpdb_adjectives = []

    print('[3/4] merging word + frequency data…')
    for entry in jmdict_json:
        # an entry might have multiple kanji & kana spellings. we'll stick with non-rare
        # ones only and treat them as distinct words (so we can analyse each spelling's
        # frequency)
        spellings = (
            *entry['kanji'],
            *entry['kana']
        )
        for spelling in spellings:
            if not spelling['common']:
                continue

            word = spelling['text']

            if len(word) == 1:
                # there are no 1-character-long verbs or adjectives
                continue

            if word not in jpdb_words:
                continue

            # it's at least in the JPDB frequency list - but is it the right type?
            tags: list[str] = entry['sense'][0]['partOfSpeech']
            for tag in tags:
                if tag in wanted_word_types:
                    kana_reading = entry['kana'][0]['text']
                    word_info = {
                        'word': word,
                        'kana': kana_reading if kana_reading != word else None,
                        'type': wanted_word_types[tag],
                        'frequency': jpdb_words[word]['frequency']
                    }
                    is_verb = tag.startswith('v')
                    if is_verb:
                        jpdb_verbs.append(word_info)
                    else:
                        jpdb_adjectives.append(word_info)
                    continue

            # this isn't the right type of word; discard it
            del jpdb_words[word]

    # finally, we limit both verbs and adjectives to `args.limit_per_type` items

    def sort_by_frequency(word_list: list[dict[str, str]]) -> None:
        """Sort the given word list by frequency in ascending order."""
        word_list.sort(key=lambda x: x['frequency'])

    print('[4/4] sorting and trimming the final output…')
    sort_by_frequency(jpdb_verbs)
    jpdb_verbs = jpdb_verbs[:args.limit_per_type]
    # we don't need the 'frequency' field anymore
    jpdb_verbs = tuple(
        {
            'word': verb['word'],
            'kana': verb['kana'],
            'type': verb['type'].value,
        } for verb in jpdb_verbs
    )

    sort_by_frequency(jpdb_adjectives)
    jpdb_adjectives = jpdb_adjectives[:args.limit_per_type]
    jpdb_adjectives = tuple(
        {
            'word': adjective['word'],
            'kana': adjective['kana'],
            'type': adjective['type'].value
        } for adjective in jpdb_adjectives
    )

    # TODO: sqlite db?
    try:
        with open(args.output, 'w') as output_file:
            json.dump(
                (*jpdb_verbs, *jpdb_adjectives),
                output_file,
                ensure_ascii=False,
                indent=0,
            )
    except OSError:
        logging.error(f'could not write the result to "{args.output}".')
        raise

    print('done.')
