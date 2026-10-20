import json

from clearpass.contracts.models import (
    ConsumerFact,
)
from clearpass.services.context_gaps import (
    RuleBasedContextGapDetector,
)


def test_matching_rule_generates_gap(tmp_path):
    rules = {
        "context_rules": [
            {
                "id": "CR1",
                "question": "Has the insurer been informed?",
                "fires_if": {
                    "claim_topics_any": ["business_stock_cover"],
                    "consumer_facts_any": ["business_activity_at_home"],
                },
                "resolved_if": {
                    "fact_key": "insurer_told_about_business",
                    "status": "Confirmed by consumer",
                },
            }
        ]
    }

    path = tmp_path / "rules.json"
    path.write_text(json.dumps(rules))

    detector = RuleBasedContextGapDetector(
        path,
        topics={"business_stock_cover"},
    )

    facts = [
        ConsumerFact(
            field_id="business_activity_at_home",
            value="Handmade goods",
            status="stated",
        )
    ]

    results = detector.find_gaps(facts)

    assert len(results) == 1
    assert results[0].gap_id == "CR1"


def test_confirmed_fact_resolves_gap(tmp_path):
    rules = {
        "context_rules": [
            {
                "id": "CR1",
                "question": "Has the insurer been informed?",
                "fires_if": {
                    "claim_topics_any": ["business_stock_cover"],
                    "consumer_facts_any": ["business_activity_at_home"],
                },
                "resolved_if": {
                    "fact_key": "insurer_told_about_business",
                    "status": "Confirmed by consumer",
                },
            }
        ]
    }

    path = tmp_path / "rules.json"
    path.write_text(json.dumps(rules))

    detector = RuleBasedContextGapDetector(
        path,
        topics={"business_stock_cover"},
    )

    facts = [
        ConsumerFact(
            field_id="business_activity_at_home",
            value="Handmade goods",
            status="stated",
        ),
        ConsumerFact(
            field_id="insurer_told_about_business",
            value="Confirmed",
            status="consumer_confirmed",
        ),
    ]

    assert detector.find_gaps(facts) == []


def test_maya_scenario_finds_five_unresolved_questions():
    facts = [
        ConsumerFact(
            field_id="business_activity_at_home",
            value="Handmade candles",
            status="stated",
        ),
        ConsumerFact(
            field_id="stock_held_at_home",
            value="Yes",
            status="stated",
        ),
        ConsumerFact(
            field_id="stock_value_band",
            value="1k_to_5k",
            status="stated",
        ),
        ConsumerFact(
            field_id="stock_storage_location",
            value="attached_garage",
            status="stated",
        ),
        ConsumerFact(
            field_id="policy_type",
            value="standard_contents",
            status="stated",
        ),
    ]

    detector = RuleBasedContextGapDetector(
        topics={
            "business_stock_cover",
            "business_activity_disclosure",
            "home_business_liability",
            "business_equipment_cover",
            "policy_type_for_home_business",
        }
    )

    actual = [gap.gap_id for gap in detector.find_gaps(facts)]

    assert actual == ["CR1", "CR2", "CR5", "CR6", "CR7"]
