"""Regression checks for integrity, CSV interpretation, and input bounds."""
import csv

import pytest
from pydantic import ValidationError

from agents.base import AuditTrail
from agents.models import SystemTaskPayload
from cli import main as generic_main
from immunosuppression_trough_agent.models import ClinicalCasePayload
from transplant_tdm import TransplantTDMCoordinator, parse_boolean


def test_audit_signature_tamper_detection():
    trail = AuditTrail(secret_key="a-regression-key")
    trail.log("worker", "tier", "EVENT", {"result": "ok"})
    assert trail.verify_integrity()
    trail.logs[0]["event_type"] = "FORGED"
    assert not trail.verify_integrity()


def test_audit_log_is_defensive_copy():
    trail = AuditTrail(secret_key="a-regression-key")
    trail.log("worker", "tier", "EVENT", {"result": "ok"})
    trail.get_trail()[0]["actor"] = "attacker"
    assert trail.verify_integrity()


def test_nonfinite_and_negative_metrics_rejected():
    for value in (float("nan"), float("inf"), -1):
        with pytest.raises(ValidationError):
            SystemTaskPayload(task_id="T", target_identifier="X", primary_metric=value)
        with pytest.raises(ValueError):
            ClinicalCasePayload(case_id="T", patient_synthetic_id="S", primary_metric=value, secondary_metric=1)
        with pytest.raises(ValueError):
            TransplantTDMCoordinator().audit_case({"metric_primary": value})


def test_csv_false_is_not_true(tmp_path):
    source = tmp_path / "input.csv"
    output = tmp_path / "output.csv"
    source.write_text("task_id,target_identifier,primary_metric,secondary_metric,status_descriptor,is_critical_flag\n"
                      "DEMO1,SYNTH1,1,1,NOMINAL,False\n"
                      "DEMO2,SYNTH2,1,1,NOMINAL,True\n", encoding="utf-8")
    assert generic_main(["batch", "-i", str(source), "-o", str(output)]) == 0
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["overall_urgency"] == "ROUTINE"
    assert rows[1]["overall_urgency"] == "CRITICAL_STAT_PANIC"


def test_transplant_csv_bool():
    assert parse_boolean("False") is False
    assert parse_boolean("TRUE") is True
    with pytest.raises(ValueError):
        parse_boolean("perhaps")
