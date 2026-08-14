import re

# Jira keys: uppercase project prefix + "-" + digits.
# Matches JIRA-1234, feature/JIRA-1234-branch-name, JIRA-1234_branch_name, etc.
TICKET_KEY_PATTERN = re.compile(r"[A-Z][A-Z0-9]+-\d+")


def extract_ticket_key(branch: str) -> str | None:
    """Extract a Jira ticket key (e.g. JIRA-1234) from a branch name."""
    match = TICKET_KEY_PATTERN.search(branch)
    return match.group(0) if match else None
