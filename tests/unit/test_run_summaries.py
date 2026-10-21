from unittest.mock import patch

from trackio.server import get_run_summaries


def test_run_summaries_preserve_order_and_ids():
    records = [
        {"id": "id-1", "name": "duplicate"},
        {"id": "id-2", "name": "duplicate"},
    ]

    with (
        patch(
            "trackio.server.SQLiteStorage.get_run_records",
            return_value=records,
        ) as get_records,
        patch("trackio.server._get_run_summary_resolved") as summary,
    ):
        summary.side_effect = [
            {"run_id": "id-1", "num_logs": 2},
            {"run_id": "id-2", "num_logs": 5},
        ]
        result = get_run_summaries("demo")

    assert [row["run_id"] for row in result] == ["id-1", "id-2"]
    assert [row["num_logs"] for row in result] == [2, 5]
    assert summary.call_count == 2
    summary.assert_any_call("demo", "duplicate", "id-1")
    summary.assert_any_call("demo", "duplicate", "id-2")

    get_records.assert_called_once_with("demo")
