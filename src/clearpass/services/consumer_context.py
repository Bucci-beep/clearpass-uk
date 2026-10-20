"""Build explicit consumer facts without mistaking statements for policy verification."""

from clearpass.contracts.models import ConsumerFact

STOCK_BANDS = {
    "Not sure / prefer not to say": None,
    "Under £1,000": "under_1k",
    "£1,000 to £5,000": "1k_to_5k",
    "£5,000 to £20,000": "5k_to_20k",
    "Over £20,000": "over_20k",
}
STORAGE = {
    "Not sure": None,
    "Main house": "main_house",
    "Attached garage": "attached_garage",
    "Separate outbuilding": "separate_outbuilding",
}
POLICY_TYPES = {
    "Not sure": None,
    "Standard home contents": "standard_contents",
    "Home contents with business add-on": "contents_with_home_business_addon",
    "Separate business policy": "separate_business_policy",
}


def build_context_facts(
    *,
    business: str,
    has_stock: bool,
    stock_band: str,
    storage: str,
    policy_type: str,
    insurer_told: bool,
    stock_cover_checked: bool,
    visitors: str,
    equipment: str,
) -> list[ConsumerFact]:
    """Only consumer-supplied details are stated; checkboxes indicate self-confirmation."""
    facts: list[ConsumerFact] = []

    def add(field_id: str, value: str | None, status: str = "stated") -> None:
        if value:
            facts.append(ConsumerFact(field_id=field_id, value=value, status=status))

    add("business_activity_at_home", business.strip())
    if has_stock:
        add("stock_held_at_home", "Yes")
        add("stock_value_band", STOCK_BANDS[stock_band])
        add("stock_storage_location", STORAGE[storage])
    add("policy_type", POLICY_TYPES[policy_type])
    if insurer_told:
        add(
            "insurer_told_about_business",
            "Consumer says they checked with insurer",
            "consumer_confirmed",
        )
    if stock_cover_checked:
        add(
            "stock_cover_checked",
            "Consumer says they checked their policy or insurer",
            "consumer_confirmed",
        )
    if visitors != "Not sure":
        add("visitors_for_business", visitors)
    if equipment != "Not sure":
        add("business_equipment_at_home", equipment)
    return facts


def consumer_state(facts: list[ConsumerFact]) -> dict[str, str]:
    """Safe labels for display, never an assertion of actual cover."""
    by_id = {f.field_id: f for f in facts}
    return {
        "Insurance type": (
            "Stated by consumer, not verified" if "policy_type" in by_id else "Unknown"
        ),
        "Business stock cover": (
            "Consumer says they checked; ClearPass cannot confirm coverage"
            if "stock_cover_checked" in by_id
            else "Unknown — ask insurer / check wording"
        ),
        "Business disclosed to insurer": (
            "Consumer says they told insurer; not independently verified"
            if "insurer_told_about_business" in by_id
            else "Unknown"
        ),
    }
