from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BinaryClassificationMetrics:
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int
    precision: float
    recall: float
    f1: float
    false_positive_rate: float
    false_negative_rate: float

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


def _safe_divide(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def compute_binary_metrics(
    expected: list[bool],
    predicted: list[bool],
) -> BinaryClassificationMetrics:
    """Compute deterministic binary metrics without external dependencies."""
    if len(expected) != len(predicted):
        raise ValueError("expected and predicted must have the same length")
    if not expected:
        raise ValueError("at least one scored record is required")

    true_positive = sum(
        1 for truth, prediction in zip(expected, predicted, strict=True)
        if truth and prediction
    )
    true_negative = sum(
        1 for truth, prediction in zip(expected, predicted, strict=True)
        if not truth and not prediction
    )
    false_positive = sum(
        1 for truth, prediction in zip(expected, predicted, strict=True)
        if not truth and prediction
    )
    false_negative = sum(
        1 for truth, prediction in zip(expected, predicted, strict=True)
        if truth and not prediction
    )

    precision = _safe_divide(true_positive, true_positive + false_positive)
    recall = _safe_divide(true_positive, true_positive + false_negative)
    f1 = _safe_divide(2 * precision * recall, precision + recall)
    false_positive_rate = _safe_divide(
        false_positive,
        false_positive + true_negative,
    )
    false_negative_rate = _safe_divide(
        false_negative,
        false_negative + true_positive,
    )

    return BinaryClassificationMetrics(
        true_positive=true_positive,
        true_negative=true_negative,
        false_positive=false_positive,
        false_negative=false_negative,
        precision=precision,
        recall=recall,
        f1=f1,
        false_positive_rate=false_positive_rate,
        false_negative_rate=false_negative_rate,
    )
