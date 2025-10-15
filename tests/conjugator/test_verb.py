import conjugator
from inflection import (
    VerbType, VerbInflection,
)

import japanese_verb_conjugator_v2 as jvc


# -- ichidan verbs --

sample_ichidan_verbs = tuple(
    {
        'dictionary_form': f'{stem}る',
        'negative': f'{stem}ない',
        'past': f'{stem}た',
        'past-negative': f'{stem}なかった',
        'polite': f'{stem}ます',
        'polite-negative': f'{stem}ません',
        'polite-past': f'{stem}ました',
        'polite-past-negative': f'{stem}ませんでした',
        'te-form': f'{stem}て',
        'negative-te-form': f'{stem}なくて',
    } for stem in ('調べ', '始め', '信じ')  # word minus the る
)

def test_conjugate_verb_ichidan_default_inflection_returns_unchanged_word():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(),
        ) == word['dictionary_form']

def test_conjugate_verb_ichidan_negative_inflection():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(polarity=VerbInflection.Polarity.NEGATIVE),
        ) == word['negative']

def test_conjugate_verb_ichidan_past_inflection():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(tense=VerbInflection.Tense.PAST),
        ) == word['past']

def test_conjugate_verb_ichidan_negative_past_inflection():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(
                polarity=VerbInflection.Polarity.NEGATIVE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['past-negative']

# polite

def test_conjugate_verb_ichidan_polite():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(base_form=VerbInflection.BaseForm.POLITE),
        ) == word['polite']

def test_conjugate_verb_ichidan_polite_negative_inflection():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                polarity=VerbInflection.Polarity.NEGATIVE
            ),
        ) == word['polite-negative']

def test_conjugate_verb_ichidan_polite_past_inflection():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['polite-past']

def test_conjugate_verb_ichidan_polite_negative_past_inflection():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                polarity=VerbInflection.Polarity.NEGATIVE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['polite-past-negative']

# te-form

def test_conjugate_verb_ichidan_te_form():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.TE,
            ),
        ) == word['te-form']

def test_conjugate_verb_ichidan_negative_te_form():
    for word in sample_ichidan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.TE,
                polarity=VerbInflection.Polarity.NEGATIVE,
            ),
        ) == word['negative-te-form']


# -- irregular ichidan verbs (ending in する, くる/来る) --

irregular_verbs = tuple(
    (
        *tuple(
            {
                'dictionary_form': f'{stem}する',
                'negative': f'{stem}しない',
                'past': f'{stem}した',
                'past-negative': f'{stem}しなかった',
                'polite': f'{stem}します',
                'polite-negative': f'{stem}しません',
                'polite-past': f'{stem}しました',
                'polite-past-negative': f'{stem}しませんでした',
                'te-form': f'{stem}して',
                'negative-te-form': f'{stem}しなくて',
            } for stem in ('', '利用', 'インストール')  # word minus the する
        ),
        *tuple(
            {
                'dictionary_form': f'{stem}くる',
                'negative': f'{stem}こない',
                'past': f'{stem}きた',
                'past-negative': f'{stem}こなかった',
                'polite': f'{stem}きます',
                'polite-negative': f'{stem}きません',
                'polite-past': f'{stem}きました',
                'polite-past-negative': f'{stem}きませんでした',
                'te-form': f'{stem}きて',
                'negative-te-form': f'{stem}こなくて',
            } for stem in ('', '持って', '連れて')  # word minus the くる
        ),
        *tuple(
            {
                'dictionary_form': f'{stem}来る',
                'negative': f'{stem}来ない',
                'past': f'{stem}来た',
                'past-negative': f'{stem}来なかった',
                'polite': f'{stem}来ます',
                'polite-negative': f'{stem}来ません',
                'polite-past': f'{stem}来ました',
                'polite-past-negative': f'{stem}来ませんでした',
                'te-form': f'{stem}来て',
                'negative-te-form': f'{stem}来なくて',
            } for stem in ('', '持って', '連れて')  # word minus the 来る
        ),
    )
)

def test_conjugate_verb_ichidan_irregular_default_inflection_returns_unchanged_word():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(),
        ) == word['dictionary_form']

def test_conjugate_verb_ichidan_irregular_negative_inflection():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(polarity=VerbInflection.Polarity.NEGATIVE),
        ) == word['negative']

def test_conjugate_verb_ichidan_irregular_past_inflection():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(tense=VerbInflection.Tense.PAST),
        ) == word['past']

def test_conjugate_verb_ichidan_irregular_negative_past_inflection():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(
                polarity=VerbInflection.Polarity.NEGATIVE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['past-negative']

# polite

def test_conjugate_verb_ichidan_irregular_polite():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(base_form=VerbInflection.BaseForm.POLITE),
        ) == word['polite']

def test_conjugate_verb_ichidan_irregular_polite_negative_inflection():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                polarity=VerbInflection.Polarity.NEGATIVE
            ),
        ) == word['polite-negative']

def test_conjugate_verb_ichidan_irregular_polite_past_inflection():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['polite-past']

def test_conjugate_verb_ichidan_irregular_polite_negative_past_inflection():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                polarity=VerbInflection.Polarity.NEGATIVE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['polite-past-negative']

# te-form

def test_conjugate_verb_ichidan_irregular_te_form():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(
                base_form=VerbInflection.BaseForm.TE,
            ),
        ) == word['te-form']

def test_conjugate_verb_ichidan_irregular_negative_te_form():
    for word in irregular_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.ICHIDAN_IRREGULAR,
            VerbInflection(
                base_form=VerbInflection.BaseForm.TE,
                polarity=VerbInflection.Polarity.NEGATIVE,
            ),
        ) == word['negative-te-form']


# -- godan verbs --

sample_godan_verbs = tuple(
    {
        'dictionary_form': verb,
        'negative': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.PLAIN.value,
            jvc.Polarity.NEGATIVE.value
        ),
        'past': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.PLAIN.value,
            jvc.Tense.PAST.value
        ),
        'past-negative': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.PLAIN.value,
            jvc.Tense.PAST.value, jvc.Polarity.NEGATIVE.value
        ),
        'polite': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.POLITE.value
        ),
        'polite-negative': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.POLITE.value,
            jvc.Polarity.NEGATIVE.value
        ),
        'polite-past': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.POLITE.value,
            jvc.Tense.PAST.value
        ),
        'polite-past-negative': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.POLITE.value,
            jvc.Tense.PAST.value, jvc.Polarity.NEGATIVE.value
        ),
        'te-form': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.TE.value
        ),
        'negative-te-form': jvc.generate_japanese_verb_by_str(
            verb, jvc.VerbClass.GODAN, jvc.BaseForm.TE.value,
            jvc.Polarity.NEGATIVE.value
        ),
    } for verb in (
        '書く', '目指す', '打つ', '包む', '頑張る', '死ぬ'
    )
)

def test_conjugate_verb_godan_default_inflection_returns_unchanged_word():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(),
        ) == word['dictionary_form']

def test_conjugate_verb_godan_negative_inflection():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(polarity=VerbInflection.Polarity.NEGATIVE),
        ) == word['negative']

def test_conjugate_verb_godan_past_inflection():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(tense=VerbInflection.Tense.PAST),
        ) == word['past']

def test_conjugate_verb_godan_negative_past_inflection():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(
                polarity=VerbInflection.Polarity.NEGATIVE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['past-negative']

# polite

def test_conjugate_verb_godan_polite():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(base_form=VerbInflection.BaseForm.POLITE),
        ) == word['polite']

def test_conjugate_verb_godan_polite_negative_inflection():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                polarity=VerbInflection.Polarity.NEGATIVE
            ),
        ) == word['polite-negative']

def test_conjugate_verb_godan_polite_past_inflection():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['polite-past']

def test_conjugate_verb_godan_polite_negative_past_inflection():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.POLITE,
                polarity=VerbInflection.Polarity.NEGATIVE,
                tense=VerbInflection.Tense.PAST
            ),
        ) == word['polite-past-negative']

# te-form

def test_conjugate_verb_godan_te_form():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.TE,
            ),
        ) == word['te-form']

def test_conjugate_verb_godan_negative_te_form():
    for word in sample_godan_verbs:
        assert conjugator.conjugate_verb(
            word['dictionary_form'],
            VerbType.GODAN,
            VerbInflection(
                base_form=VerbInflection.BaseForm.TE,
                polarity=VerbInflection.Polarity.NEGATIVE,
            ),
        ) == word['negative-te-form']
