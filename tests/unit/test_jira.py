import pytest

from ciopen.jira import extract_ticket_key


@pytest.mark.parametrize(
    argnames=["branch", "expected_key"],
    argvalues=[
        ("JIRA-1234-branch-name", "JIRA-1234"),
        ("JIRA-1234_branch_name", "JIRA-1234"),
        ("feature/JIRA-1234", "JIRA-1234"),
        ("feature/JIRA-1234-some-fix", "JIRA-1234"),
        ("bugfix/AB-42_fix_thing", "AB-42"),
        ("JIRA-1234", "JIRA-1234"),
    ],
)
def test_extract_ticket_key_finds_key(branch, expected_key):
    assert extract_ticket_key(branch) == expected_key


@pytest.mark.parametrize(
    argnames=["branch"],
    argvalues=[
        ("main",),
        ("feature/no-ticket-here",),
        ("jira-1234-lowercase-not-matched",),
    ],
)
def test_extract_ticket_key_returns_none_when_no_match(branch):
    assert extract_ticket_key(branch) is None
