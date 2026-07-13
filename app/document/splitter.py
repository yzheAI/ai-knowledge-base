import re


def clean_chunks(chunks: list[str]):
    cleaned = []
    for c in chunks:
        c = c.strip()

        if not c:
            continue

        if len(c) < 10:
            continue

        if len(c.replace("。", "").strip()) == 0:
            continue

        cleaned.append(c)
    return cleaned


# def split_text(text: str, chunk_size: int = 500, overlap: int = 50):
#     sentences = text.split("。")
#     chunks = []
#
#     current = ""
#     for sentence in sentences:
#         sentence = sentence.strip()
#         if not sentence:
#             continue
#         sentence += "。"
#
#         if len(current)+len(sentence) <= chunk_size:
#             current += sentence
#         else:
#             if current:
#                 chunks.append(current)
#                 # overlap
#                 overlap_text = current[-overlap:]
#
#                 current = overlap_text + sentence
#
#     if current:
#         chunks.append(current)
#
#     return chunks


def split_paragraph(text: str):
    paragraphs = re.split(
        r"\n\s*\n",
        text
    )
    return [
        p.strip()
        for p in paragraphs
        if p.strip()
    ]


def split_sentence(paragraph: str):
    sentences = re.split(
        r"(?<=[。！；？])",
        paragraph
    )
    return [
        s.strip()
        for s in sentences
        if s.strip()
    ]


def sentences_merge(sentences: list[str], chunk_size: int = 500):
    chunks = []

    current = ""

    for sentence in sentences:

        if len(current) + len(sentence) <= chunk_size:
            current += sentence

        else:
            if current:
                chunks.append(current)

            current = sentence

    if current:
        chunks.append(current)

    return chunks


def add_overlap(chunks, overlap_size: int):
    result = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            result.append(chunk)
        else:
            pre = chunks[i - 1]
            overlap = pre[-overlap_size:]
            result.append(overlap + chunk)
    return result


def split_text(text: str, chunk_size: int = 500, overlap_size: int = 100):
    paragraphs = split_paragraph(text)
    all_sentences = []
    for paragraph in paragraphs:
        sentences = split_sentence(paragraph)
        all_sentences.extend(sentences)

    chunks = sentences_merge(
        all_sentences,
        chunk_size
    )

    chunks = add_overlap(
        chunks,
        overlap_size
    )

    return chunks
