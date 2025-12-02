const statusEl = document.getElementById('status');
const bodyEl = document.getElementById('results-body');
const seasonInput = document.getElementById('season');
const scrapeBtn = document.getElementById('scrape');

function setStatus(message, variant = 'info') {
  statusEl.textContent = message;
  statusEl.dataset.variant = variant;
}

function renderRows(fixtures) {
  bodyEl.innerHTML = '';
  if (!fixtures.length) {
    bodyEl.innerHTML = '<tr><td colspan="6" class="placeholder">No fixtures returned for this season.</td></tr>';
    return;
  }

  const fragment = document.createDocumentFragment();
  fixtures.forEach((fixture) => {
    const row = document.createElement('tr');
    ['date', 'round', 'home', 'away', 'score', 'venue'].forEach((key) => {
      const cell = document.createElement('td');
      cell.textContent = fixture[key] || '';
      row.appendChild(cell);
    });
    fragment.appendChild(row);
  });
  bodyEl.appendChild(fragment);
}

async function scrape() {
  const season = seasonInput.value.trim();
  if (!season) {
    setStatus('Please enter a season like 2023-2024.', 'error');
    return;
  }

  setStatus(`Scraping fixtures for ${season}...`, 'loading');
  scrapeBtn.disabled = true;
  bodyEl.innerHTML = '<tr><td colspan="6" class="placeholder">Loading...</td></tr>';

  try {
    const response = await fetch('/api/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ season })
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || 'Failed to scrape fixtures.');
    }

    renderRows(payload.fixtures || []);
    setStatus(`Fetched ${payload.fixtures.length} fixtures for ${payload.season}.`, 'success');
  } catch (error) {
    bodyEl.innerHTML = '<tr><td colspan="6" class="placeholder">No data available.</td></tr>';
    setStatus(error.message, 'error');
  } finally {
    scrapeBtn.disabled = false;
  }
}

scrapeBtn.addEventListener('click', scrape);
seasonInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    scrape();
  }
});

setStatus('Ready to scrape. Enter a season and click "Scrape Fixtures".');
