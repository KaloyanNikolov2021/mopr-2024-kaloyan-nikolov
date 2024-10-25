# tests/test_main.py
import pytest
from main import load_model, calculate_similarity, find_most_similar_to_given, doesnt_match, find_common_meaning

@pytest.fixture
def model():
    return load_model()

def test_calculate_similarity(model):
    assert calculate_similarity(model, "king", "queen") > calculate_similarity(model, "king", "car")

def test_find_most_similar_to_given(model):
    assert find_most_similar_to_given(model, "bridge", ["car", "man", "arch"]) == "arch"

def test_doesnt_match(model):
    assert doesnt_match(model, ["lunch", "breakfast", "dinner", "homework"]) == "homework"

def test_find_common_meaning(model):
    assert find_common_meaning(model, "man", "king", "woman") == "queen"
