/**
 *
 * Persists interview answers and generated ideas to SQLite.
 */
(function() {
  'use strict';

  if (typeof OpenClaw === 'undefined') return;

  const DB_NAME = 'agent-spark';

  async function initDB() {
    if (!OpenClaw.storage) return;
    await OpenClaw.storage.exec(DB_NAME, `
      CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        created_at TEXT,
        locale TEXT,
        answers TEXT,
        ideas TEXT,
        filter_results TEXT
      )
    `);
  }

  OpenClaw.on('agent-spark:complete', async function(data) {
    await initDB();
    const session = {
      id: crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(),
      created_at: new Date().toISOString(),
      locale: document.documentElement.lang || 'en',
      answers: JSON.stringify(data.answers),
      ideas: '[]',
      filter_results: 'null',
    };
    if (OpenClaw.storage) {
      await OpenClaw.storage.exec(DB_NAME,
        `INSERT INTO sessions (id, created_at, locale, answers) VALUES (?, ?, ?, ?)`,
        [session.id, session.created_at, session.locale, session.answers]
      );
    }
  });

  OpenClaw.on('agent-spark:filter_done', async function(data) {
    await initDB();
    if (OpenClaw.storage && data.sessionId) {
      await OpenClaw.storage.exec(DB_NAME,
        `UPDATE sessions SET ideas = ?, filter_results = ? WHERE id = ?`,
        [JSON.stringify(data.ideas), JSON.stringify(data.filterResults), data.sessionId]
      );
    }
  });

  initDB();
})();

