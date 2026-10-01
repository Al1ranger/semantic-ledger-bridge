import json


LEFT_COMPLETE = [
    {"id": "l-host", "description": "Annual hosted compute subscription", "amount": 120, "currency": "USD"},
    {"id": "l-audit", "description": "External security assessment for application", "amount": 120, "currency": "USD"},
    {"id": "l-support", "description": "Overnight incident response standby", "amount": 300, "currency": "USD"},
]
RIGHT_COMPLETE = [
    {"id": "r-security", "description": "Third-party app cybersecurity audit", "amount": 120, "currency": "USD"},
    {"id": "r-infra", "description": "Yearly cloud hosting service", "amount": 120, "currency": "USD"},
    {"id": "r-support", "description": "After-hours emergency response retainer", "amount": 300, "currency": "USD"},
]
LEFT_PARTIAL = LEFT_COMPLETE[:2] + [
    {"id": "l-lunch", "description": "Team lunch catering", "amount": 50, "currency": "USD"},
]
RIGHT_PARTIAL = RIGHT_COMPLETE[:2] + [
    {"id": "r-clean", "description": "Office janitorial cleaning", "amount": 50, "currency": "USD"},
]
COMPLETE_PAIRS = [
    {"left": "l-host", "right": "r-infra"},
    {"left": "l-audit", "right": "r-security"},
    {"left": "l-support", "right": "r-support"},
]
PARTIAL_PAIRS = COMPLETE_PAIRS[:2]


def register(contract, vm, owner, batch="batch-one", kind="complete"):
    vm.sender = owner
    contract.register_batch(batch,
                            "Al1ranger", "semantic-ledger-bridge", "a" * 40,
                            "fixtures/left-" + kind + ".json",
                            "Al1ranger", "semantic-ledger-bridge", "a" * 40,
                            "fixtures/right-" + kind + ".json")


def sources(vm, left=LEFT_COMPLETE, right=RIGHT_COMPLETE, left_status=200):
    vm.mock_web(r".*left-.*\.json", {"status": left_status, "body": json.dumps(left)})
    vm.mock_web(r".*right-.*\.json", {"status": 200, "body": json.dumps(right)})


def model(vm, pairs):
    vm.mock_llm(r"(?s).*Match only records describing.*", json.dumps({"pairs": pairs}))


def test_semantic_pairs_disambiguate_identical_amounts(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/SemanticLedgerBridge.py")
    register(c, direct_vm, direct_alice)
    sources(direct_vm)
    model(direct_vm, COMPLETE_PAIRS)
    c.reconcile("batch-one")
    report = json.loads(c.get_report("batch-one"))
    assert report["state"] == "RECONCILED"
    assert report["pairs"] == sorted(COMPLETE_PAIRS, key=lambda p: p["left"])
    assert c.get_match("batch-one", "l-host") == "r-infra"
    assert c.get_match("batch-one", "l-audit") == "r-security"
    assert report["unmatched_left"] == report["unmatched_right"] == []


def test_equal_amounts_do_not_force_unrelated_match(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/SemanticLedgerBridge.py")
    register(c, direct_vm, direct_alice, kind="partial")
    sources(direct_vm, LEFT_PARTIAL, RIGHT_PARTIAL)
    model(direct_vm, PARTIAL_PAIRS)
    c.reconcile("batch-one")
    report = json.loads(c.get_report("batch-one"))
    assert report["state"] == "PARTIAL"
    assert report["unmatched_left"] == ["l-lunch"]
    assert report["unmatched_right"] == ["r-clean"]
    assert c.get_match("batch-one", "l-lunch") == ""


def test_amount_mismatch_model_pair_fails_closed(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/SemanticLedgerBridge.py")
    register(c, direct_vm, direct_alice)
    sources(direct_vm)
    model(direct_vm, [{"left": "l-host", "right": "r-support"}])
    c.reconcile("batch-one")
    report = json.loads(c.get_report("batch-one"))
    assert report["state"] == "UNRESOLVED" and not report["model_valid"]
    assert report["pairs"] == []
    assert c.get_match("batch-one", "l-host") == ""
    with direct_vm.expect_revert("reconciliation is terminal"):
        c.reconcile("batch-one")


def test_duplicate_right_record_fails_closed(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/SemanticLedgerBridge.py")
    register(c, direct_vm, direct_alice)
    sources(direct_vm)
    model(direct_vm, [{"left": "l-host", "right": "r-infra"},
                      {"left": "l-audit", "right": "r-infra"}])
    c.reconcile("batch-one")
    report = json.loads(c.get_report("batch-one"))
    assert report["state"] == "UNRESOLVED" and not report["model_valid"]
    assert c.get_match("batch-one", "l-host") == ""


def test_unavailable_source_can_retry_without_false_match(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/SemanticLedgerBridge.py")
    register(c, direct_vm, direct_alice)
    sources(direct_vm, left_status=404)
    c.reconcile("batch-one")
    assert json.loads(c.get_report("batch-one"))["state"] == "UNAVAILABLE"
    assert c.get_match("batch-one", "l-host") == ""
    direct_vm.clear_mocks()
    sources(direct_vm)
    model(direct_vm, COMPLETE_PAIRS)
    c.reconcile("batch-one")
    assert c.get_match("batch-one", "l-host") == "r-infra"


def test_batch_scoping_and_source_validation(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/SemanticLedgerBridge.py")
    register(c, direct_vm, direct_alice)
    register(c, direct_vm, direct_alice, batch="batch-two", kind="partial")
    assert c.get_match("batch-two", "l-host") == ""
    with direct_vm.expect_revert("unique batch ID"):
        register(c, direct_vm, direct_alice)
    with direct_vm.expect_revert("two distinct pinned source paths"):
        c.register_batch("bad", "Al1ranger", "semantic-ledger-bridge", "a" * 40,
                         "../secret.json", "Al1ranger", "semantic-ledger-bridge", "a" * 40,
                         "fixtures/right-complete.json")
