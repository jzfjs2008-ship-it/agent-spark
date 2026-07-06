/**
 * agent-spark / ?菜? ??OpenClaw Panel Logic (v2.0)
 * 
 * Implements 5-round interactive interview ??search ??diverge ??filter pipeline.
 */
(function() {
  'use strict';

  // ?? Interview data ??
  const STEPS = [
    { id: 'domain', icon: '?',
      en: 'What domain do you want ideas for? (or "random")',
      zh: '雿閬?銝芷??????菜?嚗?瘝⊥??孵???"?"嚗?,
      placeholder: 'e.g. pet supplies / home organization / 摰?典?' },
    { id: 'pain', icon: '?',
      en: 'What frustrates you in this domain? What\'s inconvenient or broken?',
      zh: '餈葵憸????芯?銝靘踴???曄??唳嚗?,
      placeholder: 'e.g. cat litter smells, food dispenser jams' },
    { id: 'flaws', icon: '??',
      en: 'What products have you tried? What are their flaws?',
      zh: '餈葵憸?雿餈鈭漣????銋撩?對?',
      placeholder: 'e.g. Product X is too expensive, Product Y breaks easily' },
    { id: 'style', icon: '?',
      en: 'A) Incremental improvement, or B) Novel creation?',
      zh: 'A ?寡隡???餈 B ?冽?砍???',
      placeholder: 'A or B' },
    { id: 'niche', icon: '?儭?,
      en: 'Any niche scenarios or unusual needs?',
      zh: '?瓷??隡?舀??寞??瘙?',
      placeholder: 'optional' },
  ];

  const answers = {};
  let currentStep = 0;

  // ?? DOM refs ??
  const stepContainer = document.getElementById('step-container');
  const stepIndicator = document.getElementById('step-indicator');
  const progressFill = document.getElementById('progress-fill');
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const outputArea = document.getElementById('output');
  const searchResults = document.getElementById('search-results');
  const ideasPreview = document.getElementById('ideas-preview');

  // ?? Render step ??
  function renderStep(idx) {
    const step = STEPS[idx];
    const val = answers[step.id] || '';
    const isLast = idx === STEPS.length - 1;

    stepIndicator.textContent = `Step ${idx+1}/${STEPS.length}`;
    progressFill.style.width = `${((idx+1)/STEPS.length)*100}%`;
    btnPrev.disabled = idx === 0;

    if (step.id === 'style') {
      stepContainer.innerHTML = `
        <div class="step-card">
          <div class="step-icon">${step.icon}</div>
          <p class="step-question-en">${step.en}</p>
          <p class="step-question-zh">${step.zh}</p>
          <div class="style-options">
            <label class="style-option ${val === 'A' ? 'selected' : ''}">
              <input type="radio" name="style" value="A" ${val === 'A' ? 'checked' : ''}>
              <span class="option-label">
                <strong>A</strong> ??Incremental improvement / ?寡隡?
              </span>
              <span class="option-desc">Low risk, easier to build</span>
            </label>
            <label class="style-option ${val === 'B' ? 'selected' : ''}">
              <input type="radio" name="style" value="B" ${val === 'B' ? 'checked' : ''}>
              <span class="option-label">
                <strong>B</strong> ??Novel creation / ?冽?砍?
              </span>
              <span class="option-desc">Higher risk, higher reward</span>
            </label>
          </div>
        </div>`;

      // Radio change handler
      document.querySelectorAll('input[name="style"]').forEach(el => {
        el.addEventListener('change', function() {
          answers[step.id] = this.value;
          document.querySelectorAll('.style-option').forEach(s => s.classList.remove('selected'));
          this.closest('.style-option').classList.add('selected');
        });
      });
    } else {
      stepContainer.innerHTML = `
        <div class="step-card">
          <div class="step-icon">${step.icon}</div>
          <p class="step-question-en">${step.en}</p>
          <p class="step-question-zh">${step.zh}</p>
          <textarea id="step-input" rows="3" placeholder="${step.placeholder}">${val}</textarea>
        </div>`;

      // Auto-save on input
      const input = document.getElementById('step-input');
      input.addEventListener('input', function() {
        answers[step.id] = this.value;
      });
      // Trigger save on Next via the stored value
    }

    btnNext.textContent = isLast ? '??Generate / ??' : 'Next / 銝?甇???;
  }

  // ?? Save current step, advance ??
  function saveCurrentStep() {
    const step = STEPS[currentStep];
    if (step.id === 'style') {
      const selected = document.querySelector('input[name="style"]:checked');
      if (selected) answers[step.id] = selected.value;
    } else {
      const input = document.getElementById('step-input');
      if (input) answers[step.id] = input.value;
    }
  }

  // ?? Show final output (search + diverge results) ??
  function showOutput() {
    stepContainer.style.display = 'none';
    btnPrev.style.display = 'none';
    btnNext.style.display = 'none';
    outputArea.style.display = 'block';

    const domain = answers.domain || '(random)';
    // Generate search links
    const searchQueries = [
      `site:zhihu.com ${domain} ?`,
      `site:reddit.com ${domain} complaints problems`,
      `"${domain}" "wish there was" OR "doesn't exist"`,
    ];
    searchResults.innerHTML = searchQueries.map(q =>
      `<div class="search-item">?? ${q}</div>`
    ).join('');

    // Prompt user to complete flow
    ideasPreview.innerHTML = `
      <div class="flow-complete">
        <p>??<strong>Interview complete!</strong> / <strong>?桃?摰?嚗?/strong></p>
        <p>Use the <strong>filter engine</strong> to validate AI-generated ideas:</p>
        <code>python3 core/filter/five_layer_filter.py ideas.json</code>
        <br><br>
        <p>Or load the <strong>Hermes skill</strong> to run the full pipeline automatically.</p>
      </div>`;
  }

  // ?? Navigation ??
  btnNext.addEventListener('click', function() {
    saveCurrentStep();

    if (currentStep === STEPS.length - 1) {
      // All done ??show output
      showOutput();
      if (window.OpenClaw && OpenClaw.trigger) {
        OpenClaw.trigger('agent-spark:complete', { answers });
      }
      return;
    }

    currentStep++;
    renderStep(currentStep);
  });

  btnPrev.addEventListener('click', function() {
    if (currentStep > 0) {
      saveCurrentStep();
      currentStep--;
      renderStep(currentStep);
    }
  });

  // ?? Export handler ??
  document.getElementById('btn-export').addEventListener('click', function() {
    if (window.OpenClaw && OpenClaw.export) {
      OpenClaw.export('markdown', { answers });
    }
  });

  // ?? Init ??
  renderStep(0);
})();

