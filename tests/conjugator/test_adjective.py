import conjugator
from inflection import (
    AdjectiveInflection,
)


# -- い-adjectives --

sample_i_adjectives = tuple(
    {
        'dictionary_form': f'{stem}い',
        'negative': f'{stem}くない',
        'past': f'{stem}かった',
        'past-negative': f'{stem}くなかった',
        'polite': f'{stem}いです',
        'polite-negative': f'{stem}くないです',
        'polite-past': f'{stem}かったです',
        'polite-past-negative': f'{stem}くなかったです',
    } for stem in ('強', 'おいし', 'ラグ')  # adjective minus the い
)

def test_conjugate_i_adjective_default_inflection_returns_unchanged_word():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection()
        ) == word['dictionary_form']

def test_conjugate_i_adjective_negative_inflection():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['negative']

def test_conjugate_i_adjective_past_inflection():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                tense=AdjectiveInflection.Tense.PAST
            )
        ) == word['past']

def test_conjugate_i_adjective_past_negative_inflection():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                tense=AdjectiveInflection.Tense.PAST,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['past-negative']

# polite

def test_conjugate_i_adjective_polite_inflection():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE
            )
        ) == word['polite']

def test_conjugate_i_adjective_polite_negative_inflection():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['polite-negative']

def test_conjugate_i_adjective_polite_past_inflection():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                tense=AdjectiveInflection.Tense.PAST
            )
        ) == word['polite-past']

def test_conjugate_i_adjective_polite_past_negative_inflection():
    for word in sample_i_adjectives:
        assert conjugator._conjugate_i_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                tense=AdjectiveInflection.Tense.PAST,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['polite-past-negative']


# -- い-adjectives with the 良い ending written as いい --

sample_i_yoi_ii_adjectives = tuple(
    {
        'dictionary_form': f'{stem}いい',
        'negative': f'{stem}よくない',
        'past': f'{stem}よかった',
        'past-negative': f'{stem}よくなかった',
        'polite': f'{stem}よいです',
        'polite-negative': f'{stem}よくないです',
        'polite-past': f'{stem}よかったです',
        'polite-past-negative': f'{stem}よくなかったです',
    } for stem in ('', 'かっこ', '気持ち')  # adjective minus the いい
)

def test_conjugate_i_yoi_ii_adjective_default_inflection_returns_unchanged_word():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection()
        ) == word['dictionary_form']

def test_conjugate_i_yoi_ii_adjective_negative_inflection():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['negative']

def test_conjugate_i_yoi_ii_adjective_past_inflection():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                tense=AdjectiveInflection.Tense.PAST
            )
        ) == word['past']

def test_conjugate_i_yoi_ii_adjective_past_negative_inflection():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                tense=AdjectiveInflection.Tense.PAST,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['past-negative']

# polite

def test_conjugate_i_yoi_ii_adjective_polite_inflection():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE
            )
        ) == word['polite']

def test_conjugate_i_yoi_ii_adjective_polite_negative_inflection():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['polite-negative']

def test_conjugate_i_yoi_ii_adjective_polite_past_inflection():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                tense=AdjectiveInflection.Tense.PAST
            )
        ) == word['polite-past']

def test_conjugate_i_yoi_ii_adjective_polite_past_negative_inflection():
    for word in sample_i_yoi_ii_adjectives:
        assert conjugator._conjugate_i_yoi_ii_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                tense=AdjectiveInflection.Tense.PAST,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['polite-past-negative']


# -- な-adjectives --

sample_na_adjectives = tuple(
    {
        'dictionary_form': word,
        'positive': f'{word}だ',
        'negative': f'{word}じゃない',
        'past': f'{word}だった',
        'past-negative': f'{word}じゃなかった',
        'polite': f'{word}です',
        'polite-negative': f'{word}ではありません',
        # TODO: 'lax-polite' e.g. ～じゃないです, じゃありません, ではない, etc
        'polite-past': f'{word}でした',
        'polite-past-negative': f'{word}ではありませんでした',
    } for word in ('有名', 'きれい', 'シンプル')
)

def test_conjugate_na_adjective_positive_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection()
        ) == word['positive']

def test_conjugate_na_adjective_negative_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['negative']

def test_conjugate_na_adjective_past_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                tense=AdjectiveInflection.Tense.PAST
            )
        ) == word['past']

def test_conjugate_na_adjective_negative_past_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                tense=AdjectiveInflection.Tense.PAST,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['past-negative']

# polite

def test_conjugate_na_adjective_polite_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE
            )
        ) == word['polite']

def test_conjugate_na_adjective_polite_negative_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['polite-negative']

def test_conjugate_na_adjective_polite_past_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                tense=AdjectiveInflection.Tense.PAST
            )
        ) == word['polite-past']

def test_conjugate_na_adjective_polite_negative_past_inflection():
    for word in sample_na_adjectives:
        assert conjugator._conjugate_na_adjective(
            word['dictionary_form'],
            AdjectiveInflection(
                politeness=AdjectiveInflection.Politeness.POLITE,
                tense=AdjectiveInflection.Tense.PAST,
                polarity=AdjectiveInflection.Polarity.NEGATIVE
            )
        ) == word['polite-past-negative']
