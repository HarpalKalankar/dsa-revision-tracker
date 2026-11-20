from datetime import date, timedelta

from conftest import auth_headers
from revision_logic import first_due, next_revision, today_ist


def test_schedule_on_time_gives_1_3_7_21_days():
    solved = date(2026, 11, 1)
    due = first_due(solved)
    assert due == solved + timedelta(days=1)
    stage = 1
    expected = {2: 3, 3: 7, 4: 21}
    while True:
        upcoming = next_revision(stage, "easy", due)
        if upcoming is None:
            break
        stage, due = upcoming
        assert due == solved + timedelta(days=expected[stage])
    assert stage == 4


def test_hard_restarts_at_stage_1_tomorrow():
    today = date(2026, 11, 20)
    assert next_revision(3, "hard", today) == (1, today + timedelta(days=1))


def test_last_stage_easy_finishes():
    assert next_revision(4, "easy", date(2026, 11, 20)) is None


def test_full_flow_add_problem_then_revise(client):
    headers = auth_headers(client)
    yesterday = today_ist() - timedelta(days=1)
    problem = {
        "title": "Two Sum",
        "url": "https://leetcode.com/problems/two-sum/",
        "topic": "Hashing",
        "difficulty": "Easy",
        "solved_on": yesterday.isoformat(),
    }
    created = client.post("/problems", json=problem, headers=headers)
    assert created.status_code == 201

    # Logging the same link twice is refused
    assert client.post("/problems", json=problem, headers=headers).status_code == 409

    queue = client.get("/revisions/today", headers=headers).json()
    assert len(queue) == 1 and queue[0]["problem"]["title"] == "Two Sum"

    done = client.post(
        f"/revisions/{queue[0]['id']}/complete", json={"result": "easy"}, headers=headers
    )
    assert done.status_code == 200
    assert done.json()["next_stage"] == 2

    # Nothing left for today, and it can't be completed twice
    assert client.get("/revisions/today", headers=headers).json() == []
    again = client.post(
        f"/revisions/{queue[0]['id']}/complete", json={"result": "easy"}, headers=headers
    )
    assert again.status_code == 409


def test_users_cannot_see_each_others_problems(client):
    asha = auth_headers(client)
    ravi = auth_headers(client, email="ravi@example.com")
    created = client.post(
        "/problems",
        json={
            "title": "Valid Anagram",
            "url": "https://leetcode.com/problems/valid-anagram/",
            "topic": "Hashing",
            "difficulty": "Easy",
            "solved_on": today_ist().isoformat(),
        },
        headers=asha,
    ).json()
    assert client.get(f"/problems/{created['id']}", headers=ravi).status_code == 404
    assert client.get("/problems", headers=ravi).json() == []


def test_edit_and_delete_problem(client):
    headers = auth_headers(client)
    created = client.post(
        "/problems",
        json={
            "title": "3Sum",
            "url": "https://leetcode.com/problems/3sum/",
            "topic": "Two Pointers",
            "difficulty": "Medium",
            "solved_on": today_ist().isoformat(),
        },
        headers=headers,
    ).json()
    edited = client.patch(
        f"/problems/{created['id']}", json={"notes": "Sort first"}, headers=headers
    )
    assert edited.json()["notes"] == "Sort first"
    assert client.delete(f"/problems/{created['id']}", headers=headers).status_code == 204
    assert client.get("/problems", headers=headers).json() == []