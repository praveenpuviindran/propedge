"""Utility function for converting odds between different formats."""

def american_to_implied_prob(odds: int) -> float:

    """
    Converts American odds to implied probability.
    Args: 
        odds (int): The American odds.
    Returns:
        float: The implied probability.
    """

    if odds == 0:
        raise ValueError("Odds cannot be zero.")
    
    elif odds < 0:
        return abs(odds) / (abs(odds) + 100)
    
    else:
        return 100 / (odds + 100)

   
def remove_vig (prob_over: float, prob_under: float) -> tuple[float, float]:

    """
    Removes the vig from the implied probabilities.
    Args:
        prob_over(float): the implied probability of the over bet.
        prob_under(float): the implied probability of the under bet.
    Returns:
        tuple[float, float]: no-vig probabilities as over, under - summing to 1.
    """

    if not (0 < prob_over < 1) or not (0 < prob_under < 1):
        raise ValueError("Probabilities must be between 0 and 1 exclusive.")
    
    total = prob_over + prob_under

    no_vig_over = prob_over / total

    no_vig_under = prob_under / total

    return (no_vig_over, no_vig_under)


def implied_prob_to_american(prob: float) -> int:

    """
    Converts implied probabilities to american with rounding.
    Args:
        prob(float): the implied probability.
    Returns:
        int: the American odds as an integer (ex. -110, 110, etc.)
    """

    if not (0 < prob < 1):
        raise ValueError("Probabilities must be between 0 and 1 exclusive.")

    if prob == 0.5:
        return -100
    
    elif prob > 0.5:
        return -round((prob * 100) / (1 - prob))
    
    elif prob < 0.5:
        return round((1 - prob) * 100 / prob)
    

def calculate_edge(model_prob: float, market_odds_over: int, market_odds_under: int) -> float:

    """
    This function converts market odds to raw implied probabilities to 
    return no-vig probabilities for both over and under market predictions.
    Args:
        model_prob(float): Model's estimated probability for the over outcome
        market_odds_over(int): American odds for the over
        market_odds_under(int): American odds for the under
    Returns:
        float: Edge value as a decimal. Positive = model favors the over relative to the market
    """

    if not (0 < model_prob < 1):
        raise ValueError("Probabilities must be between 0 and 1 exclusive.")
    
    raw_prob_over = american_to_implied_prob(market_odds_over)

    raw_prob_under = american_to_implied_prob(market_odds_under)

    no_vig_over, no_vig_under = remove_vig(raw_prob_over, raw_prob_under)

    return model_prob - no_vig_over