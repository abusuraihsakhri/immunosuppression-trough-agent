/** Demonstration-only rules reflecting the generic Python workers. Not a clinical model. */
export function evaluate(input) {
  const {task_id, target_identifier, status_descriptor, is_critical_flag} = input;
  if (![task_id, target_identifier].every(x => typeof x === "string" && /^[A-Za-z0-9._-]{1,80}$/.test(x))) {
    throw new Error("Use synthetic task and target IDs (1–80 letters, digits, dots, underscores or hyphens).");
  }
  if (typeof status_descriptor !== "string" || !status_descriptor.trim() || status_descriptor.length > 100) {
    throw new Error("Provide a short status descriptor.");
  }
  const primary = input.primary_metric;
  const secondary = input.secondary_metric;
  if (![primary, secondary].every(v => typeof v === "number" && Number.isFinite(v) && v >= 0)) {
    throw new Error("Both metrics must be finite, non-negative numbers.");
  }
  if (typeof is_critical_flag !== "boolean") throw new Error("Critical flag must be boolean.");
  const alerts = [];
  if (primary > 25) alerts.push({worker:"InvariantQCWorker",urgency:"ELEVATED_RISK",finding:"Primary demonstration metric exceeds 25."});
  if (is_critical_flag || secondary > 12) {
    alerts.push({worker:"SafetyEscalationWorker",urgency:is_critical_flag?"CRITICAL_STAT_PANIC":"ELEVATED_RISK",finding:"Secondary demonstration metric exceeds 12 or critical flag set."});
  }
  if (["DISCORDANT","ANOMALY","MUTANT","VIOLATION","FAIL","REJECT"].some(word => status_descriptor.toUpperCase().includes(word))) {
    alerts.push({worker:"ProtocolConformanceWorker",urgency:"ELEVATED_RISK",finding:"Status descriptor matches a configured demonstration keyword."});
  }
  const critical = alerts.some(alert => alert.urgency === "CRITICAL_STAT_PANIC");
  const elevated = alerts.length > 0;
  return {
    mode:"LOCAL_RULE_DEMONSTRATION_NOT_FOR_CLINICAL_USE",
    task_id,
    target_identifier,
    overall_urgency:critical?"CRITICAL_STAT_PANIC":elevated?"ELEVATED_RISK":"ROUTINE",
    integrity_status:critical?"RECALIBRATION_REQUIRED":elevated?"DISCORDANT_ANOMALY":"VALIDATED_OPTIMAL",
    total_alerts:alerts.length,
    alerts
  };
}

if (typeof document !== "undefined") {
  const form = document.getElementById("audit-form");
  const summary = document.getElementById("summary");
  const report = document.getElementById("report");
  const download = document.getElementById("download");
  let current = null;
  form.addEventListener("submit", event => {
    event.preventDefault();
    try {
      const primaryText = document.getElementById("primary").value.trim();
      const secondaryText = document.getElementById("secondary").value.trim();
      current = evaluate({
        task_id:document.getElementById("task").value.trim(),
        target_identifier:document.getElementById("target").value.trim(),
        primary_metric:primaryText ? Number(primaryText) : NaN,
        secondary_metric:secondaryText ? Number(secondaryText) : NaN,
        status_descriptor:document.getElementById("status").value.trim(),
        is_critical_flag:document.getElementById("critical").checked
      });
      summary.classList.remove("error");
      summary.textContent = current.overall_urgency + " • " + current.total_alerts + " rule alerts";
      report.textContent = JSON.stringify(current,null,2);
      download.disabled = false;
    } catch (error) {
      current = null;
      download.disabled = true;
      summary.classList.add("error");
      summary.textContent = "Validation error";
      report.textContent = error.message;
    }
  });
  form.addEventListener("reset", () => {
    current = null;
    download.disabled = true;
    summary.classList.remove("error");
    summary.textContent = "No evaluation yet.";
    report.textContent = "Complete the form and select Evaluate rules.";
  });
  download.addEventListener("click", () => {
    if (!current) return;
    const url = URL.createObjectURL(new Blob([JSON.stringify(current,null,2)+"\n"],{type:"application/json"}));
    const a = document.createElement("a");
    a.href = url;
    a.download = "trough-agent-demonstration.json";
    document.body.append(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  });
}
