import { useEffect, useState } from "react";
import { api } from "../api.js";

export default function Today() {
  const [revisions, setRevisions] = useState(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    api("/revisions/today")
      .then(setRevisions)
      .catch((err) => setError(err.message));
  }, []);

  async function complete(id, result) {
    try {
      const done = await api(`/revisions/${id}/complete`, { method: "POST", body: { result } });
      setMessage(
        done.next_due_on
          ? `Saved. Next revision on ${done.next_due_on}.`
          : "Finished. No more revisions for this problem."
      );
      setRevisions((current) => current.filter((r) => r.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  if (error) return <p className="error">{error}</p>;
  if (revisions === null) return <p>Loading… The first load can take up to a minute.</p>;

  return (
    <section>
      <h2>Due today ({revisions.length})</h2>
      {message && <p className="note">{message}</p>}
      {revisions.length === 0 ? (
        <p>Nothing due today. Log a problem you solved under Add problem.</p>
      ) : (
        <ul className="list">
          {revisions.map((r) => (
            <li key={r.id} className="card">
              <a href={r.problem.url} target="_blank" rel="noreferrer">
                {r.problem.title}
              </a>
              <span className="meta">
                {r.problem.topic} · {r.problem.difficulty} · revision {r.stage} of 4
              </span>
              {r.problem.notes && <p>{r.problem.notes}</p>}
              <div className="actions">
                <button onClick={() => complete(r.id, "easy")}>Easy</button>
                <button className="secondary" onClick={() => complete(r.id, "hard")}>
                  Hard
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}