TYPE_ACTIONS = {
    "Internal Policy": "Review and update the affected internal policy and map the new obligation to an accountable owner.",
    "Business Process": "Run a process-level compliance gap assessment and create an implementation checklist.",
    "API": "Review the API contract, validation rules and monitoring required by the regulatory change.",
    "Microservice": "Create an engineering change task and add regression tests for the impacted compliance behavior.",
    "Database": "Verify retention, access, lineage and audit fields against the new obligation.",
    "Compliance Control": "Re-test the control, update its evidence requirements and assign a control owner.",
    "Audit Artifact": "Regenerate or update the evidence artifact and preserve the dependency trace.",
    "Business Unit": "Notify the responsible business unit and assign an accountable implementation owner.",
}

def generate_recommendations(impacted):
    recommendations, seen = [], set()
    for item in impacted[:10]:
        action = TYPE_ACTIONS.get(item["type"])
        if action and action not in seen:
            recommendations.append(action)
            seen.add(action)
    return recommendations[:6] or [
        "Perform human-reviewed compliance impact assessment before implementation."
    ]
