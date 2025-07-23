from datetime import datetime, timedelta, timezone

def is_eligible(member):
    """Returns True if member has been in server for at least 2 weeks"""
    if not member.joined_at:
        return False

    now = datetime.now(timezone.utc)  # aware datetime in UTC
    joined_at = member.joined_at

    return (now - joined_at) >= timedelta(weeks=2)
