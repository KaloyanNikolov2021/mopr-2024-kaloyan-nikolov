import json
import math

def load_model(filepath="word_embeddings.json"):
    with open(filepath, 'r') as file:
        model = json.load(file)
    return model

def calculate_similarity(model, base_word, target_word):
    vector1 = model.get(base_word)
    vector2 = model.get(target_word)
    if not vector1 or not vector2:
        return None

    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    norm1 = math.sqrt(sum(a * a for a in vector1))
    norm2 = math.sqrt(sum(b * b for b in vector2))

    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0

def find_most_similar_to_given(model, given_word, target_words):
    similarities = {word: calculate_similarity(model, given_word, word) for word in target_words}
    return max(similarities, key=similarities.get)

def doesnt_match(model, given_words):
    dissimilarities = {}
    for word in given_words:
        total_similarity = sum(calculate_similarity(model, word, other) for other in given_words if other != word)
        dissimilarities[word] = total_similarity
    return min(dissimilarities, key=dissimilarities.get)

def find_common_meaning(model, base_word, related_word, target_word):
    base_vector = model.get(base_word)
    related_vector = model.get(related_word)
    target_vector = model.get(target_word)
    if not base_vector or not related_vector or not target_vector:
        return None

    relation_vector = [rb - ba for rb, ba in zip(related_vector, base_vector)]
    target_relation = [tb + r for tb, r in zip(target_vector, relation_vector)]
    
    best_match, best_similarity = None, -1
    for word, vector in model.items():
        if word in {base_word, related_word, target_word}:
            continue
        similarity = calculate_similarity({word: vector, "target": target_relation}, word, "target")
        if similarity > best_similarity:
            best_similarity, best_match = similarity, word
    return best_match
