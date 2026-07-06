/**
 * agent-spark 繚 OpenClaw Search Integration (v2.0)
 * ?菜? 繚 OpenClaw ?揣??
 *
 * Integrates with OpenClaw's built-in web_search interface.
 */
(function() {
  'use strict';

  if (typeof OpenClaw === 'undefined') return;

  const SEARCH_DIMENSIONS = {
    pain: [
      '{domain} ? ?局',
      '{domain}撣貉??桅? 銝靘?,
    ],
    flaws: [
      '{domain}鈭批? 撌株? 蝻箇',
      '{domain}review comparison problems',
    ],
    gaps: [
      '{domain} "why isn\'t there" "wish there was"',
      '{domain} alternative underserved',
    ],
    niche: [
      '{domain}撠??箸',
      '{domain} for elderly/children/pets',
    ],
  };

  OpenClaw.on('agent-spark:complete', async function(data) {
    const domain = data.answers.domain || 'random';
    const results = {};

    for (const [dim, queries] of Object.entries(SEARCH_DIMENSIONS)) {
      for (const query of queries) {
        const filled = query.replace(/\{domain\}/g, domain);
        try {
          const res = await OpenClaw.web_search(filled);
          results[dim] = results[dim] || [];
          results[dim].push({ query: filled, results: res.slice(0, 5) });
        } catch (e) {
          console.warn(`agent-spark: search failed for "${filled}"`);
        }
      }
    }

    OpenClaw.trigger('agent-spark:search_done', { results });
  });

})();

