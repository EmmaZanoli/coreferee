from typing import Set
from string import punctuation
from spacy.tokens import Token
from ...rules import RulesAnalyzer
from ...data_model import Mention


class LanguageSpecificRulesAnalyzer(RulesAnalyzer):

    random_word = "cibo"

    or_lemmas = ("o", "oppure")

    entity_noun_dictionary = {
        "PERSON": ["persona", "individuo", "uomo", "donna"],
        "NORP": ["nazione", "popolo", "etnia"],
        "FAC": ["edificio"],
        "ORG": ["azienda", "ditta", "organizzazione"],
        "GPE": ["paese", "stato", "città"],
        "LOC": ["luogo"],
        "LAW": ["legge"],
        "LANGUAGE": ["lingua", "linguaggio", "idioma"],
    }

    quote_tuples = [
            ('"', '"'),
            ("„", "“"),
            ("‚", "‘"),
            ("«", "»"),
            ("»", "«"),
        ]

    dependent_sibling_deps = ("conj", "appos")

    conjunction_deps = ("cc", "punct")

    adverbial_clause_deps = ("advcl", "advmod", "dep")
    
    term_operator_pos = ("DET",)

    clause_root_pos = ("VERB", "AUX")

    def get_dependent_siblings(self, token: Token) -> List[Token]:
        def add_siblings_recursively(
            recursed_token: Token, visited_set: set
        ) -> Tuple[Set[Token], bool]:
            visited_set.add(recursed_token)
            siblings_set = set()
            coordinator = False
            if recursed_token.lemma_ in self.or_lemmas:
                token._.coref_chains.temp_has_or_coordination = True
            if recursed_token.dep_ in self.dependent_sibling_deps:
                siblings_set.add(recursed_token)
            for child in (
                child
                for child in recursed_token.children
                if child not in visited_set
                and (
                    child.dep_ in self.dependent_sibling_deps
                    or child.dep_ in self.conjunction_deps
                )
            ):
                if child.dep_ == "cc":
                    coordinator = True
                child_siblings_set, returned_coordinator = add_siblings_recursively(
                    child, visited_set
                )
                coordinator = coordinator or returned_coordinator
                siblings_set |= child_siblings_set

            return siblings_set, coordinator

        if (
            token.dep_ not in self.conjunction_deps
            and token.dep_ not in self.dependent_sibling_deps
        ):
            siblings_set, coordinator = add_siblings_recursively(token, set())
            if coordinator:
                return sorted(siblings_set)  # type:ignore[type-var]
        return []

    def is_independent_noun(self, token: Token) -> bool:
        if not (
            (token.pos_ in self.noun_pos and token.dep_ not in ("compound", "npadvmod"))
            or (token.tag_ == "CD" and token.dep_ != "nummod")
            or (token.tag_ == "DT" and token.dep_ != "det")
            or (token.pos_ == "PRON" and token.tag_ == "NN")
        ):
            return False
        return not self.is_token_in_one_of_phrases(
            token, self.blacklisted_phrases  # type:ignore[attr-defined]
        )
