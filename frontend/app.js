const cardsEl = document.getElementById('cards');
const emptyEl = document.getElementById('empty');
const searchEl = document.getElementById('search');
const categoryEl = document.getElementById('category');
const sourceEl = document.getElementById('source');
const sortEl = document.getElementById('sort');
const clearEl = document.getElementById('clear');
const metaLineEl = document.getElementById('metaLine');
const statsEl = document.getElementById('stats');

let allItems = [];

const fmtPrice = (price, currency) => {
  if (typeof price !== 'number') return 'price n/a';
  return `${new Intl.NumberFormat('sv-SE').format(price)} ${currency || 'SEK'}`;
};

function setStats(items) {
  const priced = items.filter((i) => typeof i.price === 'number');
  const avg = priced.length ? Math.round(priced.reduce((s, i) => s + i.price, 0) / priced.length) : null;
  statsEl.innerHTML = [
    `<span class="badge">items: ${items.length}</span>`,
    `<span class="badge">priced: ${priced.length}</span>`,
    `<span class="badge">avg: ${avg ? new Intl.NumberFormat('sv-SE').format(avg) + ' SEK' : 'n/a'}</span>`
  ].join('');
}

function card(item) {
  const location = item.location ? `<span class="pill">${item.location}</span>` : '';
  const condition = item.condition ? `<span class="pill">${item.condition}</span>` : '';
  const query = item.query ? `<span class="pill">q: ${item.query}</span>` : '';
  return `
    <article class="card">
      <h3>${item.title}</h3>
      <div class="price">${fmtPrice(item.price, item.currency)}</div>
      <div class="meta">
        <span class="pill">${item.source}</span>
        <span class="pill">${item.category}</span>
        ${location}${condition}${query}
      </div>
      ${item.url ? `<a href="${item.url}" target="_blank" rel="noopener">open listing ↗</a>` : ''}
    </article>
  `;
}

function applyFilters() {
  const q = searchEl.value.trim().toLowerCase();
  const cat = categoryEl.value;
  const src = sourceEl.value;
  const sort = sortEl.value;

  let items = allItems.filter((i) => {
    if (cat && i.category !== cat) return false;
    if (src && i.source !== src) return false;
    if (!q) return true;
    const hay = `${i.title} ${i.category} ${i.source} ${i.location || ''}`.toLowerCase();
    return hay.includes(q);
  });

  if (sort === 'price_asc') {
    items.sort((a, b) => (a.price ?? Number.MAX_SAFE_INTEGER) - (b.price ?? Number.MAX_SAFE_INTEGER));
  } else if (sort === 'price_desc') {
    items.sort((a, b) => (b.price ?? -1) - (a.price ?? -1));
  } else {
    items.sort((a, b) => a.title.localeCompare(b.title));
  }

  cardsEl.innerHTML = items.map(card).join('');
  emptyEl.classList.toggle('hidden', items.length !== 0);
  setStats(items);
}

async function loadData() {
  const r = await fetch('./data/items-normalized.json', { cache: 'no-store' });
  if (!r.ok) throw new Error(`failed to load data: ${r.status}`);
  const data = await r.json();
  allItems = Array.isArray(data.items) ? data.items : [];

  const categories = [...new Set(allItems.map((i) => i.category).filter(Boolean))].sort();
  const sources = [...new Set(allItems.map((i) => i.source).filter(Boolean))].sort();

  categoryEl.innerHTML = `<option value="">all categories</option>` + categories.map((c) => `<option value="${c}">${c}</option>`).join('');
  sourceEl.innerHTML = `<option value="">all sources</option>` + sources.map((s) => `<option value="${s}">${s}</option>`).join('');

  const generatedAt = data.generated_at ? new Date(data.generated_at).toLocaleString('sv-SE') : 'unknown';
  metaLineEl.textContent = `workspace: ${data.workspace || 'unknown'} · generated: ${generatedAt}`;

  applyFilters();
}

[searchEl, categoryEl, sourceEl, sortEl].forEach((el) => el.addEventListener('input', applyFilters));
clearEl.addEventListener('click', () => {
  searchEl.value = '';
  categoryEl.value = '';
  sourceEl.value = '';
  sortEl.value = 'price_asc';
  applyFilters();
});

loadData().catch((err) => {
  metaLineEl.textContent = `error loading data: ${err.message}`;
  cardsEl.innerHTML = '';
  emptyEl.classList.remove('hidden');
});
