from datetime import timedelta

from conftest import auth_headers
from revision_logic import today_ist


def add(client, headers, slug, topic):
    return client.post(
        "/problems",
        json={
            "title": slug,
            "url": f"https://leetcode.com/problems/{slug}/",
            "topic": topic,
            "difficulty": "Easy",
            "solved_on": (today_ist() - timedelta(days=1)).isoformat(),
        },
        headers=headers,
    )


def test_topic_stats_counts_solved_and_hard(client):
    headers = auth_headers(client)
    add(client, headers, "two-sum", "Hashing")
    add(client, headers, "valid-anagram", "Hashing")
    add(client, headers, "3sum", "Two Pointers")
    queue = client.get("/revisions/today", headers=headers).json()
    hashing = next(r for r in queue if r["problem"]["topic"] == "Hashing")
    client.post(f"/revisions/{hashing['id']}/complete", json={"result": "hard"}, headers=headers)

    stats = client.get("/stats/topics", headers=headers).json()
    assert stats[0] == {"topic": "Hashing", "solved": 2, "hard_revisions": 1}
    assert {"topic": "Two Pointers", "solved": 1, "hard_revisions": 0} in stats


def test_cors_allows_the_vite_dev_server(client):
    response = client.options(
        "/problems",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"