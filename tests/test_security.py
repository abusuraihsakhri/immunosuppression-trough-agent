"""
Security-focused test suite for Immunosuppression Trough Agent.
Tests PHI guard enforcement, audit trail integrity, and input validation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, AuditTrail, SecurityException, assert_no_phi


class TestPHIGuard:
    """Tests for PHI outbound guard enforcement."""

    def test_mrn_pattern_blocked(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive")

    def test_ssn_pattern_blocked(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("SSN: 123-45-6789")

    def test_phone_number_blocked(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Call patient at 555-123-4567")

    def test_email_blocked(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Email: patient@example.com")

    def test_dob_pattern_blocked(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("DOB: 01/15/1985")

    def test_patient_name_blocked(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Patient Name: John Smith")

    def test_generic_name_blocked(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Patient John Doe admitted")

    def test_clean_text_passes(self):
        PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")
        PHIGuard.assert_no_phi("Tacrolimus trough level 12.5 ng/mL")
        PHIGuard.assert_no_phi("CYP3A5 *1/*3 genotype result")

    def test_empty_text_passes(self):
        PHIGuard.assert_no_phi("")

    def test_none_text_passes(self):
        PHIGuard.assert_no_phi(None)

    def test_phi_redaction(self):
        text = "Patient MRN-123456 has SSN 123-45-6789"
        redacted = PHIGuard.redact_phi(text)
        assert "MRN-123456" not in redacted
        assert "123-45-6789" not in redacted
        assert "[REDACTED_IDENTIFIER]" in redacted


class TestAuditTrail:
    """Tests for HMAC-SHA256 audit trail integrity."""

    def test_audit_trail_creation(self):
        trail = AuditTrail(secret_key="test-key-123")
        assert len(trail.logs) == 0

    def test_audit_trail_logging(self):
        trail = AuditTrail(secret_key="test-key-123")
        entry = trail.log(
            actor="test_actor",
            actor_tier="test",
            event_type="TEST_EVENT",
            details={"key": "value"}
        )
        assert entry["audit_id"].startswith("AUDIT-")
        assert entry["actor"] == "test_actor"
        assert entry["event_type"] == "TEST_EVENT"
        assert entry["current_hash"] != ""
        assert entry["prev_hash"] == "GENESIS_BLOCK_0000000000000000"

    def test_audit_trail_chain_integrity(self):
        trail = AuditTrail(secret_key="test-key-123")
        trail.log("actor1", "tier1", "EVENT_1", {"data": 1})
        trail.log("actor2", "tier2", "EVENT_2", {"data": 2})
        trail.log("actor3", "tier3", "EVENT_3", {"data": 3})
        assert trail.verify_integrity() is True

    def test_audit_trail_chain_linking(self):
        trail = AuditTrail(secret_key="test-key-123")
        entry1 = trail.log("actor1", "tier1", "EVENT_1", {"data": 1})
        entry2 = trail.log("actor2", "tier2", "EVENT_2", {"data": 2})
        assert entry2["prev_hash"] == entry1["current_hash"]

    def test_audit_trail_tamper_detection(self):
        trail = AuditTrail(secret_key="test-key-123")
        trail.log("actor1", "tier1", "EVENT_1", {"data": 1})
        trail.log("actor2", "tier2", "EVENT_2", {"data": 2})
        # Tamper with the first entry
        trail.logs[0]["current_hash"] = "TAMPERED_HASH"
        assert trail.verify_integrity() is False

    def test_audit_trail_phi_blocked_in_details(self):
        trail = AuditTrail(secret_key="test-key-123")
        with pytest.raises(SecurityException):
            trail.log("actor1", "tier1", "EVENT_1", {"note": "Patient MRN-123456"})

    def test_global_audit_logger(self):
        entry = AuditLogger.log(
            actor="test",
            actor_tier="test",
            event_type="TEST",
            details={"key": "value"}
        )
        assert entry["audit_id"].startswith("AUDIT-")
        assert len(AuditLogger.get_trail()) > 0
        assert AuditLogger.verify_integrity() is True


class TestInputValidation:
    """Tests for input validation functions."""

    def test_assert_no_phi_with_clean_text(self):
        assert_no_phi("Safe text without PHI")  # Should not raise

    def test_assert_no_phi_with_phi(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Patient SSN: 123-45-6789")

    def test_assert_no_phi_with_none(self):
        assert_no_phi(None)  # Should not raise

    def test_assert_no_phi_with_empty(self):
        assert_no_phi("")  # Should not raise
