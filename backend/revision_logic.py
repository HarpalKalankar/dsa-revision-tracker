from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

# Days to wait after the previous revision before the next stage is due.
# Done on time, this gives revisions 1, 3, 7 and 21 days after solving.
FIRST_GAP = 1
NEXT_GAP = {2: 2, 3: 4, 4: 14}
LAST_STAGE = 4


def today_ist() -> date:
    """Today's date in India. Render's servers run on UTC."""
    return datetime.now(ZoneInfo("Asia/Kolkata")).date()


def first_due(solved_on: date) -> date:
    return solved_on + timedelta(days=FIRST_GAP)


def next_revision(stage: int, result: str, today: date) -> tuple[int, date] | None:
    """Return (next stage, due date), or None when the problem is finished."""
    if result == "hard":
        return 1, today + timedelta(days=FIRST_GAP)
    if stage >= LAST_STAGE:
        return None
    next_stage = stage + 1
    return next_stage, today + timedelta(days=NEXT_GAP[next_stage])