import { useState } from "react";
import { api } from "../api.js";

// Must match the Topic list in backend/schemas.py
const TOPICS = [
  "Arrays", "Strings", "Hashing", "Two Pointers", "Sliding Window",
  "Linked List", "Stack", "Queue", "Binary Search", "Recursion",
  "Trees", "Heaps", "Graphs", "Backtracking", "Dynamic Programming",
  "Greedy", "Other",
];

// Today's date as YYYY-MM-DD in the user's own time zone
const todayString = () => new Date().toLocaleDateString("en-CA");

const emptyForm = () => ({
  title: "",
  url: "",
  topic: "Arrays",
  difficulty: "Easy",
  notes: "",
  solved_on: todayString(),
});

export default function AddProblem() {
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const update = (field) => (event) => setForm({ ...form, [field]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await api("/problems", { method: "POST", body: { ...form, notes: form.notes || null } });
      setMessage(`Saved "${form.title}". Its first revision is due the day after you solved it.`);
      setForm(emptyForm());
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="narrow">
      <h2>Add a problem</h2>
      <form className="card" onSubmit={handleSubmit}>
        <label>
          Title
          <input value={form.title} onChange={update("title")} placeholder="Two Sum" required />
        </label>
        <label>
          LeetCode link
          <input
            type="url"
            value={form.url}
            onChange={update("url")}
            placeholder="https://leetcode.com/problems/two-sum/"
            required
          />
        </label>
        <label>
          Topic
          <select value={form.topic} onChange={update("topic")}>
            {TOPICS.map((topic) => (
              <option key={topic}>{topic}</option>
            ))}
          </select>
        </label>
        <label>
          Difficulty
          <select value={form.difficulty} onChange={update("difficulty")}>
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
        </label>
        <label>
          Date solved
          <input type="date" value={form.solved_on} onChange={update("solved_on")} required />
        </label>
        <label>
          Notes (optional)
          <textarea value={form.notes} onChange={update("notes")} placeholder="Key idea, mistakes to avoid" />
        </label>
        {error && <p className="error">{error}</p>}
        {message && <p className="note">{message}</p>}
        <button>Save problem</button>
      </form>
    </section>
  );
}