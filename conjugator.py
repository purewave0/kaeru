import japanese_verb_conjugator_v2 as jvc

from inflection import (
    AdjectiveType, AdjectiveInflection,
    VerbType, VerbInflection
)


def _conjugate_i_adjective(
    adjective: str, inflection: AdjectiveInflection
) -> str:
    """Return the given い-adjective in the given conjugation."""
    conjugated = adjective[:-1]  # remove the い at the end

    if inflection.polarity is AdjectiveInflection.Polarity.NEGATIVE:
        conjugated += 'くな'

    if inflection.tense is AdjectiveInflection.Tense.PAST:
        conjugated += 'かった'
    else:
        conjugated += 'い'

    if inflection.politeness is AdjectiveInflection.Politeness.POLITE:
        conjugated += 'です'

    return conjugated

def _conjugate_i_yoi_ii_adjective(
    adjective: str, inflection: AdjectiveInflection
) -> str:
    """Return the given い-adjective ending in いい (from 良い) in the given
    conjugation.
    """
    conjugated = adjective

    is_default = (
        inflection.tense is AdjectiveInflection.Tense.NONPAST
        and inflection.polarity is AdjectiveInflection.Polarity.POSITIVE
        and inflection.politeness is None
    )
    if is_default:
        return conjugated

    conjugated = conjugated[:-2] + 'よい'  # turn ~いい into ~よい

    return _conjugate_i_adjective(conjugated, inflection)

def _conjugate_na_adjective(
    adjective: str, inflection: AdjectiveInflection
) -> str:
    """Return the given な-adjective in the given conjugation."""
    conjugated = adjective

    if inflection.politeness is AdjectiveInflection.Politeness.POLITE:
        conjugated += 'で'
        if inflection.polarity is AdjectiveInflection.Polarity.POSITIVE:
            if inflection.tense is AdjectiveInflection.Tense.NONPAST:
                conjugated += 'す'
            else:
                conjugated += 'した'
        else:
            conjugated += 'はありません'
            if inflection.tense is AdjectiveInflection.Tense.PAST:
                conjugated += 'でした'
    elif inflection.polarity is AdjectiveInflection.Polarity.POSITIVE:
        conjugated += 'だ'
        if inflection.tense is AdjectiveInflection.Tense.PAST:
            conjugated += 'った'
    else:
        conjugated += 'じゃな'
        if inflection.tense is AdjectiveInflection.Tense.PAST:
            conjugated += 'かった'
        else:
            conjugated += 'い'

    return conjugated


def conjugate_adjective(
    word: str, adjective_type: AdjectiveType, inflection: AdjectiveInflection
) -> str:
    """Return the given adjective of the given type in the given conjugation."""
    if adjective_type is AdjectiveType.I:
        return _conjugate_i_adjective(word, inflection)

    if adjective_type == AdjectiveType.I_YOI_II:
        return _conjugate_i_yoi_ii_adjective(word, inflection)

    if adjective_type == AdjectiveType.NA:
        return _conjugate_na_adjective(word, inflection)

    raise ValueError("adjective_type doesn't refer to an adjective")


def conjugate_verb(
    verb: str,
    verb_type: VerbType,
    verb_inflection: VerbInflection,
) -> str:
    """Return the given verb of the given type in the given conjugation."""
    verb_class = None
    if verb_type is VerbType.GODAN:
        verb_class = jvc.VerbClass.GODAN
    elif verb_type is VerbType.ICHIDAN:
        verb_class = jvc.VerbClass.ICHIDAN
    elif verb_type is VerbType.ICHIDAN_IRREGULAR:
        verb_class = jvc.VerbClass.IRREGULAR

    conjugated = jvc.generate_japanese_verb_by_str(
        verb,
        verb_class,
        verb_inflection.base_form.value,
        None if not verb_inflection.tense else verb_inflection.tense.value,
        verb_inflection.polarity.value
    )

    return conjugated
