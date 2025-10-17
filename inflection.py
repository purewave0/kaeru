"""Inflections for adjectives and verbs."""

from enum import Enum
import random

import japanese_verb_conjugator_v2 as jvc


class AdjectiveType(Enum):
    """A type of adjective that can be conjugated.

    This will determine its conjugation pattern.
    """
    I = 'adjective-i'
    """い-adjective."""
    I_YOI_II = 'adjective-i-yoi-ii'
    """いい, and any other い-adjective with the 良い ending written as いい."""
    NA = 'adjective-na'
    """な-adjective."""

class VerbType(Enum):
    """A type of verb that can be conjugated.

    This will determine its conjugation pattern.
    """
    ICHIDAN = 'verb-ichidan'
    """る-verbs."""
    GODAN = 'verb-godan'
    """う-verbs."""
    ICHIDAN_IRREGULAR = 'verb-ichidan-irregular'
    """する and 来る/くる, and any other verbs ending with those irregular forms."""


class AdjectiveInflection:
    """Inflection (tense, polarity, politeness) for an adjective."""
    class Tense(Enum):
        """The time of the state."""
        NONPAST = 'nonpast'
        """Set in the present or in the future; the default. E.g. 美味しい, 有名."""
        PAST = 'past'
        """Set in the past. E.g. 美味しかった, 有名だった."""

    class Polarity(Enum):
        """Whether the adjective is positive or negative."""
        POSITIVE = 'positive'
        """The default. E.g. 遅い, 完璧."""
        NEGATIVE = 'negative'
        """E.g. 遅くない, 完璧じゃない."""

    class Politeness(Enum):
        """The politeness of the ending.

        PLAIN shouldn't be used with い-adjectives, as they do not accept the plain
        copula.
        """
        PLAIN = 'plain'
        """Informal; the default. E.g. 立派だ. Not valid for い-adjectives."""
        POLITE = 'polite'
        """Formal. E.g. 高いです, 立派です."""

    tense: Tense
    polarity: Polarity
    politeness: Politeness | None

    def __init__(
        self,
        *,
        tense: Tense = Tense.NONPAST,
        polarity: Polarity = Polarity.POSITIVE,
        politeness: Politeness | None = None,
    ):
        self.tense = tense
        self.polarity = polarity
        self.politeness = politeness

    def formatted(self):
        """Return each nondefault feature inside brackets, separated by spaces."""
        nondefault_features = []
        if self.polarity is AdjectiveInflection.Polarity.NEGATIVE:
            nondefault_features.append('[NEGATIVE]')
        if self.tense is AdjectiveInflection.Tense.PAST:
            nondefault_features.append('[PAST]')
        if self.politeness is AdjectiveInflection.Politeness.POLITE:
            nondefault_features.append('[POLITE]')
        return ' '.join(nondefault_features)

    @staticmethod
    def generate_random(adjective_type: AdjectiveType) -> 'AdjectiveInflection':
        """Return a random inflection for the given adjective type.

        At least 1 of the features in the returned inflection has a nondefault value,
        or else there'd be no inflection at all.

        い-adjectives never have Politeness.PLAIN (it'll be None).
        """
        tense = random.choice(list(AdjectiveInflection.Tense))
        polarity = random.choice(list(AdjectiveInflection.Polarity))
        valid_features = ['tense', 'polarity', 'politeness']

        politeness_choices = [AdjectiveInflection.Politeness.POLITE]

        accepts_plain_copula = adjective_type is AdjectiveType.NA
        if accepts_plain_copula:
            politeness_choices.append(
                AdjectiveInflection.Politeness.PLAIN
            )
        politeness = random.choice(politeness_choices)

        required_nondefault_feature = random.choice(valid_features)
        # force at least one nondefault value
        match required_nondefault_feature:
            case 'tense':
                tense = AdjectiveInflection.Tense.PAST
            case 'polarity':
                polarity = AdjectiveInflection.Polarity.NEGATIVE
            case 'politeness':
                politeness = AdjectiveInflection.Politeness.POLITE

        return AdjectiveInflection(
            tense=tense, polarity=polarity, politeness=politeness
        )


class VerbInflection:
    """Inflection (base form, tense, polarity) for a verb."""
    class BaseForm(Enum):
        """The base for the conjugation."""
        PLAIN = jvc.BaseForm.PLAIN.value
        POLITE = jvc.BaseForm.POLITE.value
        TE = jvc.BaseForm.TE.value

    Tense = jvc.Tense
    """The time of the action."""

    Polarity = jvc.Polarity
    """Whether the verb is positive or negative."""

    base_form: BaseForm
    tense: Tense | None
    polarity: Polarity

    def __init__(
        self,
        *,
        base_form: BaseForm = BaseForm.PLAIN,
        tense: Tense | None = None,
        polarity: Polarity = Polarity.POSITIVE,
    ):
        if base_form is VerbInflection.BaseForm.TE:
            assert tense is None, 'BaseForm.TE requires Tense to be None'
        self.base_form = base_form
        self.tense = tense
        self.polarity = polarity

    def formatted(self):
        """Return each nondefault feature inside brackets, separated by spaces."""
        nondefault_features = []
        if self.base_form is VerbInflection.BaseForm.POLITE:
            nondefault_features.append('[POLITE]')
        elif self.base_form is VerbInflection.BaseForm.TE:
            nondefault_features.append('[て-FORM]')

        if self.tense is VerbInflection.Tense.PAST:
            nondefault_features.append('[PAST]')
        if self.polarity is VerbInflection.Polarity.NEGATIVE:
            nondefault_features.append('[NEGATIVE]')
        return ' '.join(nondefault_features)

    @staticmethod
    def generate_random() -> 'VerbInflection':
        """Return a random verb inflection.

        At least 1 of the features in the returned inflection has a nondefault value,
        or else there'd be no inflection at all.

        Verbs with BaseForm.TE never have Tense (it'll be None).
        """
        base_form = random.choice(list(VerbInflection.BaseForm))
        tense = random.choice(list(VerbInflection.Tense))
        polarity = random.choice(list(VerbInflection.Polarity))
        valid_features = ['base_form', 'polarity']

        required_nondefault_feature = random.choice(valid_features)
        match required_nondefault_feature:
            case 'base_form':
                base_form = random.choice(
                    (
                        VerbInflection.BaseForm.POLITE,
                        VerbInflection.BaseForm.TE,
                    )
                )
            case 'tense':
                tense = VerbInflection.Tense.PAST
            case 'polarity':
                polarity = VerbInflection.Polarity.NEGATIVE

        accepts_tense = base_form is not VerbInflection.BaseForm.TE
        if not accepts_tense:
            tense = None

        return VerbInflection(
            base_form=base_form, tense=tense, polarity=polarity
        )
