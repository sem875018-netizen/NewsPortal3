import re

from django import template

register = template.Library()

# Замените примеры на слова, которые требуется скрывать.
CENSORED_WORDS = {
    "редиска",
}

# Ищет последовательности букв, в том числе русских.
WORD_PATTERN = re.compile(r"[^\W\d_]+", re.UNICODE)


@register.filter
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр censor можно применять только к строкам.")

    def replace_word(match):
        word = match.group(0)

        if word.casefold() in CENSORED_WORDS:
            return word[0] + "*" * (len(word) - 1)

        return word

    return WORD_PATTERN.sub(replace_word, value)