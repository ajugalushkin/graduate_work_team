import logging
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
    def __init__(self):
        self.genres: list[str] | None = None
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.compiled_patterns = {
            "movie-author": re.compile(r".*кто автор фильма\s+(.+)\?", re.IGNORECASE),
            "author-count_movies": re.compile(
                r".*сколько фильмов выпустил автор\s+(.+)\?", re.IGNORECASE
            ),
            "movie-duration": re.compile(r".*сколько длится фильм\s+(.+)\?", re.IGNORECASE),
            "movie-rating": re.compile(r".*какой рейтинг у фильма\s+(.+)\?", re.IGNORECASE),
            "movie-genre": re.compile(
                r".*к какому жанру относится фильм\s+(.+)\?", re.IGNORECASE
            ),
        }

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
    
    def _extract_pattern(self, query: str) -> dict | None:
        for key, pattern in self.compiled_patterns.items():
            match = pattern.match(query.strip())
            if match:
                return {
                    "intent": key,
                    "keyword": match.group(1).strip()
                }
        return None

    async def update_genres(self, genres: list[str] | None = None) -> None:
        self.genres = genres

    async def parse_query(self, query: str) -> dict:
        return self._extract_info(query=query)
    
    async def parse_pattern(self, query: str) -> dict:
        return self._extract_pattern(query=query)
