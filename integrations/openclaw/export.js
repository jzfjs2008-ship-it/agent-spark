/**
 *
 * Exports refined project plan as Markdown.
 */
(function() {
  'use strict';

  if (typeof OpenClaw === 'undefined') return;

  OpenClaw.on('agent-spark:export', async function(data) {
    const plan = generatePlan(data);
    const filename = `agent-spark-plan-${Date.now()}.md`;

    if (OpenClaw.exportFile) {
      await OpenClaw.exportFile(filename, plan, 'text/markdown');
    } else {
      // Fallback: download as blob
      const blob = new Blob([plan], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    }
  });

  function generatePlan(data) {
    const d = data.answers || {};
    return `# ${d.title || 'Creative Project Plan'} ??Full Project Plan

## 1. Executive Summary
**One-liner:** ${d.one_line || '(to be generated)'}
**Core problem:** ${d.pain || '(to be defined)'}
**Why now:** (market timing analysis)

## 2. Target User
${d.target || '(to be defined)'}

## 3. Product Scope (MVP)
| Priority | Feature | Effort |
|----------|---------|--------|
| P0 | (core feature) | (estimate) |
| P1 | (enhancement) | (estimate) |
| P2 | (nice-to-have) | (estimate) |

## 4. Technical Path
(to be designed)

## 5. Next Actions
- [ ] Validate core assumption (Week 1)
- [ ] Build MVP prototype (Weeks 2-4)
- [ ] User test (Week 5)

---
`;
  }
})();

