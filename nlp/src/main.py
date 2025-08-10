from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsNERTagger,
    NewsMorphTagger,
    Doc,
)

from typing import Dict
import re

# NLP инициализация
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
ner_tagger = NewsNERTagger(emb)

# Словарь жанров — можно расширять
GENRES = {
    "боевик",
    "комедия",
    "драма",
    "триллер",
    "ужасы",
    "мелодрама",
    "фантастика",
    "фэнтези",
    "приключения",
}


def normalize_genre(word: str) -> str | None:
    for genre in GENRES:
        if word.startswith(genre[:4]):  # грубое приближение
            return genre
    return None


def extract_info(query: str) -> Dict:
    doc = Doc(query)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    result = {}

    # 🎭 Актёры / Режиссёры — любые Имена
    actors = []
    for span in doc.spans:
        if span.type == "PER":
            span.normalize(morph_vocab)
            actors.append(span.normal)
    if actors:
        result["actors"] = actors

    # 📅 Год
    years = re.findall(r"(19|20)\d{2}", query)
    if years:
        result["year"] = int(years[0])

    # 🎬 Жанры (по словам)
    for token in doc.tokens:
        normal = token.text.lower()
        genre = normalize_genre(normal)
        if genre:
            result["genre"] = genre
            break

    return result


if __name__ == "__main__":
    test_queries = [
        "Покажи мне боевики 2020 года с Томом Крузом",
        "Найди фантастику с Арнольдом Шварценеггером",
        "Фильмы ужасов 2019 года",
        "Комедии с Джимом Керри и Адамом Сэндлером",
        "Что можно посмотреть нового из комедий?"
    ]

    for query in test_queries:
        print(f"Запрос: {query}")
        print("Результат:", extract_info(query))
        print("-" * 40)
