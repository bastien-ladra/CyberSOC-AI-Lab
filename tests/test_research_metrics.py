import pytest

from research.metrics import compute_binary_metrics


def test_compute_binary_metrics_tracks_confusion_and_rates() -> None:
    metrics = compute_binary_metrics(
        expected=[True, True, False, False],
        predicted=[True, False, True, False],
    )

    assert metrics.true_positive == 1
    assert metrics.true_negative == 1
    assert metrics.false_positive == 1
    assert metrics.false_negative == 1
    assert metrics.precision == pytest.approx(0.5)
    assert metrics.recall == pytest.approx(0.5)
    assert metrics.f1 == pytest.approx(0.5)
    assert metrics.false_positive_rate == pytest.approx(0.5)
    assert metrics.false_negative_rate == pytest.approx(0.5)


def test_compute_binary_metrics_rejects_empty_inputs() -> None:
    with pytest.raises(ValueError, match="at least one scored record"):
        compute_binary_metrics([], [])


def test_compute_binary_metrics_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError, match="same length"):
        compute_binary_metrics([True], [True, False])
