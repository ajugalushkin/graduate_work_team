import logging
import json
import re

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsNERTagger,
    NewsMorphTagger,
    Doc,
)


class NLPService:
    def __init__(self, patterns_path: str):
        self.patterns_path = patterns_path
        self.genres: list[str] | None = None
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.compiled_patterns = self._load_and_compile_patterns()

    def _load_and_compile_patterns(self) -> dict:
        with open(self.patterns_path, "r", encoding="utf-8") as f:
            raw_patterns = json.load(f)

        compiled_patterns = {}

        for category, intents in raw_patterns.items():
            compiled_patterns[category] = {}
            for intent, regex_list in intents.items():
                compiled_patterns[category][intent] = [
                    (re.compile(pattern, re.IGNORECASE), pattern) for pattern in regex_list
                ]

        return compiled_patterns

    def _normalize_genre(self, word: str) -> str | None:
        for genre in self.genres:
            if word.startswith(genre[:4]):  # грубое приближение
                return genre
        return None
    
    def _extract_info(self, query: str) -> dict | None:
        doc = Doc(query)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.tag_ner(self.ner_tagger)

        result = {}
        logging.debug(query)
        
        # Обработка ФИО
        actors = []
        for span in doc.spans:
            if span.type == "PER":
                span.normalize(self.morph_vocab)
                actors.append(span.normal)
        if actors:
            result["actors"] = actors

        # Обработка года
        years = re.findall(r"(19|20)\d{2}", query)
        if years:
            result["year"] = int(years[0])

        # Обработка жанров
        for token in doc.tokens:
            normal = token.text.lower()
            genre = self._normalize_genre(normal)
            if genre:
                result["genre"] = genre
                break
        
        return result

    def extract_intent_and_keyword(self, query: str) -> dict | None:
        query = query.strip().rstrip('?.!')
        for category, intents in self.compiled_patterns.items():
            for intent, pattern_list in intents.items():
                for compiled_regex, _ in pattern_list:
                    match = compiled_regex.match(query)
                    if match:
                        keyword = match.group(1).strip()
                        return {
                            "category": category,
                            "intent": intent,
                            "keyword": keyword
                        }
        return None

    async def update_genres(self, genres: list[str] | None = None) -> None:
        self.genres = genres

    async def parse_query(self, query: str) -> dict:
        return self._extract_info(query=query)
    
    async def parse_pattern(self, query: str) -> dict:
        return self.extract_intent_and_keyword(query=query)
