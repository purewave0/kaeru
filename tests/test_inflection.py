from inflection import (
    AdjectiveType, AdjectiveInflection,
    VerbInflection,
)


ITERATIONS = 1_000

# -- い-adjectives --

def test_i_adjective_inflection_generate_random_generates_at_least_one_nondefault_value():
    for _ in range(ITERATIONS):
        inflection = AdjectiveInflection.generate_random(AdjectiveType.I)

        are_all_values_default = (
            inflection.tense is AdjectiveInflection.Tense.NONPAST
            and inflection.polarity is AdjectiveInflection.Polarity.POSITIVE
            and inflection.copula_politeness
                is AdjectiveInflection.CopulaPoliteness.PLAIN
        )
        assert not are_all_values_default

def test_i_adjective_inflection_generate_random_copula_politeness_is_not_PLAIN():
    for _ in range(ITERATIONS):
        inflection = AdjectiveInflection.generate_random(AdjectiveType.I)

        assert (
            inflection.copula_politeness
            is not AdjectiveInflection.CopulaPoliteness.PLAIN
        )


# -- な-adjectives --

def test_na_adjective_inflection_generate_random_generates_at_least_one_nondefault_value():
    for _ in range(ITERATIONS):
        inflection = AdjectiveInflection.generate_random(AdjectiveType.NA)

        are_all_values_default = (
            inflection.tense is AdjectiveInflection.Tense.NONPAST
            and inflection.polarity is AdjectiveInflection.Polarity.POSITIVE
            and inflection.copula_politeness
                is AdjectiveInflection.CopulaPoliteness.PLAIN
        )
        assert not are_all_values_default


# -- verbs --

def test_verb_inflection_generate_random_generates_at_least_one_nondefault_value():
    for _ in range(ITERATIONS):
        inflection = VerbInflection.generate_random()

        are_all_values_default = (
            inflection.base_form is VerbInflection.BaseForm.PLAIN
            and inflection.tense is VerbInflection.Tense.NONPAST
            and inflection.polarity is VerbInflection.Polarity.POSITIVE
        )
        assert not are_all_values_default

def test_verb_inflection_generate_random_tense_is_None_only_when_base_form_is_TE():
    for _ in range(ITERATIONS):
        inflection = VerbInflection.generate_random()

        if inflection.base_form is VerbInflection.BaseForm.TE:
            assert inflection.tense is None
        else:
            assert inflection.tense is not None
