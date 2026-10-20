"""Regression tests for knowing versus not knowing policy details."""

from clearpass.services.consumer_context import build_context_facts, consumer_state
from clearpass.services.context_gaps import RuleBasedContextGapDetector


def maya(**overrides):
    info = dict(
        business="Making candles",
        has_stock=True,
        stock_band="£1,000 to £5,000",
        storage="Attached garage",
        policy_type="Standard home contents",
        insurer_told=False,
        stock_cover_checked=False,
        visitors="Not sure",
        equipment="Not sure",
    )
    info.update(overrides)
    return build_context_facts(**info)


def test_maya_explicit_details_keep_policy_cover_unknown():
    facts = maya()
    ids = {f.field_id for f in facts}
    assert {
        "stock_held_at_home",
        "stock_value_band",
        "stock_storage_location",
        "policy_type",
    } <= ids
    assert "stock_cover_checked" not in ids
    assert consumer_state(facts)["Business stock cover"].startswith("Unknown")


def test_maya_context_gaps_match_team_scenario():
    topics = {
        "business_stock_cover",
        "business_activity_disclosure",
        "home_business_liability",
        "business_equipment_cover",
        "policy_type_for_home_business",
    }
    gaps = RuleBasedContextGapDetector(topics=topics).find_gaps(maya())
    assert [g.gap_id for g in gaps] == ["CR1", "CR2", "CR5", "CR6", "CR7"]


def test_self_confirmations_resolve_only_matching_questions():
    facts = maya(insurer_told=True, stock_cover_checked=True)
    topics = {
        "business_stock_cover",
        "business_activity_disclosure",
        "policy_type_for_home_business",
    }
    ids = {g.gap_id for g in RuleBasedContextGapDetector(topics=topics).find_gaps(facts)}
    assert "CR1" not in ids
    assert "CR2" not in ids
    assert "CR7" in ids
    assert "cannot confirm" in consumer_state(facts)["Business stock cover"]


def test_missing_stock_information_not_falsely_stated():
    facts = maya(stock_band="Not sure / prefer not to say", storage="Not sure")
    ids = {
        g.gap_id
        for g in RuleBasedContextGapDetector(topics={"business_stock_cover"}).find_gaps(facts)
    }
    assert {"CR3", "CR4"} <= ids


def test_no_stock_does_not_invent_stock_facts():
    facts = maya(has_stock=False)
    ids = {f.field_id for f in facts}
    assert "stock_held_at_home" not in ids
    assert "stock_storage_location" not in ids
