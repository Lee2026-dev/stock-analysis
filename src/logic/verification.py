from typing import Dict, Optional


def verify_prediction(previous_report: Dict, current_report: Dict) -> Optional[Dict]:
    """
    Verify if previous day's prediction was correct.

    Criteria: Direction match (predicted up & actual up OR predicted down & actual down)

    Args:
        previous_report: Previous day's report containing prediction
        current_report: Current day's report containing actual change

    Returns:
        Verification result dict or None if cannot verify
    """
    if not previous_report or not current_report:
        return None

    prediction = previous_report.get("prediction", {})
    up_prob = prediction.get("up_probability", 50)

    predicted_up = up_prob > 50

    tech_analysis = current_report.get("technical_analysis", {})
    actual_change_pct = tech_analysis.get("change_pct", 0)

    actual_up = actual_change_pct > 0

    is_correct = predicted_up == actual_up

    return {
        "is_correct": is_correct,
        "predicted_direction": "上涨" if predicted_up else "下跌",
        "predicted_probability": up_prob,
        "actual_direction": "上涨" if actual_up else "下跌",
        "actual_change_pct": actual_change_pct,
        "verified_at": current_report.get("date"),
    }


def calculate_accuracy_rate(verification_results: list) -> float:
    """
    Calculate accuracy rate from list of verification results.

    Args:
        verification_results: List of dicts with 'is_correct' field

    Returns:
        Accuracy rate (0-100)
    """
    if not verification_results:
        return 0.0

    correct_count = sum(1 for r in verification_results if r.get("is_correct", False))
    total_count = len(verification_results)

    return round(correct_count / total_count * 100, 1)
