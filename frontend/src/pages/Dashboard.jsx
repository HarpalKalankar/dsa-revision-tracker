import { useEffect, useState } from "react";
import { api } from "../api.js";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/stats/topics")
      .then(setStats)
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (stats === null) return <p>Loading…</p>;
  if (stats.length === 0) return <p>No problems logged yet.</p>;

  const total = stats.reduce((sum, row) => sum + row.solved, 0);

  return (
    <section>
      <h2>Your topics</h2>
      <p>
        {total} problems solved. Topics you marked "hard" most often are at the top, so start your
        practice there.
      </p>
      <table>
        <thead>
          <tr>
            <th>Topic</th>
            <th>Solved</th>
            <th>Marked hard</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((row) => (
            <tr key={row.topic} className={row.hard_revisions > 0 ? "weak" : ""}>
              <td>{row.topic}</td>
              <td>{row.solved}</td>
              <td>{row.hard_revisions}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}