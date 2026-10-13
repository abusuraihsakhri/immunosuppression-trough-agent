"""
Clinical Algorithmic Engine & Guideline Rules for TransplantTDM Sentinel: Tacrolimus, Cyclosporine & Everolimus Trough Agent.
Domain: Transplant Medicine
Standard: unvalidated demonstration rules
"""
import math
from typing import Dict, Any, List, Optional
from .models import ClinicalCasePayload, AgentAlert, UrgencyLevel, ClinicalIntegrityStatus


class ClinicalDomainEngine:
    GUIDELINE = "unvalidated demonstration rules"
    PRIMARY_BASELINE_LIMIT = 20.0
    SECONDARY_ALERT_LIMIT = 10.0

    @classmethod
    def evaluate_primary_index(cls, value: float) -> Optional[Dict[str, Any]]:
        if value > cls.PRIMARY_BASELINE_LIMIT:
            return {
                "title": "Primary Metric Threshold Exceeded",
                "finding": f"Observed value ({value:.2f}) exceeds unvalidated demonstration rules configured demonstration threshold ({cls.PRIMARY_BASELINE_LIMIT:.1f}).",
                "recommendation": "Review demonstration inputs; use a validated drug-specific protocol for clinical decisions.",
            }
        return None

    @classmethod
    def evaluate_secondary_kinetics(cls, value: float, is_stat: bool) -> Optional[Dict[str, Any]]:
        if value > cls.SECONDARY_ALERT_LIMIT or is_stat:
            return {
                "title": "Demonstration Secondary Metric / Flag Triggered",
                "finding": f"Kinetic parameter ({value:.2f}) with STAT={is_stat} matches a demonstration escalation rule.",
                "recommendation": "No clinical action is implied by this demonstration threshold.",
            }
        return None

    @classmethod
    def evaluate_biomarker_concordance(cls, status_flag: str, biomarkers: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        status_upper = str(status_flag).upper()
        if "DISCORDANT" in status_upper or "EQUIVOCAL" in status_upper or "MUTANT" in status_upper:
            return {
                "title": "Demonstration Status Keyword Detected",
                "finding": f"Status flag '{status_flag}' matches a configured status keyword.",
                "recommendation": f"Interpret using a validated clinical protocol; no testing recommendation is generated.",
            }
        return None
