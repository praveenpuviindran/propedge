import pytest
from src.utils.odds_converter import (
    american_to_implied_prob,
    remove_vig,
    implied_prob_to_american,
    calculate_edge,
)

def test_american_to_implied_prob_negative_odds():
    result = american_to_implied_prob(-110)
    assert result == pytest.approx(0.5238, abs=1e-4)

def test_american_to_implied_prob_positive_odds():
    result = american_to_implied_prob(150)
    assert result == pytest.approx(0.4000, abs=1e-4)

def test_american_to_implied_prob_zero_raises():
    with pytest.raises(ValueError):
        american_to_implied_prob(0)

def test_remove_vig_returns_correct_no_vig_over():
    prob_over = american_to_implied_prob(-115)
    prob_under = american_to_implied_prob(-105)
    no_vig_over, no_vig_under = remove_vig(prob_over, prob_under)
    assert no_vig_over == pytest.approx(0.5108, abs=1e-4)

def test_remove_vig_sums_to_one():
    prob_over = american_to_implied_prob(-115)
    prob_under = american_to_implied_prob(-105)
    no_vig_over, no_vig_under = remove_vig(prob_over, prob_under)
    assert no_vig_over + no_vig_under == pytest.approx(1.0, abs=1e-10)

def test_remove_vig_invalid_prob_raises():
    with pytest.raises(ValueError):
        remove_vig(1.5, 0.5)

def test_implied_prob_to_american_favorite():
    result = implied_prob_to_american(0.5238)
    assert result == -110

def test_implied_prob_to_american_underdog():
    result = implied_prob_to_american(0.4000)
    assert result == 150

def test_implied_prob_to_american_even_money():
    result = implied_prob_to_american(0.5)
    assert result == -100

def test_calculate_edge_positive_edge():
    result = calculate_edge(0.58, -115, -105)
    assert result > 0

def test_calculate_edge_negative_edge():
    result = calculate_edge(0.44, -115, -105)
    assert result < 0

def test_calculate_edge_invalid_model_prob_raises():
    with pytest.raises(ValueError):
        calculate_edge(1.5, -115, -105)

