import timeit

# Алгоритм Боєра-Мура
def boyer_moore(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return -1

    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    skip = {c: skip.get(c, m) for c in text}

    i = m - 1
    while i < n:
        j = m - 1
        while text[i] == pattern[j]:
            if j == 0:
                return i
            i -= 1
            j -= 1
        i += skip.get(text[i], m)
    return -1

# Алгоритм Кнута-Морріса-Пратта
def knuth_morris_pratt(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return -1

    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[j] != pattern[i]:
            j = lps[j - 1]
        if pattern[j] == pattern[i]:
            j += 1
        lps[i] = j

    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1
    return -1

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern, prime=101):
    n, m = len(text), len(pattern)
    if m == 0:
        return -1

    base = 256
    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * base) % prime

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            text_hash = (text_hash + prime) % prime
    return -1

file1_path = "./стаття 1.txt"
file2_path = "./стаття 2.txt"

with open(file1_path, "r", encoding="utf-8", errors="ignore") as f1, \
     open(file2_path, "r", encoding="utf-8", errors="ignore") as f2:
    text1 = f1.read()
    text2 = f2.read()

pattern_existing = "алгоритм"
pattern_non_existing = "неіснуючий"

results = {}

# Вимірювання часу
for text, title in [(text1, "Стаття 1"), (text2, "Стаття 2")]:
    results[title] = {}
    for algo, func in [
        ("Боєра-Мура", boyer_moore),
        ("Кнута-Морріса-Пратта", knuth_morris_pratt),
        ("Рабіна-Карпа", rabin_karp)
    ]:
        for pattern in [pattern_existing, pattern_non_existing]:
            time_taken = timeit.timeit(lambda: func(text, pattern), number=10)
            results[title][f"{algo} - {pattern}"] = time_taken

# Визначення найшвидшого алгоритму для кожного тексту
fastest_per_text = {
    text: min(results[text], key=results[text].get) for text in results
}

# Визначення загального найшвидшого алгоритму
all_results = {k: v for text in results for k, v in results[text].items()}
fastest_overall = min(all_results, key=all_results.get)

markdown_content = f"""# Порівняння швидкості алгоритмів пошуку підрядка

## Результати вимірювань

| Текст | Алгоритм - Підрядок | Час (сек) |
|-------|----------------------|-----------|
"""

for text in results:
    for key, value in results[text].items():
        markdown_content += f"| {text} | {key} | {value:.6f} |\n"

markdown_content += f"""

## Найшвидший алгоритм для кожного тексту

"""

for text, algo in fastest_per_text.items():
    markdown_content += f"- **{text}**: {algo}\n"

markdown_content += f"""

## Найшвидший алгоритм загалом

- **{fastest_overall}**
"""

markdown_path = "./readme.md"
with open(markdown_path, "w", encoding="utf-8") as md_file:
    md_file.write(markdown_content)

